# Capex source packet

## Topic, reader and purpose

This fictional pre-investment memorandum compares immediate automation of four warehouse zones with a one-zone pilot followed by conditional expansion. The operations director and investment committee need to distinguish released worker-hours from cash savings and the proposed pilot authorization from any later expansion approval. The recommendation is only for the pilot tranche. No pilot is approved, started or completed, and no equipment performance is measured.

이 가상 투자 전 검토서는 물류센터 4개 구역의 전면 자동화와 1개 구역 파일럿 후 조건부 확장을 비교한다. 운영총괄과 투자심의위원회가 절감 작업시간과 실제 현금지출 감소액, 파일럿 승인 권고와 후속 확장 승인을 구분하도록 작성했다. 승인 권고 대상은 파일럿 예산뿐이다. 승인·착수·완료된 파일럿이나 측정된 설비 성과는 없다.

## Provenance and rights

The scenario, numbers, ledger and both drafts are original project-authored illustration material. There are no external source URLs, vendor quotations, real-company data, copied figures or third-party tables. Accordingly, `source_mode` is `fictional`, `sources` is empty and every fact has an empty `source_ids` array. `C01` through `C08` are scenario assumptions, including their arithmetic consequences. `C09` is the scenario management recommendation and is classified as author judgment, not external evidence.

The governing input was the proposed four-zone warehouse case in `local://professional-examples/capex-plan.md`, as narrowed by `local://professional-examples/production-contract.md`. Those planning documents are not empirical evidence or records of executed checks. The self-contained public packet consists of this note, `facts.json`, `before.en.md` and `before.ko.md`.

The repository's root `LICENSE` is the MIT License, copyright 2026 Hyunbin Jang, and covers associated documentation. These original example files are intended as project documentation under that license. Its copyright and permission notice must be retained when applicable. There is no third-party material whose rights could be expanded through that license.

The scenario assumptions are original source material, not measured equipment performance.

## Selected fact set and bilingual alignment

Nine records, `C01` through `C09`, are selected for both drafts. They retain the same assumptions and recommendation strength in English and Korean.

| Fact | Content carried by both drafts |
| --- | --- |
| C01 | Fictional assumptions, four comparable zones, fixed eligible volume, operating calendar, occupied versus scheduled time, no sales uplift |
| C02 | Two-worker manual team, unvalidated automation target, same case mix and staffing, team-hour to worker-hour relationship |
| C03 | Conditional agency cancellation, invoiced hourly rate, unchanged permanent payroll, redeployment without cash savings |
| C04 | Full, pilot and expansion capital, one operating-year pilot, equipment reuse, staged total |
| C05 | Gross cash savings, incremental operating costs and net annual savings |
| C06 | Spend and go-live timing, no ramp, constant and uniform accrual, expansion timing, all appraisal exclusions |
| C07 | Full, pilot-only and conditional staged simple payback with distinct timelines |
| C08 | Proposed throughput, error, safety and cancellation gates, finance and operations ownership, remaining-zone economics, separate approval |
| C09 | Pilot-only recommendation, neither tranche approved or completed, lower initial commitment but capital premium and slower modeled recovery |

The English draft places the financial assumptions before the recommendation. The Korean draft follows a natural internal-review register rather than translating each sentence mechanically. Both retain the operational-to-cash relationship, timing, exclusions and decision gates, with the recommendation at the end.

## Arithmetic and condition notes

All capital, costs and savings below are in constant KRW million unless another unit is shown. These are arithmetic relationships within a fictional model, not measurements.

### Processing time is not cash savings

- Baseline occupied time per zone is 8 scheduled hours × 75% = 6 team-hours daily.
- Manual volume is 200 cases per team-hour × 6 team-hours = 1,200 cases daily. The two-worker team is the denominator, not one worker.
- The target is 300 cases per team-hour with unchanged two-worker staffing and case mix. At fixed volume, 1,200 / 300 = 4 team-hours daily. This is unvalidated, not an observed improvement.
- Released time per zone is (6 - 4) team-hours × 2 workers = 4 worker-hours daily. Over 300 operating days, this is 1,200 worker-hours annually per zone and 4,800 across four zones.
- Only 600 invoiced agency hours per zone are assumed cancelable. At KRW 30,000 each, this is KRW 18,000,000, or 18, annually per zone. Four zones cancel 2,400 hours and save 72, not the value of all 4,800 released worker-hours.
- The remaining 600 worker-hours per zone support redeployment. They generate no modeled cash savings. Permanent payroll is unchanged. The scenario does not establish that agency contracts can actually be canceled or that gains scale across zones.

### Capital and annual net cash savings

| Item | One-zone pilot | Immediate four-zone deployment |
| --- | ---: | ---: |
| Upfront capital | 75 | 240 |
| Annual gross cash savings | 18 | 4 × 18 = 72 |
| Annual incremental maintenance, software and energy | 4 | 12 |
| Annual net cash savings | 18 - 4 = 14 | 72 - 12 = 60 |

Conditional expansion costs an additional 190 even though pilot equipment is reused. Staged capital is 75 + 190 = 265. The pilot's initial commitment is 240 - 75 = 165 less than immediate full deployment, but total staged capital is 265 - 240 = 25 more. The 12 annual recurring cost and 60 annual net savings after expansion are for all four zones, including the pilot zone. Adding the pilot's 14 again would double-count it.

### Payback follows the spending timeline

The first outlay and go-live are time zero. Spending and go-live coincide for each tranche. Savings accrue uniformly at constant rates, with no ramp period. Conditional expansion spends 190 and goes live immediately after the first operating year. This timing is a model assumption, not an implementation promise.

- Immediate deployment pays back in 240 / 60 = 4.00 years from time zero.
- If only the pilot continues with unchanged annual net savings and no expansion, 75 / 14 = 5.3571 years, rounded to 5.36. This is not recovery within the proposed one-year pilot evaluation period.
- At the end of pilot year one, 14 has been recovered from the initial 75. Expansion then adds 190, leaving 75 - 14 + 190 = 251 unrecovered.
- At 60 annual net savings after expansion, the remaining recovery takes 251 / 60 = 4.1833 years. Total staged payback is 1 + 251 / 60 = 5.1833 years, rounded to 5.18 from the initial outlay.
- Dividing 265 by stabilized annual savings of 60 would ignore the pilot year's lower savings and the actual outlay timing. It is not the staged payback calculation.

The simple-payback model excludes tax, depreciation, financing, discounting, working capital and salvage. Its cash-realization assumption depends on agency cancellation. It does not value redeployment, revenue growth or changes in permanent payroll. Immediate deployment is superior on these assumed economics. The pilot recommendation instead limits initial commitment while the throughput and cash-realization assumptions remain unvalidated. Its capital premium and slower modeled payback remain explicit.

### Expansion remains a proposal

All of the following are proposed gates, not achieved results:

- Target throughput on comparable case mix.
- Case-error rate no higher than 0.5%.
- No unresolved critical safety findings.
- Documented cancellation of 600 agency hours during the pilot year.

Finance and operations must substantiate the remaining zones' economics. Passing the pilot gates does not itself authorize expansion. Expansion needs separate approval. Neither the pilot nor expansion is approved or completed. The packet does not invent cross-zone scalability evidence, a safety test protocol or an error-measurement protocol.

## Background not selected for the drafts

The planning case includes capital components. Immediate deployment is equipment 180 + integration 35 + training 10 + contingency 15 = 240. The pilot is equipment 50 + integration 15 + training 5 + contingency 5 = 75. These component breakdowns are background only, not selected facts required in either draft. The aggregate capital amounts, extra expansion outlay and reuse assumption remain selected.

No sensitivity case is selected. In particular, the planning example of a 25% reduction in canceled agency hours is not a result and is not included in either draft. Vendor selection, financing arrangements, discounted-cash-flow appraisal, tax effects, salvage estimates and later implementation decisions are outside scope. Unknown actual costs and performance are not represented as zero. The listed appraisal exclusions describe what the model omits, not facts about real expenditures.

## Terminology

| English | Korean | Scope |
| --- | --- | --- |
| Capital expenditure | 설비투자액 | Cash capital outlay, distinct from annual operating costs |
| Staged deployment | 단계적 도입 | Pilot first, separately approved expansion after year one |
| Throughput | 처리량 | Eligible cases per occupied two-worker team-hour |
| Occupied team-hour | 실제 팀 작업시간 1시간 | One hour of processing by the two-worker team |
| Worker-hour | 인시 | One worker's hour, not one team's hour |
| Released worker-hours | 절감 작업시간 | Available time, not automatically canceled payroll |
| Agency hours | 외주 인력 시간 | Invoiced hours assumed cancelable at the stated rate |
| Cash savings | 실제 현금지출 감소액 | Avoided agency cash cost, not all labor-time value |
| Net cash savings | 순현금절감액 | Avoided cash cost less incremental annual operating costs |
| Simple payback period | 단순 투자회수기간 | Undiscounted recovery under the stated timing and exclusions |
| Proposed authorization | 승인 권고 | A request, not an approval or an accomplished pilot |

## Recorded outputs

The [English attempt](../../../verification/professional-examples-20261111/remaining-run/capex/en/attempt.json) and [Korean attempt](../../../verification/professional-examples-20261111/remaining-run/capex/ko/attempt.json) record actual requests, model, package hashes and observed reference reads. The [fidelity review](review.md) covers C01–C09 without changing the outputs.
