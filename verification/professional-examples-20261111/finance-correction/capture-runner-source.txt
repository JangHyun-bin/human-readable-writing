"""Capture native writing examples without treating execution as fidelity proof."""

import argparse
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CASES = ("research", "finance", "capex", "policy", "architecture")
PACKAGE = ROOT / "skills/human-readable-writing"
PACKAGE_FILES = (
    "SKILL.md", "MANIFEST.md", "LICENSE", "NOTICE.md",
    "agents/openai.yaml", "references/korean.md", "references/language-support.md",
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def public_text(text, project):
    text = text.replace(str(project), "${PROJECT}")
    text = text.replace(str(project.resolve()), "${PROJECT}")
    text = text.replace(str(Path.home()), "${HOME}")
    return re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "${EMAIL}", text)


def summarize_events(events, exit_code, language, project):
    tools = {}
    results = {}
    models = set()
    errors = []
    final = None
    for event in events:
        if event.get("type") in ("error", "api_error"):
            errors.append(event.get("error", event.get("message", "native error")))
        if event.get("type") == "result":
            final = event
            if event.get("is_error") or event.get("subtype") != "success":
                errors.append(event.get("subtype", "unsuccessful result"))
        message = event.get("message", {})
        if not isinstance(message, dict):
            continue
        if message.get("model"):
            models.add(message["model"])
        for block in message.get("content", []):
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                tools[block["id"]] = block
            elif block.get("type") == "tool_result":
                results[block["tool_use_id"]] = not block.get("is_error", False)
    reads = []
    external_read = False
    for tool_id, block in tools.items():
        if block.get("name") != "Read":
            continue
        filename = block.get("input", {}).get("file_path")
        if not filename:
            continue
        path = Path(filename)
        path = (path if path.is_absolute() else project / path).resolve()
        try:
            relative = str(path.relative_to(project.resolve()))
        except ValueError:
            relative = "${OUTSIDE_PROJECT}"
            external_read = True
        reads.append({"path": relative, "succeeded": results.get(tool_id, False)})
    manifest = any(r["succeeded"] and r["path"].endswith("/MANIFEST.md") for r in reads)
    korean = any(r["succeeded"] and r["path"].endswith("/references/korean.md") for r in reads)
    output = final.get("result", "") if final else ""
    if not isinstance(output, str):
        output = ""
    if exit_code != 0 or errors or not final or not output.strip():
        status = "execution_failed"
    elif external_read:
        status = "unexpected_context_read"
    elif not manifest or (language == "ko" and not korean):
        status = "guidance_not_observed"
    else:
        status = "captured"
    return {
        "capture_status": status,
        "exit_code": exit_code,
        "observed_models": sorted(models),
        "manifest_read": manifest,
        "korean_reference_read": korean,
        "tool_reads": reads,
        "provider_errors": errors,
        "output": output,
        "fidelity_status": "not_reviewed",
    }


def load_case(case_id):
    directory = ROOT / "examples/professional" / case_id
    facts = json.loads((directory / "facts.json").read_text())
    if facts["id"] != case_id:
        raise ValueError(f"Case ID mismatch: {case_id}")
    ids = [fact["id"] for fact in facts["facts"]]
    if not 6 <= len(ids) <= 10 or len(set(ids)) != len(ids):
        raise ValueError(f"Invalid fact identifiers: {case_id}")
    drafts = {}
    for language in ("en", "ko"):
        for field in ("genre", "topic", "audience"):
            if not facts[field][language].strip():
                raise ValueError(f"Missing {case_id}/{field}/{language}")
        for fact in facts["facts"]:
            if not fact[language].strip():
                raise ValueError(f"Missing {case_id}/{fact['id']}/{language}")
        drafts[language] = (directory / f"before.{language}.md").read_text()
        if not drafts[language].strip():
            raise ValueError(f"Missing source draft: {case_id}/{language}")
    return facts, drafts


def capture(case_id, language, facts, source, output_root, package_hashes, model, runtime,
            timeout, *, executable="claude", request_override=None):
    target = output_root / case_id / language
    target.mkdir(parents=True, exist_ok=False)
    language_name = "English" if language == "en" else "Korean"
    request = request_override if request_override is not None else (
        f"/human-readable-writing Edit this {facts['genre']['en']} in {language_name} "
        f"for {facts['audience']['en']}. Return only the revised document. "
        "Preserve its genre, tables, specialized terms, facts, quantities, units, periods, "
        "denominators, conditions, exclusions, negation, uncertainty, attribution, "
        "and the strength of judgments. Add no evidence, assumptions, outcomes, "
        "approvals, guarantees, or recommendations absent from the source.\n\n"
        "Source text:\n\n" + source
    )
    (target / "request.md").write_text(request)
    with tempfile.TemporaryDirectory(prefix=f"hrw-{case_id}-{language}-") as name:
        project = Path(name).resolve()
        installed = project / ".claude/skills/human-readable-writing"
        shutil.copytree(PACKAGE, installed)
        if {p: digest((installed / p).read_bytes()) for p in PACKAGE_FILES} != package_hashes:
            raise ValueError("Installed package differs from the frozen snapshot")
        argv = [
            str(executable), "-p", "--model", model,
            "--setting-sources", "project,local",
            "--settings", '{"disableAllHooks":true}',
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            "--tools", "Read,Skill", "--allowedTools", "Read,Skill",
            "--permission-mode", "dontAsk", "--output-format", "stream-json",
            "--verbose", "--no-session-persistence", request,
        ]
        environment = os.environ.copy()
        environment.pop("CLAUDECODE", None)
        environment["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
        started = datetime.now(timezone.utc).isoformat()
        try:
            result = subprocess.run(argv, cwd=project, env=environment, capture_output=True,
                                    text=True, timeout=timeout)
            stdout, stderr, code = result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired as error:
            stdout = error.stdout or b""
            stderr = error.stderr or b""
            stdout = stdout.decode() if isinstance(stdout, bytes) else stdout
            stderr = stderr.decode() if isinstance(stderr, bytes) else stderr
            stderr += "\nNative process exceeded the configured timeout."
            code = 124
        events = []
        malformed = False
        for line in stdout.splitlines():
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError("Non-object event")
                events.append(value)
            except (json.JSONDecodeError, ValueError):
                malformed = True
        summary = summarize_events(events, code, language, project)
        if malformed:
            summary["capture_status"] = "malformed_event_stream"
        output = summary.pop("output")
        if summary["capture_status"] == "unexpected_context_read":
            raise RuntimeError("Native process read outside its isolated project; output withheld")
        (target / "output.md").write_text(output)
        (target / "stderr.txt").write_text(public_text(stderr, project))
        safe_errors = public_text(json.dumps(summary["provider_errors"], ensure_ascii=False), project)
        summary["provider_errors"] = json.loads(safe_errors)
        summary.update({
            "case_id": case_id, "language": language,
            "request_kind": "review_feedback_correction" if request_override is not None else "source_revision",
            "started_at": started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "runtime": runtime, "requested_model": model,
            "argv": [public_text(arg, project) for arg in argv[:-1]] + ["${REQUEST}"],
            "request_file": "request.md", "output_file": "output.md",
            "input_sha256": digest(source.encode()),
            "request_sha256": digest(request.encode()),
            "output_sha256": digest(output.encode()),
            "raw_event_stream_sha256": digest(stdout.encode()),
            "package_sha256": package_hashes,
            "privacy": "Only derived tool-read evidence is public; raw initialization events are not published.",
        })
        save_json(target / "attempt.json", summary)
        return {"case_id": case_id, "language": language,
                "capture_status": summary["capture_status"],
                "fidelity_status": "not_reviewed", "path": str(target.relative_to(ROOT))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", choices=CASES)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="claude-sonnet-5-5")
    parser.add_argument("--workers", type=int, default=5, choices=range(1, 6))
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    selected = args.case or list(CASES)
    if len(set(selected)) != len(selected):
        parser.error("A case may only be selected once")
    output_root = args.output.resolve()
    if not output_root.is_relative_to(ROOT / "verification"):
        parser.error("Output must be a new directory inside verification/")
    packets = {case_id: load_case(case_id) for case_id in selected}
    package_hashes = {path: digest((PACKAGE / path).read_bytes()) for path in PACKAGE_FILES}
    executable = Path(shutil.which("claude")).resolve()
    runtime = subprocess.run([str(executable), "--version"], capture_output=True, text=True, check=True).stdout.strip()
    base_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                 capture_output=True, text=True, check=True).stdout.strip()
    output_root.mkdir(parents=True, exist_ok=False)
    for case_id, (facts, _) in packets.items():
        directory = output_root / case_id
        directory.mkdir()
        save_json(directory / "facts.json", facts)
    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        for case_id, (facts, drafts) in packets.items():
            for language, source in drafts.items():
                futures.append(executor.submit(capture, case_id, language, facts, source,
                                               output_root, package_hashes, args.model,
                                               runtime, args.timeout, executable=executable))
        for future in concurrent.futures.as_completed(futures):
            records.append(future.result())
            print(json.dumps(records[-1], ensure_ascii=False), flush=True)
    manifest = {
        "scope": "Native professional writing examples, not a readability benchmark",
        "source": "Working-tree package snapshot; not a claim of GitHub default-branch availability",
        "base_commit": base_commit, "runtime": runtime,
        "model": args.model, "package_sha256": package_hashes,
        "records": sorted(records, key=lambda record: (record["case_id"], record["language"])),
        "fidelity_status": "not_reviewed",
    }
    save_json(output_root / "manifest.json", manifest)
    return 0 if all(record["capture_status"] == "captured" for record in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
