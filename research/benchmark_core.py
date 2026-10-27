"""Frozen 21-turn comparison of no guidance, the current core, and one candidate."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from benchmark_writing import Client, CORE, TASKS


CORES = {
    "baseline": "",
    "current": CORE,
    "candidate": "주체·동작·조건·이유를 밝히고 검증·한계는 묶어 중복을 줄인다. 수치·단위·범위·부정·불확실성을 보존하고 관찰·가설·인과를 구분한다.",
}
PROMPTS = {
    "coding": TASKS["coding"],
    "api_doc": """다음 사실로 API 사용 문서를 4문장 이내로 작성해줘.
Caller가 같은 job_id로 요청하면 server는 처음 성공한 결과를 반환한다.
같은 job_id로 payload가 바뀌면 HTTP 409를 반환한다. 결과 보관 기간은 24 h이며,
그 이후 또는 다른 region에서는 중복 실행 방지를 보장하지 않는다.
Client timeout은 server의 실행 실패를 뜻하지 않는다. Timeout 뒤 재시도에는
같은 job_id를 사용하도록 안내한다. Unit test 12개가 통과했지만 production 검증은
수행하지 않았다.""",
    "incident": """다음 사실로 장애 경과를 동료에게 4문장 이내로 설명해줘.
14:00 배포 후 14:02에 HTTP 503 비율이 1.2%에서 8.6%로 증가했다.
14:09 app version을 rollback했고 14:12에 1.5%로 측정되었다.
DB schema는 변경하지 않았다. DB connection pool 지표는 수집하지 않아 원인은
미확인이다. Rollback과 비율 감소의 인과관계도 확정하지 않았다.
다음 행동으로 별도 부하 test와 pool 지표 수집을 제안하지만 실행은 미정이다.""",
}
# The first six blocks cover every arm order; each trial starts a fresh thread.
BLOCKS = [
    ("coding", 1, ("baseline", "current", "candidate")),
    ("coding", 2, ("current", "candidate", "baseline")),
    ("coding", 3, ("candidate", "baseline", "current")),
    ("coding", 4, ("baseline", "candidate", "current")),
    ("coding", 5, ("candidate", "current", "baseline")),
    ("api_doc", 1, ("current", "baseline", "candidate")),
    ("incident", 1, ("baseline", "current", "candidate")),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists; choose a new path")
    root = Path(__file__).resolve().parents[1]
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    schedule = [(task, repeat, arm) for task, repeat, order in BLOCKS for arm in order]
    assert len(schedule) == 21 and Counter(a for _, _, a in schedule) == {
        "baseline": 7, "current": 7, "candidate": 7}
    assert len({order for _, _, order in BLOCKS[:6]}) == 6
    assert all(set(order) == set(CORES) for _, _, order in BLOCKS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    client = None
    try:
        with args.output.open("x") as out, args.output.with_suffix(".stderr").open("x") as stderr:
            client = Client(stderr)
            for index, (task, repeat, arm) in enumerate(schedule, 1):
                result = client.run(task, "baseline" if arm == "baseline" else "native",
                                    PROMPTS[task], "", "gpt-6-astra", "high", root,
                                    core=CORES[arm])
                assert result["model"] == "gpt-6-astra" and result["tool_rounds"] == 0
                result.update(arm=arm, repeat=repeat, order=index, core=CORES[arm],
                              prompt=PROMPTS[task], source_commit=revision,
                              recorded_at=datetime.now(timezone.utc).isoformat())
                out.write(json.dumps(result, ensure_ascii=False) + "\n")
                out.flush()
                print(json.dumps({k: result[k] for k in ["order", "task", "repeat", "arm",
                      "ttft_ms", "elapsed_ms", "usage"]}), flush=True)
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    main()
