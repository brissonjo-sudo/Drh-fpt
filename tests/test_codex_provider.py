import json
import subprocess
import unittest
from unittest.mock import patch
import providers


class CodexProviderTests(unittest.TestCase):
    def test_timeout_retains_partial_provider_trace(self):
        partial=b'{"type":"thread.started","thread_id":"incomplete"}\n'
        with patch('providers.subprocess.run',side_effect=subprocess.TimeoutExpired(['codex'],300,output=partial)):
            with self.assertRaises(providers.ApiCallError) as caught:
                providers.complete('codex','','model','S','Q',100)
        self.assertEqual(caught.exception.provider_trace,partial.decode('utf8'))

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
        self.assertEqual(completion.provider_trace, stdout)
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
                with self.assertRaises(providers.ApiCallError):
                    providers.complete('codex', '', 'model', 'S', 'Q', 100)


if __name__ == '__main__':
    unittest.main()
