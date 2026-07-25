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


class HarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = json.loads(
            (HERE / "cas-de-test.json").read_text(encoding="utf-8")
        )

    def test_case_ids_are_unique(self) -> None:
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_each_campaign_activates_30_cases(self) -> None:
        for mode in ("integration", "degraded"):
            with self.subTest(mode=mode):
                active = [
                    case for case in self.cases
                    if mode in case.get("modes", ["integration", "degraded"])
                ]
                self.assertEqual(len(active), 30)

    def test_conditional_cases_are_separated_by_mode(self) -> None:
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

    def test_legal_skill_directory_is_loaded_with_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "references").mkdir()
            (root / "SKILL.md").write_text(
                "---\nversion: 2.2.0\n---\n# Recherche juridique\n",
                encoding="utf-8",
            )
            (root / "references" / "source.md").write_text(
                "# Source primaire\n", encoding="utf-8"
            )

            text, loaded_path, sources = RUN_TESTS.load_legal_skill(str(root))

            self.assertEqual(loaded_path, root.resolve())
            self.assertIn("Recherche juridique", text)
            self.assertIn("Source primaire", text)
            self.assertEqual(len(sources), 2)

    def test_system_context_identifies_execution_mode(self) -> None:
        integrated = RUN_TESTS.build_system_context("DRH", "LEGAL", "integration")
        degraded = RUN_TESTS.build_system_context("DRH", None, "degraded")
        self.assertIn("LEGAL", integrated)
        self.assertIn("co-activés", integrated)
        self.assertIn("mode dégradé", degraded)
        self.assertNotIn("LEGAL", degraded)


if __name__ == "__main__":
    unittest.main()
