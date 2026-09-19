"""Contrôles du chargement progressif des références."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import context_loader


class ContextLoaderTests(unittest.TestCase):
    def test_selective_career_payroll_loads_only_requested_module(self):
        case = {
            "id": "pay", "prompt": "Calcule l'ISFE", "branche": "Carrière & paie",
            "contextes": ["carriere-paie", "carriere-remuneration-paie"],
        }
        text, files = context_loader.build_case_context(case)
        self.assertIn("references/carriere-paie/remuneration-paie.md", files)
        self.assertNotIn("references/carriere-paie/temps-fin-fonctions.md", files)
        self.assertIn("Rémunération — régime indemnitaire", text)

    def test_mixed_case_loads_every_declared_branch(self):
        case = {
            "id": "mixed", "prompt": "Sanction d'un contractuel", "branche": "mixte",
            "contextes": ["carriere-paie", "carriere-statut-discipline", "contractuels"],
        }
        _, files = context_loader.build_case_context(case)
        self.assertIn("references/carriere-paie/statut-discipline.md", files)
        self.assertIn("references/contractuels.md", files)

    def test_requested_livrable_loads_matching_template(self):
        case = {
            "id": "decision", "prompt": "Rédige une décision", "branche": "Carrière & paie",
            "contextes": ["carriere-paie", "carriere-statut-discipline"],
        }
        _, files = context_loader.build_case_context(case)
        self.assertIn("assets/decision-modele.md", files)

    def test_unknown_context_is_rejected(self):
        with self.assertRaises(ValueError):
            context_loader.files_for_case({"id": "x", "contextes": ["inconnu"]})


if __name__ == "__main__":
    unittest.main()
