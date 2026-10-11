"""Contrôles du chargement progressif des références."""

import sys
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import context_loader


class ContextLoaderTests(unittest.TestCase):
    def test_restitution_is_read_last_without_duplicate_sources(self):
        case={'id':'x','prompt':'Donne les plafonds','contextes':['carriere-paie','carriere-remuneration-paie']}
        files=context_loader.files_for_case(case)
        self.assertEqual(files[-1],'references/restitution-proportionnee.md')
        self.assertEqual(len(files),len(set(files)))

    def test_real_mixed_cases_load_their_missing_business_modules(self):
        cases={x['id']:x for x in json.loads((ROOT/'tests/cas-de-test.json').read_text(encoding='utf8'))}
        expected={'01':'references/carriere-paie/statut-discipline.md',
                  '03':'references/contractuels.md',
                  '06':'references/cst-dialogue-social.md',
                  '07':'references/carriere-paie/remuneration-paie.md',
                  '17-echec-droit-prive':'references/carriere-paie/temps-fin-fonctions.md'}
        for ident,module in expected.items():
            self.assertIn(module,context_loader.files_for_case(cases[ident]))

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
