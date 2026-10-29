"""Synthetic app-server for runner tests; never calls a model."""

import json
import sys
import time


scenario = sys.argv[1]
thread_count = 0


def emit(value):
    print(json.dumps(value), flush=True)


for line in sys.stdin:
    request = json.loads(line)
    method = request.get("method")
    if method == "initialize":
        if scenario == "init_error":
            emit({"id": request["id"], "error": {
                "code": -999, "message": "synthetic sensitive diagnostic"}})
        else:
            emit({"id": request["id"], "result": {}})
    elif method == "thread/start":
        thread_count += 1
        thread = f"thread-{thread_count}"
        emit({"id": request["id"], "result": {
            "thread": {"id": thread}, "model": request["params"]["model"]}})
    elif method == "turn/start":
        thread = request["params"]["threadId"]
        item = f"final-{thread_count}"
        def event(method, **params):
            emit({"method": method, "params": {"threadId": thread, **params}})
        event("fixture/heartbeat")
        if scenario != "final_only":
            event("item/agentMessage/delta", itemId=item, delta="SYNTHETIC partial")
        event("thread/tokenUsage/updated", tokenUsage={"total": {
            "inputTokens": 100, "cachedInputTokens": 50,
            "outputTokens": 10, "reasoningOutputTokens": 4, "totalTokens": 110}})
        if thread_count == 2:
            if scenario == "eof":
                sys.exit(0)
            if scenario == "timeout":
                time.sleep(10)
            if scenario == "tool":
                event("item/completed", item={"id": "tool-1", "type": "commandExecution"})
        event("item/completed", item={"id": item, "type": "agentMessage",
              "phase": "final_answer", "text": "SYNTHETIC fixture only; not model output."})
        event("turn/completed", turn={"status": "completed"})
