# Martínez 2022: coding-agent 답변에 적용할 가설

확인일: 2026-10-28. 이 문서는 연구 근거와 독립적인 적용 제안을 구분한다. 기존 지침·사용자 B preference·code는 변경하지 않았다.

## 원문 확인과 근거

Martínez, Mollica & Gibson, *Poor writing, not specialized concepts, drives processing difficulty in legal language*. Cognition 224, 105070. [Publisher PDF](https://www.pure.ed.ac.uk/ws/files/256304933/Poor_Writing_MARTINEZ_DOA17022022_VOR_CC_BY_NC_ND.pdf) · [DOI](https://doi.org/10.1016/j.cognition.2022.105070). 아래 page는 논문의 인쇄 page이며, repository PDF에는 앞표지가 하나 더 있다.

Main experiment는 English native 완료자 108명(186명 시작; 전반 comprehension > chance)에게 legalese/simple 각 3개를 pseudorandom 배정했다. Center-embedding·word frequency·voice·capitalization을 함께 바꿨다. Comprehension은 73.5%/67.7%, recall은 42.4%/35.3%(simple/legalese). 문서를 보며 답하는 replication에서도 comprehension 이점이 남았다. [§3.1–3.3, pp.3–5](https://www.pure.ed.ac.uk/ws/files/256304933/Poor_Writing_MARTINEZ_DOA17022022_VOR_CC_BY_NC_ND.pdf#page=4)

의미 보존은 legally relevant propositions를 먼저 정리한 뒤 rewrite하고, 12쌍 중 genre별 한 쌍씩 외부 변호사가 확인했다. 모든 pair의 독립 검증은 아니다. [§3.1.1, p.4](https://www.pure.ed.ac.uk/ws/files/256304933/Poor_Writing_MARTINEZ_DOA17022022_VOR_CC_BY_NC_ND.pdf#page=5)

Center-embedding의 가장 큰 recall effect는 exploratory 분석이다. 개별 feature 일반화를 검증할 power가 부족하다고 명시했다. 전체 rewrite의 차이를 문장 분리만의 효과로 해석하면 안 된다. [§3.2.3, p.5](https://www.pure.ed.ac.uk/ws/files/256304933/Poor_Writing_MARTINEZ_DOA17022022_VOR_CC_BY_NC_ND.pdf#page=6)

**접근 범위:** 본문 Methods·Results·Discussion을 재확인했다. 본문이 공개 위치로 제시한 [OSF project](https://osf.io/xcqd9/)는 403, 공개 API는 접근 실패, publisher의 Supplementary data 경로도 403이었다. SI·전체 materials·code·raw data는 읽거나 실행하지 못했다. 아래는 그 자료를 검증한 결과가 아니다.

## 우리의 적용 제안: 먼저 시험할 규칙 3개

아래는 Korean–English coding-agent 답변에 대한 **미검증 가설**이다. 지침의 implementation 초안이며, 지금 적용한 변경은 아니다.

1. **Actor와 동작 사이를 가로막는 긴 설명을 옮긴다.** 조건과 예외의 범위를 유지할 수 있을 때만 별도 문장으로 푼다. 분리한 문장에는 무엇을 가리키는지 필요한 명사를 다시 써 준다. 짧은 문장도 의미가 더 흐려지면 유지한다.
2. **익숙한 technical term은 보존하고, term 사이의 관계를 문장으로 쓴다.** 새 noun compound를 만들기보다 누가 무엇을 했는지, 어떤 조건에서 달라지는지 설명한다. `retry_count`, 함수명, error message, `VPS fix` 같은 검색 가능한 표현은 그대로 둔다. 사용자의 English 표기 규약을 번역으로 우회하지 않는다.
3. **다시 쓴 뒤 같은 질문에 같은 답이 나오는지 확인한다.** Actor, action, 대상, condition, exception, negation, 수치·단위, 근거와 uncertainty가 보존됐는지 본다. `가능하다`를 `한다`로, `관찰되지 않았다`를 `없다`로 바꾸지 않는다. 원문이 애매하면 관계를 만들어 넣지 않고 그 애매함을 드러낸다.

최소 implementation은 새 parser나 dependency metric 없이, 답변을 마무리할 때 위 세 항목을 한 번 검토하는 prompt instruction이다. 검토용 proposition 목록은 내부 확인에만 쓰고 답변마다 새 형식을 강제하지 않는다. 사용자 B preference를 포함한 현행 답변 방식을 baseline으로 유지한 채 평가할 수 있다.

## 우리의 가상 예시: 의미를 보존하는 rewrite

아래 문장은 논문 stimulus나 실제 repository 동작을 옮긴 것이 아니다.

**예시 1 — 삽입 설명을 옮기되 조건을 유지**

Before: “worker는 `retry_count < 3`이고 `status == failed`인 job만, 이전 attempt의 output을 보존한 채, 다시 queue에 넣습니다.”

After: “worker는 `retry_count < 3`이고 `status == failed`인 job만 다시 queue에 넣습니다. 이때 이전 attempt의 output은 보존합니다.”

의미 확인: `retry_count == 3`인 job은 대상이 아니다. 두 조건은 AND다. Output 보존도 남아 있다. 조건을 `retry_count <= 3`으로 바꾸거나 첫 조건을 별도 문장에 옮겨 모든 failed job에 적용하는 rewrite는 탈락이다.

**예시 2 — 관찰과 원인 미확인을 분리**

Before: “동일한 key의 cache invalidation 요청이, 원인은 아직 확인하지 못했지만, 중복 실행됐습니다.”

After: “동일한 key의 cache invalidation 요청이 중복 실행됐습니다. 원인은 아직 확인하지 못했습니다.”

의미 확인: 중복 실행은 관찰됐지만 원인은 모른다. 이를 race condition이라고 이름 붙이거나 fix됐다고 덧붙이면 정보 추가다. 이처럼 이미 짧은 문장의 분리가 실제로 더 나은지는 preference 평가에서 확인해야 한다.

## 옮기지 않을 blanket rule

다음은 위 제안의 적용 경계다. 논문의 실험 결과로 보장된 규칙이 아니다.

- 모든 문장에 word/token 상한을 두거나 모든 괄호·passive·전문 용어를 없애지 않는다.
- 한 문장에 한 proposition만 허용하지 않는다. 조건과 결론을 함께 쓰는 편이 더 분명할 수 있다.
- 빈도가 낮다는 이유로 정확한 identifier나 domain term을 흔한 말로 바꾸지 않는다.
- 문장을 늘렸거나 preference가 높아졌다는 이유만으로 comprehension 개선을 주장하지 않는다.

## 우리의 저비용 평가안

6–10명의 동료와 coding-agent 답변 12개로 diagnostic pilot을 한다. 이 규모는 효과 크기를 확정할 powered study로 취급하지 않는다. 평가자를 구하기 어렵다면 사용자 한 명의 preference부터 확인하되 개인화 결과로만 기록한다.

1. 현행 답변 A와 위 세 규칙을 적용한 B를 만든다. 조건·예외·uncertainty가 있는 답변을 포함한다. 먼저 사람이 source와 대조해 의미 변화가 있는 pair를 탈락시킨다. 탈락 수 자체도 기록한다.
2. 각 독자는 같은 내용의 A/B 중 하나만 먼저 읽는다. 다른 독자에게는 반대 version을 배정하고 순서를 섞는다. 답변을 보면서 actor/action 질문과 조건의 boundary case 질문에 답하게 한다. 평가 전에 정답을 source에서 정한다.
3. 이해도 답변을 제출한 뒤 두 version을 함께 보여 주고 읽기 편한 쪽과 선택 이유를 묻는다. 이해도 측정이 끝난 뒤 preference를 받아 두 version을 미리 본 효과를 줄인다.
4. Comprehension 정답률, 조건·예외 오류, preference, 읽고 답하는 데 걸린 시간, 길이 차이를 따로 기록한다. Domain 경험도 짧게 묻는다. 선호는 올랐지만 조건 오류가 늘면 채택하지 않는다.

이 pilot은 세 규칙을 묶은 적용의 실용성을 본다. 어느 규칙이 효과를 냈는지는 구분하지 못한다. 문제가 나온 유형만 규칙 하나씩 바꿔 후속 비교한다. 모든 답변에 장문의 재작성 단계를 붙이는 비용도 아직 측정하지 않았다.
