import json
import time
import subprocess
from types import SimpleNamespace
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import claude_cli
from providers import ApiCallError

MODEL='claude-sonnet-4-6'

def stream(*blocks, error=False, denied=None):
    events=[{'type':'system','subtype':'init','model':MODEL,'session_id':'fresh',
             'mcp_servers':[],'plugins':[],'tools':[]}]
    if blocks:events.append({'type':'assistant','message':{'model':MODEL,'content':list(blocks)}})
    for block in blocks:
        if block.get('type')=='tool_use':
            events.append({'type':'user','message':{'content':[{'type':'tool_result',
                'tool_use_id':block['id'],'content':'lecture effectuée'}]}})
    events.append({'type':'result','subtype':'success','is_error':error,'result':'réponse',
                   'session_id':'fresh','permission_denials':denied or [],
                   'modelUsage':{MODEL:{'inputTokens':4,'outputTokens':2}},
                   'usage':{'input_tokens':4,'output_tokens':2}})
    return '\n'.join(json.dumps(x,ensure_ascii=False) for x in events)


class ClaudeCliTests(unittest.TestCase):
    def test_timeout_preserves_partial_original_stream(self):
        partial=b'{"type":"system","subtype":"init"}\n'
        failure=subprocess.TimeoutExpired('fixture',600,output=partial)
        with patch('claude_cli.isolated_environment',return_value={}),patch('claude_cli.subprocess.run',side_effect=failure):
            with self.assertRaises(ApiCallError) as caught:claude_cli.complete_cli(MODEL,'system','question',1000)
        self.assertEqual(caught.exception.provider_trace,partial.decode('utf8'))
    def test_expired_credentials_refused_before_snapshot_or_provider_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);original=root/'original';original.mkdir();isolated=root/'isolated';isolated.mkdir()
            (original/'.credentials.json').write_text(json.dumps({'claudeAiOauth':{'expiresAt':int((time.time()-1)*1000)}}))
            with patch.dict('claude_cli.os.environ',{'CLAUDE_CONFIG_DIR':str(original)}):
                with self.assertRaisesRegex(ApiCallError,'Reconnecte'):
                    claude_cli.isolated_environment(isolated)
            self.assertFalse((isolated/'.credentials.json').exists())

    def test_fresh_auth_snapshot_never_writes_persistent_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);original=root/'original';original.mkdir();isolated=root/'isolated';isolated.mkdir()
            path=original/'.credentials.json';path.write_text(json.dumps({'claudeAiOauth':{'expiresAt':int((time.time()+7200)*1000)}}))
            before=path.read_bytes()
            with patch.dict('claude_cli.os.environ',{'CLAUDE_CONFIG_DIR':str(original)}):
                env=claude_cli.isolated_environment(isolated)
            self.assertEqual(path.read_bytes(),before)
            self.assertEqual((isolated/'.credentials.json').read_bytes(),before)
            self.assertEqual(env['CLAUDE_CONFIG_DIR'],str(isolated))
    def test_large_corpus_is_loaded_from_file_not_windows_command_line(self):
        corpus='c'*100000
        def execute(args,**kwargs):
            self.assertTrue(all(len(str(value))<30000 for value in args))
            path=Path(args[args.index('--system-prompt-file')+1])
            self.assertEqual(path.read_text(encoding='utf8'),corpus)
            return SimpleNamespace(returncode=0,stdout=stream())
        with patch('claude_cli.isolated_environment',return_value={}),patch('claude_cli.subprocess.run',side_effect=execute):
            self.assertEqual(claude_cli.complete_cli(MODEL,corpus,'question',1000).text,'réponse')
    def test_windows_npm_wrapper_resolves_native_executable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);shim=root/'claude.cmd';shim.write_text('wrapper')
            native=root/'node_modules/@anthropic-ai/claude-code/bin/claude.exe'
            native.parent.mkdir(parents=True);native.write_text('binary')
            with patch('claude_cli.shutil.which',side_effect=lambda name:str(shim) if name=='claude.cmd' else None):
                self.assertEqual(claude_cli.command(MODEL,'corpus')[0],str(native))
    def test_exact_model_success_trace_and_usage(self):
        raw=stream({'type':'text','text':'réponse'})
        result=claude_cli.parse_stream(raw,MODEL)
        self.assertEqual(result.text,'réponse')
        self.assertEqual(result.provider_trace,raw)
        self.assertEqual(result.usage['input_tokens'],4)
        self.assertEqual(result.usage['resolved_model'],MODEL)

    def test_toolless_judge_rejects_tools_and_malformed_or_incomplete_streams(self):
        for raw in [stream({'type':'tool_use','id':'x','name':'Read','input':{'file_path':'x'}}),
                    '{}',stream(error=True),stream()+'\ninvalid',stream(denied=[{'tool_name':'Read'}])]:
            with self.assertRaises(ApiCallError):claude_cli.parse_stream(raw,MODEL)

    def test_model_substitution_refused(self):
        with self.assertRaises(ApiCallError):claude_cli.parse_stream(stream(),'claude-opus-4-8')

    def test_hooks_and_truncated_streams_refused(self):
        raw=stream()+'\n'+json.dumps({'type':'system','subtype':'hook_started'})
        with self.assertRaises(ApiCallError):claude_cli.parse_stream(raw,MODEL)
        raw=stream().replace('"subtype": "success"','"subtype": "success", "stop_reason": "max_tokens"')
        with self.assertRaises(ApiCallError):claude_cli.parse_stream(raw,MODEL)

    def test_native_reads_only_archived_runtime_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'SKILL.md';path.write_text('skill')
            runtime={'root':str(root),'files':{'SKILL.md':claude_cli.file_sha(path)}}
            raw=stream({'type':'tool_use','id':'r','name':'Read','input':{'file_path':str(path)}})
            result=claude_cli.parse_stream(raw,MODEL,runtime=runtime)
            self.assertEqual(result.usage['loaded_files'][0]['path'],'SKILL.md')
            path.write_text('altéré')
            with self.assertRaises(ApiCallError):claude_cli.parse_stream(raw,MODEL,runtime=runtime)
            escaped=stream({'type':'tool_use','id':'r','name':'Read','input':{'file_path':str(root.parent/'secret')}})
            with self.assertRaises(ApiCallError):claude_cli.parse_stream(escaped,MODEL,runtime=runtime)
            for name in ['Bash','WebFetch','Agent']:
                with self.assertRaises(ApiCallError):
                    claude_cli.parse_stream(stream({'type':'tool_use','id':'x','name':name,'input':{}}),MODEL,runtime=runtime)

    def test_commands_no_fallback_no_resume_confined_and_no_tools_for_judge(self):
        judge=claude_cli.command(MODEL,'corpus')
        self.assertIn('--restricted',judge)
        self.assertIn('--strict-mcp-config',judge)
        self.assertEqual(judge[judge.index('--tools')+1],'')
        self.assertNotIn('--fallback-model',judge)
        self.assertNotIn('--resume',judge)
        native=claude_cli.command(MODEL,'',native=True)
        self.assertNotIn('--safe-mode',native)
        self.assertNotIn('--system-prompt',native)
        self.assertEqual(native[native.index('--tools')+1],'Read,Glob,Grep,Skill')


if __name__=='__main__':unittest.main()
