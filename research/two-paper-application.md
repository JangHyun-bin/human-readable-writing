# 두 논문을 writing 지침으로 옮기는 방안

검토일: 2026-10-28. 연구·적용 제안이며, 승인된 implementation plan이나 적용 완료 기록이 아니다. B의 사용자 선호와 기존 benchmark 원본을 보존한다.

## 판단

현재 manifest의 원칙 2·3은 이미 명사 관계와 주어·서술의 거리를 다룬다. 이번 연구에서 필요한 것은 원칙의 누적보다 **문제가 있는 표현을 알아보고 의미를 유지하며 바꾸는 예시**다. B를 만든 core는 개인 선호의 기준으로 유지한다. 그 답변의 줄바꿈이나 다음 행동의 위치가 선호를 만들었는지는 밝혀지지 않았다.

Reinhart는 model과 human의 문체 차이를, Martínez는 법률 문장 rewrite의 comprehension·recall을 분석했다. 두 연구의 역할은 다르며, 특정 한국어 편집 규칙의 효과로 합산하지 않는다. [Reinhart 원문](https://arxiv.org/html/2410.16107v2) · [Martínez 원문](https://doi.org/10.1016/j.cognition.2022.105070)

확인한 방법·결과·자료 접근 한계는 [Reinhart 적용 note](reinhart-2025-application.md)와 [Martínez 적용 note](martinez-2022-application.md)에 기록하였다. 이하 규칙·예시·평가 규모는 우리 환경에 맞춘 독립적인 제안이다.

## 무엇을 바꿀 것인가

| 발견한 문제 | 편집 동작 | 그대로 둘 것 |
|---|---|---|
| 행동이 명사로 뭉쳐 누가 무엇을 했는지 읽기 어려움 | 원문에 있는 행위자와 동작을 주어·서술로 꺼내기 | API 이름, 식별자, 정착한 technical term |
| 주어와 서술 사이의 긴 삽입 설명 | 핵심 조건과 동작을 한 문장에 두고 부연 설명을 분리하기 | 조건·예외의 적용 범위와 연결 대상 |
| 조건과 한계가 여러 주장에 뒤섞임 | 각 주장에 적용되는 범위를 가까이 붙이고, 중복되는 검증 설명만 묶기 | 부정·불확실성·검증 범위 |
| 이미 짧고 관계가 명확한 문장 | 그대로 두기 | 독자의 기존 어휘와 문체 |

`명사가 많음`은 오류 판정이 아니다. `regression dilution`, `VPS fix`, `retry_count` 같은 이름은 보존한다. `검증·한계는 묶는다`는 모든 제한 조건을 글 마지막으로 옮긴다는 뜻으로 쓰지 않는다. 예를 들어 `단일 process에서만`은 보장 범위이므로 보장하는 동작과 붙여 쓰고, `부하 test 미수행` 같은 검증 상태를 별도로 정리할 수 있다.

### 가상 예시 1: 행동을 드러내기

Before:

> worker의 connection 재설정 수행은 timeout 발생 이후에만 이루어진다.

After:

> worker는 timeout이 발생한 뒤에만 connection을 다시 설정한다.

행위자와 `뒤에만`이라는 조건은 이미 원문에 있다. 행위자가 없는 문장에 임의로 worker를 추가하면 안 된다.

### 가상 예시 2: 긴 삽입을 분리하기

Before:

> worker는 `status == failed`이고 `retry_count < 3`인 job만, 이전 attempt의 output을 보존하면서, 다시 queue에 넣는다.

After:

> worker는 `status == failed`이고 `retry_count < 3`인 job만 다시 queue에 넣는다. 이때 이전 attempt의 output은 보존한다.

두 조건은 AND이며 `< 3`은 `<= 3`으로 바뀌지 않는다. Output 보존은 해당 재시도 상황에 연결한다. 문장마다 줄바꿈하는 효과는 이 rewrite와 별개의 layout 가설이다.

### 가상 예시 3: 범위를 주장에 붙이기

Before:

> 이 guard는 중복 write를 막는다. Unit test 6개가 통과했다. 단일 process 안에서만 유효하며 여러 process에서는 미검증이다.

After:

> 이 guard는 단일 process 안에서만 중복 write를 막는다. Unit test 6개가 통과했지만, 여러 process에서의 중복 방지는 검증하지 않았다.

예시들은 논문 stimulus나 실제 제품 동작이 아니다. Before의 의미가 정확하다는 전제하에 표현만 바꾼 것이다.

## 구현 경로와 비용

| 경로 | 실행 방식 | 비용·판단 |
|---|---|---|
| 짧은 core로 한 번에 작성 | 기존 답변 생성에 inline instruction을 포함 | 평소 답변에 적용할 경우 우선 후보. 별도 file 조회·rewrite 호출을 요구하지 않지만 input·reasoning·output 비용은 남는다 |
| 기존 explicit skill로 문서 검토 | 요청받은 작업에서만 manifest의 예시·보존 검사를 읽기 | 긴 문서나 문장 개선 요청에 적합. 현재 등록 방식 재사용 |
| 매번 별도 editor·parser 실행 | 생성 후 분석과 재작성 | 현 단계에서는 우선순위를 낮춘다. Korean–English 혼용의 판정 정확도와 추가 왕복 비용을 입증한 근거가 없다 |

추천은 첫 두 경로의 역할 분담이다. Skill을 새로 만들거나 항상 두 번 생성하는 구조는 필요하지 않다. 여기서 inline은 model weights 변경이 아니라 기존 generation에 지침을 포함하는 방식이다.

### 비교용 초안 C — 아직 미적용

```text
명사 관계와 조건을 풀고 긴 삽입 설명은 나눈다. 검증·한계는 묶는다. 수치·단위·범위·부정·불확실성을 보존하고 관찰·가설·인과를 구분한다.
```

Local `tiktoken`의 `o200k_base`로 본문만 계수하면 B는 61 tokens, C는 60 tokens이다. C는 B의 의미 보존 문장을 그대로 유지하고 첫 문장의 편집 행동을 바꾼다. 이미 선호를 확인한 B에 덧붙이는 방식이 아니라 별도 비교 조건이다. C가 B보다 낫다는 근거는 아직 없다.

Tokenizer의 기본 cache가 없어 첫 계수는 download 단계에서 실패했다. 설치된 dependency의 local encoding cache를 사용한 계수는 성공했다. 새 dependency·network download·model generation은 수행하지 않았다. Reference count는 provider usage나 전역 설치 시 제목·pointer를 포함한 비용과 구분한다. 이 1-token 차이는 품질 개선 근거가 아니다.

## 가장 작은 검증 순서

1. **표현 변화부터 확인:** 새로운 가상 설명 6개를 고른다. 행동을 숨긴 명사 표현 2개, 긴 삽입 설명 2개, 이미 명확한 문장 2개를 포함한다. 문체를 바꾸기 전에 source의 행위자·조건·수치·부정·미검증 상태와 이해 확인 질문의 정답을 고정한다.
2. **비용 없이 목표를 구체화:** 사람이 만든 의미 보존 rewrite를 검토한다. 먼저 문장 구조만 바꾸고 layout·정보 순서는 유지한다. 별도 비교에서는 동일 문구의 줄바꿈만 바꾼다. B 선호를 어느 변화에 연결할지 처음부터 단정하지 않는다.
3. **선택한 방식만 generation 비교:** 구현을 진행한다면 B와 C를 6과제×2반복으로 비교한다(총 24회). 이 규모는 오류를 찾는 pilot이며 일반적 우위를 입증할 sample로 취급하지 않는다. 필요가 없으면 실험을 실행하지 않는다.
4. **의미 확인을 먼저 수행:** Source와 의미가 달라진 output은 실패로 기록한다. 품질·선호 결과에서 조용히 제외하지 않는다. 정확한 식별자·수치 확인과 의미 관계의 검토를 구분하며, 단어 일치만으로 의미 보존을 통과시키지 않는다.
5. **선호·이해·비용을 따로 기록:** 이해도를 보려면 독자는 같은 사례의 한 version만 먼저 읽고 source 기반 질문에 답한다. 이후 pair를 제시해 선호를 받는다. 사용자가 이미 본 사례는 독립 이해도 측정에 쓰지 않는다. Input·visible output·reasoning usage·TTFT·전체 시간·도구 event도 보존한다.

기존 runner의 `tool_rounds`는 reference dynamic tool만 센다. 실제 generation 비교를 구현할 때는 builtin tool event도 보존하여 추가 왕복 부재를 점검해야 한다. 현재 측정 원본은 재해석하거나 덮어쓰지 않는다.

## 구현 시 닿는 위치

- `MANIFEST.md`의 원칙 2·3·5·6과 적용 예시: 중복 규칙을 추가하기보다 trigger·편집 동작·보존 대상을 구체화한다. 인용 근거와 적용 가설은 구분한다.
- 새 비교 runner 또는 비교 조건: 과거 `benchmark_core.py`의 동결된 CORES·schedule은 보존한다. 실행된다면 별도 산출물로 기록한다.
- `benchmark_writing.py`·기존 test: 새 비교에서 tool event 기록을 보완할 때만 변경 범위에 포함한다.
- `SKILL.md`·invocation 설정·전역 용어 지침: 현 단계에서 변경할 이유가 없다. 전역 배포는 비교와 채택 이후의 별도 작업이다.

이번 작업은 논문 조사, 적용 예시와 구현 선택지, local token 계수까지다. 지침·runner·global 설정·원본 benchmark는 변경하지 않았다.

## 2026-10-28 후속 pilot 반영

[문장 구조·줄바꿈 pilot](structure-layout-pilot.md)에서 사용자는 N1의 formal한 source(Y)를 선호했고, 이 비교가 읽기 편함보다 formal/casual 차이로 보인다고 밝혔다. N2에서는 문구가 동일한 두 배치 중 문장 사이에 빈 줄을 둔 X를 선호했다. E1의 이해 확인 문항에는 응답하지 않았다.

후속 후보는 formal한 문체를 유지하는 조건으로 좁힌다. 명사형을 동사형으로 바꾸는 동작 자체를 개선으로 취급하지 않고, 문구를 보존한 layout 변화부터 확인한다. N1은 register가 함께 달라진 비교이므로 syntax의 독립 효과를 판정할 수 없다. N2 한 쌍의 선호도 모든 문장에 빈 줄을 요구하는 규칙으로 일반화하지 않는다.

위의 B/C 24회 generation은 이번 선호에 그대로 대응하지 않아 아직 실행하지 않았다. C의 실패나 B의 일반적 우위를 입증한 결과는 아니다. 새 비교가 필요하면 formal한 문체를 공통 조건으로 두고 선택한 layout 변화만 별도 조건으로 검토한다. Core·manifest·global 설정은 변경하지 않았다.

위 순서 제안의 “사람이 만든” rewrite는 실제 수행의 저자를 정확히 설명하지 못한다. Pilot 자료는 assistant가 작성했고 별도 agent가 의미를 검토했다. Human 참여는 사용자의 선호 응답이며, 별도 generation 호출은 없었다. 실제 자료의 작성 방식과 범위는 pilot 기록을 따른다.

이후 N1의 formal한 source를 유지하고 문장 사이에 빈 줄을 둔 조합에 사용자도 “응 좋다.”라고 답했다. 해당 방향을 후속 후보의 기준으로 기록했다. 이어 기존 B의 API 답변 네 문장을 사용해 두 문단으로 묶는 배치와 문장마다 나누는 배치의 선호를 질문했다. 문구는 고정했으며 결과는 [pilot 기록](structure-layout-pilot.md)에 누적한다.

후속 API 비교에서도 사용자는 문장마다 나눈 Y를 선호했다. Formal한 문체를 공통 조건으로 두고 문단 분리 지시의 유무만 달리하는 12회 generation protocol을 작성했다. App-server의 권한 오류로 완료된 답변은 0개이며, 준수율·사실 보존·provider 비용은 아직 확인하지 못했다. [Generation 검증 상태](layout-generation-pilot.md)
