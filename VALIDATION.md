# 작성 원칙의 검증 기록

검증일: 2026-10-27.

## 1. 검증 목적과 한계

논문 분석의 근거 범위와 manifest의 적용 가능성을 확인하였다. 원문을 독립적으로 검토한 agent 1개와 작성 과제를 수행한 agent 2개를 사용하였다. Agent들은 root의 대화 이력을 전달받지 않았다. 두 작성 agent의 결과는 아래에 원문 그대로 기록하였다.

이 검증은 사람을 대상으로 한 독해 실험이 아니다. 작성 agent의 단일 baseline·적용 확인이며 model별 반복 sample, 읽기 시간, 이해도 정답률을 측정하지 않았다. 따라서 개선 효과나 통계적 유의성을 산출하지 않는다.

## 2. 작성 과제

두 agent에게 동일하게 다음 세 과제를 부여하였다.

1. Android pose timestamp가 10 ms grid에 snap된 사실과 label noise 가능성을 바탕으로 동료에게 전달할 짧은 보고를 작성한다. Regression dilution은 미확인이다. Replay의 median error는 1.4 m → 1.1 m이며 120 session 중 성공한 96 session만 집계하고 실패 24 session은 제외하였다. 같은 data로 threshold를 선택하여 independent holdout은 아니다. iOS·현장 실기는 미검증이다. 다음 행동은 성공·실패 전체 session을 포함한 새 holdout 측정이다. 보고는 5문장 이내로 요청하였다.
2. `holdout regression dilution mitigation gate`를 동료가 이해할 제목으로 개정한다.
3. 영어 corpus의 feature 관찰과 작은 model의 length-penalty 실험을 한 문장으로 설명한다. Frontier model의 실제 훈련 원인과 한국어 독해 개선 효과는 미검증이라는 사실을 함께 제공하였다.

Baseline agent에는 새 manifest나 논문을 읽지 않도록 하였다. 적용 agent에는 manifest를 읽고 같은 요청을 수행하도록 하였다. Manifest에는 첫 과제와 같은 가상 측정 예시가 포함되어 있으므로, 이 과제는 예시와 다른 상황으로의 일반화 검증이 아니다.

적용 agent에는 다음 문장만으로 상태 보고를 작성하는 별도 과제도 부여하였다. 이 문장은 manifest의 예시에 포함되지 않았다.

```text
iOS fallback relocalization timeout carryover path regression gate가 probe freshness debt를 먹어서 candidate release parity를 닫았다.
```

평가 기준은 수치·단위·분모·제외 대상·불확실성·검증 범위·다음 행동의 보존, 불명확한 관계에 대한 사실 추가 여부이다. 마지막 과제에는 의미가 정의되지 않은 표현이 있으므로 그럴듯한 성공·실패 상태를 확정하지 않는지 확인하였다. 문장별 금칙어 개수는 평가 기준으로 사용하지 않았다.

## 3. Baseline 산출물

아래는 agent가 반환한 원문이다. 인용의 어체와 표기를 보존하였다.

> Android pose timestamp가 10 ms grid에 snap돼 label에 noise가 들어갔을 가능성이 있으나, regression dilution이 실제 원인인지는 아직 확인되지 않았습니다. Replay에서 median error는 1.4 m에서 1.1 m로 줄었지만, 전체 120 session 중 성공한 96 session만 포함했고 실패한 24 session은 제외했습니다. 같은 replay data로 threshold도 선택했으므로 independent holdout 결과로 볼 수 없습니다. iOS와 현장 실기는 미검증이며, 다음에는 성공·실패 전체 session을 포함한 새 holdout을 측정하겠습니다.
>
> 제목: 새 holdout에서 위치 오차 개선 효과 확인
>
> 논문 요지: 영어 corpus에서 difficulty와 관련된 feature가 관찰됐고 작은 model의 length penalty 실험에서 일부 짧은 문법 형태에 대한 preference가 강화됐으며, frontier model의 실제 훈련 원인과 한국어 독해 개선 효과는 미검증입니다.

**판정:** 보고의 의미 보존 기준을 충족하였다. 논문 요지도 관찰·작은 model의 실험·미검증 범위를 보존하였다. 제목은 원문의 `mitigation gate` 관계가 무엇인지 명시적으로 검토하지 않았지만, 성공·실패 조건을 새로 확정하지도 않았다. 이 결과에서 정보 누락 실패를 관찰하였다고 주장하지 않는다.

## 4. Manifest 적용 산출물

아래는 agent가 반환한 원문이다.

> 성공한 96 session의 replay에서 median error가 1.4 m에서 1.1 m로 감소했습니다. 다만 전체 120 session 중 실패한 24 session을 제외했고, 같은 replay data로 threshold를 선택했으므로 independent holdout 결과는 아닙니다. Android pose timestamp가 10 ms grid에 snap되어 label에 noise가 생겼을 가능성이 있으나, regression dilution이 실제 원인인지는 아직 확인하지 못했습니다. iOS와 현장 실기는 미검증이며, 다음에는 성공·실패 전체 session을 포함한 새 holdout을 측정하겠습니다.
>
> 제목: **holdout 측정 결과와 regression dilution 가설** — gate의 진행 조건은 확인이 필요합니다.
>
> 논문은 영어 corpus에서 difficulty와 관련된 feature를 관찰하고 작은 model의 length penalty 실험에서 일부 짧은 문법 형태에 대한 preference가 강화됨을 보였지만, frontier model의 실제 훈련 원인과 한국어 독해 개선 효과는 확인하지 않았습니다.
>
> 원문만으로는 iOS fallback relocalization의 timeout carryover path에서 무엇이 달라졌고 probe freshness debt가 regression gate에 어떤 영향을 줬는지 불명확해, candidate release parity의 달성 여부는 확인이 필요합니다.

**판정:** 보고의 의미 보존 기준을 충족하였다. 제목에서는 정의되지 않은 gate 조건을 확인 대상으로 표시하였다. 추가 문장에서는 성공이나 실패를 확정하는 대신 의미 확인이 필요하다고 응답하였다. 다만 마지막 문장 자체가 여전히 길고 명사 연쇄를 포함한다. 불명확한 내용을 추측하지 않는 동작은 확인하였지만, 그 한 문장만으로 가독성 개선을 입증할 수는 없다.

두 agent의 보고는 모두 4문장이며 수치·분모·제외 대상·미검증 범위를 유지하였다. 핵심 차이는 적용 산출물이 결과부터 제시하고 제목의 모호한 조건을 명시한 점이다. 단일 관찰이고 예시와 겹치는 과제를 사용하였으므로 manifest의 인과 효과로 해석하지 않는다.

## 5. 독립 검토와 보완

원문 근거 검토자는 본문·appendix·figure를 대조하고 [evidence-review.md](research/evidence-review.md)에 결과를 기록하였다. 이어 [ANALYSIS.md](ANALYSIS.md)와 [MANIFEST.md](MANIFEST.md)를 검토하였다.

검토 후 두 부분을 보완하였다.

- Trained alternation의 지표를 `정답으로 판정된 sampled output 중 short 비율`로 명확히 하였다.
- Manifest의 예시에서 새 holdout 측정을 이미 정한 계획처럼 서술한 부분을 `후속 측정 제안`으로 표시하였다. 원문 사실과 새로 제안한 행동의 경계를 보존하였다.

핵심 논문 해석은 두 trained `that` alternation의 >98% 범위, forced-choice transfer와 실제 산출 비율의 구분, human baseline이 없는 panel, 다른 translator·pivot 검토의 word-count 범위를 유지하였다.

## 6. 산출물 확인

Korean report style 검사에는 `--loanwords english`를 지정하고 morphology 검사도 포함하였다. Markdown 4개 모두 finding 0, 미수행 검사 0으로 통과하였다. Local link 35개의 대상이 존재함을 확인하였고, corpus 수량·RL 조합 수·예시 odds 계산도 확인하였다. 이 검사는 내용의 과학적 타당성이나 인간 독해 효과를 보장하지 않는다.

분석에 사용한 `acl_latex.tex`는 778 lines이며 SHA-256은 다음과 같다. Official arXiv source와의 byte-level 일치를 확인한 hash는 아니며, 이번에 읽은 local source의 식별값이다.

```text
f300288c906d7e6cdaf285c9fda5b6894dadd20dab8ee7eeb2dcecf13bd504cc
```

Global instruction, 기존 skill, repository 설정, 원문 source는 변경하지 않았다. 새 dependency 설치·training·원문 통계 재현·human reader 평가는 수행하지 않았다.
