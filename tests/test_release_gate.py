import json,tempfile,unittest
from pathlib import Path
import release_gate
import hashlib

class ReleaseGateTests(unittest.TestCase):
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
