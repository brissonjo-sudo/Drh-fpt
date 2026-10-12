"""Invariants documentaires de la relecture PR18 (sans appel de modèle)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'tests')]
import build_bundle
import campaign
import context_loader


class ReviewContractTests(unittest.TestCase):
    def test_native_reference_base_and_companion_activation_precede_analysis(self):
        opening=self.read('SKILL.md').split('## 1. Déclenchement')[0]
        self.assertTrue('répertoire contenant `SKILL.md`' in opening,'base de résolution native absente')
        self.assertTrue('co-activer' in opening,'activation du compagnon absente du démarrage')
    def test_native_career_parent_is_explicit_in_initial_loading_contract(self):
        opening=self.read('SKILL.md').split('## 1. Déclenchement')[0]
        self.assertIn('references/carriere-paie.md',opening)
        self.assertIn('avant tout sous-module',opening)

    def test_degraded_final_rule_blocks_exact_legal_hints_but_keeps_supplied_facts(self):
        final=self.read('references/restitution-proportionnee.md')
        self.assertIn('même présentés comme des pistes',final)
        self.assertIn('faits chiffrés fournis',final)
        self.assertIn('Décision suspendue',final)
        self.assertNotIn('aucun chiffre en mode dégradé',self.read('references/carriere-paie.md'))
    def test_native_loading_contract_is_visible_before_the_business_sections(self):
        opening=self.read('SKILL.md').split('## 1. Déclenchement')[0]
        for rel in context_loader.CORE_FILES[1:]:self.assertIn(rel,opening)
        self.assertIn('chargement natif',opening)
    def read(self, name):
        return (ROOT / name).read_text(encoding='utf8')

    def test_restitution_is_last_and_once_in_full_and_selective_contexts(self):
        texts = [build_bundle.build_bundle_text('0.7.0'),
                 context_loader.build_case_context({'id':'x','prompt':'paie',
                 'contextes':['carriere-paie','carriere-remuneration-paie']})[0]]
        marker = '## Rappel final de restitution'
        for text in texts:
            final = campaign.build_system_context(text, None, 'degraded')
            self.assertEqual(final.count(marker), 1)
            self.assertTrue(final.rstrip().endswith(self.read('references/restitution-proportionnee.md').rstrip()))

    def test_four_requested_options_replace_cascade(self):
        text = self.read('references/carriere-paie/temps-fin-fonctions.md')
        self.assertIn('prise en charge directe', text)
        self.assertIn('quatre options', text)
        self.assertNotIn('si aucune de ces solutions', text)

    def test_promotion_cdg_depends_on_conferred_lists(self):
        text = self.read('references/carriere-paie/statut-discipline.md')
        self.assertIn('volontairement affiliée', text)
        self.assertIn('confié', text)
        self.assertIn('R413-37', text)

    def test_no_legacy_ceiling_permission(self):
        for path in ['references/carriere-paie.md','scripts/bundle-preambule.md',
                     'tests/prompt-claude-code.md']:
            text = self.read(path)
            for phrase in ['citable sous réserve', 'citables +', 'daté et assorti']:
                self.assertNotIn(phrase, text)

    def test_explicit_contract_and_retirement_routing(self):
        text = self.read('SKILL.md')
        self.assertIn('references/contrat-execution.md', text)
        self.assertIn('retraite progressive', text)
        self.assertIn('ordre de raisonnement', text)
        self.assertNotIn('relire `references/restitution-proportionnee.md`', text)

    def test_grief_references_target_submodule(self):
        text = self.read('references/statut-garanties.md')
        self.assertNotIn('carriere-paie §5.5', text)

    def test_grievance_authorities_are_in_strike_section(self):
        text = self.read('references/carriere-paie/temps-fin-fonctions.md')
        self.assertNotIn('303588', text.split('### 5.12')[0])
        self.assertIn('303588', text.split('### 5.12')[1])


if __name__ == '__main__':
    unittest.main()
