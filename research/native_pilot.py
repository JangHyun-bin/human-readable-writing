"""Enable, inspect, or remove the frozen writing core in the shared instructions."""

import argparse
import os
from pathlib import Path
import tempfile

from benchmark_writing import CORE


def configure(target, action):
    if action not in {"enable", "disable", "status"}:
        raise ValueError("Unknown action")
    target = Path(target).resolve(strict=True)
    before = target.read_bytes()
    core = CORE.encode("utf-8")
    block = b"\n" + core + b"\n"
    count = before.count(block)
    if count > 1 or core in before.replace(block, b""):
        raise ValueError("Conflicting copies of the writing core; file left unchanged")
    status = "enabled" if count else "disabled"
    if action == "status":
        return status
    if action == "enable":
        after = before if count else before + block
    else:
        after = before.replace(block, b"", 1)
    if after == before:
        return status

    descriptor, temporary = tempfile.mkstemp(prefix=".writing-core-", dir=target.parent)
    try:
        with os.fdopen(descriptor, "wb") as out:
            os.fchmod(out.fileno(), target.stat().st_mode & 0o777)
            out.write(after)
            out.flush()
            os.fsync(out.fileno())
        if target.read_bytes() != before:
            raise RuntimeError("Instructions changed during update; retry after checking the file")
        os.replace(temporary, target)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return "enabled" if action == "enable" else "disabled"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["enable", "disable", "status"], nargs="?", default="status")
    args = parser.parse_args()
    target = Path.home() / ".agents/TERMINOLOGY.md"
    try:
        status = configure(target, args.action)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"{status}: {target}")


if __name__ == "__main__":
    main()
