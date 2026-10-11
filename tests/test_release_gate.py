import json,tempfile,unittest
from pathlib import Path
import release_gate
import hashlib
from unittest.mock import patch
from test_claude_cli import stream, MODEL
import sys

class ReleaseGateTests(unittest.TestCase):
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
