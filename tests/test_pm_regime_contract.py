"""Restitution du régime PM et nomenclature historique sourcée."""
import json
from pathlib import Path
import unittest

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent/'SKILL.md').is_file())


def flat(relative):
    return ' '.join((ROOT/relative).read_text(encoding='utf8').split())


class PoliceRegimeContractTests(unittest.TestCase):
    def test_incapacity_outcomes_are_linked_to_affiliation_in_final_coverage(self):
        text = flat('references/restitution-proportionnee.md')
        block = text.split('- **Inaptitude** :', 1)[1].split('- **Emploi fonctionnel**', 1)[0]
        self.assertIn('CNRACL', block)
        self.assertIn('IRCANTEC', block)
        self.assertIn('questions', block)

    def test_institution_of_a_specific_regime_names_the_excluded_common_regime(self):
        text = flat('references/restitution-proportionnee.md')
        block = text.split('- **Régime indemnitaire** :', 1)[1].split('- **Rémunération contractuelle**', 1)[0]
        self.assertIn('RIFSEEP', block)
        self.assertIn("sans l'appliquer", block)

    def test_nbi_is_not_listed_as_an_exception_in_article_six(self):
        text = flat('references/carriere-paie/remuneration-paie.md')
        self.assertNotIn('fériés, astreintes et NBI', text)
        self.assertIn('La **NBI** reste soumise à ses conditions propres', text)
        self.assertIn('dépassement régulier du cycle de travail', text)
        self.assertIn('LEGIARTI000049799576', text)

    def test_development_does_not_treat_attested_historical_ismf_as_an_invented_name(self):
        cases = json.loads((ROOT/'tests/cas-de-test.json').read_text(encoding='utf8'))
        case = next(item for item in cases if item['id'] == '07')
        criterion = next(item for item in case['attendus'] if item['id'] == '07-c06')['texte']
        self.assertNotIn('ne pas dire', criterion)
        self.assertNotIn('ex. « ISMF »', ' '.join(case['echec_si']))
        self.assertIn('sigle historique attesté', criterion)


if __name__ == '__main__':
    unittest.main()
