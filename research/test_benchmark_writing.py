import unittest
from unittest.mock import patch

from benchmark_writing import Client


class MeasurementTests(unittest.TestCase):
    def client(self, tool=False):
        events = [
            (1.01, {"method": "item/agentMessage/delta", "params": {"itemId": "comment"}}),
            (1.02, {"method": "item/completed", "params": {"item": {
                "id": "comment", "type": "agentMessage", "phase": "commentary", "text": "working"}}}),
            (1.05, {"method": "item/agentMessage/delta", "params": {"itemId": "final"}}),
            (1.06, {"method": "item/completed", "params": {"item": {
                "id": "final", "type": "agentMessage", "phase": "final_answer", "text": "done"}}}),
            (1.07, {"method": "thread/tokenUsage/updated", "params": {"tokenUsage": {
                "total": {"inputTokens": 100, "cachedInputTokens": 50, "outputTokens": 10}}}}),
            (1.08, {"method": "turn/completed", "params": {"turn": {"status": "completed"}}}),
        ]
        if tool:
            events.insert(0, (1.005, {"id": 44, "method": "item/tool/call", "params": {
                "tool": "read_writing_reference"}}))
        client = object.__new__(Client)
        client.sequence = 0
        client.request = lambda *args: {"thread": {"id": "thread"}, "model": "test"}
        client.sent = []
        client.send = client.sent.append
        stream = iter(events)
        client.receive = lambda **kwargs: next(stream)
        return client

    @patch("benchmark_writing.time.perf_counter", return_value=1.0)
    def test_first_final_token_excludes_commentary(self, _clock):
        result = self.client().run("task", "baseline", "prompt", "reference", "test", "high", ".")
        self.assertEqual(result["ttft_ms"], 50)
        self.assertEqual(result["elapsed_ms"], 80)
        self.assertEqual(result["output"], "done")
        self.assertEqual(result["usage"]["cachedInputTokens"], 50)

    @patch("benchmark_writing.time.perf_counter", return_value=1.0)
    def test_reference_round_returns_frozen_content(self, _clock):
        client = self.client(tool=True)
        result = client.run("task", "loaded", "prompt", "frozen", "test", "high", ".")
        self.assertEqual(result["tool_rounds"], 1)
        self.assertEqual(client.sent[-1]["result"]["contentItems"][0]["text"], "frozen")

    @patch("benchmark_writing.time.perf_counter", return_value=1.0)
    def test_baseline_rejects_reference_call(self, _clock):
        with self.assertRaisesRegex(RuntimeError, "Unexpected tool call"):
            self.client(tool=True).run("task", "baseline", "prompt", "reference", "test", "high", ".")


if __name__ == "__main__":
    unittest.main()
