# Writing core 고도화 비교

## 사전 설계

사용자가 선호한 PR 설명의 내용 배치와 기존 coding 답변의 중복, 연구 해석에서 빠진 추론 연결을 기준으로 후보 하나를 작성하였다. 기존 core의 명사 연쇄 지시를 주체·동작·조건·이유의 명시와 검증·한계의 묶음으로 바꾸었다. 이 교체로 원래의 명사 관계 설명이 약해질 수 있으므로 개선 효과를 가정하지 않는다.

기존 core와 후보는 `o200k_base` 기준 각각 61 tokens이다. 실제 provider input usage 차이는 실행 후 별도로 확인한다. 전역 지침·skill invocation 설정은 변경하지 않는다.

| 조건 | 추가 지침 |
|---|---|
| baseline | 없음 |
| current | 기존 benchmark의 CORE |
| candidate | `benchmark_core.py`의 CORES에 고정한 문구 |

`current`는 이전 실험에서 사용한 축약 지침을 뜻한다. 현재 전역에 상시 적용된 지침이라는 의미는 아니다. 두 축약 지침 모두 이번 비교에서만 developer instructions에 포함한다.

기존 coding 과제는 각 조건 5회 반복한다. 후보 작성에 사용하지 않은 API 문서·incident 과제는 각 조건 1회 실행한다. 총 21회이며 실행 중 후보를 변경하지 않는다. 새 과제의 output을 확인한 뒤 지침을 고치면 별도의 실험으로 취급한다. 모든 과제는 가상 사실을 사용한다.

기존 [runner](benchmark_writing.py)의 app-server·host instructions·tool 정의·계측을 재사용한다. Model·effort는 이전 비교와 같은 `gpt-6-astra/high`로 고정하며 현재 local config의 effort 값에 따라 변경하지 않는다. 각 실행은 fresh ephemeral thread이고 다른 skill·tool을 사용하지 않는다. [OpenAI app-server 문서](https://learn.chatgpt.com/docs/app-server)의 thread·turn 경계를 사용한다.

첫 여섯 block은 조건 순서의 여섯 permutation을 모두 포함한다. 실행은 한 번에 하나씩 진행하며 output·token usage·최종 답변 첫 token까지의 시간·전체 시간을 보존한다. Provider의 cache 상태를 강제하거나 cold/warm으로 지정하지 않으므로 시간 차이를 지침의 인과 효과로 확정하지 않는다.

Blind 비교 자료는 과제별로 답변을 A·B·C에 무작위 배정하고 지침·usage·시간은 제외한다. 대응표는 별도 file에 보존한다. 대표 비교는 결과를 보기 전 정한 각 과제의 첫 번째 repeat이며, 나머지 coding repeat도 모두 제공한다. 사실 보존 검토와 읽기 선호도는 별도로 기록한다. Agent 평가를 추가하면 model 판단임을 표시하고 인간 독해 측정으로 해석하지 않는다.

## 실행·검증

- [x] 기존 runner가 후보 지침을 기존 core에 덧붙이지 않고 교체하는지 검사한다.
- [x] 고정한 세 조건을 21회 실행하고 원본을 보존한다.
- [x] 모든 output의 수치·범위·부정·불확실성과 추가된 주장을 입력과 대조한다.
- [x] Blind 비교 자료·조건 대응표·계측 요약을 작성한다.

문서와 code의 최종 확인 후 private remote에 반영한다. 원격 반영 여부는 마지막 commit과 remote HEAD의 일치 여부로 확인한다.

## 실측 결과

2026-10-27에 21개 답변을 생성하였다. 실행 당시 runner의 source commit은 `ca31306`이다. [원본 기록](core-refinement.jsonl)에는 실행 순서·prompt·실제 core·usage·output·timeline을 포함한다. 지침 내용과 계측값을 보기 전 [blind 비교](core-refinement-blind.md)의 T1·T6·T7부터 확인할 수 있다. [조건 대응표](core-refinement-key.json)는 별도로 제공한다.

### Input budget

일곱 비교 block 모두에서 `current`와 `candidate`의 실제 input usage가 같았다. 두 조건의 input은 해당 block의 `baseline`보다 정확히 61 tokens 많았다. 모든 답변의 reference tool 왕복은 0이었다. 이 결과는 지침 본문의 input 비용이며, 전역에 제목·설명·추가 pointer를 함께 설치할 경우 그 부분의 비용은 별도로 발생한다.

후보 문구는 다음과 같다. 기본 적용 설정에는 반영하지 않았다.

```text
주체·동작·조건·이유를 밝히고 검증·한계는 묶어 중복을 줄인다. 수치·단위·범위·부정·불확실성을 보존하고 관찰·가설·인과를 구분한다.
```

### Coding 반복 측정

같은 coding 과제를 조건별 5회 실행한 중앙값이다. Output usage에는 reasoning이 포함되며 두 열의 수치를 합산하지 않는다. 시간 범위는 다섯 실행의 최솟값과 최댓값이다.

| 조건 | Input usage | Output usage | Reasoning usage | TTFT | 전체 시간 | 전체 시간 범위 |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 18,010 | 328 | 173 | 17.96 s | 21.08 s | 12.44–23.25 s |
| current | 18,071 | 393 | 251 | 18.41 s | 21.28 s | 16.84–24.65 s |
| candidate | 18,071 | 378 | 225 | 16.24 s | 19.89 s | 14.74–27.11 s |

후보의 TTFT·전체 시간 중앙값이 더 짧았지만 분포가 겹쳤고 후보의 가장 느린 실행은 27.11 s였다. Cache hit도 실행마다 달랐다. 이 sample에서 후보가 안정적으로 빠르다거나 output·reasoning 비용을 항상 줄인다고 판단하지 않는다.

### 새 과제

각 cell은 한 번 측정한 값이다. 조건별 5회 반복의 coding 중앙값과 다른 성격의 기록이므로 반복 측정 결과와 구분한다.

| 과제 | 조건 | Input usage | Cached input | Output usage | TTFT | 전체 시간 |
|---|---|---:|---:|---:|---:|---:|
| API 문서 | baseline | 17,986 | 13,184 | 293 | 9.91 s | 11.15 s |
| API 문서 | current | 18,047 | 0 | 349 | 12.90 s | 14.01 s |
| API 문서 | candidate | 18,047 | 13,184 | 317 | 11.35 s | 12.61 s |
| Incident 경과 | baseline | 18,001 | 13,184 | 281 | 10.03 s | 11.75 s |
| Incident 경과 | current | 18,062 | 13,184 | 377 | 14.27 s | 15.97 s |
| Incident 경과 | candidate | 18,062 | 0 | 331 | 10.51 s | 12.10 s |

21개 답변 생성의 누적 usage는 input 378,965 tokens이며 이 중 cached input은 96,896 tokens이다. Output은 reasoning을 포함하여 7,450 tokens이다. 이 합계에는 실험 설계·문서 작성·별도 agent 검토의 비용을 포함하지 않는다. Billing 금액으로 환산하지 않았다.

### 사실 보존

작성자가 조건 이름을 알고 전체 21개 output을 입력과 직접 대조하였다. 수치·범위·부정·불확실성의 중대한 누락이나 모순을 발견하지 못하였고, 모든 답변은 4문장 이내였다. 이는 완전한 의미 동등성이나 읽기 품질에 대한 판정이 아니다.

| 과제 | 필수 확인 항목 | 검토 수 |
|---|---|---:|
| Coding 보고 | 20 ms, noise의 가능성과 원인 미확인, p95 2.4 m→1.8 m, 전체 150·성공 135·실패 15, 같은 data의 threshold 선택과 holdout 부재, iOS·현장 미검증, 후속 평가가 제안이며 미확정임 | 15 |
| API 문서 | 같은 job_id의 첫 성공 결과, payload 변경 시 HTTP 409, 24 h, 그 이후·다른 region의 비보장, timeout의 의미와 같은 job_id 재시도, unit test 12개·production 미검증 | 3 |
| Incident 경과 | 14:00·14:02·14:09·14:12, 1.2%→8.6%→1.5%, app version rollback과 DB schema 불변, pool 지표 부재, 원인·rollback의 인과 미확인, 후속 실행 미정 | 3 |

Coding 일부 답변에는 평가 조건 때문에 일반화가 제한된다는 해석이 추가되었다. 한 답변에는 성능이 실제보다 좋게 평가되었을 수 있다는 가능성이 추가되었다. 이를 입력에서 직접 측정한 사실로 취급하지 않고, 명시된 평가 제약에 대한 해석으로 구분하였다. 향후 측정에서는 원문 사실의 보존과 추가 해석의 적절성을 별도로 확인한다.

### 조건을 가린 agent 평가

별도의 agent에게 입력과 익명 답변 file만 제공하였다. 지침·조건 대응표·계측값·기존 평가를 제공하지 않았고, 일곱 비교의 순위와 사실 보존 판단을 [평가 원본](core-refinement-reader.json)에 저장한 뒤 조건을 해제하였다. 이후 같은 agent가 code와 실험 방법을 검토하였으므로, 선호 평가는 해당 추가 검토 이전에 저장한 내용으로 고정하였다.

| 비교 | 기존 core와 후보의 읽기 선호 |
|---|---|
| T1 · Coding repeat 1 | current |
| T2 · Coding repeat 2 | current |
| T3 · Coding repeat 3 | candidate |
| T4 · Coding repeat 4 | current |
| T5 · Coding repeat 5 | current |
| T6 · API 문서 | candidate |
| T7 · Incident 경과 | 동률 |

일곱 비교에서 current 4회·candidate 2회·동률 1회였다. 이 중 다섯 비교는 같은 coding 과제의 반복이며, 일곱 개의 독립된 domain 표본으로 해석하지 않는다. 평가자 한 agent의 선호로서 사람의 독해 속도·오류율을 측정한 결과가 아니다. 사용자 선호는 이 집계에 포함하지 않았다.

Baseline을 포함하면 T3에서는 baseline과 candidate가, T6에서도 baseline과 candidate가 공동 선호였고 T7은 세 조건 동률이었다. T5에서는 baseline이 가장 선호되었다. 따라서 축약 지침이 모든 과제에서 baseline보다 낫다는 근거도 확보하지 못하였다. 별도 agent의 사실 보존 검토에서도 중대한 누락이나 모순은 보고되지 않았다.

### 적용 판단

후보가 기존 core를 대체할 만큼 일관된 개선을 보이지 않아 이번 후보 교체는 보류한다. 기본 응답 경로와 명시적 skill 호출 설정을 유지하였다.

Coding 답변에서는 제안을 먼저 제시한 뒤 제약을 설명하는 순서가 여러 번 관찰되었다. Agent는 제약에서 제안으로 이어지는 답변을 더 선호하는 경향을 보였다. API 문서에서는 사용 규칙·보장 범위 사이에 unit test 결과가 끼어드는 current 답변보다, 사용 규칙 다음에 보장 범위와 검증 상태를 둔 candidate와 baseline 답변을 동등하게 선호하였다.

이 결과는 검증·한계를 한곳에 모으는 단일 지시만으로 읽기 품질이 안정적으로 개선되지는 않음을 보여주는 사례이다. 후속 후보는 독자가 제안의 근거를 먼저 이해하도록 관계를 명시하는 방향으로 검토할 수 있지만, 이번 실험에서 검증한 지침으로 취급하지 않는다.

## 판단 범위

원본의 `tool_rounds`는 `read_writing_reference`라는 dynamic tool 호출을 센 값이다. 기존 runner는 builtin tool의 completed item type을 보존하지 않았으므로, 이 값만으로 builtin tool도 전혀 사용되지 않았음을 독립적으로 입증하지는 못한다. 따라서 reference tool 호출 부재와 모든 종류의 tool 사용 부재를 구분한다. 이 계측 한계는 같은 runner를 사용한 이전 pilot에도 적용된다.

Coding 반복은 같은 과제에서 생성 결과가 얼마나 달라지는지 확인한다. 새 과제는 각 cell이 한 번뿐이므로 domain 일반화나 latency의 p95·통계적 유의성을 추정하지 않는다. 추가 billing 금액·인간 이해 시간·다중 turn coding 작업은 측정하지 않는다. 결과 확인 전 새 core를 상시 적용하지 않는다.
