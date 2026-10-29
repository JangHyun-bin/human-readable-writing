"""Run a frozen writing pilot into a new evidence directory."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

from benchmark_writing import Client, COMMON


PROTOCOLS = {
    "layout": ("layout-generation-protocol.json",
               "a0573f11039be65b0462217ce5c41ef498b4518c2d7bcfe85256e748f5986331"),
    "source-fidelity": ("source-fidelity-protocol.json",
                        "f7237f874c55b1aa3a87947b9fd861c3e43a2f5fec1e7f8c2931c412b8bfb4ef"),
    "source-fidelity-six": ("source-fidelity-six-protocol.json",
                            "d7e4c1d17a1ed40908c571f15315b104f1a7b03b46f53ed830865fb6d7e665fc"),
}
TIMEOUT = 180


def load_protocol(root, experiment="layout"):
    name, expected_hash = PROTOCOLS[experiment]
    raw = (root / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_hash:
        raise ValueError("Frozen protocol hash mismatch")
    protocol = json.loads(raw)
    for name, key in [("structure-layout-source.json", "source_sha256"),
                      ("benchmark_writing.py", "common_runner_sha256")]:
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != protocol[key]:
            raise ValueError(f"Frozen input hash mismatch: {name}")
    return protocol


def write_record(stream, record):
    stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    stream.flush()


class RecordingClient(Client):
    def __init__(self, stderr, journal, state):
        self.journal, self.state = journal, state
        self.origin = time.perf_counter()
        self.runtime_recorded = False
        try:
            super().__init__(stderr)
        except (KeyboardInterrupt, SystemExit):
            if hasattr(self, "process"):
                self.close()
            raise

    def send(self, message):
        self.state["stage"] = message.get("method", self.state["stage"])
        if not self.runtime_recorded:
            write_record(self.journal, {"kind": "runtime", "command": self.process.args})
            self.runtime_recorded = True
        write_record(self.journal, {"kind": "event", **self.state,
                                   "direction": "sent", **message})
        super().send(message)

    def receive(self, timeout=TIMEOUT):
        at, event = super().receive(timeout=timeout)
        params = event.get("params", {})
        item = params.get("item", {})
        record = {"kind": "event", **self.state, "direction": "received",
                  "at_ms": round((at - self.origin) * 1000, 3),
                  "method": event.get("method"), "id": event.get("id"),
                  "thread_id": params.get("threadId"), "item_type": item.get("type"),
                  "item_id": item.get("id", params.get("itemId"))}
        # Error bodies and tool arguments can contain unrelated sensitive content.
        if event.get("error"):
            error = event["error"]
            record["error_code"] = error.get("code") if isinstance(error, dict) else None
            record["error_present"] = True
        if event.get("method") == "item/agentMessage/delta":
            record["delta"] = params.get("delta")
        if item.get("type") == "agentMessage":
            record.update(text=item.get("text"), phase=item.get("phase"))
        if event.get("method") == "thread/tokenUsage/updated":
            record["usage"] = params["tokenUsage"]["total"]
        if "turn" in params:
            record["turn_status"] = params["turn"].get("status")
        write_record(self.journal, record)
        return at, event

    def request(self, method, params):
        self.sequence += 1
        request_id = self.sequence
        deadline = time.perf_counter() + TIMEOUT
        self.send({"id": request_id, "method": method, "params": params})
        while True:
            _, event = self.receive(timeout=max(0, deadline - time.perf_counter()))
            if event.get("error"):
                raise RuntimeError("App-server RPC failed; inspect event metadata and stderr")
            if event.get("id") == request_id:
                return event["result"]

    def generate(self, prompt, core, model, effort, cwd):
        thread = self.request("thread/start", {
            "model": model, "cwd": str(cwd), "ephemeral": True, "environments": [],
            "sandbox": "read-only", "approvalPolicy": "never",
            "developerInstructions": COMMON + "\n" + core,
            "dynamicTools": [{"type": "function", "name": "read_writing_reference",
                              "description": "Read the frozen writing skill and manifest.",
                              "inputSchema": {"type": "object", "properties": {},
                                              "additionalProperties": False}}],
        })
        if thread["model"] != model:
            raise RuntimeError("Requested model was not selected")
        thread_id = thread["thread"]["id"]
        self.sequence += 1
        started = time.perf_counter()
        self.send({"id": self.sequence, "method": "turn/start", "params": {
            "threadId": thread_id, "input": [{"type": "text", "text": prompt}], "effort": effort}})
        deltas, finals, item_types, methods = {}, {}, set(), set()
        usage = None
        while True:
            at, event = self.receive(timeout=max(0, started + TIMEOUT - time.perf_counter()))
            if event.get("error"):
                raise RuntimeError("App-server turn failed; inspect event metadata and stderr")
            method, params = event.get("method", ""), event.get("params", {})
            if params.get("threadId") not in (None, thread_id):
                continue
            methods.add(method)
            item = params.get("item", {})
            if item.get("type"):
                item_types.add(item["type"])
                if item["type"] not in {"agentMessage", "reasoning", "userMessage"}:
                    raise RuntimeError("Unexpected item type; trial stopped")
            if method.startswith("item/") and method not in {"item/started", "item/completed"}:
                if not method.startswith(("item/agentMessage/", "item/reasoning/")):
                    raise RuntimeError("Unexpected item method; trial stopped")
            if method == "item/agentMessage/delta":
                deltas.setdefault(params["itemId"], at)
            elif method == "item/completed" and item.get("type") == "agentMessage":
                if item.get("phase") != "commentary":
                    finals[item["id"]] = item["text"]
            elif method == "thread/tokenUsage/updated":
                usage = params["tokenUsage"]["total"]
            elif method == "turn/completed":
                if params["turn"]["status"] != "completed":
                    raise RuntimeError("Turn did not complete successfully")
                finished = at
                break
        if not finals or usage is None:
            raise RuntimeError("Missing final output or usage; partial evidence retained")
        first = min(deltas[key] for key in finals) if all(key in deltas for key in finals) else None
        return {"model": thread["model"], "effort": effort, "thread_id": thread_id,
                "ttft_ms": round((first - started) * 1000, 3) if first is not None else None,
                "elapsed_ms": round((finished - started) * 1000, 3), "usage": usage,
                "output": "\n".join(finals.values()), "observed_item_types": sorted(item_types),
                "observed_methods": sorted(methods)}

    def close(self):
        try:
            super().close()
        finally:
            self.process.stdin.close()
            self.process.stdout.close()


def run(output, *, experiment="layout"):
    root = Path(__file__).resolve().parent
    protocol = load_protocol(root, experiment)
    protocol_hash = PROTOCOLS[experiment][1]
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    state = {"stage": "startup", "order": None, "case_id": None, "arm": None}
    client, completed = None, 0
    with (output / "events.jsonl").open("x") as journal, \
         (output / "results.jsonl").open("x") as results, \
         (output / "app-server.stderr").open("x") as stderr:
        write_record(journal, {"kind": "start", "recorded_at": datetime.now(timezone.utc).isoformat(),
                              "protocol_sha256": protocol_hash,
                              "adapter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                              "source_sha256": protocol["source_sha256"],
                              "common_runner_sha256": protocol["common_runner_sha256"],
                              "cwd": str(output), "event_clock_origin": "client construction"})
        try:
            client = RecordingClient(stderr, journal, state)
            for order, trial in enumerate(protocol["schedule"], 1):
                case_id, arm = trial["case_id"], trial["arm"]
                state.update(order=order, case_id=case_id, arm=arm, stage="trial/start")
                write_record(journal, {"kind": "trial_start", **state})
                prompt, core = protocol["prompts"][case_id], protocol["cores"][arm]
                result = client.generate(prompt, core, protocol["model"], protocol["effort"], output)
                result.update(order=order, case_id=case_id, arm=arm, prompt=prompt, core=core,
                              protocol_sha256=protocol_hash,
                              recorded_at=datetime.now(timezone.utc).isoformat())
                write_record(results, result)
                completed += 1
            write_record(journal, {"kind": "complete", "completed": completed})
        except BaseException as error:
            write_record(journal, {"kind": "failure", **state, "completed": completed,
                                  "error_type": type(error).__name__,
                                  "usage_status": "consult observed usage events; missing usage is unknown"})
            raise
        finally:
            if client is not None:
                client.close()
    return completed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", choices=PROTOCOLS, default="layout")
    parser.add_argument("--output", type=Path, required=True, help="New evidence directory; never reused")
    args = parser.parse_args()
    completed = run(args.output, experiment=args.experiment)
    print(f"{completed}회 생성 완료. 결과: {args.output.resolve() / 'results.jsonl'}")
