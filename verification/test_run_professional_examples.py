import unittest
from pathlib import Path

from run_professional_examples import summarize_events


class NativeEvidenceRejectionTests(unittest.TestCase):
    def test_zero_exit_does_not_hide_a_provider_error(self):
        events = [
            {"type": "api_error", "error": {"type": "rate_limit_error"}},
            {"type": "result", "subtype": "success", "is_error": False,
             "result": "Partial text must not count as a completed example."},
        ]
        result = summarize_events(events, 0, "en", Path("/tmp/isolated"))
        self.assertEqual(result["capture_status"], "execution_failed")

    def test_a_claimed_manifest_read_is_not_observed_loading(self):
        events = [{"type": "result", "subtype": "success", "is_error": False,
                   "result": "I loaded MANIFEST.md and revised the source."}]
        result = summarize_events(events, 0, "en", Path("/tmp/isolated"))
        self.assertEqual(result["capture_status"], "guidance_not_observed")

    def test_a_denied_read_is_not_successful_loading(self):
        events = [
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "read-1", "name": "Read",
                 "input": {"file_path": "/tmp/isolated/.claude/skills/human-readable-writing/MANIFEST.md"}},
            ]}},
            {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "read-1", "is_error": True,
                 "content": "Permission denied"},
            ]}},
            {"type": "result", "subtype": "success", "is_error": False,
             "result": "A revision without loaded guidance."},
        ]
        result = summarize_events(events, 0, "en", Path("/tmp/isolated"))
        self.assertEqual(result["capture_status"], "guidance_not_observed")


if __name__ == "__main__":
    unittest.main()
