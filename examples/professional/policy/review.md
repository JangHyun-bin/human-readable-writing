# Policy input and source-fidelity review

The review checks whether both native revisions preserve the policy memo's evidence request and selected claims. Input parity passes. English passes P01 through P08. Korean passes P01 through P08. No consequential textual source-fidelity issue was found.

## Evidence examined

I examined both complete source drafts, the current `facts.json`, `sources.md`, the frozen `remaining-run/policy/facts.json`, and both languages' complete `request.md`, `output.md` and `attempt.json` under `verification/professional-examples-20261111/remaining-run/policy/`.

The current and frozen fact ledgers are structurally identical. Each request embeds its corresponding current source draft exactly. SHA-256 values calculated from both source drafts, requests and outputs match the corresponding attempt records. The inspected output hashes are:

- English `2efa5820352c7e314ae4c71f0434927c0949e77bbf337ac8ea3005dfd73a46d7`.
- Korean `909188e7c67127b505a8e94261d32cf678ad38556b8a7e00c228fa5da051e9a9`.

Both attempts record native Claude Code runtime `2.1.322 (Claude Code)`, requested and observed model `claude-sonnet-5-5`, `capture_status` of `captured`, exit code 0 and no provider errors. Both record `manifest_read: true` with a successful MANIFEST tool-read entry. Korean also records `korean_reference_read: true` with a successful Korean-reference tool-read entry. English records that reference as unread, which is not a missing Korean-language prerequisite for its English revision. These observations come from the published derived tool-read evidence in the attempt records, not a fresh inspection of private raw initialization events. Capture success and the records' `fidelity_status: not_reviewed` are not fidelity verdicts.

## Findings

The English and Korean inputs carry equivalent selected facts, attribution, exclusions, unknowns and author judgments. Neither supplies a hidden denominator, exact baseline, shared annual comparison or independent causal finding. The memo's attribution and the author's request have the same strength in both languages.

Both revisions retain MTA, the board date, title and page 13. They preserve the CBD entry reductions of 11% and 71,000 per day as entry counts, not unique cars or vehicle-miles. They preserve the rounded-baseline limitation and unknown observation and comparison periods and baseline construction.

Both retain the 4.3% CBD car-speed increase without converting it into a 4.3% travel-time decrease. Absolute speed, weighting, hours, measurement provider, baseline and periods remain unspecified.

Both retain the attributed 22% PM2.5 first-six-month claim and Cornell University, 2025 credit. They retain the concentration limitation, the Congestion Relief Zone heading context, and unknown study dates, statistic, denominator and detailed geography. Neither substitutes emissions, all pollutants, personal exposure or a citywide result. Neither infers a common full-year comparison from the title.

The author's distinction between agency summary and independent causal proof remains explicit. The requested traffic data, calculation methods, periods, baselines and underlying study definitions and uncertainty remain requested evidence. Neither revision converts the request into MTA advice, a completed independent review, or a repeal or expansion decision.

The English table and Korean metric labels are legitimate restructuring. Review of the complete outputs found no added study findings, correction specifics, policy outcomes or guarantees. Unselected Cornell study and correction details were not preservation requirements.

Only text and evidence review was performed. This was not a native rerun, external validation of MTA's reported results, a reader study or a comprehension benchmark. No build, lint, test or formatter was run. Source drafts, native outputs and historical evidence were not changed.
