# Human-readable writing 관련 문헌

확인일: 2026-10-28. Primary source의 Methods·Results를 확인한 결과와, 우리 writing 지침으로 옮길 때의 판단을 구분한다.

기준 논문은 Clark, Martin & Mahowald의 [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1)이다. 아래 7편은 직접 연결되는 LLM 문체 연구와, 실제 독해·평가 방법을 보완하는 연구를 함께 선정한 목록이다. Systematic review나 모든 관련 논문의 목록은 아니다. 원문·figure·dataset을 복제하지 않고 출처와 연구 결과를 요약하였다.

## 실제 독자의 comprehension·recall을 측정한 연구

### Martínez, Mollica & Gibson (2022), *Poor writing, not specialized concepts, drives processing difficulty in legal language*

Cognition 224, 105070. [Publisher PDF — University of Edinburgh](https://www.pure.ed.ac.uk/ws/files/256304933/Poor_Writing_MARTINEZ_DOA17022022_VOR_CC_BY_NC_ND.pdf) · [DOI](https://doi.org/10.1016/j.cognition.2022.105070)

- **확인 범위:** 본문 Methods·Results·Discussion을 읽었다. Supplementary information과 raw data는 별도 확인하지 않았다.
- **실험:** 약 150-word 계약 발췌문 12쌍. Main experiment 완료자 n=108은 각자 legalese 3개와 simple 3개를 읽었다. Simple 조건은 의미를 유지하며 center-embedded clause를 별도 문장으로 풀고, word frequency·voice·capitalization도 함께 바꿨다.
- **측정 결과:** Comprehension accuracy는 simple 73.5%, legalese 67.7%; proposition recall은 42.4%, 35.3%였다. 문서를 보면서 답하고 monetary incentive를 받는 replication에서도 simple 조건의 comprehension 이점이 유지됐다. [§3.1–3.3](https://www.pure.ed.ac.uk/ws/files/256304933/Poor_Writing_MARTINEZ_DOA17022022_VOR_CC_BY_NC_ND.pdf)
- **해석의 한계:** Center-embedding이 recall에 가장 크게 관련된다는 결과는 proposition별 exploratory 분석이다. 저자는 개별 feature의 일반화 가능성을 검증할 power가 부족하다고 명시했다. 위 5.8 percentage-point comprehension 차이를 문장 분리만의 효과로 해석하면 안 된다. Main sample은 첫 절반의 comprehension이 chance를 넘긴 완료자만 포함했다. [§3.1.2·3.2.3](https://www.pure.ed.ac.uk/ws/files/256304933/Poor_Writing_MARTINEZ_DOA17022022_VOR_CC_BY_NC_ND.pdf)
- **우리 판단:** 긴 삽입 설명을 풀어 관계를 드러내는 지침을 지지한다. 모든 문장을 짧게 만들거나 모든 passive를 없애라는 규칙까지 뒷받침하지는 않는다.

### Martínez, Mollica & Gibson (2023), *Even lawyers do not like legalese*

PNAS 120(23), e2302672120. [Full text — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10266064/) · [DOI](https://doi.org/10.1073/pnas.2302672120)

- **확인 범위:** 본문 Methods·Results·Discussion을 읽었다. Supplementary information과 raw data는 별도 확인하지 않았다.
- **실험:** Preregistered Experiment 1의 미국 변호사 n=105가 2022 연구와 같은 materials·procedure로 recall·comprehension 과제를 수행했다. 비교한 일반 독자 n=108은 2022 data의 재분석이므로 새로운 일반 독자 replication으로 세면 안 된다.
- **측정 결과:** 변호사도 simple 조건에서 recall·comprehension이 더 좋았다. Register×legal training interaction은 유의하지 않았다. 별도 Experiment 2(n=102)에서는 simple 계약의 quality 등을 더 높게 평가했고, enforceability rating의 차이는 유의하지 않았다. 이는 실제 법적 효력이 같다는 실증은 아니다. [Results·Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC10266064/)
- **우리 판단과 한계:** 독자가 expert라는 이유만으로 복잡한 syntax를 유지할 근거는 약하다. 다만 미국 계약 발췌문과 hypothetical rating 과제이며, 모든 전문 용어가 불필요하다거나 모든 전문 문서에 같은 효과가 난다는 뜻은 아니다. 다른 국가로의 일반화가 불확실하다는 점도 저자가 명시했다. [Constraints on Generality](https://pmc.ncbi.nlm.nih.gov/articles/PMC10266064/)

두 연구 모두 English 법률 문서 실험이다. Korean–English code-switching writing으로의 전이는 **우리 가설**이며, 한국어 문장의 효과 크기나 최적 길이를 측정한 근거로 쓰지 않는다.

### Guidroz et al. (2025), *LLM-based Text Simplification and its Effect on User Comprehension and Cognitive Load*

[arXiv:2505.01980v1](https://arxiv.org/abs/2505.01980v1) · [원문 PDF](https://arxiv.org/pdf/2505.01980). 확인 범위: Methods·Results·Discussion, pp. 2–8. Google Research 소개에는 제목에 “Lossless”가 추가되어 있지만, 여기서는 확인한 논문 제목을 사용한다.

Gemini 기반으로 readability와 정보 보존을 함께 평가하며 prompt를 개선하였다. 6개 분야의 31개 발췌문을 사용한 randomized study에서 4,563명이 참여했다. 문서를 보며 답한 조건의 MCQ accuracy는 원문 44.3%에서 단순화 문장 48.2%로 높아졌다(+3.9 percentage points, 95% CI 1.6–6.3). [Methods·Results](https://arxiv.org/pdf/2505.01980)

**우리 판단:** 표현을 쉽게 만드는 것과 사실 보존을 별도로 검사하고, 실제 독자의 답변으로 확인하는 평가 설계를 참고할 수 있다. 효과는 단일 61-token 지침이나 줄바꿈의 효과가 아니다. 저자도 정보 왜곡 가능성·MCQ가 포착하는 이해 깊이의 한계를 인정한다. 개발 시 여러 model과 반복 refinement를 사용했으므로 그 절차를 매 응답마다 실행하는 방식은 우리의 비용 목표와 별도 판단해야 한다. [Discussion](https://arxiv.org/pdf/2505.01980)

### Guo et al. (2025), *Are LLM-generated plain language summaries truly understandable? A large-scale crowdsourced evaluation*

[arXiv:2505.10409v1 본문](https://arxiv.org/html/2505.10409v1). 확인 범위: §2 Results·§3 Discussion·§4 Method. 이 note의 근거는 2025 preprint이며, 검색에서 확인한 2026 journal version과의 변경 대조는 하지 않았다.

50개 biomedical abstract를 GPT-4로 6가지 방식의 plain language summary로 작성하고 human summary와 비교했다. 참여자는 150명이며 complete annotation은 1,346개, 추가 quality control을 통과한 subset은 459개다. 주관적 평가는 대부분 유의한 차이가 없었지만 human summary의 MCQ accuracy가 더 높았다. Recall 차이는 유의하지 않았다. [§2.3–2.4](https://arxiv.org/html/2505.10409v1#S2.SS3)

**우리 판단:** 사용자의 B 선호는 개인 스타일 선택의 근거로 보존하고, 사실 이해를 평가할 때는 적용 범위·미검증 상태를 묻는 질문을 따로 둔다. 이 연구가 사용자의 선호를 무효화하거나 A가 더 정확히 이해된다고 증명하는 것은 아니다. 어떤 문장 요소가 이해도 차이를 만들었는지는 저자도 미확인으로 남겼다. [§3](https://arxiv.org/html/2505.10409v1#S3)

## LLM 문체와 training objective를 다룬 연구

### Reinhart et al. (2025), *Do LLMs write like humans? Variation in grammatical and rhetorical styles*

PNAS 122, e2422455122. [arXiv 본문 v2](https://arxiv.org/html/2410.16107v2) · [DOI](https://doi.org/10.1073/pnas.2422455122). 확인 범위: Methods·Results·Discussion.

Llama 3 계열과 GPT-4o 계열의 output을 대응하는 human text와 비교하였다. Instruction-tuned model은 nominalization·participial clause 등에서 특정 문체를 선호했고, genre에 따른 human variation을 충분히 재현하지 못했다. 분석한 model들에서는 base보다 instruction-tuned model의 차이가 더 컸다. [Results](https://arxiv.org/html/2410.16107v2)

**우리 판단:** 기준 논문과 가장 직접적으로 연결되는 선행 연구다. 단어 금지 목록만으로는 충분하지 않고 명사 사이의 관계와 문서 목적을 살펴야 한다는 판단을 보강한다. 문체 차이를 관찰한 연구이며, 사람의 comprehension 저하나 특정 training objective의 인과 효과를 직접 입증하지는 않는다.

### Li & Xu (2026), *Uniform Information Density-Based Preference Optimization*

[arXiv:2610.14578v1 본문](https://arxiv.org/html/2610.14578v1), 2026-10-10 preprint. 확인 범위: §2 objective·§3 setup·§4 results.

정보량 분포를 preference optimization에 도입한다. 전체 문장의 density를 동일하게 만들기보다 global 변동은 허용·장려하면서 local 변화의 급격함을 줄이는 objective다. Llama-3-8B-Instruct와 Mistral-7B-Instruct를 사용했으며, SimPO 대비 benchmark 결과는 일부 우위·일부 열위였다. [§2.2·§4.1](https://arxiv.org/html/2610.14578v1)

**우리 판단:** 단순한 token 최소화와 독자가 처리할 정보의 배치를 구분하는 데 유용한 연구 방향이다. 문장마다 같은 길이나 줄바꿈을 강제하는 근거는 아니다. 평가가 LLM judge 기반이므로 human comprehension 개선으로 해석하지 않는다. Training algorithm의 결과를 짧은 writing prompt의 효과로 옮길 수도 없다. [§3 Table 1](https://arxiv.org/html/2610.14578v1#S3)

## Agent 평가를 보완하는 연구

### Dubois et al. (2024), *Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators*

COLM 2024. [arXiv 본문 v2](https://arxiv.org/html/2404.04475v2), 2025-03-10 개정. 확인 범위: 방법·§4 results·§5 limitations.

LLM evaluator의 긴 답변 선호를 regression으로 조정하였다. Chatbot Arena와의 model 순위 Spearman correlation은 0.94에서 0.98로 높아졌고, verbosity 지시로 평가를 조작하는 데 대한 민감도도 줄었다. Correlation 차이의 bootstrap p-value는 기존 AlpacaEval 대비 0.07이므로 일반적인 0.05 기준의 유의한 개선으로 표현하지 않는다. [§4.1–4.2](https://arxiv.org/html/2404.04475v2)

**우리 판단:** Agent 선호를 사용자 개인의 판단과 분리하고 답변 길이도 함께 기록할 근거다. 우리 4:2 선호 차이가 length bias 때문이라고 밝혀진 것은 아니다. Input 지침이 같은 61 tokens라는 사실도 output 길이가 같다는 뜻은 아니다. 이 연구의 집계 benchmark 보정을 일곱 답변 쌍에 그대로 fitting하지 않는다.

## 우리 작업에서의 활용 순서

1. **작성·의미 보존:** Guidroz의 평가 설계와 Martínez의 syntax 연구를 먼저 읽는다. 관계를 드러내되 수치·조건·부정·불확실성을 보존하는 현재 원칙을 점검한다.
2. **평가:** Guo와 Dubois를 참고하여 개인 선호, 실제 이해, agent 평가를 각각 기록한다. B 선택은 개인 선호의 기준으로 유지한다.
3. **배경·후속 연구:** Reinhart는 LLM 문체 차이의 근거로, UIDPO는 training objective의 연구 방향으로 사용한다.

이 활용 순서는 위 연구들을 우리 비용·작성 목표에 연결한 판단이다. 이번 조사에서 새 benchmark를 실행하거나 core·manifest·전역 설정을 변경하지 않았다. Korean–English code-switching에서 각 원칙의 효과와 개인 선호의 반복성은 별도 검증 대상이다.
