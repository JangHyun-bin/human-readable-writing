"""Request a separate, recorded correction without editing the failed output."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "verification"))
from run_professional_examples import capture, load_case, save_json


def main():
    previous = ROOT / "verification/professional-examples-20261111/remaining-run/finance/ko"
    original = json.loads((previous / "attempt.json").read_text())
    facts, drafts = load_case("finance")
    source = drafts["ko"]
    assert hashlib.sha256(source.encode()).hexdigest() == original["input_sha256"]
    prior_output = (previous / "output.md").read_text()
    assert hashlib.sha256(prior_output.encode()).hexdigest() == original["output_sha256"]
    executable = Path(shutil.which("claude")).resolve()
    runtime = subprocess.run([str(executable), "--version"], capture_output=True,
                             text=True, check=True).stdout.strip()
    assert runtime == original["runtime"], "The correction must use the recorded runtime"
    feedback = (
        "F07 원문은 그 밖의 조정 합계가 설계상 0이라는 가정과, 나열한 비현금 변동이 "
        "세 운전자본 잔액의 증감에 영향을 주지 않는다는 가정을 함께 제시합니다. "
        "후자가 전자의 이유라는 관계는 제시하지 않았습니다. 이전 수정본의 "
        "'가정했기 때문이다'는 이 관계를 추가합니다. 두 가정을 원문처럼 별도로 제시하고, "
        "그 밖의 사실·수치·단위·조건·제외 사항·불확실성과 문서 장르도 보존하는 재수정이 필요합니다."
    )
    request = (
        "/human-readable-writing 다음 재무 분석 브리프의 이전 수정본에서 원문 대조로 확인된 "
        "오류를 바로잡아 한국어 개정문만 반환해 주세요. 원문에 없는 인과관계나 설명은 추가하지 마세요.\n\n"
        "원문 대조 의견:\n" + feedback + "\n\n원문:\n\n" + source +
        "\n\n이전 수정본. 아래 내용도 틀릴 수 있으므로 원문을 기준으로 재검토합니다:\n\n" + prior_output
    )
    output_root = ROOT / "verification/professional-examples-20261111/finance-correction"
    output_root.mkdir(exist_ok=False)
    (output_root / "finance").mkdir()
    save_json(output_root / "finance/facts.json", facts)
    (output_root / "feedback.md").write_text(feedback + "\n")
    shutil.copyfile(ROOT / "verification/run_professional_examples.py",
                    output_root / "capture-runner-source.txt")
    record = capture("finance", "ko", facts, source, output_root,
                     original["package_sha256"], original["requested_model"], runtime, 300,
                     executable=executable, request_override=request)
    save_json(output_root / "provenance.json", {
        "kind": "Explicit review-feedback correction in a fresh native session",
        "previous_attempt": str((previous / "attempt.json").relative_to(ROOT)),
        "previous_verdict": "fail", "fact_id": "F07",
        "original_source_unchanged": True, "previous_output_unchanged": True,
        "automatic_retry": False, "record": record,
    })
    print(json.dumps(record, ensure_ascii=False))
    return 0 if record["capture_status"] == "captured" else 1


if __name__ == "__main__":
    raise SystemExit(main())
