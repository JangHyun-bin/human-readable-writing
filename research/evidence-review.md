# arXiv:2610.29162v1 — 원문 근거 검토

검토일: 2026-10-27. 대상 원문: [acl_latex.tex](/Users/janghyunbin/Downloads/arXiv-2610.29162v1/acl_latex.tex), 778 lines. 본문, Limitations, appendix 전체와 포함된 figure PDF 10개를 확인하였다. 아래 `L`은 이 local TeX file의 line 번호이다. 외부 문헌의 결과를 재현하거나 frontier model의 실제 training history를 확인한 검토는 아니다.

## 핵심 판단

**H1은 특정 English corpus에서 측정한 linguistic feature의 분포 차이에 관한 결과이며, 독자의 실제 이해 저하를 직접 측정한 결과가 아니다. H2는 한 소형 model의 제한된 sentence-generation task에서 length penalty가 일부 syntactic preference를 바꿀 수 있다는 실험적 근거이다. 두 결과를 결합하여 frontier model의 training 원인이나 특정 instruction의 comprehension 개선 효과까지 확정할 수는 없다.** H1/H2 정의는 Introduction L103–106, 실험 범위는 Experiment 1 L199–214 및 Experiment 2 L269–275, 저자의 causal-identification 한계는 Limitations L313–314에 명시되어 있다.

실무 skill에는 **“최소 token” 대신 “의미와 관계를 분명하게 전달하는 데 필요한 길이”를 목표로 하고, 모호한 수식 관계·불명확한 주체·의미 복원을 독자에게 요구하는 압축을 점검한다**는 원칙을 반영할 수 있다. 이는 원문의 기제에서 도출한 실무 추론이다. 논문에서 해당 skill이나 prompt의 효과를 검증한 것은 아니다. 특히 “모든 noun compound 제거”, “항상 that 삽입”, “항상 active voice”, “모든 inanimate subject 금지”, “번역 왕복으로 의미 보장”은 논문의 실험 결과를 벗어난다. 근거: linguistic alternation의 context 의존성 L123–127, L272–275; feature 정의 L138–170, L194–197; round-trip 가정 L210–213; transfer 제한 L283, L703.

## 1. 주장과 증거의 수준

| 주장 | 원문 근거 | 판단 가능한 범위 |
|---|---|---|
| 일부 frontier output에는 human processing difficulty와 연관된 feature가 많다 | H1 L104; feature 문헌 L138–170, L194–195; 결과 L227–256 | **관찰.** 해당 sample과 detector 기준에서 feature의 빈도가 높다. feature마다 model·genre별 예외가 있다. |
| AI text는 같은 의미를 더 어렵게 표현한다 | round-trip 해석 L210–213 | **조건부 해석.** 번역 전후의 의미 보존을 가정한다. 이 논문에는 의미 동등성의 항목별 human 평가나 자동 semantic score가 보고되지 않는다. |
| 정보 압축 압력이 frontier style의 원인이다 | Introduction L98–101; Experiment 2 L267; Discussion L291–293 | **가설.** frontier model의 post-training을 관찰하거나 그 objective를 조작하지 않았다. 저자도 L314에서 causal identification의 proxy 사용을 인정한다. |
| length penalty에 따라 일부 grammatical preference가 변한다 | Setup L269–275; 결과 L279–287; objective L589–620 | **제한된 실험적 인과.** 같은 Qwen2.5-1.5B-Instruct, 같은 GRPO task에서 penalty를 달리한 비교이다. |
| learned preference가 새로운 construction으로 transfer한다 | L275, L283, L703 | **제한된 일반화.** 두 near-transfer that construction에서 나타났다. far transfer는 네 종류 중 genitive, 그것도 KL 없는 조건에 한정되었다. |
| model text가 실제로 human에게 더 이해하기 어렵다 | Abstract L67–71; Background L117–127 | **직접 미측정.** 실험의 outcome은 parse feature·n-gram statistics·variant probability이다. participant, reading time, recall, comprehension accuracy를 측정한 실험은 전체 실험/appendix에 없다. |
| 긴 conversation에서 압축이 누적된다 | L232 | **저자 추정.** single-turn essay와 multi-turn chat/code를 비교하였으나 turn 수나 context length를 따로 조작한 factorial experiment는 아니다. |
| 새로운 Opus variant의 communication이 개선되었다 | L255, L293 | **proxy 비교.** L255의 19/21은 difficulty-linked measure의 방향이며 독자 이해 향상률이 아니다. |

“humanlike”는 이 연구에서 대부분 **human corpus와 비슷한 feature 분포**를 뜻한다. humanlike 분포가 모든 개별 문장의 최적 표현이라는 결론이나, 기계적 human imitation이 모든 전문 문서의 목표라는 결론은 도출되지 않는다. human speakers도 context에 따라 짧은 variant와 긴 variant를 모두 사용한다는 설명이 L123–127, L273–274에 있다.

## 2. Experiment 1의 설계와 검산

### 2.1 Corpus 범위

| Setting | 설계·보고 수량 | 해석상 경계 |
|---|---|---|
| Chat | 12 models × 10 topics = **120 conversations**, 총 **1,428 turn-final replies**. 113개는 12 replies까지 진행, 7개 Olmo Think conversation은 reasoning을 포함한 output-token ceiling으로 조기 종료. L346–366 | topic당 model별 1 conversation이다. simulated user가 후속 내용을 생성하므로 첫 prompt 뒤의 content는 model별로 동일하지 않다. simulated user는 Claude Sonnet 4.6이다. L336, L352–366 |
| Coding | 9 models × 5 repositories = **45 sessions**. 11 episodes 또는 episode-final text 약 8,000 tokens에서 종료한 뒤 closing reply는 제외. L371–393 | tool 사이 commentary, tool output, 실제 diff, 최종 MEMORY.md 응답을 분석하지 않았다. 따라서 결과는 coding 성능이나 모든 agent communication의 결과가 아니다. L375, L387–393 |
| Essay | 14 models × 7 assignments × 10 essays = **980 model essays**. human comparison은 score 5–6의 US grade 6–12 학생 **2,934 essays**. L399–403 | 성인 전문가나 일반 human writing의 대표 sample이 아니다. model은 학생의 문체로 쓰라는 지시나 student essay example을 받지 않았다. L403 |

전체 model은 frontier/near-frontier 9개와 작은 open model 5개로 **14개**이다. 작은 model은 Llama 3.1 8B base/Instruct와 Olmo 3 7B base/Instruct/Think이다. 구성은 L201, L333–336; generation은 provider default와 Pi의 medium reasoning, 작은 model은 local 8-bit weights와 family별 sampling 설정이다. L335, L338–340. “모든 조건이 완전히 동일한 model ranking experiment”로 읽으면 안 된다. Olmo Think에는 지정한 system prompt가 전달되지 않은 예외도 있다. L350.

수량 검산:

- `120 × 12 = 1,440`; 실제 1,428 replies는 이 최대치보다 12개 적다. L366과 정합한다. 7개가 token limit에 먼저 도달하였다는 설명만으로 conversation별 reply 수는 복원할 수 없다.
- `14 × 7 × 10 = 980`, `9 × 7 × 10 = 630` frontier essays. Table API run 수 L446과 정합한다.
- 두 base model의 essay 140개 중 31개가 2,000-token limit에 도달하였다. **31/140 ≈ 22.14%**이다. L403. base text의 낮은 feature 빈도를 해석할 때 종료 조건과 completion 방식 차이를 고려해야 한다.
- 설계 전체의 model × setting 조합은 `12 + 9 + 14 = 35`이다. `feature_consistency_sd_roundtrip_by_setting.pdf`의 12/9/14 표기와 `feature_consistency_sd_roundtrip_by_category.pdf`의 `2 + 6 + 6 + 9 + 12 = 35` 표기는 이와 정합한다. 해당 figure 연결은 L178–190, L215–219이다.
- 반면 `feature_consistency_sd.pdf`는 왼쪽을 **33 model × setting cells**, 오른쪽 essay 비교를 **12 models**로 표기한다. `12 + 9 + 12 = 33`은 두 base essay model을 제외한 수량과 같지만, 이 exclusion 이유는 TeX 설명에 명시되어 있지 않다. **제외 이유는 미확인**으로 유지한다. 위 figure는 L185–189에서 참조한다.

### 2.2 Human baseline의 범위

Chat는 OpenSubtitles, coding은 StackExchange, essay는 PERSUADE student essay이며 Wikipedia comparison을 추가하였다. L204–206. OpenSubtitles·StackExchange·Wikipedia baseline은 각각 약 500,000 words의 random sample이다. L503.

이 대응은 저자의 표현대로 **approximately genre-matched**이다. movie subtitle conversation과 assistant response, 일반 StackExchange 글과 repository bug-sweep summary가 task·독자·전문성·형식까지 통제된 sample은 아니다. 이는 source 선정 L205와 실제 생성 절차 L346–403에 근거한 설계상 한계이다.

특히 **chat/code의 denominal verb와 inanimate-subject feature에는 human score 자체가 없다.** 또한 chat/code는 human corpus 자체가 n-gram reference이므로 human n-gram baseline line을 그리지 않았다. L504–515. 따라서 “모든 genre에서 모든 frontier model이 human보다 inanimate subject와 rare n-gram을 더 사용했다”는 표현은 이 실험에서 직접 확인한 비교 범위보다 넓다. Abstract L68의 비교를 상세히 인용할 때에는 essay의 human 비교와 round-trip 비교를 구분해야 한다.

### 2.3 Feature별 의미와 측정 한계

| Feature | 측정 정의·원문 | 실무 적용 시 주의 |
|---|---|---|
| Low-frequency n-grams | reference에 없는 bigram 비율, reference trigram model perplexity. L138–141, L503–504 | corpus 비등재는 부자연스러움·오류·이해 불가능과 같지 않다. 전문 표현, 새 사실, 적절한 새 조합도 rare할 수 있다. 예시는 `early perceptual`, `home outweigh`, `rigid worksheets`까지 포함한다. L483–485 |
| Dependency length | dependency arc 길이. sentence length를 5개 bin으로 구분하여 Wikipedia arc 비중으로 standardize한다. **30 words 초과 문장은 제외**한다. L506–510 | 문장을 짧게 쓰라는 hard cap의 근거가 아니다. 가장 긴 문장은 이 measure에서 제외되므로 전체 긴 문장의 실제 이해 난이도를 측정한 것도 아니다. clause·목록·의미 단위의 배치 검토에 활용한다. |
| Object relative clauses | overt relativizer가 있는 ORC와 없는 ORC를 따로 측정한다. L147–150 | 모든 ORC, 모든 that 생략이 나쁘다는 결과가 아니다. animacy·frequency·context에 따라 비용이 달라진다는 원문 조건을 보존한다. L149, L273–274 |
| Stacked nouns | modifier 관계로 연결된 **3개 이상의 noun** 빈도. L161–165 | ambiguity를 점검할 신호이다. “세 명사 이상 무조건 금지”는 grammar 규칙이나 실험적으로 최적화한 threshold가 아니다. 실제 용어·identifier의 의미와 검색 가능성을 보존한다. |
| Denominal verbs | noun에서 유래한 verb; parser 후보를 classifier로 판정한다. L167–170, L498 | conventionalized verb와 ad-hoc innovation을 분리해야 한다. 원문도 `bottle`처럼 일반적인 용례를 인정한다. coding의 `staging`, `masking` 같은 표현까지 예시에 포함한다. L475 |
| Inanimate subject + animate verb | 보통 animate subject를 요구하는 active verb에 inanimate subject가 결합한 사례. L194–197 | 모든 inanimate subject, 기술 분야의 모든 관습적 표현이 대상인 것은 아니다. 저자는 context 없는 mismatch의 processing cost를 언급한다. 전문 관습과 독자 familiarity를 고려해야 한다. |

모든 syntactic feature는 spaCy `en_core_web_trf` parse를 사용한다. denominal/inanimate 후보는 external classifier Jev 1.13.0이 probability >0.5로 판정한 것만 센다. L498. **이 corpus에서의 parser accuracy, classifier precision/recall, annotator agreement, threshold sensitivity는 보고하지 않는다.** 따라서 측정 오차와 domain별 오차 차이는 미확인이다. “detector가 잡은 문장 = 이해를 해치는 문장”이라는 instruction으로 전환하면 안 된다.

### 2.4 통계와 ranking 해석

주요 figure의 pooled 값과 95% bootstrap interval은 chat 10 conversations, coding 5 sessions, essay 70개를 대상으로 하며 conversation 전체 또는 prompt 안의 essay를 resample한다. L515. 문장 수가 많더라도 coding의 독립 session 수는 model당 5개이다. 범위를 넓힌 model ranking이나 모든 업무로의 일반화에는 추가 sample이 필요하다. limited seed와 model family 한계는 L313에도 있다.

Round-trip 별표는 paired jackknife two-sided t-test이며 **multiple-comparison adjustment를 하지 않았다.** L517. 개별 `p<.05`를 확정적 model 성능 차이로 전환하지 않는다. source의 SD normalization은 독자 이해도의 SD가 아니라 **model별 원래 feature 값의 SD**이다. summary change bar는 이 SD를 absolute difference의 분모로 사용한 뒤 feature pair 및 setting별로 평균한 값이다. L519. 따라서 “2 SD 더 이해하기 어렵다”는 표현은 오독이다.

Opus 5.5가 Opus 5보다 낮은 difficulty-linked measure가 21개 중 19개, 그중 8개는 95% interval이 겹치지 않았다는 수치는 L255의 보고값이다. **19/21 ≈ 90.48%**, **8/21 ≈ 38.10%**이지만 이 비율은 readability 향상률이 아니다. source의 eight-feature figure와 21개 comparison의 관계는 ORC with relativizer를 제외한 7개 feature × 3 settings로 해석할 수 있으나, 본문에서 그 denominator 산식을 명시하지는 않는다. 원수치가 없는 상태에서 나머지 두 비교나 정확한 effect size를 역산하지 않는다.

## 3. Round-trip translation의 해석 한계

저자는 English→Japanese→English NLLB-200 3.3B paraphrase를 sentence별로 생성하고, “같은 의미에서 다른 wording” 비교로 해석한다. L210–213. 번역이 frequent form으로 normalize하고 lexical/syntactic richness를 줄인다는 점도 원문 자체가 L210에서 설명한다. 따라서 feature 감소는 **더 일반적인 대체 표현을 생성할 수 있다는 근거**이지만, 그 대체 표현의 의미·문체·정보 구조가 동등하고 독자에게 더 유익하다는 검증과는 다르다.

확인한 한계와 대응은 다음과 같다.

1. **의미 보존 검증 미보고.** TeX의 round-trip procedure L208–213, L521–525, word-count caption L774에는 human semantic equivalence rating, factual consistency score, entailment, round-trip failure rate가 없다. 실무 skill은 번역 결과를 최종 정답으로 채택하지 않고, actor/action/object, negation, 조건·예외, 수치·단위, uncertainty, 인용·identifier가 보존되었는지 직접 검토해야 한다. 이 보존 목록은 실무 설계 제안이며 논문에서 시험한 목록은 아니다.
2. **Sentence별 번역의 discourse 제한.** L212, L525에 따라 문장을 독립적으로 번역한다. 앞 문장의 referent, list의 논리 관계, code context를 이용하는 대명사·생략은 sentence 내부만으로 복원되지 않을 수 있다. 이는 절차에서 도출되는 가능성이고, 논문이 해당 손실을 실측한 결과는 아니다.
3. **길이와 segmentation 변화.** 번역 결과가 여러 문장으로 분리되는 비율은 NLLB Japanese 2.4%, NLLB Russian 0.8%, TranslateGemma Japanese 14.1%, TranslateGemma Russian 3.0%이다. L525. sentence 단위 feature의 denominator와 dependency profile이 함께 달라질 수 있다. `14.1/2.4 ≈ 5.88`은 translator/pivot 조건별 split rate의 비율이며 품질의 배율이 아니다.
4. **Word-count filter와 별도의 semantic filter 부재.** word-count figure에서는 round trip이 원문 길이의 절반 미만 또는 두 배 초과인 line을 양쪽에서 제외한다. L774. 길이 ratio 안에 있다는 사실만으로 의미가 보존되지는 않는다. 이 filter를 main feature analysis 전부에 사용하였다고 source가 명시하지 않으므로 범위를 확장해 서술하지 않는다.
5. **대체 pivot/translator의 검증 범위.** Japanese/Russian × NLLB/TranslateGemma 4B를 9개 frontier model에 적용한 check는 L525와 `roundtrip_words_per_response.pdf`에 있다. appendix에 제시한 outcome은 word count이다. 이 자료만으로 모든 linguistic feature의 효과가 pivot·translator에 robust하다고 주장할 수 없다.
6. **원래부터 단순해지는 intervention.** 저자가 번역의 normalization을 L210에서 인정하므로 n-gram rarity 감소 일부는 선택한 translation process의 예상 속성이기도 하다. 감소 자체가 원문이 불필요하게 어렵다는 독립적 판정이나 density training의 유일 원인을 제공하지는 않는다.
7. **Genre별 반대 방향.** essay dependency length는 변화가 없거나 round trip 뒤 오히려 길어진다. stacked nouns는 essay에서 두 model만 유의하게 바뀐다. L230. `roundtrip_combined_nllb_jpn_compact.pdf`도 이 방향 차이를 표시한다. 일괄적인 “번역하면 모든 difficulty feature 감소” 규칙은 지원하지 않는다.

`roundtrip_words_per_response.pdf`를 직접 보면 TranslateGemma 두 pivot에서는 거의 모든 model/setting에서 번역 뒤 word count가 증가하고, NLLB Japanese에서는 더 혼합된 결과이다. 이 시각적 경향의 근거는 figure 연결 L773–775이다. 정확한 막대값을 raw table 없이 새 수치로 인용하지 않는다. **“더 이해하기 쉬운 표현은 언제나 더 짧다”와 “더 쉬운 표현은 언제나 더 길다”는 보편 법칙을 이 결과에서 도출할 수 없다.**

## 4. Experiment 2의 개입과 결과

### 4.1 실제 조작과 reward

Base는 Qwen2.5-1.5B-Instruct이며 JSON-style event를 한 English sentence로 표현한다. LoRA와 GRPO를 사용하고, `λ ∈ {0,.01,.03,.1}`, `β ∈ {0,.04}`, seeds 3개를 조합한 **24 runs**이다. L269–275, L667–689. 이는 frontier pretraining을 재현한 실험이 아니며 `Instruct` model을 reference로 추가 post-training한 실험이다.

Reward는 `R(x,y) = c(x,y) f(y) − λ |y|`이다. correctness `c`와 format `f`는 binary이며 output token마다 penalty를 차감한다. L608–620. correctness는 event의 argument phrase가 대소문자를 제외하고 원문 그대로 포함되는지, spaCy parse에서 role에 맞는지, event verb lemma가 같은지를 검사한다. 양쪽 alternation과 일부 다른 paraphrase를 허용한다. prompt는 past tense를 요구하지만 **tense는 correctness에서 검사하지 않는다.** L569–573, L615–620.

따라서 실험의 “correct”는 이 task의 rule-based validator 통과이다. unrestricted factual equivalence나 모든 natural-language meaning의 보장을 뜻하지 않는다. 잘못된 짧은 answer로 reward를 얻었는지에 대한 우려는 가능한 reward-design issue이지만, 이 원문만으로 실제 reward hacking이 발생하였다고 단정하지 않는다.

각 run은 500 steps × 8 prompts = **4,000 prompt presentations**, distinct prompts는 3,750개이다. step당 16 completions/prompt이므로 `8 × 16 = 128`, run당 `500 × 128 = 64,000 sampled completions`, 전체 24 runs에서 **1,536,000 completions**이다. L626–628, L672–689. 이 수량은 산술상 sampling budget이며 저장된 raw record를 독립적으로 센 값은 아니다.

Training alternation은 dative, object relative, complement clause, particle control이다. 앞의 세 alternation은 표의 예시에서 short가 1 token 짧고, particle 두 variant는 token 수가 같다. holdout은 passive, genitive, all (of), (in order) to, so (that), adjective + that이다. L539–555. passive holdout 150개는 Δ2가 132개, Δ3가 15개, Δ1이 3개로 합계 150개이며 평균 token 차이는 `(132×2+15×3+3×1)/150 = 2.08`이다. L555.

`β=.04`에서 task reward가 같은 두 variant의 theoretical optimum odds에는 `exp(λΔ/β)`가 곱해진다. L589–606. Δ1이면 λ=.01/.03/.1에서 약 **1.284 / 2.117 / 12.182배**이다. 이는 objective의 이상적 optimum에 관한 관계이며 finite LoRA training의 관측 odds나 comprehension effect size가 아니다. `β=0`에는 이 Gibbs 식을 대입하지 않는다. 원문의 “this optimum doesn't exist” L605–606은 적어도 **해당 regularized optimum 식이 정의되지 않는다**는 범위로 이해하는 편이 정확하다. 유한 completion 집합의 무정규화 reward 최대화 문제 자체에 optimum이 없다는 일반 명제로 확대할 필요는 없다.

### 4.2 Trained preference의 정확한 범위

본문 L282에는 `any λ>0`에서 모든 seed가 categorical short preference로 수렴한다는 넓은 표현이 있으나, L287은 **KL 없는 두 trained that alternation에서 λ>0마다 >98% short**라고 범위를 한정한다. `summary_transfer_figure.pdf`의 dative panel은 낮은 λ에서 비범주적 값을 보인다. 그러므로 결과의 안전한 서술은 다음과 같다.

- **Object relative·complement that**: KL 없는 조건에서는 λ>0에서 거의 범주적으로 생략한다. KL이 있으면 증가가 더 완만하다. 수치 >98%의 근거는 L287이다.
- **Dative**: length penalty 증가에 따른 short preference 증가는 figure에서 관찰되지만 모든 양의 penalty에서 near-categorical인 것은 아니다. `summary_transfer_figure.pdf`, 연결 L260–262.
- **Particle control**: 두 ordering의 token 수가 같으며 큰 λ-specific short preference 변화의 근거로 사용할 수 없다. L543 및 같은 figure의 control panel.
- **λ=0, β=0**: trained that preference가 seed에 따라 0–100%로 달라졌다는 L282의 결과는 KL 없는 training 자체의 불안정성과 추가 training effect를 보여준다. “penalty만이 모든 observed drift의 원인”이라는 해석을 피한다.

훈련된 alternation의 결과는 **correct sampled outputs 중 short share**이다. L703. 전체 generation의 correctness rate를 같은 그림에서 보여주는 것이 아니다. L287의 task success 설명을 “모든 조건의 accuracy가 같았다”는 수치적 결론으로 바꾸면 안 된다. 세 seed의 mean과 faint individual seed가 figure에 있으며 confidence interval이나 seed 수가 큰 replication은 아니다. L261, L683.

### 4.3 Transfer와 open-ended response

Near transfer는 training에 없던 `sure (that)`와 `so (that)` 두 construction이다. far transfer는 genitive, quantifier, passive, purpose clause 네 종류이다. L275, L545–555. **trained test와 transfer test의 outcome을 구분해야 한다.** trained는 sampled output 비율이고, near/far transfer는 두 후보 문장의 model probability를 비교하는 **forced choice**이다. L261, L703. unrestricted writing에서 같은 빈도로 그 construction을 산출하였다는 결과가 아니다.

Far transfer는 **genitive에서만, KL이 없을 때만** 나타났다. passive와 purpose-clause는 λ에 따라 shift하지 않았고 quantifier는 base부터 ceiling에 가까웠다. L283, L703. “정보 압축 선호가 모든 문법으로 일반화된다”는 주장은 반증되거나 적어도 이 실험에서 뒷받침되지 않는다. near transfer도 KL 조건에서 λ 전체의 깔끔한 단조 증가나 human comprehension 저하를 보여준다는 뜻은 아니다.

추가로 base와 24 fine-tuned models가 task와 무관한 40 prompts에 답하였다. L705, L765–767. `ngram_figure.pdf`는 greedy 1 response/prompt와 T=1에서 5 responses/prompt를 구분한다. 시각적으로 sampled·β=0 조건에서 λ가 증가할수록 trigram surprisal·unattested trigram rate가 증가하는 경향은 있으나 greedy 결과는 비단조이고, words per response도 λ에 따라 단조 감소하지 않는다. 이 figure에는 human outcome이나 의미 정확도 평가가 없다. **국소 sentence task의 compression training 때문에 일반 대화 전체가 더 짧고 더 이해하기 어려워진다고 확정할 근거는 아니다.**

### 4.4 Causal generalization의 범위

조작한 것은 output-token penalty이고, 비교한 것은 한 model의 특정 generation task에서의 preference이다. 실제 frontier model의 RLVR reward에 이 penalty가 적용되었는지, context-window 제약이 이 style을 만들었는지, math/code 능력 향상이 comprehension 비용을 유발하는지는 직접 시험하지 않았다. Discussion L292는 RLHF의 verbosity 선호에 관한 기존 연구와 대비하여 RLVR 쪽 원인이 더 그럴듯하다고 추정하지만, 그 구분 자체를 여기서 실험적으로 조작하지 않았다. 저자의 proof-of-concept 표현 L286과 proxy 한계 L314를 유지해야 한다.

또한 “information density”라는 넓은 기제를 시험하기 위해 token count를 조작하였지만, 자연어의 semantic information per word나 human 정보처리 capacity를 직접 측정한 실험은 아니다. 원문의 length objective L608–614와 결과 measure L703–705의 범위에 따른 구분이다.

## 5. Skill·manifest 반영 범위

아래는 원문에서 **도출한 실무 제안**이다. 논문에 해당 instruction의 A/B test나 human 검증은 없다. 각 항목의 근거는 feature 정의·context-dependent alternation·실험 범위에 한정한다.

| 반영 가능한 원칙 | 실제 instruction의 최소 범위 | 원문 근거와 검증 경계 |
|---|---|---|
| 목적을 communication success로 설정 | 독자가 이해하거나 결정하거나 실행하는 데 필요한 관계·조건을 명시한다. token 수 감소만을 최종 목표로 삼지 않는다. | L94–101, L123–127, L286–293. skill 효과는 별도 미검증. |
| 압축된 수식 관계 점검 | stacked noun에서 수식 대상이 둘 이상으로 읽히면 관계를 풀어 쓴다. 확립된 용어·code identifier는 보존한다. | ambiguity 근거 L161–165. 3-noun hard ban의 검증은 없음. |
| 주체·행위·대상 명료화 | unfamiliar metaphor나 생략으로 누가 무엇을 하는지 복원하기 어려우면 구체적인 관계를 명시한다. | inanimate mismatch L194–197. 모든 inanimate subject 금지의 근거는 없음. |
| 선택적 function word 보존 | English에서 that 등의 단어가 clause 경계나 해석을 명확하게 하면 유지한다. 짧게 만들 목적으로 일괄 삭제하지 않는다. | context dependence L273–275, categorical omission L287. 일괄 삽입의 우월성은 미검증. |
| Dependency의 국소성 점검 | 주어와 핵심 동사 사이의 삽입 설명을 줄이거나 별도 문장으로 분리하되 인과·예외·scope를 유지한다. | L143–145, L506–510. 임의 sentence-length limit은 연구 결과가 아님. |
| 의미 보존 우선 검토 | rewrite 후 수치·부정·조건·예외·불확실성·actor/action/object·인용·identifier를 대조한다. | round-trip 가정 L211과 validator 범위 L615–620에서 도출한 engineering safeguard. 이 checklist는 저자의 실험 산출물이 아님. |
| 독자와 task 기준 | 전문 용어는 유지하고 필요할 때 관계나 의미를 짧게 설명한다. familiarity가 있는 표현을 낮은 빈도만으로 제거하지 않는다. | n-gram proxy L138–141; conventional denominals L167–168; limited genre L313. |
| 비용이 작은 적용 | 사용자에게 보낼 설명에서 필요할 때 한 번 검토한다. raw log·정확한 인용·code·schema·machine-consumed payload의 의도적 문법은 훼손하지 않는다. | 분석 대상이 prose와 turn-final reply에 한정됨 L393, L408–416. 적용 방법은 실무 선택. |

Manifest에는 최소한 **적용 대상**, **의미 보존 우선순위**, **수행 절차**, **검증 상태**, **English-specific 근거의 한계**를 명시하는 편이 적절하다. 논문을 근거로 새 external translator, parser, classifier, dependency를 필수로 도입할 이유는 없다. 원문의 detector는 연구 측정을 위한 도구이지, 효과가 검증된 production editing pipeline이 아니다. L136, L498, L521–525.

Korean/code-switching writing에서는 English의 relative-clause alternation을 형태 그대로 적용하지 않는다. 이 논문은 **English만 분석**하였고 Korean reader comprehension을 측정하지 않았다. L313. 한국어의 조사·어순·생략에서 주체·수식 범위를 명확히 한다는 전이는 실무 가설로 두며, English에서 유래한 기술 용어나 code identifier를 번역·음차하여 희귀어 비율을 낮추는 방식은 사용자 terminology 약속과 맞지 않는다.

## 6. 반영 제외 및 별도 검증 항목

다음 주장은 최종 skill의 논문 근거 설명에 포함하면 안 된다.

- **“이 skill로 comprehension이 입증되어 개선된다.”** 논문이 comprehension을 직접 측정하지 않았다. H1과 실험 outcome의 범위는 L104, L135–145, L498–517; RL outcome은 L703–705.
- **“AI의 난해한 문체는 RLVR/length penalty 때문이다.”** frontier causal chain은 가설과 circumstantial evidence에 한정된다. L267, L291–293, L314.
- **“모든 model이 모든 feature를 과용한다.”** model·genre·feature별 예외와 반대 방향이 있다. L228–230, L253–256.
- **“모든 압축·metaphor·noun compound가 해롭다.”** 측정은 aggregate이고, 익숙한 denominal verb·context-dependent alternation을 원문도 인정한다. L149, L167–168, L273–274.
- **“Round-trip paraphrase는 의미를 보장한다.”** 절차의 가정과 의미 보존의 직접 검증을 구분해야 한다. L210–213, L525, L774.
- **“사람처럼 쓰려면 언제나 길게 써야 한다.”** UID는 균일한 정보 분산과 맥락적 선택에 관한 설명이고, 단순한 최대 길이 선호가 아니다. L123–127.
- **“short preference는 모든 construction에 categorical하게 transfer한다.”** 정확한 categorical 결과는 두 trained that alternation과 KL 없는 조건에 한정된다. L287; far transfer 한계는 L283, L703.
- **“English-specific grammar rule은 모든 언어의 공통 가독성 규칙이다.”** English-only limitation은 L313에 명시되어 있다.

실무 validation은 **표현 명료화와 정보 보존을 따로 확인**해야 한다. 최소 예시는 모호한 noun stack, 긴 삽입절, 불분명한 metaphor, optional function word가 필요한 문장, 그리고 확립된 기술 용어·identifier를 그대로 유지해야 하는 반례이다. 이러한 example 검사는 skill의 동작 확인이며 human comprehension 실험의 대체가 아니다. 실제 이해 개선을 주장하려면 대상 독자의 이해 질문 정확도·수행 오류·읽는 시간 등을 별도로 측정해야 한다. 이는 후속 검증 제안이며 논문이 제시한 실측 결과는 아니다.

## 7. 부차 수치 검산과 미확인 범위

API cost table의 row 합계는 chat **$25.40**, code **$173.37**, essay **$11.08**, 합계 **$209.85**로 일치한다. L435–445. 여기에 local model의 simulated user **$1.92**를 더하면 **$211.77**인데, prose는 dataset cost를 **$211.78**로 보고한다. L423. **$0.01 차이**는 개별 cost 반올림으로 설명될 수 있으나 원세부 비용을 확인하지 않아 확정할 수 없다. prose 기준 `$211.78 + $29.61 + $9.80 = $251.19`는 정확히 일치한다. 논문의 주요 결론에 영향을 주는 차이로 볼 근거는 없다.

RL 비용은 run당 73–83분 × 24이므로 **29.2–33.2 GPU-hours** 범위이고 약 **31 GPU-hours** 보고와 정합한다. L694–697. training step당 7.7–8.6초 × 500은 약 64.2–71.7분이며, run 전체 시간에 base/checkpoint evaluation이 포함된다는 설명도 수치상 정합한다. L695–697.

검토에서 미확인인 범위는 다음과 같다.

- Raw corpus, feature extractor code, classifier outputs, bootstrap draws, training checkpoints는 제공된 TeX/figure 안에 없으므로 재분석하지 않았다. 보고 수량·산식과 figure의 방향만 대조하였다.
- Figure의 plotted exact coordinate를 raw numerical effect size로 변환하지 않았다. 눈으로 읽은 경향과 본문에 명시된 수치를 구분하였다.
- 인용된 psycholinguistics 논문의 개별 result와 classifier vendor의 accuracy는 별도 원문 검증하지 않았다. 본 검토의 확정 근거는 제공된 논문의 주장·설계·보고 결과이다.
- Local archive와 공식 arXiv version의 byte-level 일치나 공식 publication 상태는 이 독립 검토에서 확인하지 않았다.

EOD
