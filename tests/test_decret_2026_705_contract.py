"""Invariants documentaires du décret n° 2026-705 (congés pour raison de santé)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def flat(name):
    return ' '.join((ROOT / name).read_text(encoding='utf8').split())


def section(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]


class Decret2026705ContractTests(unittest.TestCase):
    def setUp(self):
        self.qvt = flat('references/qvt-sante.md')

    def test_council_no_longer_consulted_on_renewal_after_full_pay(self):
        s52 = section(self.qvt, '### 5.2', '### 5.3')
        for phrase in ['2° du I de l\'article 5', 'abrogé à compter du 1er septembre 2026',
                       'première période de CLM ou de CLD', 'art. 5, II, 2°',
                       'LEGIARTI000054641701', 'LEGIARTI000049428779']:
            self.assertIn(phrase, s52)
        s58 = section(self.qvt, '### 5.8', '## 6.')
        self.assertIn('ne passe plus par le conseil médical', s58)
        self.assertIn('restent soumis à son avis', s58)

    def test_sick_leave_rules_cite_each_new_article_with_its_identifier(self):
        s53 = section(self.qvt, '### 5.3', '### 5.4')
        for article, legiarti in [('art. 15', '054641709'), ('26-1', '054641691'),
                                  ('31-1', '054641693'), ('31-2', '054641695'),
                                  ('34-1', '054641697'), ('37-9-1', '054641699'),
                                  ('37-2', '054641722'), ('28', '054641717')]:
            self.assertIn(article, s53)
            self.assertIn('LEGIARTI000' + legiarti, s53)
        self.assertIn('consultées sur Légifrance le 03/11/2026', s53)
        self.assertIn('JORFTEXT000054570030', s53)

    def test_staggered_application_dates_follow_article_11(self):
        s53 = section(self.qvt, '### 5.3', '### 5.4')
        self.assertIn('débutant ou prolongés à compter du 1er septembre 2026', s53)
        self.assertIn('1er janvier 2028', s53)
        self.assertIn("retenir la règle de l'article 11", s53)
        self.assertIn('lendemain de la publication', s53)

    def test_unverified_social_security_durations_stay_control_points(self):
        s53 = section(self.qvt, '### 5.3', '### 5.4')
        self.assertIn('R. 162-1-7-1', s53)
        self.assertIn('points de contrôle', s53)
        # Aucune durée maximale d'arrêt chiffrée n'est tirée du code non relu.
        bullet = section(s53, "Avis d'arrêt (art. 15)", 'CLM et CLD (art. 26)')
        self.assertIsNone(re.search(r'\b\d+\s*(jours|mois)\b', bullet))

    def test_contract_agents_keep_their_own_regime_and_flag_article_9_2(self):
        s53 = section(self.qvt, '### 5.3', '### 5.4')
        for phrase in ['décret 88-145', 'LEGIARTI000054641818', 'articles 12, 13 et 14',
                       'point de contrôle', 'grave maladie', 'articulation à contrôler']:
            self.assertIn(phrase, s53)
        self.assertIn('décret n° 2026-705', flat('references/contractuels.md'))

    def test_state_only_remuneration_rule_is_excluded(self):
        self.assertIn('n° 2010-997', self.qvt)
        self.assertIn('ne pas le transposer', self.qvt)

    def test_doubtful_wording_of_article_28_is_not_asserted(self):
        s53 = section(self.qvt, '### 5.3', '### 5.4')
        self.assertIn('Faire confirmer sa portée', s53)

    def test_socle_announces_integration_instead_of_pending_work(self):
        socle = flat('references/socle-sources-verification.md')
        bullet = section(socle, '**Instances médicales**', '**CAP / LDG**')
        self.assertIn('intégré le 03/11/2026', bullet)
        self.assertNotIn('à intégrer', bullet)


if __name__ == '__main__':
    unittest.main()
