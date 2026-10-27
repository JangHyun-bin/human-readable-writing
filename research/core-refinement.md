# Writing core 고도화 비교

## 사전 설계

사용자가 선호한 PR 설명의 내용 배치와 기존 coding 답변의 중복, 연구 해석에서 빠진 추론 연결을 기준으로 후보 하나를 작성하였다. 기존 core의 명사 연쇄 지시를 주체·동작·조건·이유의 명시와 검증·한계의 묶음으로 바꾸었다. 이 교체로 원래의 명사 관계 설명이 약해질 수 있으므로 개선 효과를 가정하지 않는다.

기존 core와 후보는 `o200k_base` 기준 각각 61 tokens이다. 실제 provider input usage 차이는 실행 후 별도로 확인한다. 전역 지침·skill invocation 설정은 변경하지 않는다.

| 조건 | 추가 지침 |
|---|---|
| baseline | 없음 |
| current | 기존 benchmark의 CORE |
| candidate | `benchmark_core.py`의 CORES에 고정한 문구 |

기존 coding 과제는 각 조건 5회 반복한다. 후보 작성에 사용하지 않은 API 문서·incident 과제는 각 조건 1회 실행한다. 총 21회이며 실행 중 후보를 변경하지 않는다. 새 과제의 output을 확인한 뒤 지침을 고치면 별도의 실험으로 취급한다. 모든 과제는 가상 사실을 사용한다.

기존 [runner](benchmark_writing.py)의 app-server·host instructions·tool 정의·계측을 재사용한다. Model·effort는 이전 비교와 같은 `gpt-6-astra/high`로 고정하며 현재 local config의 effort 값에 따라 변경하지 않는다. 각 실행은 fresh ephemeral thread이고 다른 skill·tool을 사용하지 않는다. [OpenAI app-server 문서](https://learn.chatgpt.com/docs/app-server)의 thread·turn 경계를 사용한다.

첫 여섯 block은 조건 순서의 여섯 permutation을 모두 포함한다. 실행은 한 번에 하나씩 진행하며 output·token usage·최종 답변 첫 token까지의 시간·전체 시간을 보존한다. Provider의 cache 상태를 강제하거나 cold/warm으로 지정하지 않으므로 시간 차이를 지침의 인과 효과로 확정하지 않는다.

Blind 비교 자료는 과제별로 답변을 A·B·C에 무작위 배정하고 지침·usage·시간은 제외한다. 대응표는 별도 file에 보존한다. 대표 비교는 결과를 보기 전 정한 각 과제의 첫 번째 repeat이며, 나머지 coding repeat도 모두 제공한다. 사실 보존 검토와 읽기 선호도는 별도로 기록한다. Agent 평가를 추가하면 model 판단임을 표시하고 인간 독해 측정으로 해석하지 않는다.

## 실행 순서

- [ ] 기존 runner가 후보 지침을 기존 core에 덧붙이지 않고 교체하는지 검사한다.
- [ ] 고정한 세 조건을 21회 실행하고 원본을 보존한다.
- [ ] 모든 output의 수치·범위·부정·불확실성과 추가된 주장을 입력과 대조한다.
- [ ] Blind 비교 자료·조건 대응표·계측 요약을 작성한다.
- [ ] 문서와 code를 확인하고 private remote에 반영한다.

## 판단 범위

Coding 반복은 같은 과제에서 생성 결과가 얼마나 달라지는지 확인한다. 새 과제는 각 cell이 한 번뿐이므로 domain 일반화나 latency의 p95·통계적 유의성을 추정하지 않는다. 추가 billing 금액·인간 이해 시간·다중 turn coding 작업은 측정하지 않는다. 결과 확인 전 새 core를 상시 적용하지 않는다.
