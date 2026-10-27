"""Small Codex app-server pilot; runs only when explicitly executed."""

import argparse
import json
from pathlib import Path
import queue
import subprocess
import threading
import time
import tomllib


REFERENCE = "aefe5a8cca80e7ef9ed4fbeaeb975aaee952a53e"
CORE = "기술 설명은 명사 연쇄의 관계와 주체·행동·조건을 분명하게 쓴다. 수치·단위·범위·부정·불확실성을 보존하고 관찰·가설·확인한 인과를 구분한다."
COMMON = """This is a controlled writing experiment. Follow the current task, reply in Korean
with English technical terms, and output only the final requested prose. For this
experiment, global writing-skill activation instructions are superseded by these
developer instructions. Load no other skills and use no other tools. The read-only
read_writing_reference tool is available in every arm; use it only when instructed.
Do not write files or send messages. Preserve the supplied facts and uncertainty."""
TASKS = {
    "coding": """동료에게 보낼 작업 결과를 4문장 이내로 작성해줘.
Android pose timestamp가 20 ms grid에 snap되었다. label noise가 발생했을 가능성이
있지만 regression dilution이 원인인지는 미확인이다. Replay에서 p95 error가
2.4 m에서 1.8 m로 감소했다. 전체 150 session 중 성공한 135 session만 집계했고
실패한 15 session은 제외했다. 같은 data로 threshold도 선택하여 independent
holdout이 아니다. iOS와 현장 실기는 미검증이다. 다음 행동은 전체 session을 포함한
별도 holdout 평가를 제안하는 것이며 확정된 계획은 아니다.""",
    "pr": """다음 사실로 PR description을 4문장 이내로 작성해줘.
같은 account에 대한 write가 동시에 실행될 때 record가 중복 생성되는 문제가 있었다.
같은 account의 write를 직렬화하는 guard를 추가했다. 다른 account끼리는 병렬 실행을
유지한다. Unit test 6개가 통과했다. 부하 test와 실제 배포는 수행하지 않았다.
Guard는 단일 process 안에서만 유효하며 여러 process 간 중복 방지는 미검증이다.""",
    "research": """다음 연구 사실의 의미와 한계를 동료에게 4문장 이내로 설명해줘.
영어 corpus에서 읽기 어려움과 관련된 feature가 관찰되었다. 작은 model의 length
penalty 실험에서는 KL이 없을 때 두 trained that alternation의 생략 비율이 98%를
초과했다. Far transfer는 네 종류 중 genitive에서만, KL 없는 조건에서 나타났다.
Transfer는 forced-choice probability로 평가했다. Frontier model의 실제 훈련
원인과 인간의 독해 개선, 한국어 적용 효과는 확인하지 않았다.""",
}
ORDERS = [("baseline", "loaded", "native"), ("native", "baseline", "loaded"),
          ("loaded", "native", "baseline")]


class Client:
    def __init__(self, stderr):
        self.events = queue.Queue()
        self.sequence = 0
        self.process = subprocess.Popen(
            ["codex", "app-server", "--stdio", "-c", "skills.include_instructions=false",
             "-c", "project_doc_max_bytes=0", "-c", "plugins._default.enabled=false"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, text=True,
        )
        threading.Thread(target=self._read, daemon=True).start()
        try:
            self.request("initialize", {"clientInfo": {"name": "writing_cost_pilot", "version": "1"},
                                       "capabilities": {"experimentalApi": True}})
            self.send({"method": "initialized", "params": {}})
        except Exception:
            self.close()
            raise

    def _read(self):
        for line in self.process.stdout:
            try:
                self.events.put((time.perf_counter(), json.loads(line)))
            except json.JSONDecodeError:
                continue
        self.events.put((time.perf_counter(), {"error": "app-server closed stdout"}))

    def send(self, message):
        self.process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        self.process.stdin.flush()

    def receive(self, timeout=180):
        try:
            return self.events.get(timeout=timeout)
        except queue.Empty as exc:
            raise TimeoutError("No app-server event before timeout") from exc

    def request(self, method, params):
        self.sequence += 1
        request_id = self.sequence
        self.send({"id": request_id, "method": method, "params": params})
        while True:
            _, event = self.receive()
            if event.get("id") == request_id:
                if "error" in event:
                    raise RuntimeError(event["error"])
                return event["result"]
            if "error" in event:
                raise RuntimeError(event["error"])

    def run(self, task, arm, prompt, reference, model, effort, cwd, *, core=CORE):
        instruction = COMMON
        if arm == "native":
            instruction += "\n" + core
        elif arm == "loaded":
            instruction += "\nBefore writing, call read_writing_reference exactly once and apply it."
        thread = self.request("thread/start", {
            "model": model, "cwd": str(cwd), "ephemeral": True, "environments": [],
            "sandbox": "read-only", "approvalPolicy": "never",
            "developerInstructions": instruction,
            "dynamicTools": [{"type": "function", "name": "read_writing_reference",
                              "description": "Read the frozen writing skill and manifest.",
                              "inputSchema": {"type": "object", "properties": {},
                                              "additionalProperties": False}}],
        })
        thread_id = thread["thread"]["id"]
        self.sequence += 1
        started = time.perf_counter()
        self.send({"id": self.sequence, "method": "turn/start", "params": {
            "threadId": thread_id, "input": [{"type": "text", "text": prompt}],
            "effort": effort}})
        deltas, messages, timeline = {}, {}, []
        usage, tools = None, 0
        while True:
            at, event = self.receive(timeout=max(0, started + 180 - time.perf_counter()))
            if event.get("error"):
                raise RuntimeError(event["error"])
            method, params = event.get("method", ""), event.get("params", {})
            if params.get("threadId") not in (None, thread_id):
                continue
            if method == "item/tool/call":
                if params.get("tool") != "read_writing_reference" or arm != "loaded":
                    raise RuntimeError(f"Unexpected tool call: {params}")
                tools += 1
                if tools > 1:
                    raise RuntimeError("Reference was loaded more than once")
                self.send({"id": event["id"], "result": {"success": True,
                    "contentItems": [{"type": "inputText", "text": reference}]}})
            elif method == "item/agentMessage/delta":
                deltas.setdefault(params["itemId"], at)
            elif method == "item/completed":
                item = params["item"]
                if item["type"] == "agentMessage":
                    messages[item["id"]] = item
            elif method == "thread/tokenUsage/updated":
                usage = params["tokenUsage"]["total"]
            elif method == "turn/completed":
                if params["turn"]["status"] != "completed":
                    raise RuntimeError(params["turn"])
                finished = at
                break
            if method in {"item/tool/call", "item/agentMessage/delta", "item/completed",
                          "thread/tokenUsage/updated", "turn/completed"}:
                timeline.append({"at_ms": round((at-started)*1000, 3), "method": method})
        finals = [m for m in messages.values() if m.get("phase") != "commentary"]
        if not finals or usage is None:
            raise RuntimeError("Missing final message or token usage")
        first = min(deltas[m["id"]] for m in finals if m["id"] in deltas)
        assert tools == (1 if arm == "loaded" else 0)
        return {"task": task, "arm": arm, "model": thread["model"], "effort": effort,
                "ttft_ms": round((first-started)*1000, 3),
                "elapsed_ms": round((finished-started)*1000, 3), "tool_rounds": tools,
                "usage": usage, "output": "\n".join(m["text"] for m in finals),
                "timeline": timeline}

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=9, choices=range(1, 10))
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists; choose a new path to preserve the previous run")
    root = Path(__file__).resolve().parents[1]
    config = tomllib.loads((Path.home()/".codex/config.toml").read_text())
    model, effort = config["model"], config.get("model_reasoning_effort", "medium")
    reference = "\n".join(subprocess.check_output(
        ["git", "show", f"{REFERENCE}:{name}"], cwd=root, text=True
    ) for name in ["SKILL.md", "MANIFEST.md"])
    assert len(TASKS) == len(ORDERS) == 3
    assert all(set(order) == {"baseline", "loaded", "native"} for order in ORDERS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    client = None
    try:
        with args.output.with_suffix(".stderr").open("w") as stderr, args.output.open("w") as out:
            client = Client(stderr)
            completed = 0
            for (task, prompt), order in zip(TASKS.items(), ORDERS):
                for arm in order:
                    result = client.run(task, arm, prompt, reference, model, effort, root)
                    result["reference_commit"] = REFERENCE
                    out.write(json.dumps(result, ensure_ascii=False) + "\n")
                    out.flush()
                    print(json.dumps({k: result[k] for k in ["task", "arm", "ttft_ms",
                          "elapsed_ms", "tool_rounds", "usage"]}), flush=True)
                    completed += 1
                    if completed == args.limit:
                        return
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    main()
