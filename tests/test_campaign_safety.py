import json
import unittest
import tempfile
from pathlib import Path
import campaign
from providers import Completion


class CampaignSafetyTests(unittest.TestCase):
    def test_non_object_json_judgments_are_failures_not_crashes(self):
        for value in ([], None, 'string'):
            completion = Completion(json.dumps(value), False, {}, 'j', 1)
            result = campaign.parse_judge_completion(completion)
            self.assertIsInstance(result, dict)
            self.assertNotEqual(result.get('verdict'), 'REUSSITE')

    def test_resume_signature_rejects_changed_commit_bundle_or_context(self):
        base = {'mode': 'degraded', 'drh_fpt': {'commit': 'A', 'dirty': False, 'sha256_bundle': 'old'},
                'context_sha256_by_case': {'01': 'context-old'}}
        for other in ({**base, 'drh_fpt': {'commit': 'B', 'dirty': False, 'sha256_bundle': 'old'}},
                      {**base, 'drh_fpt': {'commit': 'A', 'dirty': False, 'sha256_bundle': 'new'}},
                      {**base, 'context_sha256_by_case': {'01': 'context-new'}}):
            self.assertNotEqual(campaign.campaign_signature(base), campaign.campaign_signature(other))

    def test_degraded_expectations_and_failure_rules_replace_integration_rules(self):
        case = {'id': '25', 'attendus': [{'id': 'nominal', 'texte': 'Produire un arrêté'}],
            'echec_si': ['Pas de projet'],
            'attendus_degraded': [{'id': 'degraded', 'texte': 'S’abstenir de rédiger un acte'}],
            'echec_si_degraded': ['Produit un acte prêt à signer']}
        selected = campaign.case_for_mode(case, 'degraded')
        self.assertEqual(selected['attendus'][0]['id'], 'degraded')
        self.assertEqual(selected['echec_si'], ['Produit un acte prêt à signer'])

    def test_criterion_identifier_with_wrong_type_is_rejected(self):
        case = {'id': 'x', 'attendus': [{'id': 'x-c01', 'texte': 'Exigence'}]}
        result = {'criteres': [{'id': [], 'critere': 'Exigence', 'statut': 'SATISFAIT', 'note': 'x'}]}
        self.assertTrue(campaign.validate_judge_result(result, case))

    def test_live_context_passages_are_visible_to_respondent(self):
        trace = {'source_url': 'https://www.legifrance.gouv.fr/x', 'version_or_date': '2026-10-11',
                 'consulted_at': '2026-10-11T10:00:00Z', 'supporting_excerpt': 'Passage officiel'}
        context = campaign.build_system_context('DRH', 'LEGAL', 'integration', evidence_mode='live', evidence=[trace])
        self.assertIn('Passage officiel', context)

    def test_wrong_verdict_and_status_types_fail_without_crashing(self):
        case = {'id': 'x', 'attendus': [{'id': 'x-c01', 'texte': 'Exigence'}]}
        result = {'criteres': [{'id': 'x-c01', 'critere': 'Exigence', 'statut': [], 'note': 'x'}],
                  'verdict': {}, 'verdict_fiabilite_juridique': [], 'verdict_architecture': []}
        self.assertTrue(campaign.validate_judge_result(result, case))

    def test_trace_bytes_match_hash_on_windows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            raw='{"type":"turn.completed"}\n'
            completion=Completion('Answer',False,{},'j',1,raw)
            campaign.write_answer(root,{'id':'x','branche':'b','prompt':'p'},'Answer',completion,{})
            meta=json.loads((root/'x-response.json').read_text(encoding='utf8'))
            import hashlib
            self.assertEqual(meta['provider_trace_sha256'],hashlib.sha256((root/'x-respondant.jsonl').read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
