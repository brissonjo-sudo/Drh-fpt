"""Parcours local du harnais avec fournisseur simulé."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import campaign
from providers import Completion


class CampaignFlowTests(unittest.TestCase):
    def setUp(self):
        self.case = next(
            case for case in json.loads((HERE / "cas-de-test.json").read_text())
            if case["id"] == "01"
        )

    def judge_completion(self):
        payload = {
            "criteres": [
                {"id": item["id"], "critere": item["texte"], "statut": "SATISFAIT", "note": "Établi."}
                for item in self.case["attendus"]
            ],
            "erreurs": [], "score_architecture_sur_5": 5,
            "verdict_architecture": "NON_APPLICABLE",
            "score_fiabilite_juridique_sur_5": 5,
            "verdict_fiabilite_juridique": "REUSSITE",
            "score_sur_5": 5, "verdict": "REUSSITE", "synthese": "Conforme."
        }
        return Completion(json.dumps(payload, ensure_ascii=False), False, {"input_tokens": 10, "output_tokens": 5}, "judge", 2)

    def test_generate_then_judge_only_preserves_response(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = Path(tmp)
            completions = [
                Completion("Réponse initiale", False, {"input_tokens": 8, "output_tokens": 3}, "answer", 1),
                self.judge_completion(),
            ]
            with patch.object(campaign, "RESULTS", results), patch.object(
                campaign, "key_for_provider", return_value="key"
            ), patch.object(campaign, "complete", side_effect=completions):
                code = campaign.main([
                    "--mode", "degraded", "--case", "01", "--judge",
                    "--context-mode", "selective",
                ])
            self.assertEqual(code, 0)
            campaign_dir = next(results.iterdir())
            response = json.loads((campaign_dir / "01-response.json").read_text())
            self.assertEqual(response["answer"], "Réponse initiale")
            evaluations_before = list((campaign_dir / "evaluations").iterdir())

            with patch.object(campaign, "RESULTS", results), patch.object(
                campaign, "key_for_provider", return_value="key"
            ), patch.object(campaign, "complete", return_value=self.judge_completion()) as mocked:
                code = campaign.main([
                    "--mode", "degraded", "--case", "01",
                    "--judge-only", campaign_dir.name,
                    "--context-mode", "selective",
                ])
            self.assertEqual(code, 0)
            self.assertEqual(mocked.call_count, 1)
            self.assertEqual(response["answer"], json.loads((campaign_dir / "01-response.json").read_text())["answer"])
            self.assertEqual(len(list((campaign_dir / "evaluations").iterdir())), len(evaluations_before) + 1)


if __name__ == "__main__":
    unittest.main()
