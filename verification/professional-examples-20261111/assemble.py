"""Check the dated corpus and assemble its indexes without changing native records."""

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CATALOG = ROOT / "examples/professional/catalog.json"


def load(path):
    return json.loads((ROOT / path).read_text())


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def check_attempt(case_id, language, attempt_path, review_path, package, runtime, model):
    attempt = load(attempt_path)
    folder = Path(attempt_path).parent
    source = Path("examples/professional") / case_id
    review = load(review_path)["languages"][language]
    assert (attempt["case_id"], attempt["language"]) == (case_id, language), (
        f"Attempt identity mismatch: expected {(case_id, language)}, "
        f"observed {(attempt['case_id'], attempt['language'])}"
    )
    assert attempt["capture_status"] == "captured"
    assert attempt["runtime"] == runtime and attempt["requested_model"] == model
    assert attempt["observed_models"] == [model]
    assert attempt["package_sha256"] == package
    assert attempt["manifest_read"] is True
    assert language != "ko" or attempt["korean_reference_read"] is True
    assert digest(source / f"before.{language}.md") == attempt["input_sha256"]
    assert load(source / "facts.json") == load(folder.parent / "facts.json")
    assert digest(folder / "request.md") == attempt["request_sha256"]
    assert digest(folder / "output.md") == attempt["output_sha256"]
    assert review["output_sha256"] == attempt["output_sha256"]
    assert review["attempt"] == attempt_path
    expected_facts = {fact["id"] for fact in load(source / "facts.json")["facts"]}
    assert {fact["id"] for fact in review["facts"]} == expected_facts
    assert len(review["facts"]) == len(expected_facts)
    if review["status"] == "pass":
        assert all(fact["status"] == "pass" for fact in review["facts"])
        assert not review["issues"]
    return {
        "case_id": case_id,
        "language": language,
        "attempt": attempt_path,
        "review": review_path,
        "revision": str(folder / "output.md"),
        "status": review["status"],
        "output_sha256": attempt["output_sha256"],
    }


def assemble(catalog):
    manifests = [load(path) for path in catalog["initial_runs"]]
    package, runtime, model = (manifests[0][key] for key in ("package_sha256", "runtime", "model"))
    for manifest in manifests:
        assert (manifest["package_sha256"], manifest["runtime"], manifest["model"]) == (package, runtime, model)
    initial, corrections, selected = [], [], []
    for case in catalog["cases"]:
        assert load(case["review"])["source_parity"]["status"] == "pass"
        for language in ("en", "ko"):
            attempt_path = f'{case["run"]}/{language}/attempt.json'
            first = check_attempt(case["id"], language, attempt_path, case["review"], package, runtime, model)
            initial.append(first)
            correction = case.get("corrections", {}).get(language)
            if correction:
                assert correction["previous_attempt"] == attempt_path
                assert first["status"] == "fail"
                accepted = check_attempt(case["id"], language, correction["attempt"], correction["review"], package, runtime, model)
                accepted["kind"] = "review_feedback_correction"
                accepted["previous_attempt"] = attempt_path
                corrections.append(accepted)
            else:
                accepted = {**first, "kind": "first_attempt"}
            assert accepted["status"] == "pass"
            selected.append(accepted)
    captured = {f'{record["path"]}/attempt.json' for manifest in manifests for record in manifest["records"]}
    assert captured == {record["attempt"] for record in initial}
    assert len({(record["case_id"], record["language"]) for record in initial}) == len(initial)
    return {
        "date": catalog["date"],
        "scope": "Textual source-fidelity review, not a readability benchmark or cross-runtime compatibility test",
        "path_base": "repository_root",
        "runtime": runtime,
        "model": model,
        "package_sha256": package,
        "initial_runner_sha256": digest(HERE.relative_to(ROOT) / "runner-source.txt"),
        "native_calls": len(initial) + len(corrections),
        "initial_review_counts": {status: sum(record["status"] == status for record in initial) for status in ("pass", "fail")},
        "initial_attempts": initial,
        "corrections": corrections,
        "selected": selected,
    }


def index(catalog, summary, language):
    korean = language == "ko"
    title = "전문 실무 글쓰기 예시" if korean else "Professional writing examples"
    switch = "[English](README.md)" if korean else "[한국어](README.ko.md)"
    intro = (
        "다섯 장르의 원문과 실제 스킬 호출로 얻은 수정본입니다. 한·영 원문은 같은 사실을 담되 각각 작성했습니다."
        if korean else
        "Five genres, with original drafts and revisions from actual native skill calls. English and Korean drafts were independently written from the same facts."
    )
    header = "| 장르 | 주제 | 원문 | 수정본 | 출처·검토 |" if korean else "| Genre | Topic | Original | Revision | Sources and review |"
    lines = [f"# {title}", "", switch, "", intro, "", header, "| --- | --- | --- | --- | --- |"]
    for case in catalog["cases"]:
        facts = load(f'examples/professional/{case["id"]}/facts.json')
        record = next(item for item in summary["selected"] if item["case_id"] == case["id"] and item["language"] == language)
        revision = os.path.relpath(ROOT / record["revision"], CATALOG.parent)
        review = os.path.relpath((ROOT / record["review"]).with_suffix(".md"), CATALOG.parent)
        label = ("검토 후 재수정" if korean else "After review feedback") if record["kind"] == "review_feedback_correction" else ("첫 수정본" if korean else "First revision")
        sources_label, review_label = ("출처", "검토") if korean else ("Sources", "Review")
        cells = [
            facts["genre"][language],
            facts["topic"][language],
            f'[↗]({case["id"]}/before.{language}.md)',
            f"[{label}]({revision})",
            f'[{sources_label}]({case["id"]}/sources.md) · [{review_label}]({review})',
        ]
        lines.append("| " + " | ".join(cells) + " |")
    note = (
        "한국어 재무 예시의 첫 수정본에는 원문에 없는 인과관계가 붙었습니다. [첫 실패 기록](finance/review.md)은 보존했고, 오류를 지적한 별도 요청의 수정본을 위에 연결했습니다."
        if korean else
        "The first Korean finance revision added an unsupported causal explanation. Its [failed review](finance/review.md) is retained; the [Korean index](README.ko.md) links the separately requested, feedback-corrected revision."
    )
    provenance = (
        "연구·정책 예시는 공개 자료를 바탕으로 작성한 자체 문서입니다. 재무·설비투자 수치는 가상이며, 설계 예시는 공개 API 문서와 가상 시스템 조건을 구분합니다. 사실 카드와 제3자 출처·권리는 각 폴더에 있습니다."
        if korean else
        "Research and policy memos are original paraphrases of public sources. Finance and capex figures are fictional; the architecture case separates public API constraints from fictional system assumptions. Each folder includes its fact ledger and source/rights notes."
    )
    record_link = "[실행·검토 기록](../../verification/professional-examples-20261111/README.md)" if korean else "[Execution and review record](../../verification/professional-examples-20261111/README.md)"
    limit = "원문 보존을 검토한 예시이며, 이해도나 읽기 시간의 개선을 측정한 자료는 아닙니다." if korean else "These are source-fidelity-reviewed examples, not measurements of comprehension or reading time."
    return "\n".join(lines + ["", note, "", provenance, "", record_link + " · " + limit, ""])


def main():
    catalog = load(CATALOG.relative_to(ROOT))
    summary = assemble(catalog)
    (HERE / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    for language, filename in (("en", "README.md"), ("ko", "README.ko.md")):
        (CATALOG.parent / filename).write_text(index(catalog, summary, language))
    print(json.dumps({"native_calls": summary["native_calls"], "initial_review_counts": summary["initial_review_counts"], "selected": len(summary["selected"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
