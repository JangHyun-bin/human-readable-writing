# 실측 답변 비교

기존 benchmark의 실제 output을 원문 그대로 배치하였다. 새 model 요청이나 재작성은 수행하지 않았다. 가상 과제이며 실제 프로젝트의 측정 결과가 아니다.

## 적용한 축약 지침

> 기술 설명은 명사 연쇄의 관계와 주체·행동·조건을 분명하게 쓴다. 수치·단위·범위·부정·불확실성을 보존하고 관찰·가설·확인한 인과를 구분한다.

이 지침 본문은 세 과제에서 각 baseline보다 input 61 tokens를 추가하였다. 상시 적용 후보의 검토 자료이며 현재 전역 설정을 변경한 기록은 아니다.

## PR 설명

### 입력

> 다음 사실로 PR description을 4문장 이내로 작성해줘.
> 같은 account에 대한 write가 동시에 실행될 때 record가 중복 생성되는 문제가 있었다.
> 같은 account의 write를 직렬화하는 guard를 추가했다. 다른 account끼리는 병렬 실행을
> 유지한다. Unit test 6개가 통과했다. 부하 test와 실제 배포는 수행하지 않았다.
> Guard는 단일 process 안에서만 유효하며 여러 process 간 중복 방지는 미검증이다.

### 기본 답변

> 같은 account의 write가 동시에 실행될 때 record가 중복 생성되는 문제를 해결하기 위해, 해당 account의 write를 직렬화하는 guard를 추가했다.
> 다른 account끼리는 병렬 실행을 유지하며, Unit test 6개가 통과했다.
> 부하 test와 실제 배포는 수행하지 않았다.
> Guard는 단일 process 안에서만 유효하며, 여러 process 간 중복 방지는 미검증이다.

### 축약 지침 적용 답변

> 같은 account에 대한 write가 동시에 실행될 때 record가 중복 생성되는 문제가 있었다. 같은 account의 write를 직렬화하는 guard를 추가했으며, 다른 account 간 write는 병렬 실행을 유지한다.
>
> Unit test 6개가 통과했으며, 부하 test와 실제 배포는 수행하지 않았다.
> Guard는 단일 process 안에서만 유효하며, 여러 process 간 중복 방지는 미검증이다.

| 조건 | Input usage | Output usage | Reasoning usage | 첫 token | 전체 시간 |
|---|---:|---:|---:|---:|---:|---:|
| 기본 | 18,061 | 271 | 171 | 10.71 s | 12.27 s |
| 축약 지침 | 18,122 | 215 | 115 | 10.36 s | 12.27 s |

## Coding 작업 보고

### 입력

> 동료에게 보낼 작업 결과를 4문장 이내로 작성해줘.
> Android pose timestamp가 20 ms grid에 snap되었다. label noise가 발생했을 가능성이
> 있지만 regression dilution이 원인인지는 미확인이다. Replay에서 p95 error가
> 2.4 m에서 1.8 m로 감소했다. 전체 150 session 중 성공한 135 session만 집계했고
> 실패한 15 session은 제외했다. 같은 data로 threshold도 선택하여 independent
> holdout이 아니다. iOS와 현장 실기는 미검증이다. 다음 행동은 전체 session을 포함한
> 별도 holdout 평가를 제안하는 것이며 확정된 계획은 아니다.

### 기본 답변

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외한 결과입니다.
> 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며, 확정된 계획은 아닙니다.
> 같은 data로 threshold도 선택해 independent holdout이 아니며, iOS와 현장 실기는 미검증이므로 이번 결과의 일반화 여부는 확인되지 않았습니다.

### 축약 지침 적용 답변

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성은 있지만, regression dilution이 원인인지는 미확인이다.
> Replay에서 p95 error가 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계했고 실패한 15 session은 제외했다.
> 같은 data로 threshold도 선택했으므로 independent holdout 평가가 아니며, 전체 session을 포함한 별도 holdout 평가를 제안하지만 확정된 계획은 아니다.
> iOS와 현장 실기는 미검증이며, 현재 결과는 실패한 session을 제외한 평가라는 한계가 있다.

| 조건 | Input usage | Output usage | Reasoning usage | 첫 token | 전체 시간 |
|---|---:|---:|---:|---:|---:|---:|
| 기본 | 18,104 | 480 | 326 | 19.15 s | 20.98 s |
| 축약 지침 | 18,165 | 408 | 255 | 16.55 s | 17.45 s |

## 연구 해석

### 입력

> 다음 연구 사실의 의미와 한계를 동료에게 4문장 이내로 설명해줘.
> 영어 corpus에서 읽기 어려움과 관련된 feature가 관찰되었다. 작은 model의 length
> penalty 실험에서는 KL이 없을 때 두 trained that alternation의 생략 비율이 98%를
> 초과했다. Far transfer는 네 종류 중 genitive에서만, KL 없는 조건에서 나타났다.
> Transfer는 forced-choice probability로 평가했다. Frontier model의 실제 훈련
> 원인과 인간의 독해 개선, 한국어 적용 효과는 확인하지 않았다.

### 기본 답변

> 영어 corpus에서 읽기 어려움과 관련된 feature가 관찰됐지만, 그 관계만으로 읽기 어려움의 원인이라고 볼 수는 없다.
> 작은 model의 length penalty 실험에서는 KL이 없을 때 훈련 대상인 두 that alternation 모두 생략 비율이 98%를 넘었다.
> Far transfer는 네 종류 중 genitive에서만, KL 없는 조건에서 나타났으며, transfer를 forced-choice probability로 평가했으므로 실제 생성에서도 같은 변화가 나타난다고 단정할 수는 없다.
> Frontier model의 실제 훈련 원인, 인간의 독해 개선, 한국어 적용 효과는 확인하지 않았으므로 이 결과를 그 범위까지 일반화할 근거는 없다.

### 축약 지침 적용 답변

> 영어 corpus에서 읽기 어려움과 관련된 feature가 관찰되었지만, 이 관찰만으로 해당 feature가 읽기 어려움을 유발한다고 볼 수는 없다. 작은 model의 length penalty 실험에서는 KL이 없을 때 훈련한 두 that alternation의 생략 비율이 98%를 초과했다. Transfer는 forced-choice probability로 평가했으며, far transfer는 네 종류 중 genitive에서만, KL이 없는 조건에서 나타났다. Frontier model의 실제 훈련 원인, 인간의 독해 개선, 한국어 적용 효과는 확인하지 않았으므로, 이 결과를 실제 독해 개선이나 다른 언어에서의 효과로 일반화할 근거는 없다.

| 조건 | Input usage | Output usage | Reasoning usage | 첫 token | 전체 시간 |
|---|---:|---:|---:|---:|---:|---:|
| 기본 | 18,079 | 455 | 291 | 13.58 s | 16.36 s |
| 축약 지침 | 18,140 | 375 | 216 | 16.06 s | 18.28 s |

## 읽기 품질의 별도 판단

수치와 검증 범위의 보존 여부만으로 문장 배치·어체·독자의 이해 부담까지 판정할 수는 없다. 아래는 실제 output을 읽은 편집 판단이며 독자 실험 결과가 아니다.

- PR 설명에서는 축약 지침 적용 답변이 문제와 변경을 먼저 설명하고, 검증과 한계를 별도 문단으로 배치하였다. 기본 답변의 다른 account 병렬 유지와 unit test 결과는 한 문장에 포함되어 있다.
- Coding 보고의 축약 지침 적용 답변은 실패한 session을 제외하였다는 제한을 두 번째 문장과 마지막 문장에서 반복한다. 축약 지침이 항상 중복을 제거한 것은 아니다.
- 연구 해석의 기본 답변에는 forced-choice 평가만으로 실제 생성에서 같은 변화가 나타난다고 단정할 수 없다는 설명이 있다. 축약 지침 적용 답변은 forced-choice라는 평가 방식만 기재하여, 해당 개념에 익숙하지 않은 독자에게 필요한 설명이 줄었다.

축약 지침이 불필요하다는 결론도, 일관되게 우월하다는 결론도 이 sample만으로 확정하지 않는다. 전체 의미 보존 확인·cache 차이·측정 방식은 [비용 비교](invocation-cost.md), 원본은 [invocation-pilot.jsonl](invocation-pilot.jsonl)을 참조한다.
