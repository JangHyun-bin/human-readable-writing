from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from benchmark_writing import CORE
from native_pilot import configure


class NativePilotTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix="native-core-test-")
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)
        self.target = self.folder / "TERMINOLOGY.md"
        self.original = b"# Existing policy\r\nKeep every byte.\r\n"
        self.target.write_bytes(self.original)

    def test_enable_is_idempotent_and_disable_restores_original(self):
        self.assertEqual(configure(self.target, "enable"), "enabled")
        first = self.target.read_bytes()
        self.assertTrue(first.startswith(self.original))
        self.assertEqual(first.count(CORE.encode()), 1)
        self.assertEqual(configure(self.target, "enable"), "enabled")
        self.assertEqual(self.target.read_bytes(), first)
        self.assertEqual(configure(self.target, "disable"), "disabled")
        self.assertEqual(self.target.read_bytes(), self.original)

    def test_disable_keeps_policy_added_after_enable(self):
        configure(self.target, "enable")
        with self.target.open("ab") as out:
            out.write(b"\nNew policy added later.\n")
        configure(self.target, "disable")
        self.assertEqual(self.target.read_bytes(), self.original + b"\nNew policy added later.\n")

    def test_status_does_not_replace_or_write_the_file(self):
        before = self.target.stat()
        self.assertEqual(configure(self.target, "status"), "disabled")
        self.assertEqual(self.target.read_bytes(), self.original)
        self.assertEqual(self.target.stat().st_ino, before.st_ino)
        self.assertEqual(self.target.stat().st_mtime_ns, before.st_mtime_ns)

    def test_duplicate_or_unframed_core_is_rejected_without_writing(self):
        block = b"\n" + CORE.encode() + b"\n"
        for contents in [self.original + block + block, self.original + b"Quote: " + CORE.encode()]:
            with self.subTest(contents=contents[:20]):
                self.target.write_bytes(contents)
                with self.assertRaises(ValueError):
                    configure(self.target, "enable")
                self.assertEqual(self.target.read_bytes(), contents)

    def test_symlink_and_file_permissions_are_preserved(self):
        self.target.chmod(0o600)
        pointer = self.folder / "AGENTS.md"
        pointer.symlink_to(self.target)
        configure(pointer, "enable")
        self.assertTrue(pointer.is_symlink())
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o600)

    def test_failed_replace_preserves_original_and_removes_temporary_file(self):
        with patch("native_pilot.os.replace", side_effect=PermissionError("blocked")):
            with self.assertRaises(PermissionError):
                configure(self.target, "enable")
        self.assertEqual(self.target.read_bytes(), self.original)
        self.assertEqual(list(self.folder.iterdir()), [self.target])


if __name__ == "__main__":
    unittest.main()
