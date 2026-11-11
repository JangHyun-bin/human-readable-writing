# Capex source-fidelity review

The review checks whether the English and Korean native revisions preserve the fictional warehouse investment case for the operations director and investment committee.

## Verdicts

- Input parity passes. Both drafts carry the same C01-C09 assumptions, arithmetic, exclusions, proposal status and management judgment.
- English passes all nine fact checks. No material source-fidelity issue was found.
- Korean passes all nine fact checks. No material source-fidelity issue was found.

The complete outputs were examined, including additions and rearrangements. Headings, decision-first summaries and new tables do not change the source meaning. These verdicts concern textual source fidelity, not readability or human comprehension.

## Material checks

Both outputs retain fixed demand with no sales uplift. They distinguish scheduled hours, occupied two-worker team-hours and worker-hours. The unvalidated 200-to-300 throughput target releases 1,200 worker-hours per zone annually, but only 600 invoiced agency hours per zone are assumed cancelable. The sitewide figures remain 4,800 released versus 2,400 canceled hours. Neither output monetizes redeployment or reduces permanent payroll.

Capital remains 240 for immediate deployment versus 75 plus 190, totaling 265, for conditional staging despite equipment reuse. Annual net cash savings remain 14 for the pilot and 60 for all four zones. The latter already includes the pilot zone.

Both outputs preserve all timing assumptions and appraisal exclusions. They distinguish immediate 4.00-year payback, about 5.36 years for continued pilot-only operation without expansion, and about 5.18 years for conditional staging from initial outlay. The staged first year earns only 14, with the additional 190 spent immediately after the first operating year.

All four proposed expansion gates remain intact, along with finance and operations ownership of the remaining zones' economics and separate expansion approval. Only the 75 pilot tranche is recommended. Neither tranche is approved or completed. The lower initial commitment of 165 does not erase the staged capital premium of 25 or slower modeled payback. No target or cash-realization assumption becomes measured performance or a guarantee.

## Evidence examined

The review examined the full current `facts.json`, `before.en.md`, `before.ko.md` and `sources.md`, plus the frozen `facts.json` and each language's complete `request.md`, `output.md` and `attempt.json` under `verification/professional-examples-20261111/remaining-run/capex/`.

The frozen and current ledgers have the same SHA-256, `3feace0feec1e8fb12456e338c64472059681e93171624d9dce81458af7a7fce`. The source text embedded in each request matches its corresponding draft. Recomputed draft and request hashes match the attempt records.

| Language | Draft SHA-256 | Request SHA-256 |
| --- | --- | --- |
| English | `8276ef469361725afa2ff9fc2e3cab113c0ab50870455e2deca14c0020a16da1` | `98b58050adbbbb5eaa497045ec3573ba8888a971223e730da8abcbb3889dae92` |
| Korean | `9d720d774ffb9edccf22560085dd79df39212f6161e6fa4780f7c8f26d166f88` | `4e02641c78a4bccb173c4f53154e97624dc8176274d94e69ca4920ed81072965` |

Both attempt records report `captured`, exit code 0, observed model `claude-sonnet-5-5`, and runtime `2.1.322 (Claude Code)`. Each contains a successful manifest `tool_reads` entry consistent with `manifest_read: true`. The Korean record also contains a successful `references/korean.md` read consistent with `korean_reference_read: true`. English records no Korean-reference read, which is not required for its English request. Both records have empty provider-error arrays and identical package-hash maps. This is inspected recorded capture evidence, not a fresh observation of native execution. The records' `fidelity_status: not_reviewed` is historical and separate from these review verdicts.

Recomputed output hashes match the recorded hashes exactly.

| Language | Output SHA-256 |
| --- | --- |
| English | `6045cec0388790e6ea4e92b786ffb5f0d9f6f6eaf2845f71013c10312833e6f7` |
| Korean | `94b5942897b41ded790498b547f95556938596acc267fa85b7014e8407739aa2` |

Only text and evidence review, including hash comparison, was performed. No native rerun, reader study, build, lint, test or formatter was run. Source packets, raw outputs and historical execution evidence were not changed.
