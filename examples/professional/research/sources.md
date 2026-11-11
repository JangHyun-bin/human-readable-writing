# Research packet sources and editorial boundaries

## Purpose and provenance

This packet is an independently authored research-interpretation memo for an HR director considering an optional hybrid-work policy for comparable graduate office roles. Its question is how far Trip.com's randomized assignment and quit-rate result support policy consideration at another employer. It is not a recommendation for fully remote work, an implementation plan, or a review of every outcome in the paper.

`facts.json` selects eight bilingual records, R01 through R08. R01 through R07 are source-based descriptions and direct interpretations of the reported design and rates. R08 is the memo author's bounded policy judgment. It has no external source ID because the paper's authors did not make that company-specific judgment for us. The hypothetical reader's company has no invented staff count, quit rate, savings estimate or approved trial. `source_mode` is `source_based`, not a fictional-data case.

`before.en.md` and `before.ko.md` are original professional drafts, not passages copied from the published paper or deliberately damaged versions of it. They contain the same selected facts and decision strength. The dense first section places enrolment, assignment, outcomes and actual use in successive paragraphs. An editor can improve that ordering and the proximity of qualifications without deleting the distinction between assignment and use. The final section states an attributed judgment rather than disguising it as a research result.

## Primary source

S1 is Nicholas Bloom, Ruobing Han and James Liang, [Hybrid working from home improves retention without damaging performance](https://www.nature.com/articles/s41586-024-07500-2), Nature 630, 920–925, published 12 June 2024. DOI [10.1038/s41586-024-07500-2](https://doi.org/10.1038/s41586-024-07500-2). The article's main text, Methods, figure captions and rights notice were inspected directly for this packet. The selected descriptions do not rely on secondary press accounts.

The relevant source locations are as follows.

| Selected record | Source location | Boundary to retain |
| --- | --- | --- |
| R01 | Main; The experiment; Methods, Location and set-up; Methods, Employee characteristics and balancing tests | One employer in Shanghai, the Airfare and IT divisions, 1,612 graduate employees, the stated roles, and the exclusion of interns and probationary new employees. The source calls the divisions representative of the firm, not of every employer or workforce. |
| R02 | Main; Methods, Randomization; Methods, Inclusion and ethics statement; Fig. 2 caption | Odd versus even day-of-month birthdays, not odd versus even birth years. Treatment n = 792 and control n = 820. Wednesday and Friday were optional home days, with the other three days in the office. Control attended all five days. |
| R03 | Methods, Randomization | Initial volunteers n = 518 started in the week of 9 August 2021. Remaining non-volunteers n = 1,094 started in the week of 13 September 2021. These are enrolment cohorts, not the treatment and control denominators. |
| R04 | Methods, Employee characteristics and balancing tests; Extended Data Fig. 3 caption | Approximate take-up of 55% and 40% among eligible volunteers and non-volunteers uses Wednesday and Friday opportunities. The caption excludes public holidays, personal holidays and excused absence. The Methods also discusses sick leave, extreme weather and the company COVID outbreak as exclusions from daily take-up. Typical use was about one day per week. |
| R05 | Main; Methods, Employee characteristics and balancing tests; Fig. 2 caption; Discussion | The nominal six-month trial had staggered starts. The Methods says it effectively ended on Friday 21 January 2022 after a COVID case prompted access for everyone. Fig. 2's attrition follow-up is through 23 January. Those dates are reported separately, not silently reconciled. |
| R06 | Main; Effects on employee retention; Fig. 2 caption | Assigned-group quit rates during the experiment were control 7.20% and treatment 4.80%, P = 0.043 for the difference. These are not annual rates. |
| R07 | Effects on employee retention; Methods, Randomization; Methods, Inclusion and ethics statement | The rate difference is 2.40 percentage points and about 33% relative to control. Randomization assigned access, not actual use of two home days. |
| R08 | Original memo-author judgment | A comparable optional-policy trial is worth considering only subject to checking the similarity of work and commuting conditions. It is not an approved trial or a forecast of an equal effect. |

## Arithmetic and condition review

These relationships define the fact review.

- The assignment totals reconcile. 792 + 820 = 1,612. The enrolment totals also reconcile. 518 + 1,094 = 1,612. The two partitions describe different things and must not be substituted for each other.
- The absolute quit-rate difference from the published rounded rates is 7.20% minus 4.80% = 2.40 percentage points. The relative reduction is 2.40 divided by 7.20 = one-third, approximately 33%. A 33-percentage-point decrease would be a different and incorrect claim. The article's retention section uses percent notation for the 2.4 difference, but the memo makes the absolute unit explicit.
- The 55% and 40% take-up measures are approximate shares of eligible Wednesday and Friday opportunities, after exclusions. They are not the proportions of the full workforce that ever worked from home. Two available days with these approximate take-up rates are consistent with about one day of weekly use, not two required days.
- The reported quit-rate comparison follows original assignment. It must not become a comparison of employees who chose to use WFH against employees who did not, or an estimate of using exactly two home days every week.
- The trial's nominal six-month description does not give each cohort identical exposure. The start weeks differed and the policy contrast ended early. The 21 January effective end and the 23 January caption follow-up must retain their different meanings.
- The paper later followed performance reviews and promotions, but it did not maintain the randomized policy contrast for two years. The Discussion says that company-wide policy rollout was announced on 14 February 2022. That rollout date is background, not a ninth selected fact.
- R08 must remain an explicitly attributed, conditional judgment. Neither statistical significance nor a similar office role guarantees the same effect at the reader's company. The trial does not establish equivalence with fully remote work.

## Investigation notes outside the selected ledger

These notes preserve relevant source limits. They are not required draft content and must not be added to the native editing input as extra outcomes.

- Promotion equivalence is excluded. In Methods, Null results, the article describes rejecting the promotion equivalence null for July to December 2022 while giving P = 0.092, despite stating a default alpha of 0.05. That wording and value appear inconsistent. This packet does not resolve the inconsistency, claim a correction, or use a promotion-equivalence conclusion. The main text's no-evidence-of-a-difference formulation is also not a selected draft claim.
- Code output and its transformations are excluded. Extended Data Fig. 1 describes 653 coding employees and 95,494 employee-days. Its caption gives P = 0.750 for log2 of code lines after zero-value observations are dropped, but P = 0.0103 for log2 of one plus code lines, with higher treatment values. The separate equivalence analysis uses a margin of 29 daily lines. These are not interchangeable tests or evidence that code quantity equals code quality. No code-output claim appears in the ledger or drafts.
- Surveyed productivity beliefs are excluded. Fig. 5 and its surrounding discussion concern beliefs, not measured productivity gains. Baseline and endline survey sample sizes differ, so this packet does not treat the responses as a confirmed matched panel. The reported shift in managers' beliefs is not an outcome in either draft.
- Performance-review equivalence and subgroup findings are also outside the selected scope. The packet does not claim that all aspects of performance, promotion, innovation or productivity were exactly unchanged or safe in every setting.
- The Methods, Inclusion and ethics statement, says Trip.com designed, initiated and ran the experiment. The Competing interests section says James Liang is Trip.com's co-founder, former CEO and chairman, with equity holdings. It also says no funding was received from Trip.com and no other co-author had a financial relationship with it. These provenance disclosures are not a ninth selected claim and should accompany any broader research assessment rather than be inferred away.
- The linked [replication repository](https://doi.org/10.7910/DVN/6X4ZZL) was not inspected or downloaded. Its licensing and contents are not represented as verified. No reanalysis was performed.

The selected facts are supported by the inspected article. The unresolved promotion wording concerns excluded material, not the quit-rate comparison. No additional population-level representativeness, mechanism for quitting, savings estimate, confidence interval or future-employer effect is inferred into the drafts.

## Rights, attribution and changes

The article's Rights and permissions section specifies [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). It permits use, sharing, adaptation, distribution and reproduction with appropriate author and source credit, a license link, and an indication of changes. It warns that separately credited third-party material can fall outside that license and require permission if no other legal basis applies.

Attribution for any display of this source-based example should name Nicholas Bloom, Ruobing Han and James Liang, link the article and CC BY 4.0, and retain the publication information above. Change identification should say that the project selected and paraphrased findings into independently authored English and Korean policy-review memos, with the memo author's policy judgment added. The Korean text is our own memo, not an authorized translation of the paper. Published-paper prose is not being labelled a poor draft.

No article figure, photograph, table, long passage, supplementary file or replication dataset is reproduced in this packet. Original packet prose is project-authored material under the repository's terms. Citation does not relicense the article or any third-party material under MIT.

## Bilingual term choices

| English | Korean | Meaning to preserve |
| --- | --- | --- |
| Hybrid work | 하이브리드 근무 | A mix of office and home working, not full remote work. |
| Assignment to eligibility | 재택근무 허용 대상으로 배정 | Receiving the option, not necessarily using it. |
| Treatment group | 처치집단 | Employees assigned the optional policy. |
| Control group | 대조집단 | Employees assigned the five-office-day policy. |
| Volunteer and non-volunteer | 자원자·비자원자 | Enrolment cohorts, not treatment and control. |
| Take-up | 실제 이용률 | Use across the specified Wednesday and Friday opportunities. |
| Quit rate | 퇴사율 | Experiment-period rate, not an annualized rate. |
| Percentage points | 퍼센트포인트 | Absolute difference between percentage rates. |
| Relative reduction | 상대 감소율 | Difference divided by the control rate. |
| Memo-author judgment | 메모 작성자의 판단 | Conditional policy interpretation, not an empirical result. |

## Recorded outputs

The [English attempt](../../../verification/professional-examples-20261111/research-run/research/en/attempt.json) and [Korean attempt](../../../verification/professional-examples-20261111/research-run/research/ko/attempt.json) record the actual requests, model, package hashes and observed reference reads. Their raw outputs are unchanged. The [fidelity review](review.md) covers R01–R08 in both languages.

