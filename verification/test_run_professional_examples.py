import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_professional_examples as native


class NativeEvidenceRejectionTests(unittest.TestCase):
    def test_zero_exit_does_not_hide_a_provider_error(self):
        events = [
            {"type": "api_error", "error": {"type": "rate_limit_error"}},
            {"type": "result", "subtype": "success", "is_error": False,
             "result": "Partial text must not count as a completed example."},
        ]
        result = native.summarize_events(events, 0, "en", Path("/tmp/isolated"))
        self.assertEqual(result["capture_status"], "execution_failed")

    def test_a_claimed_manifest_read_is_not_observed_loading(self):
        events = [{"type": "result", "subtype": "success", "is_error": False,
                   "result": "I loaded MANIFEST.md and revised the source."}]
        result = native.summarize_events(events, 0, "en", Path("/tmp/isolated"))
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
        result = native.summarize_events(events, 0, "en", Path("/tmp/isolated"))
        self.assertEqual(result["capture_status"], "guidance_not_observed")

    def test_outside_project_output_is_withheld_despite_other_failures(self):
        events = [
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "outside", "name": "Read",
                 "input": {"file_path": "/outside-project/private.txt"}},
            ]}},
            {"type": "result", "subtype": "success", "is_error": False,
             "result": "Outside-project content must never be written."},
        ]
        hashes = {
            path: native.digest((native.PACKAGE / path).read_bytes())
            for path in native.PACKAGE_FILES
        }
        facts = {"genre": {"en": "memo"}, "audience": {"en": "reviewer"}}
        for failure in ("malformed", "provider", "process"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory(
                prefix=".capture-privacy-", dir=native.ROOT
            ) as name:
                stream = [*events]
                if failure == "provider":
                    stream.append({"type": "api_error", "error": "Provider failed"})
                stdout = "\n".join(json.dumps(event) for event in stream)
                if failure == "malformed":
                    stdout += "\nnot a JSON event"
                completed = subprocess.CompletedProcess(
                    [], 1 if failure == "process" else 0, stdout, ""
                )
                refusal = None
                with patch("run_professional_examples.subprocess.run", return_value=completed):
                    try:
                        native.capture(
                            "research", "en", facts, "Source memo.", Path(name),
                            hashes, "test-model", "test-runtime", 10,
                        )
                    except RuntimeError as error:
                        refusal = error
                self.assertFalse(
                    (Path(name) / "research/en/output.md").exists(),
                    f"Outside-project output was persisted after {failure} failure",
                )
                self.assertIsNotNone(refusal)
                self.assertIn("output withheld", str(refusal))


if __name__ == "__main__":
    unittest.main()
