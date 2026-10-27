# AI-generated language의 이해 비용과 작성 원칙

작성일: 2026-10-27 · 대상: arXiv:2610.29162v1

## 1. 핵심 판단

이 논문에서 실무로 옮길 핵심은 **독자가 의미를 복원하는 비용을 줄인다**는 작성 목표이다. 단어 수를 줄이면 문서가 짧아지지만, 관계를 생략한 명사구나 수식이 중첩된 문장에서는 독자가 원인·조건·대상을 다시 추론해야 한다. 간결함은 이러한 관계를 보존한 뒤 불필요한 내용을 제거하는 것으로 정의하는 편이 타당하다.

저자들은 영어 AI output에서 읽기 어려움과 관련된 언어적 특성을 측정하였다. 별도의 작은 model에서는 length penalty가 일부 짧은 문법 형태에 대한 preference를 강화하는 것을 보였다. 다만 **이 연구는 실제 사람의 이해도 저하를 직접 측정하지 않았으며, frontier model의 훈련 원인을 확인한 연구도 아니다.** 한국어·영어 code-switching에 대한 효과 역시 미검증이다.

따라서 논문의 feature를 일괄 금지하는 규칙보다, 기술적 의미를 보존하면서 관계를 명시하는 편집 절차가 적합하다. 권고 산출물은 [MANIFEST.md](MANIFEST.md)이다. 기존 `writing-for-agents`·`korean-report-style`·Ponytail의 범용 규칙은 유지하고, 이 manifest에서 문장의 이해 비용과 의미 보존을 점검한다. 새 skill의 추가 효과는 아직 입증하지 않았으므로 별도 skill은 생성하지 않았다.

## 2. 원문과 분석 범위

- 논문: Thomas Hikaru Clark, Matias B. Martin, Kyle Mahowald, *Why is AI-generated language so hard to understand?*
- 정본 version: [arXiv:2610.29162v1](https://arxiv.org/abs/2610.29162v1), 2026-10-21 제출.
- 사용한 local source: [acl_latex.tex](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex).
- 본문·appendix와 제공된 figure를 분석하였다. 독립 검토 결과는 [evidence-review.md](research/evidence-review.md)에 기록하였다.
- 원문 code/data를 실행하거나 저자들의 통계를 재산출하지 않았다. 본문의 수치와 figure를 대조한 분석이다.

아래에서 **관찰**은 논문 corpus의 결과, **실험적 근거**는 제한된 intervention의 결과, **저자 가설**은 논문이 제시한 설명, **실무 제안**은 이 분석에서 도출한 작성 방침을 뜻한다. 네 범주의 근거 수준을 동일하게 취급하지 않는다.

## 3. 논문의 질문과 전체 구조

| 질문 | 접근 | 확보한 근거 | 남은 문제 |
|---|---|---|---|
| H1: 최근 LLM은 사람이 처리하기 어려운 언어적 특성을 과도하게 사용하는가 | AI output을 human corpus 및 round-trip paraphrase와 비교 | 여러 feature의 빈도·길이·n-gram 차이 | 실제 독자의 이해도 차이 |
| H2: 정보 밀도에 대한 압력이 이러한 언어적 preference를 유발할 수 있는가 | 작은 model에 length penalty를 가하며 RL | 일부 syntactic alternation에서 짧은 형태 선택 증가 | frontier model에서 같은 원인이 작동하는지 |

H1은 output의 분포를 관찰한다. H2는 가능한 원인 하나를 작은 통제 실험으로 검토한다. 두 실험을 함께 고려하더라도 “frontier reasoning training 때문에 실제 사람이 덜 이해한다”는 전체 인과 관계가 확인되는 것은 아니다. 원문 Introduction, Experiment 2, Limitations 참조. [source L81–106](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:81), [L265–287](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:265), [L311–314](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:311).

## 4. Experiment 1의 설계

### 4.1 Corpus와 대조군

전체 14 model을 사용하였지만 모든 setting에 모든 model을 투입하지는 않았다.

| Setting | AI 수집 범위 | Human comparison | 해석상 주의 |
|---|---|---|---|
| Chat | 12 model × 10 topic = 120 conversation, 1,428 reply | OpenSubtitles | 영화·방송 대사와 assistant 답변은 목적과 형식이 다르다 |
| Coding | frontier/near-frontier 9 model × Python repo 5개 = 45 session | StackExchange | coding agent의 작업 보고와 Q&A는 완전히 같은 genre가 아니다 |
| Essay | 14 model × 7 assignment × 10회 = 980 essay | PERSUADE 2.0에서 선별한 2,934 student essay | 학생의 학년·작성 환경과 model의 조건이 다르다 |

AI와 대화한 user도 실제 사람이 아니라 Claude Sonnet 4.6으로 모사하였다. 공통 Pi harness를 사용하였고, skill·repository의 `AGENTS.md`·context compaction 등을 비활성화하였다. 따라서 현재 우리의 instruction이 많은 작업 환경에서 같은 분포가 관찰된다고 단정할 수 없다. [source L333–340](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:333), [L344–403](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:344).

Coding 분석 대상은 user에게 반환한 turn-final 자연어이다. tool 사이의 commentary, code diff, 마지막 `MEMORY.md` 작성 요청에 대한 답변은 분석에 포함되지 않았다. Code 자체나 agent manifest의 품질을 평가한 실험으로 해석할 수 없다. [source L389–414](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:389).

### 4.2 측정한 feature

| Feature | 논문의 측정 | 읽기 비용과의 연결 | 작성에 적용할 때의 범위 |
|---|---|---|---|
| Low-frequency n-grams | corpus에 없는 bigram 빈도, trigram model 기준 perplexity | 익숙하지 않은 연결은 예측하기 어렵다 | 새로 만든 표현의 의미 관계를 풀어 쓴다. 전문 용어 자체는 보존한다 |
| Dependency length | 문장 내 syntactic dependency의 거리, 문장 길이를 표준화 | 서로 연결해야 하는 말이 멀수록 기억 부담이 증가할 수 있다 | 주어와 핵심 서술을 가깝게 두고 긴 조건을 별도 문장으로 분리한다 |
| Object relative clauses | overt relativizer 유무별 ORC 빈도 | 일부 구조에서 word order·dependency 처리 부담이 발생한다 | 영어의 `that`을 기계적으로 추가하지 않고 구조의 명확성을 검토한다 |
| Stacked noun compounds | modifier 관계의 noun 3개 이상 | 어느 noun끼리 연결되는지 모호할 수 있다 | 낯선 명사 연쇄를 조사·전치사·동사로 풀어 쓴다 |
| Denominal verbs | noun에서 유래한 verb 후보를 classifier로 판정 | 새 용법에서 의미·품사 재해석이 필요할 수 있다 | 관용적 기술 용법은 유지하고, 임의의 verb가 숨긴 행동을 명시한다 |
| Inanimate subject + animate verb | animate subject를 주로 취하는 active verb에 inanimate subject가 결합한 후보 | personification 해석 등 추가 처리가 필요할 수 있다 | 은유가 숨긴 실제 현상·행위자를 밝힌다 |

근거: Experiment 1, Linguistic features of interest. [source L132–197](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:132).

feature는 문장별 오류 판정기가 아니다. `cache miss`, `garbage collection`, `deadlock`, `regression dilution`처럼 정착한 용어는 길이나 은유적 기원만으로 제거할 대상이 아니다. 익숙함·독자의 전문성·주변 문맥을 함께 판단해야 한다. 이 문단은 논문의 자동 판정 규칙이 아니라 실무 제안이다.

### 4.3 Round-trip translation의 역할

같은 문장을 English → Japanese → English로 번역한 뒤 원문과 비교하였다. 주요 translator는 NLLB-200 3.3B이다. 목표는 의미가 비슷한 대안에서도 원래 output의 feature가 유지되는지 확인하는 것이다. 번역 후 특정 feature가 줄었다면, 원래 표현 외의 대안이 존재한다는 근거가 된다. [source L208–213](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:208).

그러나 round-trip은 완벽한 의미 고정 실험이 아니다. 번역에서 의미·관계·강조가 바뀔 수 있으며, 원문에는 이 corpus의 의미 보존 정확도를 수동 평가한 결과가 없다. 번역 자체가 흔한 표현으로 정규화하는 경향도 논문에서 인정한다. 따라서 “번역 후 feature가 줄었으므로 반드시 더 이해하기 쉽다”는 결론은 성립하지 않는다.

Russian pivot 및 TranslateGemma 4B도 추가 확인하였지만, 제공된 appendix 결과는 word count figure이다. 모든 feature의 주요 결론이 다른 translator와 pivot에서도 재현되었다고 확인할 근거는 제시하지 않는다. 문장 분할 비율도 translator·pivot에 따라 0.8%에서 14.1%까지 달랐다. [source L521–525](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:521).

### 4.4 결과의 실제 범위

**관찰:** frontier/near-frontier output은 대부분의 setting에서 round-trip paraphrase보다 rare n-gram, denominal verb, inanimate subject, reduced ORC가 많았다. Chat·coding의 dependency length와 stacked noun에서도 유사 경향이 있었으나, essay에서는 dependency length가 유지되거나 번역 후 약간 증가하였고 stacked noun의 유의한 변화는 두 model에 한정되었다. [source L227–232](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:227).

**관찰:** model family와 training stage별 차이가 있었다. Olmo Think는 base/instruct보다 frontier model에 가까운 양상을 보였다. Opus 5.5는 Opus 5보다 21개 비교 중 19개에서 difficulty-linked measure가 낮았으며, 8개 비교에서는 95% interval이 겹치지 않았다. 이는 해당 corpus의 feature 비교이며 model의 종합 능력이나 실제 독해 성능 순위가 아니다. [source L253–256](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:253).

**저자 가설:** single-turn essay보다 multi-turn chat/coding에서 차이가 큰 것은 장기 대화의 압축 필요 때문일 수 있다. 그러나 setting·genre·task가 동시에 달라지므로 turn 수만의 인과 효과를 확인한 결과는 아니다. [source L232](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:232).

## 5. Experiment 2의 설계와 인과 해석

### 5.1 통제한 것

`Qwen2.5-1.5B-Instruct`가 JSON-style event를 영어 한 문장으로 바꾸도록 GRPO+LoRA로 학습하였다. 의미가 같은 짧은 형태와 긴 형태를 모두 정답으로 인정하면서 output token 수에 penalty를 부과하였다.

```text
R(x, y) = correctness(x, y) × format(y) − λ × tokens(y)
λ ∈ {0, 0.01, 0.03, 0.1}
β ∈ {0, 0.04}  # reference policy와의 KL regularization
3 seeds × 4 λ × 2 β = 24 runs
```

각 run은 500 step이며 step당 completion 128개를 사용하였다. Training alternation은 dative, object relative, complement clause와 같은 token 수인 particle control이다. correctness는 rule·dependency parse로 판정하였다. Prompt에서는 past tense를 요구하지만 reward에서는 tense를 확인하지 않았다. “정답”은 이러한 판정 기준 안의 정답이다. [source L537–555](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:537), [L608–628](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:608), [L661–689](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:661).

### 5.2 Length penalty와 표현 선택

두 문장이 correctness와 format에서 같은 reward를 받고 짧은 쪽이 Δ token을 절약하면, 이론적 최적 policy에서 short/long의 log odds에는 `λΔ/β`가 더해진다(`β > 0`). 예를 들어 `λ=0.03`, `Δ=1`, `β=0.04`라면 odds는 reference 대비 약 `exp(0.75) ≈ 2.12`배가 된다. 이는 논문 식을 대입한 설명용 계산이며 실측 효과 크기가 아니다.

요점은 reward가 의미의 정확성을 유지하더라도, 독자에게 도움이 되는 추가 표현까지 비용으로 처리할 수 있다는 것이다. `β=0`에서는 위 식을 나눗셈으로 적용할 수 없으며 reference policy에서 벗어나는 것에 대한 penalty가 없다. 이 이상화된 식과 실제 학습된 policy는 구분해야 한다. [source L589–606](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:589).

### 5.3 결과와 transfer의 범위

**실험적 근거:** length penalty가 증가할수록 여러 alternation에서 짧은 형태를 선호하였다. 특히 `β=0`일 때 두 trained `that` alternation은 모든 `λ>0` 조건에서 short 비율이 98%를 초과하였다. 이 결과를 모든 trained alternation으로 확대하면 안 된다. Dative는 figure에서 작은 `λ` 조건에 비범주적 preference를 보인다. 본문 Results의 포괄적 표현보다 Discussion의 구체적 범위와 figure를 함께 적용하는 편이 정확하다. [source L277–287](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:277), [summary_transfer_figure.pdf](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/summary_transfer_figure.pdf).

**실험적 근거:** 학습에 없었던 `sure (that)`·`so (that)`에서 near transfer가 나타났다. 다만 trained alternation의 지표는 정답으로 판정된 sampled output 중 short의 비율이고, transfer 지표는 주어진 두 문장 사이의 forced-choice probability이다. 두 값은 동일한 산출 행동을 측정하지 않는다.

**제한된 실험적 근거:** far transfer는 네 alternation 중 genitive에서만, KL penalty가 없을 때 관찰되었다. Passive와 purpose-clause에는 `λ`에 따른 변화가 없었고 quantifier는 base model부터 ceiling에 가까웠다. 따라서 전반적인 문법 압축이나 자유 답변 전체의 이해도 저하가 입증된 것은 아니다. [source L703–705](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:703).

Appendix의 open-ended prompt 40개에 대한 n-gram figure에서도 decoding 방식과 seed에 따라 변화가 달랐다. 특히 greedy 결과는 단조 경향이 분명하지 않고, words per response도 `λ`에 따라 일관되게 감소하지 않는다. 특정 문법 선택에서 확인한 효과와 자유 답변 전체의 변화는 구분해야 한다. 이 평가는 figure의 정성적 판독이며 raw data 재분석이 아니다. [ngram_figure.pdf](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/ngram_figure.pdf).

## 6. 결론을 제한하는 조건

| 조건 | 실무 판단에 미치는 영향 |
|---|---|
| Human comprehension 실험 없음 | feature 감소를 이해도·읽기 시간 개선량으로 환산할 수 없다 |
| 영어만 분석 | 한국어와 code-switching 규칙은 별도 적용 가설로 취급한다 |
| Chat topic 10개, code repo 5개 | 장르·업무·model 전반으로 확대하려면 재검증이 필요하다 |
| Simulated user 사용 | 실제 동료의 질문·오해·수정 행동과 차이가 있을 수 있다 |
| Human corpus의 genre 불일치 | AI-human 차이의 일부가 문체·목적의 차이일 수 있다 |
| Parse·external classifier 기반 feature 판정 | 자동 판정 오차가 있을 수 있다. 본 연구 corpus의 수동 검증 정확도는 제시되지 않았다 |
| Human baseline이 없는 panel 존재 | 모든 setting에서 모든 feature가 사람보다 많다고 서술하지 않는다 |
| Multiple-comparison correction 없음 | 개별 유의성 별표를 독립적인 확증처럼 합산하지 않는다 |
| Dependency 분석에서 30 word 초과 문장 제외 | 매우 긴 문장의 부담까지 포괄한 분석으로 해석하지 않는다 |
| Round-trip 의미 보존의 직접 검증 없음 | 번역을 자동 rewrite 후 최종 검증 수단으로 사용하지 않는다 |
| 단일 1.5B model·제한 task의 RL | 실제 frontier training objective에 대한 인과 결론을 보류한다 |

근거: Limitations 및 Analysis details. [source L311–314](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:311), [L495–525](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:495). Genre 차이·일반화 문제의 해석은 실무 분석이다.

특히 human baseline 범위를 확인할 필요가 있다. Chat/coding의 denominal verb와 inanimate subject는 human corpus에서 측정하지 않았으며, chat/coding n-gram은 human corpus가 reference 자체여서 human baseline line을 그리지 않았다. Abstract의 요약만으로 모든 panel에 human 비교가 있다고 이해하면 범위를 과장하게 된다. [source L503–517](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex:503).

## 7. 우리 작성 환경에 적용할 판단

### 7.1 보존할 것과 풀어 쓸 것

사용자의 `TERMINOLOGY.md` 원칙을 그대로 적용한다. `guard`, `gate`, `VPS fix`, `holdout`, `regression dilution` 등 code·paper·issue를 찾는 이름은 유지한다. 영어 문법 규칙을 한국어로 옮기는 대신 **이름 사이의 관계를 한국어 조사와 서술로 명시**한다.

예를 들어 `holdout regression dilution mitigation gate`는 정착한 하나의 이름인지, 임의로 만든 제목인지 확인해야 한다. 실제 의미가 “독립 holdout에서 label noise 영향을 다시 측정한 후 다음 단계로 진행한다”라면 그 관계를 문장으로 기재한다. 원문에 그 뜻이 없다면 `mitigation`이나 `gate`를 임의 해석해 문장을 완성하지 않는다. 불명확한 관계는 문체 문제가 아니라 내용 확인의 문제이다.

### 7.2 Precision과 readability의 동시 보존

명사 연쇄를 풀어 쓰면 문장이 길어질 수 있다. 그래도 무엇이 무엇을 조건으로 삼는지 즉시 이해할 수 있다면 유효한 변경이다. 반대로 문장을 여러 개로 분리하여도 `이것`, `해당`, `그 결과`의 지시 대상이 불명확하면 개선되지 않는다.

편집의 보존 대상은 **행위자·대상·인과의 강도·조건·부정·수치와 단위·집계 대상과 제외 대상·근거·다음 행동**이다. 특히 `가능성`을 `원인`으로, `성공 session만의 결과`를 `전체 성능`으로, `구현됨`을 `검증됨`으로 바꾸는 것은 문체 개선이 아니라 사실 변경이다.

### 7.3 사람에게 쓰는 문장과 agent에게 주는 지시

이 논문은 human comprehension과 agent instruction-following의 최적 문법이 같다는 것을 검증하지 않았다. 사람이 읽는 PR·설명에는 다음 판단에 필요한 결론과 조건을 배치한다. Agent manifest에는 행동과 완료 조건을 명시하고, 긴 근거는 별도 reference로 연결한다. 두 경우 모두 관계를 드러내지만, 사람에게 도움이 되는 모든 표현을 모든 agent 문서에 강제하지 않는다.

### 7.4 기존 skill과의 관계

| 기존 지침 | 이미 제공하는 기능 | 이 분석의 추가 판단 |
|---|---|---|
| 사용자 `TERMINOLOGY.md` | 영어 technical term과 식별자의 일관성 | 용어를 보존하고 주변 관계를 풀어 쓴다 |
| `korean-report-style` | 보고 문체·정밀도·상태 표기·구조 정합성 | 정밀한 명사구라도 관계가 숨겨졌는지 확인한다 |
| `writing-for-agents` | context pointer·progressive disclosure·완료 조건 | 압축을 이유로 완료 조건과 조건절을 제거하지 않는다 |
| Ponytail | 작은 완결 변경·짧은 전달·검증 | 짧은 문장에서도 evidence와 적용 범위를 보존한다 |

이미 같은 행동을 안정적으로 만들고 있다면 규칙을 추가할 필요가 없다. 이 분석에서 실시한 단일 baseline 확인에서는 sample 분모·실패 제외·미검증 조건이 보존되었다. 따라서 그 항목을 새 skill의 개선 성과로 주장하지 않는다. [VALIDATION.md](VALIDATION.md) 참조.

## 8. 채택한 산출물과 운영 방식

**Manifest를 정본으로 채택하였다.** User가 제공한 원문에 근거한 작성 원칙, 적용 예시, 의미 보존 기준을 한 file에 둔다. 이번 작업은 개인의 범용 작성 방식 정리이며 FAMOZ repository·공유 업무 문서를 변경하는 작업으로 수행하지 않았다.

| 형태 | 장점 | 비용과 판단 |
|---|---|---|
| 전역 instruction에 전체 분석 추가 | 항상 읽힌다 | 매번 긴 context를 소모하므로 부적합하다 |
| 별도 자동 호출 skill | 반복적인 실패가 확인되면 workflow를 재사용하기 쉽다 | 기존 writing skill과 겹치며 추가 효과는 미측정이다 |
| 짧은 pointer + 독립 manifest | 기존 instruction에 최소한의 연결만 추가할 수 있고 이식이 쉽다 | 실제 discovery와 사용 여부는 환경별로 확인해야 한다. 현재 채택한 형태이다 |

사용 방법은 [MANIFEST.md](MANIFEST.md)의 적용 절을 따른다. Manifest는 이미 작성한 결과물을 검토하거나 처음 작성할 때 모두 사용할 수 있다. Global `AGENTS.md`·`TERMINOLOGY.md`·기존 skill은 이번에 변경하지 않았다. 읽었다는 사실만으로 현재·향후 모든 session의 설정에 자동 반영되었다고 주장하지 않는다.

## 9. 후속 평가 기준

새 문체를 선호하는지 묻는 평가만으로는 부족하다. 같은 정보를 읽은 동료가 어떤 결론을 내리고 무엇을 해야 하는지 답할 수 있는지 확인해야 한다. 아래는 논문이 검증한 기준이 아니라 우리 적용 효과를 측정하기 위한 제안이다.

1. 실제 설명·PR·연구 보고 중 서로 다른 형식의 문서를 선정한다. 같은 문서에서 manifest 적용 전·후를 비교하되 수치·근거·결론을 고정한다.
2. 의미 보존을 먼저 검사한다. 수치·조건·부정·미검증 상태 중 하나라도 바뀌면 가독성 평가 이전에 실패로 판정한다.
3. 독자에게 순서를 바꾸어 제시하고, 결론·근거·적용 범위·다음 행동에 대한 질문을 한다. 이해 정확도를 우선하고 읽기 시간·재질문은 보조 지표로 기록한다.
4. 같은 model 조건에서 반복하여 편차를 확인한다. 이번 한 번의 agent 점검으로 개선율이나 인과 효과를 제시하지 않는다.
5. 압축 실패가 반복되고 manifest가 이를 개선한다는 근거가 확보되면 좁은 범위의 `unpack-technical-writing` skill로 전환한다. 그때의 trigger는 모든 답변이 아니라 명사 연쇄·생략된 관계 때문에 이해가 어려운 기술 문장의 작성과 개정으로 한정한다.

권고하는 목표는 token 최소화도 feature 수 최소화도 아니다. **같은 의미를 보존하면서 독자가 정확한 판단에 도달할 수 있도록 작성한다.**
