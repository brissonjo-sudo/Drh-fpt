"""Contrôles des invariants des adaptateurs, sans appel réseau."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import providers


class ProviderTests(unittest.TestCase):
    def test_anthropic_rejects_unimplemented_reasoning_effort(self):
        with self.assertRaises(providers.ApiCallError):
            providers.complete("anthropic", "key", "model", "system", "user", 10, "high")

    @patch("providers._request")
    def test_openai_normalizes_text_usage_and_truncation(self, request):
        request.return_value = ({
            "id": "resp_1", "status": "incomplete",
            "incomplete_details": {"reason": "max_output_tokens"},
            "output": [{"content": [{"type": "output_text", "text": "réponse"}]}],
            "usage": {"input_tokens": 12, "output_tokens": 4, "total_tokens": 16},
        }, 123)
        completion = providers.complete("openai", "key", "model", "system", "user", 10, "high")
        self.assertEqual(completion.text, "réponse")
        self.assertTrue(completion.truncated)
        self.assertEqual(completion.usage["input_tokens"], 12)

    @patch("providers._request")
    def test_anthropic_normalizes_usage(self, request):
        request.return_value = ({
            "id": "msg_1", "stop_reason": "end_turn",
            "content": [{"type": "text", "text": "réponse"}],
            "usage": {"input_tokens": 8, "output_tokens": 3},
        }, 50)
        completion = providers.complete("anthropic", "key", "model", "system", "user", 10)
        self.assertEqual(completion.text, "réponse")
        self.assertFalse(completion.truncated)
        self.assertEqual(completion.usage["output_tokens"], 3)


if __name__ == "__main__":
    unittest.main()
