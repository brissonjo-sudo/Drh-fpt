"""Contrôles locaux sans appel LLM du protocole de campagne."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("run_tests", HERE / "run_tests.py")
assert SPEC and SPEC.loader
RUN_TESTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN_TESTS)


def expected(criterion_id="case-c01", text="Routage correct"):
    return {"id": criterion_id, "texte": text}


def successful_result(criteria):
    return {
        "criteres": [
            {"id": item["id"], "critere": item["texte"], "statut": "SATISFAIT", "note": "Preuve précise."}
            for item in criteria
        ],
        "erreurs": [],
        "score_architecture_sur_5": 5,
        "verdict_architecture": "REUSSITE",
        "score_fiabilite_juridique_sur_5": 5,
        "verdict_fiabilite_juridique": "REUSSITE",
        "score_sur_5": 5,
        "verdict": "REUSSITE",
        "synthese": "Conforme.",
        "tronque": False,
    }


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((HERE / "cas-de-test.json").read_text(encoding="utf-8"))

    def test_case_and_criterion_ids_are_unique(self):
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in self.cases:
            criteria = RUN_TESTS.normalized_expectations(case)
            criterion_ids = [item["id"] for item in criteria]
            self.assertEqual(len(criterion_ids), len(set(criterion_ids)))

    def test_each_campaign_activates_30_cases(self):
        for mode in ("integration", "degraded"):
            self.assertEqual(len(RUN_TESTS.active_cases(self.cases, mode, [])), 30)

    def test_case_filter_is_diagnostic_and_exact(self):
        cases = RUN_TESTS.active_cases(self.cases, "integration", ["01", "02"])
        self.assertEqual([case["id"] for case in cases], ["01", "02"])

    def test_conditional_cases_are_separated_by_mode(self):
        modes_by_id = {
            case["id"]: case.get("modes") for case in self.cases
            if case["id"].startswith(("15-", "16-"))
        }
        self.assertEqual(
            modes_by_id,
            {
                "15-echec-valeur-volatile": ["integration"],
                "16-echec-hors-base": ["integration"],
                "15-degrade-valeur-volatile": ["degraded"],
                "16-degrade-hors-base": ["degraded"],
            },
        )

    def test_response_profiles_cover_targeted_and_complex_requests(self):
        profiles = {case.get("profil_restitution") for case in self.cases}
        self.assertIn("ciblee", profiles)
        self.assertIn("dossier-complexe", profiles)

    def test_legal_skill_repository_layout_is_loaded(self):
        with tempfile.TemporaryDirectory() as tmp:
            repository = Path(tmp)
            skill = repository / "skill"
            (skill / "references").mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nversion: 3.3.0\n---\n# Recherche juridique\n")
            (skill / "references" / "source.md").write_text("# Source primaire\n")
            text, loaded_path, sources = RUN_TESTS.load_legal_skill(str(repository))
            self.assertEqual(loaded_path, skill.resolve())
            self.assertIn("Source primaire", text)
            self.assertEqual(len(sources), 2)

    def test_judge_accepts_exact_complete_criteria(self):
        criteria = [expected()]
        case = {"id": "case", "type": "architectural", "attendus": criteria}
        self.assertEqual(RUN_TESTS.validate_judge_result(successful_result(criteria), case), [])

    def test_judge_rejects_duplicate_unrelated_criteria(self):
        criteria = [expected("case-c01", "Vérifier la source"), expected("case-c02", "Distinguer le régime local")]
        case = {"id": "case", "type": "standard", "attendus": criteria}
        result = successful_result(criteria)
        result["criteres"] = [
            {"id": "case-c01", "critere": "Texte sans rapport", "statut": "SATISFAIT", "note": "x"},
            {"id": "case-c01", "critere": "Texte sans rapport", "statut": "SATISFAIT", "note": "x"},
        ]
        problems = RUN_TESTS.validate_judge_result(result, case)
        self.assertTrue(any("dupliqués" in item for item in problems))
        self.assertTrue(any("absents" in item for item in problems))
        self.assertTrue(any("libellé" in item for item in problems))

    def test_judge_rejects_empty_note_and_inconsistent_verdict(self):
        criteria = [expected()]
        case = {"id": "case", "type": "standard", "attendus": criteria}
        result = successful_result(criteria)
        result["criteres"][0]["note"] = " "
        result["erreurs"] = ["Erreur critique"]
        problems = RUN_TESTS.validate_judge_result(result, case)
        self.assertTrue(any("justification vide" in item for item in problems))
        self.assertTrue(any("incohérent" in item for item in problems))

    def test_system_context_identifies_modes_and_snapshot(self):
        integrated = RUN_TESTS.build_system_context("DRH", "LEGAL", "integration", "SOURCES", "snapshot")
        degraded = RUN_TESTS.build_system_context("DRH", None, "degraded")
        self.assertIn("LEGAL", integrated)
        self.assertIn("SOURCES", integrated)
        self.assertIn("mode dégradé", degraded)
        self.assertNotIn("LEGAL", degraded)

    def test_live_evidence_requires_complete_trace_for_required_cases(self):
        cases = [{"id": "a", "type": "standard"}, {"id": "b", "type": "echec_attendu"}]
        problems = RUN_TESTS.validate_evidence([], cases, "integration", "live")
        self.assertEqual(problems, ["cas sans preuve de consultation : a"])
        trace = [{
            "case_id": "a", "source_url": "https://legifrance.gouv.fr/x",
            "consulted_at": "2026-09-19T10:00:00Z", "version_or_date": "2026-09-19",
            "supporting_excerpt": "passage", "conclusion_supported": "conclusion",
        }]
        self.assertEqual(RUN_TESTS.validate_evidence(trace, cases, "integration", "live"), [])

    def test_resume_signature_tracks_cases_and_evidence_but_not_judge(self):
        base = {
            "mode": "integration", "provider_repondant": "anthropic",
            "modele_repondant": "m", "effort_repondant": None,
            "context_mode": "selective", "evidence_mode": "live",
            "sha256_cas": "cases", "sha256_compagnon": "legal",
            "sha256_source_pack": None, "case_ids": ["01"],
            "evidence_sha256": "evidence", "modele_juge": "judge-a",
        }
        other_judge = {**base, "modele_juge": "judge-b"}
        self.assertEqual(
            RUN_TESTS.campaign_signature(base),
            RUN_TESTS.campaign_signature(other_judge),
        )
        changed_cases = {**base, "case_ids": ["02"]}
        self.assertNotEqual(
            RUN_TESTS.campaign_signature(base),
            RUN_TESTS.campaign_signature(changed_cases),
        )

    def test_strict_gate_rejects_subset_duplicate_missing_and_truncation(self):
        provenance = {
            "mode": "degraded",
            "drh_fpt": {"commit": "abc", "dirty": False},
            "recherche_juridique": {},
        }
        cases = [{"id": "a"}, {"id": "b"}]
        results = [
            {"id": "a", "statut": "ok", "tronque": True, "validation": []},
            {"id": "a", "statut": "ok", "tronque": False, "validation": []},
        ]
        problems = RUN_TESTS.validate_strict_campaign(provenance, cases, results, subset=True)
        joined = "\n".join(problems)
        self.assertIn("sélection", joined)
        self.assertIn("dupliqués", joined)
        self.assertIn("cas sans résultat", joined)
        self.assertIn("tronqué", joined)


if __name__ == "__main__":
    unittest.main()
