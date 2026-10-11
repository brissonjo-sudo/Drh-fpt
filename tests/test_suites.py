import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import suites


def profiles():
    result={}
    for slot in suites.SLOTS:
        native=slot.startswith('claude-native')
        result[slot]={'provider_repondant':'claude-cli' if native else 'codex',
                      'modele_repondant':'claude-sonnet-4-6' if native else 'gpt-6.1-sol',
                      'effort_repondant':'high','provider_juge':'codex' if native else 'claude-cli',
                      'modele_juge':'gpt-6-sol' if native else 'claude-sonnet-4-6','effort_juge':'high',
                      'execution_profile':'claude-native' if native else 'assembled',
                      'context_mode':'selective','cli_versions':{'codex':'v1','claude-cli':'v2'}}
    return result


class SuiteTests(unittest.TestCase):
    def test_legacy_default_and_targeted_exact_ids(self):
        legacy = suites.load_suite('developpement')
        targeted = suites.load_suite('regression-ciblee-v1')
        self.assertEqual(sum('integration' in x.get('modes',['integration','degraded']) for x in legacy['cases']), 30)
        self.assertEqual(len(targeted['cases']), 14)
        self.assertIn('23-architecture-variables-bloquantes', [x['id'] for x in targeted['cases']])
        self.assertFalse(targeted['qualification'])

    def test_pending_qualification_refused(self):
        for name in ['qualification-a-v1','qualification-reserve-v1']:
            with self.assertRaisesRegex(ValueError, 'approuv'):
                suites.load_suite(name)

    def test_unknown_suite_refused(self):
        with self.assertRaises(ValueError):
            suites.load_suite('my-12')

    def test_freeze_requires_jo_case_and_runtime_approval(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            cases=[{'id':f'A-{i:02}', 'prompt':f'Question {i}',
                    'attendus':[{'id':f'a{i}', 'texte':'requis'}],
                    'attendus_degraded':[{'id':f'd{i}', 'texte':'requis'}]} for i in range(12)]
            path=root/'cases.json';path.write_text(json.dumps(cases),encoding='utf8')
            approval={'reviewer':'Jo','decision':'approved','approved_at':'2026-10-12T12:00:00+02:00',
                      'cases_sha256':suites.file_sha(path),'runtime_commit':'a'*40,
                      'evidence':'message humain explicite','profiles':profiles()}
            sealed=suites.freeze(path, approval, root/'sealed.json')
            self.assertEqual(sealed['state'],'frozen')
            self.assertEqual(sealed['threshold']['mandatory'],1.0)
            bad={**approval,'cases_sha256':'b'*64}
            with self.assertRaises(ValueError):
                suites.freeze(path,bad,root/'bad.json')
            with self.assertRaises(ValueError):
                suites.freeze(path,{**approval,'decision':'pending'},root/'bad.json')
            with self.assertRaises(FileExistsError):
                suites.freeze(path,approval,root/'sealed.json')

    def test_launch_once_per_slot_and_exact_runtime(self):
        with tempfile.TemporaryDirectory() as folder:
            state=Path(folder)/'runs.json'
            suite={'name':'qualification-a-v1','qualification':True,
                   'seal_sha256':'c'*64,'runtime_commit':'a'*40}
            suites.claim_launch(suite,state,'codex:integration','run1','a'*40)
            with self.assertRaisesRegex(ValueError,'consomm'):
                suites.claim_launch(suite,state,'codex:integration','run2','a'*40)
            with self.assertRaisesRegex(ValueError,'commit'):
                suites.claim_launch(suite,state,'claude-native:integration','run3','b'*40)
            suites.claim_launch(suite,state,'claude-native:integration','run3','a'*40)

    def test_reserve_blocked_before_closed_failure_and_pins_new_runtime(self):
        with tempfile.TemporaryDirectory() as folder:
            state=Path(folder)/'runs.json'
            suite={'name':'qualification-reserve-v1','qualification':True,'reserve_for':'qualification-a-v1',
                   'seal_sha256':'d'*64,'runtime_commit':'a'*40}
            with self.assertRaisesRegex(ValueError,'échec'):
                suites.claim_launch(suite,state,'codex:integration','b1','b'*40)
            state.write_text(json.dumps({'qualification-a-v1':{'outcome':'failed'}}),encoding='utf8')
            suites.claim_launch(suite,state,'codex:integration','b1','b'*40)
            with self.assertRaisesRegex(ValueError,'commit'):
                suites.claim_launch(suite,state,'codex:degraded','b2','c'*40)
            suites.claim_launch(suite,state,'codex:degraded','b2','b'*40)

    def test_outcome_keeps_original_report_hashes_and_blocks_pending_disputes(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);state=root/'runs.json'
            suite={'name':'qualification-a-v1','qualification':True,'seal_sha256':'c'*64,'runtime_commit':'a'*40}
            reports={}
            for index,slot in enumerate(suites.SLOTS):
                run='run'+str(index);suites.claim_launch(suite,state,slot,run,'a'*40)
                path=root/(str(index)+'.json');path.write_text(json.dumps({'provenance_evaluation':{
                    'campagne_id':run,'suite':suite['name'],'drh_fpt':{'commit':'a'*40}}}),encoding='utf8')
                reports[slot]=path
            pending={'reussite':False,'motifs_echec':['doute'],'qualification_assessments':{'mode':{'case':{'unresolved':['c1']}}}}
            with self.assertRaisesRegex(ValueError,'Arbitrage'):suites.record_outcome(suite,state,reports,pending)
            result={**pending,'qualification_assessments':{'mode':{'case':{'unresolved':[],'confirmed_failures':['c1']}}}}
            suites.record_outcome(suite,state,reports,result)
            closed=json.loads(state.read_text(encoding='utf8'))[suite['name']]
            self.assertEqual(closed['outcome'],'failed')
            self.assertEqual(closed['reports']['codex:integration']['report_sha256'],suites.file_sha(reports['codex:integration']))

    def test_interrupted_game_can_be_abandoned_without_fake_completed_reports(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);state=root/'runs.json'
            suite={'name':'qualification-a-v1','qualification':True,'seal_sha256':'c'*64,'runtime_commit':'a'*40}
            suites.claim_launch(suite,state,'codex:integration','run1','a'*40)
            run=root/'run1';run.mkdir()
            (run/'_provenance.json').write_text(json.dumps({'campagne_id':'run1','suite':suite['name'],
                'drh_fpt':{'commit':'a'*40}}),encoding='utf8')
            original=(run/'_provenance.json').read_bytes()
            suites.abandon_game(suite,state,root,'interruption','Processus interrompu avant bilan')
            game=json.loads(state.read_text(encoding='utf8'))[suite['name']]
            self.assertEqual(game['outcome'],'failed')
            self.assertEqual(game['abandonment']['kind'],'interruption')
            self.assertEqual((run/'_provenance.json').read_bytes(),original)
            with self.assertRaisesRegex(ValueError,'consomm'):
                suites.claim_launch(suite,state,'codex:integration','run2','a'*40)
            with self.assertRaisesRegex(ValueError,'consomm'):
                suites.claim_launch(suite,state,'codex:degraded','run2','a'*40)

    def test_abandonment_requires_observed_provenance_and_cannot_relabel_success(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);state=root/'runs.json'
            suite={'name':'qualification-a-v1','qualification':True,'seal_sha256':'c'*64,'runtime_commit':'a'*40}
            suites.claim_launch(suite,state,'codex:integration','run1','a'*40)
            with self.assertRaises(ValueError):suites.abandon_game(suite,state,root,'interruption','arrêt')

    def test_exact_profile_no_silent_model_effort_or_cli_change(self):
        profile={'provider_repondant':'codex','modele_repondant':'gpt-6.1-sol','effort_repondant':'high',
                 'provider_juge':'claude-cli','modele_juge':'claude-sonnet-4-6','effort_juge':'high',
                 'execution_profile':'assembled','context_mode':'selective',
                 'cli_versions':{'codex':'v1','claude-cli':'v2'}}
        suite={'profiles':{'codex:integration':profile}}
        suites.validate_profile(suite,'codex:integration',profile)
        for field,value in [('modele_juge','alias'),('effort_repondant','low'),('cli_versions',{})]:
            with self.assertRaises(ValueError):suites.validate_profile(suite,'codex:integration',{**profile,field:value})


if __name__=='__main__':unittest.main()
