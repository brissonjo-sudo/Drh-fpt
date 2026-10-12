import json,tempfile,unittest
from pathlib import Path
import claude_cli,native_runtime,release_gate,live_sources
from providers import ApiCallError
from test_claude_cli import stream,MODEL

class NativeReadProofTests(unittest.TestCase):
    def test_requested_full_read_cannot_pass_with_truncated_or_altered_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'source.md';path.write_text('première\ndeuxième\n',encoding='utf8')
            runtime={'root':str(root),'files':{'source.md':claude_cli.file_sha(path)}}
            raw=stream({'type':'tool_use','id':'r','name':'Read','input':{'file_path':str(path)}})
            self.assertTrue(claude_cli.parse_stream(raw,MODEL,runtime=runtime).usage['loaded_files'][0]['full'])
            for body in ['1\tpremière','1\tpremière\n2\t[Content truncated due to size]','1\tpremière\n2\tmodifiée','']:
                events=[json.loads(s) for s in raw.splitlines()]
                next(x for x in events if x['type']=='user')['message']['content'][0]['content']=body
                with self.subTest(body=body),self.assertRaises(ApiCallError):
                    claude_cli.parse_stream('\n'.join(json.dumps(x) for x in events),MODEL,runtime=runtime)

    def test_two_exact_partial_reads_cover_file_without_false_full_on_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'source.md';path.write_text('one\ntwo\nthree',encoding='utf8')
            runtime={'root':str(root),'files':{'source.md':claude_cli.file_sha(path)}}
            first={'type':'tool_use','id':'a','name':'Read','input':{'file_path':str(path),'offset':1,'limit':1}}
            second={'type':'tool_use','id':'b','name':'Read','input':{'file_path':str(path),'offset':2,'limit':2}}
            self.assertFalse(claude_cli.parse_stream(stream(first),MODEL,runtime=runtime).usage['loaded_files'][0]['full'])
            self.assertTrue(claude_cli.parse_stream(stream(first,second),MODEL,runtime=runtime).usage['loaded_files'][0]['full'])

    def test_skill_launch_without_exact_native_body_is_not_loaded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'SKILL.md';path.write_text('---\nname: fixture\n---\n\nInstructions\n',encoding='utf8')
            runtime={'root':str(root),'files':{'SKILL.md':claude_cli.file_sha(path)},'skills':{'fixture':'SKILL.md'}}
            call={'type':'tool_use','id':'s','name':'Skill','input':{'skill':'fixture'}}
            for body in [None,f'Base directory for this skill: {root}\n\nMauvais corps',f'Base directory for this skill: {root.parent}\n\nInstructions']:
                with self.subTest(body=body),self.assertRaises(ApiCallError):
                    claude_cli.parse_stream(stream(call,skill_expansion=body),MODEL,runtime=runtime)
            valid=f'Base directory for this skill: {root}\r\n\r\nInstructions\r\n'
            self.assertTrue(claude_cli.parse_stream(stream(call,skill_expansion=valid),MODEL,runtime=runtime).usage['loaded_files'][0]['full'])

    def test_tool_results_and_ids_cannot_be_orphaned_or_duplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'source.md';path.write_text('one',encoding='utf8')
            runtime={'root':str(root),'files':{'source.md':claude_cli.file_sha(path)}}
            raw=stream({'type':'tool_use','id':'a','name':'Read','input':{'file_path':str(path)}})
            original=[json.loads(s) for s in raw.splitlines()]
            for variant in ['duplicate_result','orphan','duplicate_call']:
                events=json.loads(json.dumps(original));result=next(x for x in events if x['type']=='user')
                if variant=='duplicate_result':events.insert(-1,result)
                elif variant=='orphan':result['message']['content'][0]['tool_use_id']='unknown'
                else:events.insert(2,events[1])
                with self.subTest(variant=variant),self.assertRaises(ApiCallError):
                    claude_cli.parse_stream('\n'.join(json.dumps(x) for x in events),MODEL,runtime=runtime)

    def test_large_source_text_is_bounded_and_every_segment_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);drh=base/'drh';drh.mkdir();(drh/'SKILL.md').write_text('DRH')
            legal=base/'legal';legal.mkdir();(legal/'SKILL.md').write_text('LEGAL')
            trace={'case_id':'x','source_title':'Public','source_url':'https://www.cnil.fr/chapter','source_id':'public',
                   'version_or_date':'2026','consulted_at':'2026-10-12','supporting_excerpt':'é'*80000}
            runtime=native_runtime.stage(base/'native',drh,'integration','x',[trace],legal)
            parts=runtime.get('source_files',[])
            self.assertGreater(len(parts),1)
            text=''.join((base/'native'/rel).read_text(encoding='utf8') for rel in parts)
            self.assertEqual(text,live_sources.source_context([trace]))
            for rel in parts:self.assertLessEqual(len((base/'native'/rel).read_bytes()),16000)
            required=release_gate.native_required_files({'contextes':['communication-interne'],'prompt':'question'},'integration',runtime)
            self.assertTrue(set(parts)<=required)

if __name__=='__main__':unittest.main()
