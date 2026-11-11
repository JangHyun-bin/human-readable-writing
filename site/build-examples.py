#!/usr/bin/env python3
"""Publish the reviewed professional corpus without models, network access or dependencies."""

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import sys


CORPUS = Path("verification/professional-examples-20261111")
LANGUAGES = ("en", "ko")
START = "<!-- professional-examples:start -->"
END = "<!-- professional-examples:end -->"
PRESENTATION = {
    "research": {
        "en": ("Research", "Trip.com's hybrid-work trial"),
        "ko": ("연구", "Trip.com 연구의 퇴사율 해석"),
        "excerpts": {"en": ((1, 2), (4, 6)), "ko": ((1, 2), (4, 6))},
    },
    "finance": {
        "en": ("Finance", "Profit rises while operating cash flow falls"),
        "ko": ("재무", "이익 증가와 영업활동현금흐름 감소"),
        "excerpts": {"en": ((0, 1), (0, 2)), "ko": ((0, 1), (0, 2))},
    },
    "capex": {
        "en": ("Capital investment", "Warehouse automation before pilot approval"),
        "ko": ("설비투자", "파일럿 승인 전 물류센터 자동화"),
        "excerpts": {"en": ((1, 2), (3, 6)), "ko": ((1, 2), (5, 10))},
    },
    "policy": {
        "en": ("Policy", "Congestion-pricing figures and missing evidence"),
        "ko": ("정책", "혼잡통행료 수치와 추가 근거"),
        "excerpts": {"en": ((1, 4), (1, 4)), "ko": ((1, 4), (1, 4))},
    },
    "architecture": {
        "en": ("Architecture", "Duplicate webhooks and entitlement grants"),
        "ko": ("설계", "중복 웹훅과 이용 권한 부여"),
        "excerpts": {"en": ((2, 3), (2, 5)), "ko": ((2, 3), (3, 6))},
    },
}
ATTRIBUTION = {
    "research": {
        "en": 'Nicholas Bloom, Ruobing Han and James Liang, <a href="https://www.nature.com/articles/s41586-024-07500-2">Hybrid working from home improves retention without damaging performance</a>, Nature 630, 920–925 (2024), DOI 10.1038/s41586-024-07500-2. <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Findings selected and paraphrased into project-authored English and Korean memos, with a policy judgment added. The Korean memo is not an authorized translation.',
        "ko": 'Nicholas Bloom, Ruobing Han, James Liang의 <a href="https://www.nature.com/articles/s41586-024-07500-2">Hybrid working from home improves retention without damaging performance</a>, Nature 630, 920–925 (2024), DOI 10.1038/s41586-024-07500-2에 근거한다. <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. 연구 결과를 골라 프로젝트가 직접 쓴 영문·국문 메모로 바꾸고 정책 판단을 더했다. 국문 메모는 논문의 공인 번역이 아니다.',
    },
    "finance": {
        "en": 'The scenario, figures and drafts are project-authored fiction. The <a href="https://www.sec.gov/investor/pubs/begfinstmtguide.htm">SEC financial-statement guide</a> is a conceptual reference, not the source of the figures. No SEC graphics or tables are reproduced.',
        "ko": '시나리오·수치·초안은 프로젝트가 직접 작성한 가상 사례다. <a href="https://www.sec.gov/investor/pubs/begfinstmtguide.htm">SEC 재무제표 안내</a>는 개념 참고 자료이며 수치의 출처가 아니다. SEC의 그림이나 표는 재현하지 않았다.',
    },
    "capex": {
        "en": 'The scenario, figures and drafts are project-authored fiction. They are pre-investment assumptions, not measured equipment performance. No third-party material is reproduced.',
        "ko": '시나리오·수치·초안은 프로젝트가 직접 작성한 가상 사례다. 설비 성능 측정값이 아닌 투자 전 가정이며, 제3자 자료는 재현하지 않았다.',
    },
    "policy": {
        "en": '<a href="https://www.mta.info/document/194491">MTA, 2025 in Data</a>, December 17, 2025, p. 13. The original memo paraphrases attributed facts, not slides or graphics. MTA reserves rights. Its <a href="https://www.mta.info/terms-and-conditions">terms</a> and <a href="https://www.mta.info/copyright-notice">copyright notice</a> do not grant this project a general reproduction license.',
        "ko": '<a href="https://www.mta.info/document/194491">MTA, 2025 in Data</a>, 2025년 12월 17일, 13쪽에 근거한다. 직접 쓴 메모에 출처를 명시한 사실을 풀어 썼으며 슬라이드나 그림은 재현하지 않았다. MTA는 권리를 유보한다. <a href="https://www.mta.info/terms-and-conditions">이용약관</a>과 <a href="https://www.mta.info/copyright-notice">저작권 고지</a>는 이 프로젝트에 일반적인 재현 허가를 부여하지 않는다.',
    },
    "architecture": {
        "en": 'The fictional ADR paraphrases facts from Stripe\'s <a href="https://docs.stripe.com/webhooks">webhook</a>, <a href="https://docs.stripe.com/api/events/object">Event</a>, <a href="https://docs.stripe.com/api/events/types">event-type</a> and <a href="https://docs.stripe.com/api/invoices/object">Invoice</a> documentation. Stripe documentation redistribution permission is unverified. No vendor code, figures or tables are reproduced.',
        "ko": '가상 ADR에 Stripe의 <a href="https://docs.stripe.com/webhooks">웹훅</a>, <a href="https://docs.stripe.com/api/events/object">Event</a>, <a href="https://docs.stripe.com/api/events/types">이벤트 유형</a>, <a href="https://docs.stripe.com/api/invoices/object">Invoice</a> 문서의 사실을 출처와 함께 풀어 썼다. Stripe 문서의 재배포 허가는 확인되지 않았다. 원문 코드·그림·표는 재현하지 않았다.',
    },
}
INLINE = re.compile(r"`([^`\n]+)`|\[([^\]\n]+)\]\((https?://[^\s)]+)\)|\*\*([^*\n]+)\*\*|\*([^*\n]+)\*")
HEADING = re.compile(r"^(#{1,3}) (.+)$")
LIST_ITEM = re.compile(r"^(?:(-) |([0-9]+)\. )(.+)$")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_json(root, path):
    return json.loads((root / path).read_bytes())


def document(root, path):
    data = (root / path).read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "text": data.decode("utf-8")}


def review_record(root, path):
    return {"path": str(path), "json": load_json(root, path), "markdown": document(root, Path(path).with_suffix(".md"))}


def capture(root, case_id, language, original, ledger, entry, review, summary):
    folder = Path(entry["attempt"]).parent
    attempt = load_json(root, entry["attempt"])
    request = document(root, folder / "request.md")
    output = document(root, folder / "output.md")
    verdict = review["languages"][language]
    label = f"{case_id}/{language}: {entry['attempt']}"
    require((attempt["case_id"], attempt["language"]) == (case_id, language), f"{label}: wrong capture identity")
    require(attempt["capture_status"] == "captured" and attempt["exit_code"] == 0 and not attempt["provider_errors"], f"{label}: unsuccessful capture")
    require(attempt["runtime"] == summary["runtime"] and attempt["requested_model"] == summary["model"] and attempt["observed_models"] == [summary["model"]], f"{label}: runtime/model mismatch")
    require(attempt["package_sha256"] == summary["package_sha256"], f"{label}: package mismatch")
    require(attempt["manifest_read"] is True and (language != "ko" or attempt["korean_reference_read"] is True), f"{label}: missing reference read")
    require(attempt["request_file"] == "request.md" and attempt["output_file"] == "output.md", f"{label}: unexpected capture filenames")
    require(original["sha256"] == attempt["input_sha256"], f"{label}: source hash mismatch")
    require(request["sha256"] == attempt["request_sha256"] and output["sha256"] == attempt["output_sha256"], f"{label}: request/output hash mismatch")
    require(original["text"] in request["text"], f"{label}: original absent from request")
    require(load_json(root, folder.parent / "facts.json") == ledger, f"{label}: frozen fact ledger mismatch")
    require(entry["revision"] == str(folder / "output.md") and entry["output_sha256"] == output["sha256"], f"{label}: selection output mismatch")
    require(review["case_id"] == case_id and verdict["attempt"] == entry["attempt"] and verdict["output_sha256"] == output["sha256"] and verdict["status"] == entry["status"], f"{label}: review mismatch")
    fact_ids = {fact["id"] for fact in ledger["facts"]}
    findings = verdict["facts"]
    require(len(fact_ids) == len(ledger["facts"]) and {fact["id"] for fact in findings} == fact_ids and len(findings) == len(fact_ids), f"{label}: incomplete/duplicate fact coverage")
    require(entry["status"] in ("pass", "fail"), f"{label}: missing review verdict")
    if entry["status"] == "pass":
        require(all(fact["status"] == "pass" for fact in findings) and not verdict["issues"], f"{label}: passing review contains failures")
    else:
        require(any(fact["status"] == "fail" for fact in findings) and verdict["issues"], f"{label}: failed review lacks findings")
    return {"selection": entry, "attempt": attempt, "request": request, "output": output}


def indexed(entries, expected, label):
    result = {(entry["case_id"], entry["language"]): entry for entry in entries}
    require(len(result) == len(entries) and set(result) == expected, f"{label}: unexpected, missing or duplicate case/language")
    return result


def load_cases(root):
    catalog = load_json(root, "examples/professional/catalog.json")
    summary = load_json(root, CORPUS / "summary.json")
    require([case["id"] for case in catalog["cases"]] == list(PRESENTATION), "Catalog case order differs from the five published cases")
    require(catalog["date"] == summary["date"], "Catalog and summary dates differ")
    expected = {(case_id, language) for case_id in PRESENTATION for language in LANGUAGES}
    initials = indexed(summary["initial_attempts"], expected, "Initial attempts")
    selected = indexed(summary["selected"], expected, "Selected revisions")
    correction_keys = {(case["id"], language) for case in catalog["cases"] for language in case.get("corrections", {})}
    require(correction_keys == {("finance", "ko")}, "Korean finance must retain its recorded feedback correction")
    corrections = indexed(summary["corrections"], correction_keys, "Corrections")
    terms = {"license": document(root, "LICENSE"), "notice": document(root, "NOTICE.md")}
    records = []
    for case in catalog["cases"]:
        case_id = case["id"]
        source = Path("examples/professional") / case_id
        manifest_path = str(Path(case["run"]).parent / "manifest.json")
        require(manifest_path in catalog["initial_runs"], f"{case_id}: initial run is absent from catalog")
        manifest = load_json(root, manifest_path)
        require(all(manifest[field] == summary[field] for field in ("runtime", "model", "package_sha256")), f"{case_id}: initial manifest differs from summary")
        run_records = [entry for entry in manifest["records"] if entry["case_id"] == case_id]
        require(len(run_records) == 2 and {entry["path"] for entry in run_records} == {f"{case['run']}/{language}" for language in LANGUAGES}, f"{case_id}: initial manifest lacks the bilingual captures")
        ledger = load_json(root, source / "facts.json")
        initial_review = review_record(root, case["review"])
        require(ledger["id"] == case_id, f"{case_id}: wrong ledger identity")
        require(initial_review["json"]["source_parity"]["status"] == "pass" and not initial_review["json"]["source_parity"]["issues"], f"{case_id}: input parity not accepted")
        record = {
            "schema_version": 1,
            "case_id": case_id,
            "date": summary["date"],
            "scope": summary["scope"],
            "path_base": "repository_root",
            "fact_ledger": ledger,
            "source_notes": document(root, source / "sources.md"),
            "initial_review": initial_review,
            "initial_run": {
                "manifest_path": manifest_path,
                "metadata": {key: value for key, value in manifest.items() if key != "records"},
                "records": run_records,
                "runner_sha256": summary["initial_runner_sha256"],
            },
            "project_terms": terms,
            "languages": {},
        }
        for language in LANGUAGES:
            key = (case_id, language)
            first = initials[key]
            require(first["attempt"] == f"{case['run']}/{language}/attempt.json" and first["review"] == case["review"], f"{case_id}/{language}: initial selection differs from catalog")
            original = document(root, source / f"before.{language}.md")
            item = {"original": original, "initial": capture(root, case_id, language, original, ledger, first, initial_review["json"], summary)}
            correction = case.get("corrections", {}).get(language)
            if correction:
                accepted = corrections[key]
                require(first["status"] == "fail" and correction["previous_attempt"] == first["attempt"], "Correction must retain the failed first attempt")
                require(all(accepted[field] == correction[field] for field in ("attempt", "review", "previous_attempt")) and accepted["kind"] == "review_feedback_correction", "Correction selection differs from catalog")
                corrected_review = review_record(root, correction["review"])
                corrected_capture = capture(root, case_id, language, original, ledger, accepted, corrected_review["json"], summary)
                provenance_dir = Path(correction["review"]).parent
                provenance = load_json(root, provenance_dir / "provenance.json")
                require(provenance["previous_attempt"] == first["attempt"] and provenance["previous_verdict"] == "fail" and provenance["original_source_unchanged"] is True and provenance["previous_output_unchanged"] is True and provenance["automatic_retry"] is False, "Correction provenance differs from the retained failure")
                require(corrected_capture["attempt"]["request_kind"] == "review_feedback_correction", "Selected correction is not a feedback correction")
                item["correction"] = {"capture": corrected_capture, "review": corrected_review, "provenance": provenance, "feedback": document(root, provenance_dir / "feedback.md")}
            else:
                accepted = {**first, "kind": "first_attempt"}
            require(selected[key] == accepted and accepted["status"] == "pass", f"{case_id}/{language}: selected revision is not the accepted reviewed output")
            item["selected"] = selected[key]
            record["languages"][language] = item
        records.append(record)
    return records, terms


def inline(text):
    parts, position = [], 0
    for match in INLINE.finditer(text):
        parts.append(html.escape(text[position:match.start()]))
        code, label, url, strong, emphasis = match.groups()
        if code is not None:
            parts.append(f"<code>{html.escape(code)}</code>")
        elif url is not None:
            parts.append(f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>')
        elif strong is not None:
            parts.append(f"<strong>{inline(strong)}</strong>")
        else:
            parts.append(f"<em>{inline(emphasis)}</em>")
        position = match.end()
    parts.append(html.escape(text[position:]))
    return "".join(parts)


def table_cells(line):
    require(line.startswith("|") and line.endswith("|"), "Only complete pipe-table rows are supported")
    return [cell.strip() for cell in line[1:-1].split("|")]


def markdown(text, excerpt_range):
    """Render only the block and inline forms used by these frozen documents; never raw HTML."""
    lines, blocks, index = text.splitlines(), [], 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        heading = HEADING.fullmatch(line)
        item = LIST_ITEM.fullmatch(line)
        if heading:
            tag = "h5" if len(heading[1]) == 1 else "h6"
            blocks.append(f"<{tag}>{inline(heading[2])}</{tag}>")
            index += 1
        elif line.startswith("|"):
            headers = table_cells(line)
            require(index + 1 < len(lines), "Table is missing its delimiter row")
            delimiter = table_cells(lines[index + 1])
            require(len(delimiter) == len(headers) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in delimiter), "Unsupported table delimiter")
            rows = []
            index += 2
            while index < len(lines) and lines[index].startswith("|"):
                cells = table_cells(lines[index])
                require(len(cells) == len(headers), "Table column count differs from header")
                rows.append("<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in cells) + "</tr>")
                index += 1
            blocks.append("<table><thead><tr>" + "".join(f'<th scope="col">{inline(cell)}</th>' for cell in headers) + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>")
        elif item:
            ordered = item[2] is not None
            tag = "ol" if ordered else "ul"
            start = f' start="{int(item[2])}"' if ordered and int(item[2]) != 1 else ""
            items = []
            while index < len(lines):
                item = LIST_ITEM.fullmatch(lines[index])
                if not item or (item[2] is not None) != ordered:
                    break
                items.append(f"<li>{inline(item[3])}</li>")
                index += 1
            blocks.append(f"<{tag}{start}>" + "".join(items) + f"</{tag}>")
        else:
            require(not re.match(r"\s*(?:#{4,}\s|>|```|~~~|[-*+]\s|[0-9]+[.)]\s)", line), f"Unsupported Markdown block: {line}")
            content = [line]
            index += 1
            while index < len(lines) and lines[index].strip() and not HEADING.fullmatch(lines[index]) and not LIST_ITEM.fullmatch(lines[index]) and not lines[index].startswith("|"):
                require(not re.match(r"\s*(?:#{4,}\s|>|```|~~~|[-*+]\s|[0-9]+[.)]\s)", lines[index]), f"Unsupported Markdown block: {lines[index]}")
                content.append(lines[index])
                index += 1
            paragraph = "\n".join(content)
            rendered = f"<p>{inline(paragraph)}</p>"
            blocks.append(rendered)
    content = [block for block in blocks if not block.startswith(("<h5>", "<h6>"))]
    start, end = excerpt_range
    require(0 <= start < end <= len(content), "Excerpt range exceeds the document's content blocks")
    return "\n".join(blocks), "\n".join(content[start:end])


def diptych(case_id, mode, copies, language):
    labels = ("원문", "수정본") if language == "ko" else ("Original", "Revision")
    documents = []
    for side, label, copy in zip(("before", "after"), labels, copies):
        label_id = f"example-{case_id}-{mode}-{side}-label"
        documents.append(f'<section class="document document-{side}" aria-labelledby="{label_id}">\n<h4 class="document-label" id="{label_id}">{label}</h4>\n<div class="document-copy">\n{copy}\n</div>\n</section>')
    preview = " example-preview" if mode == "preview" else ""
    return f'<div class="diptych{preview}">\n' + "\n".join(documents) + "\n</div>"


def panel(record, language, asset_base):
    case_id = record["case_id"]
    korean = language == "ko"
    item = record["languages"][language]
    corrected = "correction" in item
    chosen = item["correction"]["capture"] if corrected else item["initial"]
    before_range, after_range = PRESENTATION[case_id]["excerpts"][language]
    before, before_preview = markdown(item["original"]["text"], before_range)
    after, after_preview = markdown(chosen["output"]["text"], after_range)
    full = diptych(case_id, "full", (before, after), language)
    preview = diptych(case_id, "preview", (before_preview, after_preview), language)
    if korean:
        notice = "실제 스킬 수정 예시"
        verdict = "원문 보존 검토는 별도 에이전트가 맡았습니다."
        if corrected:
            notice = "피드백 후 재수정한 예시"
            verdict = "통합 담당자가 검토한 재수정본입니다. 첫 수정본의 오류와 피드백도 기록에 포함했습니다."
        expand, collapse, provenance = "전체 원문·수정본", "발췌문 보기", "출처·실행 정보"
        download, license_label, notice_label = "원문·출처·실행 기록 (JSON)", "프로젝트 MIT 라이선스", "고지"
    else:
        notice = "Recorded skill revision."
        verdict = "Source-fidelity review by a separate agent."
        if corrected:
            notice = "Revision after review feedback."
            verdict = "A separately requested correction, reviewed by the integration owner. The record retains the first revision's error and review feedback."
        expand, collapse, provenance = "Full source and revision", "Excerpt view", "Sources and run record"
        download, license_label, notice_label = "Source packet and run record (JSON)", "Project MIT license", "Notice"
    if record["fact_ledger"]["source_mode"] in ("fictional", "source_based_with_fictional_design"):
        notice = ("가상 사례 · " if korean else "Fictional case · ") + notice
    model = html.escape(chosen["attempt"]["requested_model"])
    runtime = html.escape(chosen["attempt"]["runtime"])
    topic = html.escape(PRESENTATION[case_id][language][1])
    return f'''<article class="example-panel" id="example-{case_id}" data-example-panel aria-labelledby="example-topic-{case_id}">
<h3 class="example-topic" id="example-topic-{case_id}">{topic}</h3>
<p class="example-notice">{notice}</p>
<figure class="edit">
<details class="example-detail">
<summary><span class="when-closed">{expand}</span><span class="when-open">{collapse}</span></summary>
{full}
</details>
{preview}
<figcaption class="edit-notes">
<details class="example-provenance">
<summary>{provenance}</summary>
<p><code>{model}</code> · {runtime}. {verdict}</p>
<p>{ATTRIBUTION[case_id][language]}</p>
<p><a href="{asset_base}/{case_id}/record.json" download>{download}</a> · <a href="{asset_base}/LICENSE">{license_label}</a> · <a href="{asset_base}/NOTICE.md">{notice_label}</a></p>
</details>
</figcaption>
</figure>
</article>'''


def browser(records, language, asset_base):
    label = "글의 종류" if language == "ko" else "Writing genre"
    tabs = [f'<a class="example-tab" href="#example-{record["case_id"]}" id="example-tab-{record["case_id"]}">{html.escape(PRESENTATION[record["case_id"]][language][0])}</a>' for record in records]
    return '<div data-example-browser>\n' + f'<nav class="example-tabs" data-example-tabs aria-label="{label}">\n' + "\n".join(tabs) + "\n</nav>\n" + "\n".join(panel(record, language, asset_base) for record in records) + "\n</div>"


def replace_region(source, content, path):
    lines = source.splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines) if line.strip() == START]
    ends = [index for index, line in enumerate(lines) if line.strip() == END]
    require(len(starts) == len(ends) == 1 and starts[0] < ends[0], f"{path}: expected one ordered pair of exact professional-example markers")
    start, end = starts[0], ends[0]
    require(lines[start].endswith("\n"), f"{path}: start marker needs its own line")
    indent = lines[start][:len(lines[start]) - len(lines[start].lstrip(" \t"))]
    newline = "\r\n" if lines[start].endswith("\r\n") else "\n"
    generated = "".join(indent + line + newline for line in content.splitlines())
    return "".join(lines[:start + 1]) + generated + "".join(lines[end:])


def outputs(root):
    records, terms = load_cases(root)
    generated = {}
    for path, language, cases, assets in (
        (Path("site/index.html"), "en", records, "assets/examples"),
        (Path("site/ko/index.html"), "ko", records, "../assets/examples"),
        (Path("site/styleguide.html"), "en", records[:2], "assets/examples"),
    ):
        original = (root / path).read_bytes().decode("utf-8")
        generated[path] = replace_region(original, browser(cases, language, assets), path).encode("utf-8")
    base = Path("site/assets/examples")
    for record in records:
        generated[base / record["case_id"] / "record.json"] = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    generated[base / "LICENSE"] = terms["license"]["text"].encode("utf-8")
    generated[base / "NOTICE.md"] = terms["notice"]["text"].encode("utf-8")
    return generated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report generated HTML/export drift without writing")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    try:
        generated = outputs(root)
        base = root / "site/assets/examples"
        unexpected = {path.relative_to(root) for path in base.rglob("*") if path.is_file()} - set(generated)
        require(not unexpected, "Unexpected public example files: " + ", ".join(str(path) for path in sorted(unexpected)))
        changed = [path for path, data in generated.items() if not (root / path).is_file() or (root / path).read_bytes() != data]
        if args.check:
            if changed:
                print("Generated professional examples are stale:\n" + "\n".join(str(path) for path in changed), file=sys.stderr)
                return 1
            print("Professional example HTML and public records are current.")
            return 0
        for path in changed:
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            (root / path).write_bytes(generated[path])
        print(f"Updated {len(changed)} generated professional example files.")
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        print(f"Professional example publication failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
