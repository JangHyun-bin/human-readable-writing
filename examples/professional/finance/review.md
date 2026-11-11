# Finance fidelity review

The review checks whether both native revisions preserve the fictional financial-analysis packet for a finance or business lead. Input parity passes. English passes. Korean fails F07 because it adds an unsupported causal explanation. The raw outputs remain unchanged.

## Evidence examined

The review covered both original drafts, `sources.md`, current `facts.json`, the frozen run ledger, and each language's complete `request.md`, `output.md`, and `attempt.json` under `verification/professional-examples-20261111/remaining-run/finance/`.

Both attempts record Claude Code `2.1.322`, requested and observed model `claude-sonnet-5-5`, `capture_status` of `captured`, exit code 0, and no provider errors. Their derived tool-read records show a successful `MANIFEST.md` read. The Korean attempt additionally records a successful `references/korean.md` read. English records `korean_reference_read` as false. These records support capture and read evidence, not fidelity. Their historical `fidelity_status` remains `not_reviewed`; the verdicts here are independent.

SHA-256 checks of the actual files match both attempts' recorded input, request, and output hashes. Current and frozen ledgers have identical SHA-256 `d3599240113b87359c1a4cead8478748dd51df5ce9b70265af983cd444a3d91e`. The request source bodies match the inspected original drafts.

| Language | Checked output SHA-256 | Verdict |
| --- | --- | --- |
| English | `44f632baa6594a54706a30f452f03373b0e102598f270a6c319288c06941fafc` | Pass |
| Korean | `7e6627881cc315e1710d77e97829abbb7178e82a6714a991c20fd95e23eb8756` | Fail |

## Fact coverage and input parity

The original English and Korean drafts express equivalent F01 through F10 facts, including the same fictional scope, periods, units, balances, signs, denominator, assumptions, and interpretation limits. No source-parity issue was found. `review.json` records a separate finding for every fact in each output.

Both revisions retain standalone April 1 through June 30 quarters in 2025 and 2026, exact KRW-million units, net income rather than operating profit, and depreciation as a noncash add-back rather than a receipt. All quarter-specific receivable, inventory, and payable opening/closing balances and adjustment signs remain intact. Both equations still yield positive operating cash flow of 900 and 600. The 20% denominator of 1,000, additional working-capital deduction of 540, and signed change bridge ending in -300 remain intact.

Both revisions retain every unknown category and the prohibitions on inferring customer arrears, unsold inventory, financial distress, cash-balance movements, or complete liquidity. Neither adds a tax outcome, accounting-compliance assertion, or explanation of profit growth. Table and paragraph restructuring are not failures.

## Material Korean issue

F07 fails at Korean output line 21. The source says:

> 그 밖의 조정 합계는 설계상 0이며, 인수·환산·제각·재분류 또는 그 밖의 비현금 변동이 위 잔액 증감에 영향을 주지 않는다고 가정했다.

The output says:

> 그 밖의 조정 합계는 설계상 0이다. 인수·환산·제각·재분류 또는 그 밖의 비현금 변동이 위 잔액 증감에 영향을 주지 않는다고 가정했기 때문이다.

The added "때문이다" makes the excluded balance movements the reason other adjustments total zero. The source instead supplies two distinct conditions. Absence of noncash movements in the three working-capital balances does not establish a zero total for every other reconciliation adjustment. The wording therefore introduces a definite unsupported accounting rationale for the finance reader. It does not change the arithmetic or assert a particular tax treatment. The English revision preserves these as separate conditions.

Only text and recorded-evidence review, including file-hash checks, was performed. No native rerun, build, lint, test, formatter, or reader study was performed. No comprehension or readability improvement is claimed.
