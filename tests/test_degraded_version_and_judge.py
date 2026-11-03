"""Contrôles dégradés de la couverture finale et doutes consignés par le juge."""
from pathlib import Path
import sys
import unittest

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'SKILL.md').is_file())
sys.path.insert(0, str(ROOT/'tests'))
import campaign  # noqa: E402


def flat(relative):
    return ' '.join((ROOT/relative).read_text(encoding='utf8').split())


class DegradedVersionAndJudgeTests(unittest.TestCase):
    def test_incapacity_final_coverage_keeps_the_search_before_dismissal(self):
        text = flat('references/restitution-proportionnee.md')
        block = text.split('- **Inaptitude**', 1)[1].split('- **Emploi fonctionnel**', 1)[0]
        self.assertIn('avant toute décision de licenciement', block)
        self.assertIn('recherche effective', block)

    def test_degraded_protection_keeps_the_allocation_of_proof_as_a_question(self):
        text = flat('references/restitution-proportionnee.md')
        block = text.split('- **Protection fonctionnelle**', 1)[1].split('- **Insuffisance professionnelle**', 1)[0]
        self.assertIn('En mode dégradé', block)
        self.assertIn('répartition', block)
        self.assertIn('question', block)

    def test_degraded_final_rule_asks_for_the_applicable_version(self):
        text = flat('references/restitution-proportionnee.md')
        final = text.rsplit('En mode dégradé, identifier', 1)[1]
        self.assertIn('version applicable', final)
        self.assertIn('date de référence', final)

    def test_expected_reservations_do_not_automatically_become_judgment_uncertainties(self):
        judge = ' '.join(campaign.JUDGE_SYSTEM.split())
        self.assertIn('conformité de la réponse aux critères', judge)
        self.assertIn('Une réserve conforme', judge)
        self.assertIn('même hors des critères', judge)
        self.assertNotIn('Consigne toute question juridique non tranchée', judge)
        self.assertIn('énoncé ferme non vérifié reste sanctionné', judge)


if __name__ == '__main__':
    unittest.main()
