from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from benchmark_layout import RecordingClient, load_protocol, run
from benchmark_writing import COMMON


ROOT = Path(__file__).parent
POPEN = subprocess.Popen


class LayoutRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="synthetic-layout-test-")
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "run"
        self.processes = []
        self.addCleanup(self.stop_processes)

    def stop_processes(self):
        for process in self.processes:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=2)
            process.stdin.close()
            process.stdout.close()

    def launch(self, scenario):
        def start(_args, **kwargs):
            process = POPEN([sys.executable, str(ROOT / "fixtures/layout_app_server.py"), scenario], **kwargs)
            self.processes.append(process)
            return process
        return patch("benchmark_writing.subprocess.Popen", side_effect=start)

    def records(self, name):
        return [json.loads(line) for line in (self.output / name).read_text().splitlines()]

    def assert_closed(self):
        self.assertTrue(self.processes)
        self.assertTrue(all(process.poll() is not None for process in self.processes))

    def test_frozen_schedule_cores_and_all_observed_methods_survive(self):
        with self.launch("success"):
            self.assertEqual(run(self.output), 12)
        records = self.records("results.jsonl")
        self.assertEqual(len(records), 12)
        self.assertEqual([(r["case_id"], r["arm"]) for r in records],
                         [("N1", "formal"), ("N1", "formal_layout"),
                          ("N2", "formal_layout"), ("N2", "formal"),
                          ("E1", "formal"), ("E1", "formal_layout"),
                          ("E2", "formal_layout"), ("E2", "formal"),
                          ("C1", "formal"), ("C1", "formal_layout"),
                          ("C2", "formal_layout"), ("C2", "formal")])
        journal = self.records("events.jsonl")
        starts = [e for e in journal if e.get("direction") == "sent" and e.get("method") == "thread/start"]
        turns = [e for e in journal if e.get("direction") == "sent" and e.get("method") == "turn/start"]
        protocol = json.loads((ROOT / "layout-generation-protocol.json").read_text())
        self.assertEqual(len(starts), 12)
        self.assertEqual(len(turns), 12)
        for result, request, turn in zip(records, starts, turns):
            instruction = request["params"]["developerInstructions"]
            self.assertTrue(instruction.endswith(protocol["cores"][result["arm"]]))
            self.assertEqual(request["params"]["model"], "gpt-6-astra")
            self.assertEqual(turn["params"]["effort"], "high")
            self.assertEqual(turn["params"]["input"], [{"type": "text", "text": protocol["prompts"][result["case_id"]]}])
            self.assertIn("Formal한 문체와 technical term을 유지한다.", instruction)
            self.assertEqual("짧은 기술 설명은 문장마다 빈 줄로 구분한다." in instruction,
                             result["arm"] == "formal_layout")
        self.assertEqual(sum(e.get("method") == "turn/completed" for e in journal), 12)
        self.assertEqual(sum(e.get("method") == "fixture/heartbeat" for e in journal), 12)
        self.assertEqual(records[0]["usage"]["reasoningOutputTokens"], 4)
        self.assert_closed()

    def test_source_fidelity_sends_only_frozen_four_trials(self):
        protocol_path = ROOT / "source-fidelity-protocol.json"
        protocol = json.loads(protocol_path.read_text())
        protocol_hash = hashlib.sha256(protocol_path.read_bytes()).hexdigest()
        previous = load_protocol(ROOT)
        self.assertEqual(protocol["cores"]["current"], previous["cores"]["formal_layout"])
        self.assertEqual(protocol["prompts"], {case: previous["prompts"][case] for case in ("N2", "E2")})
        with self.launch("success"):
            self.assertEqual(run(self.output, experiment="source-fidelity"), 4)
        records = self.records("results.jsonl")
        self.assertEqual([(r["case_id"], r["arm"]) for r in records],
                         [("N2", "current"), ("N2", "revised"),
                          ("E2", "revised"), ("E2", "current")])
        journal = self.records("events.jsonl")
        self.assertEqual(journal[0]["protocol_sha256"], protocol_hash)
        self.assertEqual(journal[-1], {"kind": "complete", "completed": 4})
        starts = [e for e in journal if e.get("direction") == "sent" and e.get("method") == "thread/start"]
        turns = [e for e in journal if e.get("direction") == "sent" and e.get("method") == "turn/start"]
        self.assertEqual((len(starts), len(turns)), (4, 4))
        for result, request, turn in zip(records, starts, turns):
            self.assertEqual(result["protocol_sha256"], protocol_hash)
            self.assertEqual(request["params"]["developerInstructions"], COMMON + "\n" + protocol["cores"][result["arm"]])
            self.assertEqual(request["params"]["model"], "gpt-6-astra")
            self.assertEqual(turn["params"]["effort"], "high")
            self.assertEqual(turn["params"]["input"], [{"type": "text", "text": protocol["prompts"][result["case_id"]]}])
        self.assert_closed()

    def test_source_fidelity_cli_reports_four_completed(self):
        stdout = io.StringIO()
        with self.launch("success"), redirect_stdout(stdout), \
             patch.object(sys, "argv", ["benchmark_layout.py", "--experiment", "source-fidelity", "--output", str(self.output)]):
            runpy.run_path(str(ROOT / "benchmark_layout.py"), run_name="__main__")
        self.assertEqual(stdout.getvalue().strip(), f"4회 생성 완료. 결과: {self.output.resolve() / 'results.jsonl'}")
        self.assertEqual(len(self.records("results.jsonl")), 4)
        self.assert_closed()

    def test_six_case_cli_sends_unchanged_revised_core_and_source_prompts(self):
        protocol_path = ROOT / "source-fidelity-six-protocol.json"
        protocol_hash = hashlib.sha256(protocol_path.read_bytes()).hexdigest()
        focused = load_protocol(ROOT, "source-fidelity")
        original = load_protocol(ROOT)
        stdout = io.StringIO()
        with self.launch("success"), redirect_stdout(stdout), \
             patch.object(sys, "argv", ["benchmark_layout.py", "--experiment", "source-fidelity-six", "--output", str(self.output)]):
            runpy.run_path(str(ROOT / "benchmark_layout.py"), run_name="__main__")
        self.assertEqual(stdout.getvalue().strip(), f"6회 생성 완료. 결과: {self.output.resolve() / 'results.jsonl'}")
        records = self.records("results.jsonl")
        self.assertEqual([(r["case_id"], r["arm"]) for r in records],
                         [(case, "revised") for case in ("N1", "N2", "E1", "E2", "C1", "C2")])
        journal = self.records("events.jsonl")
        self.assertEqual(journal[0]["protocol_sha256"], protocol_hash)
        self.assertEqual(journal[-1], {"kind": "complete", "completed": 6})
        starts = [e for e in journal if e.get("direction") == "sent" and e.get("method") == "thread/start"]
        turns = [e for e in journal if e.get("direction") == "sent" and e.get("method") == "turn/start"]
        self.assertEqual((len(starts), len(turns)), (6, 6))
        for result, request, turn in zip(records, starts, turns):
            self.assertEqual(result["core"], focused["cores"]["revised"])
            self.assertEqual(result["protocol_sha256"], protocol_hash)
            self.assertEqual(request["params"]["developerInstructions"], COMMON + "\n" + focused["cores"]["revised"])
            self.assertEqual(request["params"]["model"], "gpt-6-astra")
            self.assertEqual(turn["params"]["effort"], "high")
            self.assertEqual(turn["params"]["input"], [{"type": "text", "text": original["prompts"][result["case_id"]]}])
        self.assert_closed()

    def test_final_without_delta_preserves_output_and_unknown_ttft(self):
        with self.launch("final_only"):
            run(self.output)
        for result in self.records("results.jsonl"):
            self.assertIsNone(result["ttft_ms"])
            self.assertEqual(result["output"], "SYNTHETIC fixture only; not model output.")
        self.assert_closed()

    def test_eof_preserves_partial_usage_and_failure_stage(self):
        with self.launch("eof"), self.assertRaises(RuntimeError):
            run(self.output)
        self.assertEqual(len(self.records("results.jsonl")), 1)
        journal = self.records("events.jsonl")
        self.assertTrue(any(e.get("order") == 2 and e.get("delta") == "SYNTHETIC partial" for e in journal))
        self.assertTrue(any(e.get("order") == 2 and e.get("usage", {}).get("inputTokens") == 100 for e in journal))
        failure = next(e for e in journal if e["kind"] == "failure")
        self.assertEqual((failure["stage"], failure["order"], failure["completed"]), ("turn/start", 2, 1))
        self.assert_closed()

    def test_tool_item_is_recorded_and_stops_remaining_trials(self):
        with self.launch("tool"), self.assertRaisesRegex(RuntimeError, "item type"):
            run(self.output)
        self.assertEqual(len(self.records("results.jsonl")), 1)
        self.assertTrue(any(e.get("item_type") == "commandExecution" for e in self.records("events.jsonl")))
        self.assert_closed()

    def test_timeout_preserves_evidence_and_closes_child(self):
        with self.launch("timeout"), patch("benchmark_layout.TIMEOUT", 0.15), self.assertRaises(TimeoutError):
            run(self.output)
        failure = next(e for e in self.records("events.jsonl") if e["kind"] == "failure")
        self.assertEqual((failure["stage"], failure["completed"]), ("turn/start", 1))
        self.assert_closed()

    def test_startup_error_keeps_stage_and_does_not_log_error_body(self):
        with self.launch("init_error"), self.assertRaises(RuntimeError):
            run(self.output)
        journal = self.records("events.jsonl")
        failure = next(e for e in journal if e["kind"] == "failure")
        self.assertEqual((failure["stage"], failure["completed"]), ("initialize", 0))
        self.assertTrue(any(e.get("error_code") == -999 for e in journal))
        self.assertTrue(any(e["kind"] == "runtime" and e["command"][-1] == "init_error" for e in journal))
        self.assertNotIn("synthetic sensitive diagnostic", (self.output / "events.jsonl").read_text())
        self.assert_closed()

    def test_existing_output_is_not_overwritten(self):
        self.output.mkdir()
        sentinel = self.output / "results.jsonl"
        sentinel.write_text("existing evidence\n")
        with patch("benchmark_writing.subprocess.Popen", side_effect=AssertionError("must not launch")):
            with self.assertRaises(FileExistsError):
                run(self.output)
        self.assertEqual(sentinel.read_text(), "existing evidence\n")

    def test_initialize_interrupt_records_failure_and_closes_child(self):
        with self.launch("success"), patch.object(RecordingClient, "receive", side_effect=KeyboardInterrupt), \
             self.assertRaises(KeyboardInterrupt):
            run(self.output)
        self.assert_closed()
        failure = next(e for e in self.records("events.jsonl") if e["kind"] == "failure")
        self.assertEqual((failure["stage"], failure["error_type"]), ("initialize", "KeyboardInterrupt"))

    def test_turn_interrupt_retains_partial_evidence_and_closes_child(self):
        receive = RecordingClient.receive
        def interrupt(client, **kwargs):
            at, event = receive(client, **kwargs)
            if client.state["order"] == 2 and event.get("method") == "item/agentMessage/delta":
                raise KeyboardInterrupt
            return at, event
        with self.launch("success"), patch.object(RecordingClient, "receive", interrupt), self.assertRaises(KeyboardInterrupt):
            run(self.output)
        self.assert_closed()
        journal = self.records("events.jsonl")
        self.assertTrue(any(e.get("order") == 2 and e.get("delta") == "SYNTHETIC partial" for e in journal))
        failure = next(e for e in journal if e["kind"] == "failure")
        self.assertEqual((failure["stage"], failure["completed"], failure["error_type"]), ("turn/start", 1, "KeyboardInterrupt"))

    def test_changed_protocol_source_or_common_runner_is_rejected(self):
        fixture = Path(self.temp.name) / "inputs"
        fixture.mkdir()
        names = ["layout-generation-protocol.json", "source-fidelity-protocol.json", "source-fidelity-six-protocol.json",
                 "structure-layout-source.json", "benchmark_writing.py"]
        for name in names:
            shutil.copyfile(ROOT / name, fixture / name)
        for experiment, protocol_name in [("layout", names[0]), ("source-fidelity", names[1]),
                                          ("source-fidelity-six", names[2])]:
            for name in [protocol_name, *names[3:]]:
                with self.subTest(experiment=experiment, name=name):
                    original = (fixture / name).read_bytes()
                    (fixture / name).write_bytes(original + b" ")
                    with self.assertRaisesRegex(ValueError, "hash"):
                        load_protocol(fixture, experiment)
                    (fixture / name).write_bytes(original)


if __name__ == "__main__":
    unittest.main()
