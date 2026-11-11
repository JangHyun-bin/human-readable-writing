# Finance source packet

## Topic, reader, and purpose

Case `finance` is a financial-analysis brief for a finance or business lead. It explains how a fictional manufacturer's net income can rise while operating cash flow falls, using a bounded indirect reconciliation for standalone Q2 2025 and Q2 2026. It does not explain profit growth or diagnose liquidity distress.

`facts.json` freezes ten selected records, F01 through F10. Both original drafts contain all ten. The company, amounts, balance changes, and exclusion assumptions are original fictional scenario design, not observed results. No real issuer or confidential data is involved. The `fictional` source mode and empty `sources` and `source_ids` arrays identify that provenance. The SEC publication below is a conceptual reference, not the origin of the scenario's figures.

## Conceptual reference and source snapshot

- Author and publisher is the U.S. Securities and Exchange Commission.
- Title is [Beginners' Guide to Financial Statement](https://www.sec.gov/investor/pubs/begfinstmtguide.htm).
- The page is dated February 4, 2007, with a displayed last-reviewed-or-updated date of February 5, 2007.
- Access date is November 11, 2026. The live page was read while authoring this packet.
- Relevant sections are “Balance Sheets,” “Income Statements,” “Cash Flow Statements,” “Operating Activities,” “Investing Activities,” “Financing Activities,” and “Bringing It All Together.”

The following original paraphrases retain the relevant conceptual snapshot without copying the source's prose or tables. Balance sheets report balances at a point in time, while income and cash flow statements cover a period. Net income is a bottom-line earnings measure, not operating profit. The operating section can reconcile net income to operating cash flow by adjusting for noncash expenses, including depreciation, and operating asset and liability changes. Investing and financing flows are separate parts of the cash flow statement. Net income and cash flows are related but not equivalent, and one statement alone does not provide the complete picture.

This educational publication is not an issuer filing or a determination that the fictional reconciliation complies with any particular accounting standard. It does not supply the company's tax position, income statement, cash balances, or reasons for changes in profits or working capital.

## Rights and attribution boundaries

The scenario, fact ledger, professional drafts, table, and arithmetic explanations are project-authored material under the repository's MIT license. Citation does not relicense third-party material. No SEC graphics, original table, long quotation, or third-party company disclosure is reproduced. The conceptual snapshot above is an attributed original paraphrase. Permissions for copying the SEC page's graphics or other embedded material have not been checked, and the packet makes no blanket rights claim for them.

## Arithmetic and condition relationships

All amounts are exact KRW million, expressed as 백만원 in Korean. Each quarter runs from April 1 through June 30 in its own year. The reporting scope is unchanged. The two quarters are not consecutive quarters, and neither table column is a year-to-date column. No intervening-quarter balances or movements are supplied.

| Account | Q2 2025 opening | Q2 2025 closing | Q2 2025 increase | Q2 2025 adjustment | Q2 2026 opening | Q2 2026 closing | Q2 2026 increase | Q2 2026 adjustment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Trade receivables | 800 | 900 | 100 | -100 | 900 | 1,300 | 400 | -400 |
| Inventory | 1,000 | 1,250 | 250 | -250 | 1,200 | 1,800 | 600 | -600 |
| Trade payables | 500 | 550 | 50 | +50 | 600 | 760 | 160 | +160 |

Each change is closing balance minus that same quarter's opening balance. Comparing the two June closing balances would not yield a quarterly operating cash flow adjustment. Receivable and inventory increases are deducted. Payable increases are added. These signs relate the supplied net income to operating cash flow under the explicit scenario exclusions, not to an assertion that the customers are overdue, inventory is unsold, or supplier payments are late.

The balance changes exclude acquisitions, currency translation, write-offs, reclassifications, and other noncash movements. Other reconciliation adjustments total zero by design, not because missing data can be presumed zero. Net income is supplied rather than reconstructed. The zero-other-adjustments assumption does not assert a zero tax rate, zero tax payment, or any specific tax treatment. Depreciation of 200 and 240 is already included as an expense in net income and is added back as a noncash adjustment, not as a receipt.

The quarterly reconciliation relationships are:

```text
Q2 2025: 1,000 + 200 - 100 - 250 + 50 + 0 = 900
Q2 2026: 1,200 + 240 - 400 - 600 + 160 + 0 = 600
```

The combined working-capital adjustments are:

```text
Q2 2025: -100 - 250 + 50 = -300
Q2 2026: -400 - 600 + 160 = -840
Change: -840 - (-300) = -540
```

The year-over-year operating cash flow change bridge is:

| Component | Change in reconciliation contribution |
| --- | --- |
| Net income | +200 |
| Depreciation add-back | +40 |
| Trade receivable adjustment | -300 |
| Inventory adjustment | -350 |
| Trade payable adjustment | +110 |
| Other adjustments | 0 |
| Operating cash flow | -300 |

`+200 + 40 - 300 - 350 + 110 = -300`, matching `600 - 900 = -300`. The extra working-capital deduction of 540 outweighs the 240 combined increase in net income and depreciation add-back. Net income growth is `200 / 1,000 = 20%`, using Q2 2025 net income as denominator. No operating cash flow percentage or cash conversion ratio is selected. Both net income inputs and both operating cash flow results remain positive.

These are arithmetic relationships of fictional inputs, not measured corporate performance, a benchmark, or native-model verification results.

## Specialized terminology

| English | Korean | Meaning constraint |
| --- | --- | --- |
| Net income | 당기순이익 | Supplied bottom-line earnings. Do not replace with operating profit or 영업이익. |
| Operating cash flow | 영업활동현금흐름 | Period flow from operating activities. Do not substitute cash balance. |
| Cash balance | 현금잔액 | Point-in-time amount, not supplied here. Do not substitute 현금성자산. |
| Depreciation expense | 감가상각비 | Noncash expense added back, not a receipt. |
| Trade receivables | 매출채권 | Balance increase is a deduction here, not evidence of overdue customers. |
| Inventory | 재고자산 | Balance increase is a deduction here, not evidence of unsold stock. |
| Trade payables | 매입채무 | Balance increase is an addition here, not evidence of late payment. |
| Noncash adjustment | 비현금 조정 | Adjustment for an item that is not itself a cash receipt or payment. |
| Working-capital adjustment | 운전자본 관련 조정 | Here, the combined receivable, inventory, and payable adjustments, not all current assets minus all current liabilities. |
| KRW million | 백만원 | Fixed unit for every amount. No conversion to 억원. |

## Editorial rationale and bilingual parity

The drafts are original professional first drafts, not adapted passages presented as defects in SEC writing. Each uses a short opening, a compact reconciliation table, connected analysis, and an interpretation-limits section. The opening reports the headline change before the reader reaches the adjustment assumptions and the full change bridge. Table cells compress balances and signed adjustments. This leaves a realistic opportunity to improve how the reader connects the bases, adjustments, and limits without introducing bad grammar or unsupported business explanations.

The drafts were authored in each language rather than forced into identical sentence structures. F01 and F02 appear in the opening and table. F03 through F06 appear in the table and the accompanying explanation. F07 appears immediately after the table. F08 and F09 appear in the opening, equations, and change-bridge discussion. F10 appears in the final section. The English and Korean drafts preserve the same quantities, date ranges, signs, percentage denominator, exclusions, unknowns, and strength of conclusion.

## Excluded claims and unresolved information

Cash balances, investing and financing flows, collection terms, receivable aging, inventory plans, and profit-growth causes are not supplied. None is zero by implication. Operating cash flow alone does not establish a cash-balance change or support a complete liquidity assessment. The packet makes no claim of overdue customers, unsold inventory, financial distress, tax outcomes, accounting-standard compliance, or a real issuer's performance.

No unresolved numeric source value blocks this fictional packet. No copied graphics are used.

## Recorded outputs

The [English attempt](../../../verification/professional-examples-20261111/remaining-run/finance/en/attempt.json) passed the [initial fidelity review](review.md). The first [Korean attempt](../../../verification/professional-examples-20261111/remaining-run/finance/ko/attempt.json) failed F07 by adding an unsupported causal explanation. It remains unchanged in the record.

A [separate Korean correction](../../../verification/professional-examples-20261111/finance-correction/finance/ko/attempt.json) used the same original source, package and model with explicit review feedback. Its [review](../../../verification/professional-examples-20261111/finance-correction/review.json) accepted all ten source facts. This is a feedback-corrected example, not a first-pass success.
