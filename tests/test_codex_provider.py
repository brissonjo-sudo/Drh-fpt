import json
import subprocess
import unittest
from unittest.mock import patch
import providers


class CodexProviderTests(unittest.TestCase):
    def test_all_cli_failure_paths_retain_the_original_stdout(self):
        fixtures = [(1, [{'type': 'error', 'message': 'fixture'}]),
                    (0, [{'type': 'turn.failed'}]),
                    (0, [{'type': 'error'}]),
                    (0, [{'type': 'item.completed', 'item': {'type': 'command_execution'}}]),
                    (0, [{'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'partial'}}]),
                    (0, [['not-an-event']]), (0, [{'type': []}]),
                    (0, [{'type': {}}]), (0, [{'type': None}]),
                    (0, [{'type': 'item.completed', 'item': 'not-an-item'}]),
                    (0, [{'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 3}}]),
                    (0, [{'type': 'turn.completed', 'usage': []}])]
        for code, events in fixtures:
            raw = '\n'.join(json.dumps(e) for e in events)
            with self.subTest(code=code, events=events), patch('providers.subprocess.run',
                    return_value=subprocess.CompletedProcess([], code, raw, 'private stderr')):
                with self.assertRaises(providers.ApiCallError) as caught:
                    providers.complete('codex', '', 'model', 'S', 'Q', 100)
                self.assertEqual(caught.exception.provider_trace, providers.annotate_codex_trace(raw, 'model'))
                self.assertNotIn('private stderr', str(caught.exception))

    def test_non_json_line_is_rejected_with_its_trace(self):
        raw = 'not json\n' + json.dumps({'type': 'turn.completed', 'usage': {}})
        with patch('providers.subprocess.run', return_value=subprocess.CompletedProcess([], 0, raw, '')):
            with self.assertRaisesRegex(providers.ApiCallError, 'mal formée') as caught:
                providers.complete('codex', '', 'model', 'S', 'Q', 100)
        self.assertTrue(caught.exception.provider_trace.endswith(raw))

    def test_timeout_retains_partial_provider_trace(self):
        partial=b'{"type":"thread.started","thread_id":"incomplete"}\n'
        with patch('providers.subprocess.run',side_effect=subprocess.TimeoutExpired(['codex'],300,output=partial)):
            with self.assertRaises(providers.ApiCallError) as caught:
                providers.complete('codex','','model','S','Q',100)
        header,raw=caught.exception.provider_trace.split('\n',1)
        self.assertEqual(raw,partial.decode('utf8'))
        self.assertEqual(json.loads(header)['statement'],'model : modèle demandé, non attesté')

    def test_preserves_usage_and_trace_in_fresh_tool_free_session(self):
        events = [
            {'type': 'thread.started', 'thread_id': 'fresh'},
            {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Réponse'}},
            {'type': 'turn.completed', 'usage': {'input_tokens': 15, 'output_tokens': 8}},
        ]
        stdout = '\n'.join(json.dumps(e) for e in events)
        with patch('providers.subprocess.run', return_value=subprocess.CompletedProcess([], 0, stdout, '')) as run:
            completion = providers.complete('codex', '', 'model-a', 'SKILL', 'QUESTION', 4000, 'medium')
        self.assertEqual(completion.text, 'Réponse')
        self.assertEqual(completion.response_id, 'fresh')
        self.assertEqual(completion.usage['input_tokens'], 15)
        header,raw=completion.provider_trace.split('\n',1)
        header=json.loads(header)
        self.assertEqual(raw,stdout)
        self.assertEqual(header['origin'],'local_harness')
        self.assertEqual(header['type'],'harness.model_identity')
        self.assertEqual(header['statement'],'model-a : modèle demandé, non attesté')
        self.assertIsNone(header['returned_model'])
        import hashlib
        self.assertEqual(header['provider_events_sha256'],hashlib.sha256(stdout.encode('utf8')).hexdigest())
        self.assertEqual(completion.usage['model_identity']['attestation'],'requested_unattested')
        command = run.call_args.args[0]
        self.assertIn('--ephemeral', command)
        self.assertIn('--ignore-user-config', command)
        self.assertIn('web_search="disabled"', command)

    def test_unexpected_tools_or_missing_completed_turn_cannot_pass(self):
        for events in [
            [{'type': 'item.completed', 'item': {'type': 'command_execution', 'command': 'read fixtures'}}],
            [{'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'partial'}}],
        ]:
            with self.subTest(events=events), patch('providers.subprocess.run',
                return_value=subprocess.CompletedProcess([], 0, '\n'.join(json.dumps(e) for e in events), '')):
                with self.assertRaises(providers.ApiCallError) as caught:
                    providers.complete('codex', '', 'model', 'S', 'Q', 100)
                header,raw=caught.exception.provider_trace.split('\n',1)
                self.assertEqual(json.loads(header)['statement'],'model : modèle demandé, non attesté')
                self.assertEqual(raw,'\n'.join(json.dumps(e) for e in events))


if __name__ == '__main__':
    unittest.main()
