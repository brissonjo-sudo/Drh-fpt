import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import campaign
from providers import Completion, ApiCallError


class NativeFlowTests(unittest.TestCase):
    def test_diagnostic_native_does_not_receive_assembled_instructions(self):
        with tempfile.TemporaryDirectory() as tmp:
            completion=Completion('Réponse dégradée',False,{},'id',1,'{}')
            with patch.object(campaign,'RESULTS',Path(tmp)),patch('claude_cli.complete_cli',return_value=completion) as call:
                result=campaign.main(['--provider','claude-cli','--model','claude-sonnet-4-6',
                    '--mode','degraded','--case','14-echec-mauvaise-fp','--execution-profile','claude-native'])
            self.assertEqual(result,0)
            self.assertEqual(call.call_args.args[1],'')
            self.assertNotIn('CRITÈRES',call.call_args.args[2])
            self.assertNotIn('CONTRAT D',call.call_args.args[2])
            folder=next(Path(tmp).glob('*/'))
            data=json.loads(campaign.response_path(folder,'14-echec-mauvaise-fp').read_text(encoding='utf8'))
            self.assertEqual(data['context']['profile'],'claude-native')
            self.assertTrue((folder/'runtime/14-echec-mauvaise-fp/_runtime.json').exists())

    def test_pending_game_stops_before_any_provider_call(self):
        with patch.object(campaign,'complete') as call:
            with self.assertRaisesRegex(SystemExit,'approuv'):
                campaign.main(['--suite','qualification-a-v1','--provider','codex','--mode','degraded'])
            call.assert_not_called()

    def test_failed_claude_call_is_reported_and_original_trace_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(campaign,'RESULTS',Path(tmp)),patch('claude_cli.complete_cli',side_effect=ApiCallError('échec',provider_trace='{"type":"error"}')):
                result=campaign.main(['--provider','claude-cli','--model','claude-sonnet-4-6',
                    '--mode','degraded','--case','14-echec-mauvaise-fp','--execution-profile','claude-native'])
            self.assertEqual(result,1)
            folder=next(Path(tmp).glob('*/'))
            self.assertEqual((folder/'14-echec-mauvaise-fp-respondant-failed.jsonl').read_text(encoding='utf8'),'{"type":"error"}')


if __name__=='__main__':unittest.main()
