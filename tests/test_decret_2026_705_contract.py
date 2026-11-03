"""Invariants documentaires du décret n° 2026-705 (congés pour raison de santé)."""
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
        self.assertIn('ne passe plus systématiquement par le conseil médical', s58)
        self.assertIn('restent soumis à son avis', s58)

    def test_last_paid_period_opinion_of_article_32_survives_the_abrogation(self):
        for name, start, end in [('§5.2', '### 5.2', '### 5.3'),
                                 ('§5.8', '### 5.8', '## 6.'),
                                 ('§8', '## 8.', '## 9.')]:
            part = section(self.qvt, start, end)
            self.assertIn('ultime période de congé rétribuée', part, name)
            self.assertIn('art. 32', part, name)
        s52 = section(self.qvt, '### 5.2', '### 5.3')
        for phrase in ['LEGIARTI000045350669', 'présomption d\'inaptitude',
                       'formation plénière', 'consultation **systématique**']:
            self.assertIn(phrase, s52)
        bullet = section(self.qvt, 'CLM et CLD (art. 26)', 'Contrôle administratif')
        self.assertIn('article 32', bullet)
        self.assertNotIn('saisine du conseil médical au renouvellement supprimée', self.qvt)
        socle = flat('references/socle-sources-verification.md')
        self.assertIn('(art. 32)', section(socle, '**Instances médicales**', '**CAP / LDG**'))

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

    def test_sick_note_ceilings_are_sourced_dated_and_bounded(self):
        bullet = section(self.qvt, "Avis d'arrêt (art. 15)", 'CLM et CLD (art. 26)')
        for phrase in ['**trente et un jours**', '**soixante-deux jours**',
                       'établies à compter du 1er septembre 2026', 'Mayotte',
                       'LEGIARTI000054252051', 'LEGIARTI000054250013',
                       'LEGIARTI000053284700', 'justifie, sur la prescription',
                       'médecin traitant', 'figure toujours dans l\'avis établi selon R. 321-2']:
            self.assertIn(phrase, bullet)
        self.assertNotIn('La mention de la « durée probable de l\'incapacité » disparaît', self.qvt)
        self.assertNotIn('sans valeur chiffrée', bullet)

    def test_contract_agents_article_9_2_is_not_applied_and_article_8_is_split(self):
        s53 = section(self.qvt, '### 5.3', '### 5.4')
        contract = section(s53, '**Contractuels (décret 88-145', '**Hors champ FPT**')
        for phrase in ['LEGIARTI000054641818', 'articles 12, 13 et 14', 'décret 86-83',
                       'erreur de renvoi est **probable**', '**ne pas opposer**',
                       'rectificatif', '1er janvier 2028']:
            self.assertIn(phrase, contract)
        grave = section(contract, '**Grave maladie (art. 8)**', '**Contrôle (art. 12)**')
        for phrase in ['À l\'**octroi**', 'avis du conseil médical',
                       'ne pas affirmer de dispense générale', '**abstention**',
                       'minimum de trois mois relève de l\'interprétation']:
            self.assertIn(phrase, grave)
        certificate = section(contract, '**Certificat (art. 7)**', '**Grave maladie (art. 8)**')
        self.assertIn('**interprétation**', certificate)
        self.assertIn('à due concurrence', certificate)
        self.assertIn('décret n° 2026-705', flat('references/contractuels.md'))

    def test_state_only_remuneration_rule_is_excluded(self):
        self.assertIn('n° 2010-997', self.qvt)
        self.assertIn('ne pas le transposer', self.qvt)

    def test_article_28_extension_to_ordinary_sick_leave_is_an_interpretation(self):
        bullet = section(self.qvt, '**Activité rémunérée (art. 28)**', '**Formation pendant le congé')
        for phrase in ['interprétation retenue, non lettre certaine', 'sans virgule',
                       'titre VI', 'art. 3, 8°', 'art. 37-9-1',
                       'sans validation juridique préalable']:
            self.assertIn(phrase, bullet)

    def test_socle_announces_integration_instead_of_pending_work(self):
        socle = flat('references/socle-sources-verification.md')
        bullet = section(socle, '**Instances médicales**', '**CAP / LDG**')
        self.assertIn('intégré le 03/11/2026', bullet)
        self.assertNotIn('à intégrer', bullet)


if __name__ == '__main__':
    unittest.main()
