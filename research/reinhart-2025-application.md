# Reinhart et al. (2025): writing 지침 적용 가설

확인일: 2026-10-28. 이 note는 자료 조사와 제안이며, manifest·global 지침을 변경하지 않는다.

## 확인한 evidence

영어 human text의 앞 약 500 words를 context로 주고, model continuation을 뒤 human chunk와 paired 비교했다. HAP-E는 6 genre, CAP는 8 register다. Human control은 실제 다음 글이며 reader comprehension 측정이 아니다. Instruction-tuned model은 present participial clause와 nominalization을 human보다 자주 썼지만 GPT-4o의 agentless passive는 약 절반이었다. Llama base는 Instruct보다 human과 가까웠다. 이는 tuning의 영향을 시사하지만 특정 training stage의 causal effect를 분리한 실험은 아니며 GPT base 비교도 없다. 따라서 한국어·영어 혼용의 PR이나 agent report에 editing 지침을 적용했을 때 이해도가 개선된다는 근거는 아니다. [Methods·Results·Discussion](https://arxiv.org/html/2410.16107v2)

## 우리 적용 가설

**B를 유지하고, 평소 instruction을 늘리기 전에 모호한 관계만 푸는 편이 낫다.** 아래는 논문에서 검증한 intervention이 아니라 이 프로젝트의 실무 가설이다.

> 주체·동작·조건·이유를 밝히고 검증·한계는 묶어 중복을 줄인다. 수치·단위·범위·부정·불확실성을 보존하고 관찰·가설·인과를 구분한다.

현재 B의 `밝힌다`는 **이미 확인한 관계를 드러낸다**는 뜻으로 적용한다. 주체나 이유가 없다고 추측해 채우지 않는다. `검증·한계는 묶는다`도 서로 다른 주장에 적용되는 제한 조건을 한 곳으로 몰아넣으라는 뜻으로 쓰지 않는다. 각각의 주장과 조건이 연결된 상태에서 같은 내용을 반복하지 않는다는 뜻이다.

이해를 방해하는 경우에만 다음 operations를 적용한다.

| 걸리는 부분 | 하는 일 | 보존할 것 |
|---|---|---|
| 누가 무엇을 하는지 감추는 nominalization | 행위자를 알고 있으면 동사로 풀기 | 결과물·측정량·API를 가리키는 명칭 |
| 이유·조건·결과가 섞인 participial clause | 확인된 관계에 맞춰 문장을 잇거나 분리하기 | `may`, 부정, 적용 범위 |
| 관계를 알 수 없는 noun chain | 명칭 사이를 조사·전치사·동사로 잇기 | 검색 가능한 technical term |
| 구체적 결과를 되풀이하는 평가 문장 | 새 사실이나 판단 기준이 없으면 제거하기 | 실제 검증 범위·한계 |

`noun-heavy`를 모든 명사나 긴 technical term의 결함으로 판정하지 않는다. Passive를 지우려고 모르는 행위자를 만들지 않는다. 참여자·대상을 앞세우는 passive가 목적에 맞으면 유지한다. `-ing`나 접미사 개수, AI detector 점수를 품질 기준으로 쓰지 않는다. 한국어 명사형이나 연결어미를 영어 feature와 일대일로 대응시키지도 않는다.

## Synthetic before/after

아래 수치·동작은 모두 가상이다. 실제 프로젝트의 검증 결과가 아니다.

### 1. Nominalization에서 확인된 동작 꺼내기

Before: `worker의 connection 재설정 수행은 timeout 발생 이후에만 이루어진다.`

After: `worker는 timeout이 발생한 뒤에만 connection을 다시 설정한다.`

주체·조건은 원문에 있으므로 드러낼 수 있다. `뒤에만`은 유지한다. 여기서 `reconnection`이 API나 event 이름이면 그 이름은 보존한다.

### 2. Participial structure에서 가능성의 범위 보존하기

Before: `The worker retries only timed-out requests, potentially reducing transient failures without changing the 2 s timeout.`

After: `The worker retries only timed-out requests; the timeout remains 2 s. The retry may reduce transient failures.`

Retry의 대상, 2 s, 가능성은 그대로다. “Failure를 줄였다”로 바꾸면 관찰하지 않은 결과를 만든다. 영어 PR 예시이므로 두 문장 모두 영어로 두었다.

### 3. 모르는 noun chain을 억지로 해석하지 않기

Before: `holdout calibration validation gate`

After: `holdout에서 무엇을 검증하는지, 그 결과로 어떤 진행을 허용하는지 확인이 필요하다.`

원문만으로 `calibration을 끝낸다`거나 `threshold를 정했다`고 쓰지 않는다. 제목의 간결함보다 의미 확인이 먼저다.

### 4. 반복만 줄이고 검증 범위 남기기

Before: `성공한 96/120 session의 replay에서 median error는 1.4 m → 1.1 m였다. 실패한 24 session은 제외했다. 이는 개선을 보여준다. 현장 검증은 하지 않았다. 현장 성능 개선 여부는 아직 모른다.`

After: `성공한 96/120 session의 replay에서 median error가 1.4 m에서 1.1 m로 줄었다. 실패한 24 session은 제외했고 현장에서는 검증하지 않아, 현장 성능 개선 여부는 모른다.`

숫자와 제외 범위는 유지하고 결과 재진술만 지웠다. 실패 session까지 포함한 전체 성능 개선을 주장하지 않는다.

## 작은 평가 제안

아직 실행하지 않았다. 기존 평가 구조를 그대로 쓰고 새 parser·dependency·tool call을 만들지 않는다.

1. 고정한 가상 fact set 12개를 report·PR·연구 해석에 4개씩 배분한다. 각 fact set에 필수 수치·부정·조건·미검증 범위를 미리 적는다.
2. 같은 model·generation 조건에서 **B**와 **B + `관계가 불명확한 명사 연결과 수식만 풀어 쓴다.`**를 비교한다. 각 12개 output이면 24회 generation이다. 먼저 이 한 문장만 검토하고 다른 지침을 동시에 섞지 않는다.
3. Reader에게 variant를 가리고 순서를 섞는다. 누가 무엇을 바꿨는지, 언제 성립하는지, 무엇을 검증하지 않았는지를 묻고 답의 정확도·답을 찾는 시간·선호를 기록한다. Source fact set을 기준으로 의미 누락·추가도 따로 판정한다.
4. Input/output token 수와 tool call 수를 함께 비교한다. 숫자·부정·범위가 하나라도 달라진 output은 더 짧거나 선호가 높아도 실패다. 12개 pilot의 결과를 일반적 개선 효과로 해석하지 않는다.

효과가 없으면 추가 문장을 채택하지 않는다. 예시는 요청받아 검토할 때 읽는 자료에 두고 매 turn instruction에 싣지 않는다.

## Primary materials와 접근 상태

- [PNAS 본문](https://www.pnas.org/doi/10.1073/pnas.2422455122), [arXiv v2](https://arxiv.org/html/2410.16107v2): Methods·Results·Discussion 확인.
- [저자의 HAP-E 설명](https://cmustatistics.github.io/data-repository/language/hap-e.html), [공개 corpus card](https://huggingface.co/datasets/browndw/human-ai-parallel-corpus): 접근 확인. 전체 corpus를 내려받거나 재분석하지 않았다.
- [PNAS SI Appendix](https://www.pnas.org/doi/suppl/10.1073/pnas.2422455122/suppl_file/pnas.2422455122.sapp.pdf): 403. PMC 본문은 browser check, SI 경로는 fetch 실패. Prompt의 exact wording·decoding setting·SI 표를 직접 확인하지 못했다.
- [OSF analysis code](https://osf.io/7mrqn/): 403. 공개 API와 files URL도 fetch 실패. Code를 실행하거나 classifier split을 audit하지 않았다.

한국어·영어 혼용 독해 효과와 실제 tool 왕복 감소는 미검증이다. 위 editing 예시는 논문의 번역이나 저자가 검증한 지침이 아니다.
