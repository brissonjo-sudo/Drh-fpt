import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
from providers import ApiCallError, Completion
import quota_guard
import campaign


def trace(usage, reset=110, weekly=.44, weekly_reset=1000, status='allowed'):
    return json.dumps({'type': 'rate_limit_event', 'rate_limit_info': {
        'status': status, 'unifiedWindows': {
            'five_hour': {'utilization': usage, 'resetsAt': reset},
            'seven_day': {'utilization': weekly, 'resetsAt': weekly_reset}}}})


def completion(raw):
    return Completion('OK', False, {}, 'diagnostic', 1, raw)


class QuotaGuardTests(unittest.TestCase):
    def test_game_closed_during_wait_prevents_even_the_next_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            clock = [100]
            root = Path(tmp)
            (root/'state.json').write_text(json.dumps(quota_guard.snapshot(trace(1.01))), encoding='utf8')
            probe, target = Mock(), Mock()
            def validate():
                if clock[0] >= 111:
                    raise ValueError('closed during wait')
            guard = quota_guard.Controller(root, probe=probe, now=lambda: clock[0],
                sleep=lambda seconds: clock.__setitem__(0, clock[0]+seconds), validate=validate,
                emit=lambda _: None)
            with self.assertRaisesRegex(ValueError, 'closed during wait'):
                guard.call('claude-opus-4-8', 'high', target)
            probe.assert_not_called()
            target.assert_not_called()

    def test_runtime_invalid_before_admission_does_not_even_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            probe = Mock(return_value=completion(trace(.1)))
            def validate():
                raise ValueError('closed game')
            guard = quota_guard.Controller(Path(tmp), probe=probe, now=lambda: 100, validate=validate)
            with self.assertRaisesRegex(ValueError, 'closed game'):
                guard.call('claude-sonnet-4-6', 'high', lambda: self.fail('target called'))
            probe.assert_not_called()

    def test_codex_call_rechecks_runtime_without_using_claude_admission(self):
        guard = Mock()
        guard.validate.side_effect = ValueError('closed game')
        target = Mock()
        with self.assertRaisesRegex(ValueError, 'closed game'):
            campaign.call_with_admission(guard, 'codex', 'gpt-6.1-sol', 'high', target)
        target.assert_not_called()
        guard.call.assert_not_called()

    def test_post_wait_runtime_validation_precedes_the_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Mock()
            def validate():
                raise ValueError('candidate changed')
            guard = quota_guard.Controller(Path(tmp), probe=lambda *_: completion(trace(.1)),
                now=lambda: 100, validate=validate)
            with self.assertRaisesRegex(ValueError, 'candidate changed'):
                guard.call('claude-sonnet-4-6', 'high', target)
            target.assert_not_called()

    def test_campaign_admission_wraps_claude_only_without_changing_role_model(self):
        guard = Mock()
        guard.call.return_value = 'guarded'
        target = Mock(return_value='direct')
        self.assertEqual(campaign.call_with_admission(guard, 'claude-cli', 'claude-opus-4-8', 'high', target), 'guarded')
        guard.call.assert_called_once_with('claude-opus-4-8', 'high', target)
        target.assert_not_called()
        self.assertEqual(campaign.call_with_admission(guard, 'codex', 'gpt-6.1-sol', 'high', target), 'direct')
        self.assertEqual(campaign.call_with_admission(None, 'claude-cli', 'claude-opus-4-8', 'high', target), 'direct')

    def test_invalid_probe_is_archived_before_refusing_the_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            guard = self.controller(tmp, lambda *_: completion('{}'), [100], lambda _: None)
            with self.assertRaises(ValueError):
                guard.call('claude-sonnet-4-6', 'high', lambda: self.fail('target called'))
            paths = list((Path(tmp)/'probes').glob('*.jsonl'))
            self.assertEqual(len(paths), 1)
            self.assertEqual(paths[0].read_text(encoding='utf8'), '{}')

    def test_existing_lease_file_without_live_os_lock_does_not_block_forever(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'admission.lock').write_bytes(b'old process ended')
            guard = self.controller(tmp, lambda *_: completion(trace(.1)), [100], lambda _: self.fail('stale file blocked'))
            guard.call('claude-sonnet-4-6', 'high', lambda: None)

    def controller(self, folder, probe, clock, sleep):
        return quota_guard.Controller(Path(folder), probe=probe, now=lambda: clock[0],
            sleep=sleep, emit=lambda _: None)

    def test_waits_before_any_qualification_call_without_retrying_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            clock = [100]
            def sleep(seconds):
                self.assertLessEqual(seconds, 30)
                clock[0] += seconds
            probe = Mock(side_effect=[completion(trace(.9)), completion(trace(.1, reset=200))])
            target = Mock(return_value='one answer')
            guard = self.controller(tmp, probe, clock, sleep)
            self.assertEqual(guard.call('claude-sonnet-4-6', 'high', target), 'one answer')
            target.assert_called_once_with()
            self.assertEqual(clock[0], 111)
            self.assertEqual(len(list((Path(tmp)/'probes').glob('*.jsonl'))), 2)

    def test_quota_rejected_probe_is_preserved_but_target_not_retried(self):
        with tempfile.TemporaryDirectory() as tmp:
            clock = [100]
            probe = Mock(side_effect=[ApiCallError('quota', provider_trace=trace(1.01, status='rejected')),
                                     completion(trace(.1, reset=200))])
            guard = self.controller(tmp, probe, clock, lambda seconds: clock.__setitem__(0, clock[0]+seconds))
            target = Mock(side_effect=ApiCallError('target failure'))
            with self.assertRaisesRegex(ApiCallError, 'target failure'):
                guard.call('claude-opus-4-8', 'high', target)
            target.assert_called_once()
            self.assertEqual(probe.call_args.args, ('claude-opus-4-8', 'high'))

    def test_weekly_budget_is_checked_even_after_five_hour_reset(self):
        with tempfile.TemporaryDirectory() as tmp:
            clock = [100]
            probe = Mock(side_effect=[completion(trace(.1, reset=110, weekly=.9, weekly_reset=150)),
                                     completion(trace(.1, reset=200, weekly=.1, weekly_reset=300))])
            guard = self.controller(tmp, probe, clock, lambda seconds: clock.__setitem__(0, clock[0]+seconds))
            guard.call('claude-opus-4-8', 'high', lambda: None)
            self.assertEqual(clock[0], 151)

    def test_missing_or_malformed_quota_data_prevents_the_target_call(self):
        for raw in ['{}', trace(-.1), trace(float('nan')), trace(.1).replace('110', 'true')]:
            with self.subTest(raw=raw), tempfile.TemporaryDirectory() as tmp:
                target = Mock()
                guard = self.controller(tmp, lambda *_: completion(raw), [100], lambda _: None)
                with self.assertRaises(ValueError):
                    guard.call('claude-sonnet-4-6', 'high', target)
                target.assert_not_called()

    def test_known_exhausted_window_waits_before_even_the_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            clock = [100]
            root = Path(tmp)
            root.joinpath('state.json').write_text(json.dumps(quota_guard.snapshot(trace(1.01))))
            def probe(*_):
                self.assertGreater(clock[0], 110)
                return completion(trace(.1, reset=200))
            guard = self.controller(tmp, probe, clock, lambda seconds: clock.__setitem__(0, clock[0]+seconds))
            guard.call('claude-sonnet-4-6', 'high', lambda: None)


if __name__ == '__main__':
    unittest.main()
