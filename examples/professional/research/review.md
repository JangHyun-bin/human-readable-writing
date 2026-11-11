# Research source-fidelity review

Input parity passes. English and Korean outputs both pass textual source-fidelity review for R01 through R08. No material omission, unsupported claim or change in interpretation strength was found in either complete output.

The review examined both original drafts, `sources.md`, the current and frozen `facts.json`, both native requests, complete outputs and attempt records. The current and frozen ledgers contain the same selected facts. Both requests contain the corresponding original draft, and the draft SHA-256 values match the attempts' recorded input hashes. The bilingual inputs preserve the same facts, exclusions and conditional author judgment.

Both outputs retain these boundaries:

- Optional assignment differs from actual use. Treatment/control counts of 792/820 differ from volunteer/non-volunteer enrolment counts of 518/1,094.
- Approximate 55%/40% take-up uses eligible Wednesday/Friday opportunities, with the stated exclusions, not all employees or all weekdays. Typical use remains about one day weekly.
- The nominal six-month experiment effectively ended on 21 January 2022. Caption follow-up through 23 January remains separate, without two-year randomized exposure.
- Assigned-group quit rates remain 7.20%/4.80% during the experiment, not annually, with P = 0.043. The 2.40-percentage-point difference remains about 33% relative to control.
- The trial consideration remains the memo author's conditional judgment, not an approved program, guaranteed effect or fully remote equivalence finding. Neither output adds excluded promotion, code-output, performance or productivity claims.

Both attempt records report `captured`, observed model `claude-sonnet-5-5`, Claude Code runtime `2.1.322`, exit code 0 and no provider errors. Derived tool-read records report successful manifest reads in both runs and a successful Korean-reference read in Korean. English records no Korean-reference read. Both attempts still label fidelity `not_reviewed`; capture metadata alone does not establish fidelity.

Direct SHA-256 calculation matched each attempt's recorded output hash:

- English `8893a89984aecb10550f7b706dd50570e976aec7fc0c63b05e030d0da5c7f9aa`.
- Korean `8379b9dbc401c60b2454a8e589a21a8994ff7dbcdb948b372d9e06ebd2155412`.

This was text and recorded-evidence review only, not a native rerun, independent paper reanalysis or reader study. Raw outputs and historical evidence were not changed. Fact-level findings and exact attempt paths are in `review.json`.
