import json,tempfile,unittest
from pathlib import Path
import release_gate
import hashlib
from unittest.mock import patch
from test_claude_cli import stream, MODEL
from test_suites import profiles
import sys

class ReleaseGateTests(unittest.TestCase):
    def test_portable_close_uses_the_same_launch_registry_as_validation(self):
        common={'suite':'qualification-a-v1','sha256_cas':'c','suite_seal_sha256':'s',
                'suite_registry_sha256':'r','drh_fpt':{'commit':'A','dirty':False,'sha256_bundle':'b'}}
        codex={**common,**profiles()['codex:integration']}
        native={**common,**profiles()['claude-native:integration']}
        responses=[({**codex,'mode':'integration'},[]),({**codex,'mode':'degraded'},[]),
                   ({**native,'mode':'integration'},[]),({**native,'mode':'degraded'},[])]
        with tempfile.TemporaryDirectory() as tmp:
            state=Path(tmp)/'portable.json'
            argv=['gate','--integration','i','--degraded','d','--claude-integration','ci','--claude-degraded','cd',
                  '--launch-state',str(state),'--close-game','--expected-commit','A']
            with patch.object(sys,'argv',argv),patch.object(release_gate,'check_report',side_effect=responses) as check,patch('release_gate.suites.load_suite',return_value={}),patch('release_gate.suites.record_outcome') as close:
                self.assertEqual(release_gate.main(),0)
            self.assertEqual(close.call_args.args[1],state)
            self.assertEqual(check.call_args.kwargs['launch_state'],str(state))
    def test_abandoned_game_cannot_pass_even_with_other_checks_stubbed_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cases=root/'cases.json';cases.write_text('[]',encoding='utf8')
            spec={'name':'qualification-a-v1','qualification':True,'cases':[],
                  'cases_path':str(cases),'expected_per_mode':0,'runtime_commit':'a'*40,
                  'registry_sha256':'r','seal_sha256':'s','profiles':profiles()}
            provenance={**profiles()['codex:degraded'],'suite':spec['name'],'mode':'degraded',
                'campagne_id':'run1','suite_registry_sha256':'r','suite_seal_sha256':'s',
                'sha256_cas':release_gate.campaign.sha256_text('[]'),'case_ids':[],
                'drh_fpt':{'commit':'a'*40,'dirty':False,'sha256_bundle':'bundle'}}
            report=root/'_bilan.json';report.write_text(json.dumps({'provenance_evaluation':provenance,
                'gate_strict':{'active':True,'reussite':True},'cas':[]}),encoding='utf8')
            state=root/'qualification-launches.json';state.write_text(json.dumps({spec['name']:{
                'seal_sha256':'s','runtime_commit':'a'*40,'runs':{'codex:degraded':'run1'},
                'outcome':'failed','abandonment':{'kind':'runtime_changed'}}}),encoding='utf8')
            with patch('release_gate.suites.load_suite',return_value=spec),patch('release_gate.campaign.validate_strict_campaign',return_value=[]),patch.object(release_gate.campaign,'RESULTS',root):
                problems=release_gate.check_report(report)[1]
            self.assertTrue(any('clos en échec' in item for item in problems),problems)
    def test_qualification_requires_two_native_campaigns(self):
        provenance={'mode':'integration','suite':'qualification-a-v1','sha256_cas':'cases',
                    'drh_fpt':{'commit':'A','dirty':False,'sha256_bundle':'bundle'}}
        with patch.object(release_gate,'check_report',side_effect=[(provenance,[]),({**provenance,'mode':'degraded'},[])]),patch.object(sys,'argv',['gate','--integration','i','--degraded','d','--expected-commit','A']):
            self.assertEqual(release_gate.main(),1)
    def test_claude_trace_matches_raw_message_and_exact_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'trace.jsonl';path.write_text(stream(),encoding='utf8')
            sha=hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(release_gate.check_claude_trace(path,sha,'réponse',MODEL)[1],[])
            self.assertTrue(release_gate.check_claude_trace(path,sha,'modifiée',MODEL)[1])
            self.assertTrue(release_gate.check_claude_trace(path,None,'réponse',MODEL)[1])
            self.assertTrue(release_gate.check_claude_trace(path,sha,'réponse','claude-substitué')[1])

    def test_different_commits_cannot_validate_release(self):
        left={'mode':'integration','drh_fpt':{'commit':'A','dirty':False,'sha256_bundle':'bundle'},'sha256_cas':'cases'}
        right={**left,'mode':'degraded','drh_fpt':{**left['drh_fpt'],'commit':'B'}}
        self.assertTrue(release_gate.compare_provenances(left,right,'A'))

    def test_same_commit_requires_same_cases_bundle_and_clean_repositories(self):
        left={'mode':'integration','drh_fpt':{'commit':'A','dirty':False,'sha256_bundle':'bundle'},'sha256_cas':'cases'}
        right={**left,'mode':'degraded'}
        self.assertEqual(release_gate.compare_provenances(left,right,'A'),[])
        for field,value in [('sha256_cas','different'),('drh_fpt',{'commit':'A','dirty':True,'sha256_bundle':'bundle'})]:
            self.assertTrue(release_gate.compare_provenances(left,{**right,field:value},'A'))

    def test_summary_without_answers_and_judgments_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'_bilan.json';p.write_text(json.dumps({'gate_strict':{'active':True,'reussite':True},'cas':[],'provenance_evaluation':{'mode':'degraded'}}))
            self.assertTrue(release_gate.check_report(p)[1])

    def test_unchanged_trace_does_not_validate_tampered_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'trace.jsonl';p.write_bytes(b'{"type":"item.completed","item":{"type":"agent_message","text":"Original"}}\n{"type":"turn.completed"}\n')
            sha=hashlib.sha256(p.read_bytes()).hexdigest()
            self.assertEqual(release_gate.check_codex_trace(p,sha,'Original'),[])
            self.assertTrue(release_gate.check_codex_trace(p,sha,'Modifie'))
            self.assertTrue(release_gate.check_codex_trace(p,None,'Original'))
