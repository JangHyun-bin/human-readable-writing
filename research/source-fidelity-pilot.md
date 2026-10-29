# 원문 의미 보존 보완안 — 4회 확인

2026-10-29 사용자가 승인한 다음 단계다. [이전 12회 결과](layout-generation-pilot.md)에서 N2 두 arm은 source에 없는 검증 상태를 추가했고, E2의 formal_layout은 불확실성의 대상을 다르게 읽힐 수 있게 표현했다. 문장별 문단 분리는 유지하며 이 실패를 확인하는 4회 비교를 준비했다.

## 고정한 변경

Current는 이전 `formal_layout`의 전체 문구다. 전역 실사용 pilot에 설치한 original CORE와는 다르다. Revised는 아래 두 문장으로 의미 보존 부분만 교체한다.

> 원문의 주체·동작·조건·이유를 보존하고 제시된 검증·한계만 쓴다. 수치·단위·범위·부정과 불확실성의 대상·강도를 보존하고 관찰·가설·인과를 구분한다.

두 arm 모두 다음 문구를 그대로 붙인다.

> Formal한 문체와 technical term을 유지한다. 짧은 기술 설명은 문장마다 빈 줄로 구분한다.

Core 본문의 `o200k_base` reference count는 current 88, revised 93 tokens다. 실제 input·cached input·output·reasoning usage와 TTFT·elapsed는 실행에서 따로 확인한다. Reference count를 실제 총비용으로 간주하지 않는다.

## 실행과 판정

[Frozen protocol](source-fidelity-protocol.json)의 SHA-256은 `f7237f874c55b1aa3a87947b9fd861c3e43a2f5fec1e7f8c2931c412b8bfb4ef`이다. Source와 common runner의 기존 hash를 유지하고, 이전 prompt를 그대로 사용한다. Model은 `gpt-6-astra`, effort는 `high`, case·arm당 한 번이다.

| 순서 | Case | Arm |
|---|---|---|
| 1 | N2 | current |
| 2 | N2 | revised |
| 3 | E2 | revised |
| 4 | E2 | current |

모든 output을 같은 기준으로 `pass`·`fail`·`uncertain` 판정한다. 원문 밖의 검증 상태·보장을 추가하지 않아야 하며, 다음 관계를 보존해야 한다.

- N2: controller가 batch 재시작을 **허용**한다. operator 승인 후에만 가능하며, batch당 최대 2회이고 자동 승인 기능은 없다. controller가 재시작을 수행한다고 바꾸거나 구현 검증 상태를 추가하면 실패다.
- E2: 5 s timeout이면 client가 같은 `request_id`로 재시도한다. Timeout은 server 처리 실패의 증거가 아니며 성공을 확정하지도 않는다. 미검증 대상은 다른 `request_id`에서 중복 처리가 방지되는지다. 이를 위험 없음·확인된 위험 없음으로 바꾸거나 같은 ID의 중복 방지를 보장하면 실패다.
- 두 사례 모두 formal 문체·technical term, 4문장 상한, 완결된 한 문장마다 빈 줄을 유지한다. 불확실성의 대상·강도가 애매하면 `uncertain`으로 남긴다.

실제 전송 내용·schedule·완료 event·usage가 protocol과 일치하고 **revised 두 사례가 모두 pass**여야 다음 단계로 간다. Current도 통과하면 그 관측을 그대로 기록하며 보완 효과를 단정하지 않는다. Current의 pass·fail·uncertain은 진입 조건이 아니다. Revised에 실패·불확실이 있거나 4회 실행이 불완전·protocol 불일치이면 6회 확인으로 진행하지 않는다.

통과 후 같은 revised core로 N1·N2·E1·E2·C1·C2를 한 번씩 생성하는 후속 6회를 별도로 고정한다. 이번 command는 4회만 실행하며 후속 6회를 자동 실행하지 않는다. 그 결과까지 확인한 뒤 기존 writing skill 반영 여부를 판단한다.

기존 실패를 본 뒤 만든 보완안이며 후속 6개도 이미 본 사례다. 이 확인을 독립 holdout이나 human comprehension 평가로 부르지 않는다. 1회씩의 결과로 일반적인 품질·latency 우위, 또는 실패 원인의 인과를 주장하지 않는다. 현재 전역 native pilot은 별도 실사용 기록으로 관리한다.

## 실행 방법과 준비 검증

일반 Terminal에서 다음 command를 한 번 실행한다. Script의 절대 경로이므로 현재 directory와 무관하다.

```sh
python3 /Users/janghyunbin/dev/human-readable-writing/research/benchmark_layout.py \
  --experiment source-fidelity \
  --output /private/tmp/human-readable-fidelity-run-20261029
```

성공하면 `4회 생성 완료. 결과: …/results.jsonl`이 출력된다. 기존 output directory는 덮어쓰지 않는다. 오류가 나면 해당 directory의 `events.jsonl`·`results.jsonl`·`app-server.stderr`를 보존하여 완료 범위와 관측 usage를 먼저 확인한다. 같은 경로로 재실행하거나 결과를 지우지 않는다.

Runner의 기존 생성·계측 loop와 오류 처리를 재사용하고, 고정된 experiment 선택과 실제 완료 건수 출력만 추가했다. 기존 12회가 기본값이고, 새 command는 4회만 전송한다. 두 protocol·source·common runner의 hash 검사를 유지한다.

Offline test는 먼저 새 선택 기능·완료 건수·CLI가 없는 상태에서 실패를 확인한 뒤 구현했다. 전체 22개가 통과했으며, 새 4회 schedule과 실제 전송 instruction·prompt·model·effort·protocol hash, 기존 12회 유지, CLI의 4회 완료 표시를 확인했다. Fixture는 synthetic 응답을 반환하며 실제 model을 호출하지 않는다.

현재 실제 generation은 **0/4**, 후속 확인은 **0/6**이다. Agent sandbox의 기존 app-server 권한 제한을 해결했다고 주장하지 않으며 이번에는 반복 실행을 시도하지 않았다. Global core·skill·manifest·invocation 설정을 변경하지 않았다.


## 2026-10-29 실행 전 review

Fresh-context reviewer `source_fidelity_review`가 code·protocol·판정 기준을 read-only로 확인했다. Current의 실패도 후속 진입을 막는 것으로 읽힐 수 있던 문장을, revised 두 사례 pass와 전체 4회의 실행 무결성만 gate임이 명확하도록 고쳤다. 아직 실행 전이므로 protocol hash를 새 값으로 고정하고 runner·문서에도 반영했다. 남은 Critical·Important·Minor finding은 없었다.

문서의 절대 경로가 가리키는 main checkout에 최종 준비본을 반영했고, worktree와 네 파일의 byte 일치를 확인했다. 해당 main checkout의 전체 offline test 22개가 통과했다. 이전 21회·12회 결과와 12회 protocol·event·adapter·source·common runner, 총 7개 보존 대상의 hash도 그대로다. 실제 app-server compatibility·hook 영향·보완 효과는 generation 이후 확인할 범위다.


## 2026-10-29 실제 결과 — 4/4 완료, 후속 6회 진입 조건 충족

사용자가 일반 Terminal에서 실행한 시작 timestamp `2026-10-29T07:23:31.151487+00:00`의 결과다. 앞 절의 0/4는 실행 전 상태이며 현재 네 응답과 `complete: 4`를 확인했다. [사례별 audit](source-fidelity-audit.json)에 실행 무결성과 의미·형식 판정을 기록했다.

Lead와 fresh-context agent `fidelity_six_review`가 frozen source·acceptance와 네 output을 별도로 대조했다. Agent는 lead의 판정을 읽지 않았으나 arm 이름은 볼 수 있었으므로 blind 평가라고 부르지 않는다. Human comprehension 측정도 아니다.

| Case | Current | Revised | 판정 근거 |
|---|---|---|---|
| N2 | pass | pass | controller의 허용 역할·승인 필요조건·최대 2회·자동 승인 없음 유지, 원문 밖 검증 상태 없음 |
| E2 | pass | pass | timeout의 의미와 재시도 조건, 다른 request_id에서의 중복 방지 미검증 범위 유지 |

네 output 모두 formal 문체·technical term·4문장 상한·문장마다 빈 줄 조건을 충족했다. 순서대로 2·3·2·3문장이다. Current E2의 “다른 request_id로 재시도했을 때”는 원문의 재시도 문맥을 명시한 것으로 판단했고, 불확실성의 대상·강도를 바꾸지 않았다.

**Revised N2·E2가 모두 pass여서 사전에 정한 후속 진입 조건을 충족했다. Current도 두 사례 모두 pass이므로 이번 결과가 revised의 개선 효과를 입증하지는 않는다.** 이전 current 실패와 이번 통과를 함께 보존하며, 원인을 특정 core 문구나 layout에 귀속하지 않는다.

### 실행 증거와 usage

- [원본과 동일한 결과](source-fidelity-results.jsonl): SHA-256 `23b9b15e3b750f7192eb0580f1e6b6cd779ebb8fafe1617fc49ac43458cdb49b`.
- [Event journal](source-fidelity-events.jsonl): SHA-256 `f80c345f17dcb24601840382df71e355b1c402693a409a5d3d67596c39380081`.
- [실행 당시 adapter](source-fidelity-adapter.txt): SHA-256 `94a3140e79e12e0b07b5863f55a0e3ef07b60197df1b0e6db3e043f36b9bded6`.
- Stderr는 원본 directory `/private/tmp/human-readable-fidelity-run-20261029`에 보존했다. SHA-256은 `cbb817c34a0ca31ac7311ea65b7dc6426bb059d44361b2f4965a291292d3b44d`이다.

Protocol·source·common runner·실행 adapter hash, 네 schedule 항목, 실제 전송 core·prompt·model·effort, 네 완료 event·최종 응답·usage가 모두 일치했다. Failure record는 없었다. 관측 item type은 agentMessage·reasoning·userMessage뿐이며 tool item이나 item/tool call은 없었다. Hook started/completed는 각각 8회 관측됐으며 payload는 보존하지 않아 모든 hook·외부 작업의 부재를 주장하지 않는다.

| 측정값 | Current 2회 | Revised 2회 |
|---|---:|---:|
| Input tokens | 34,819 | 34,829 |
| Output tokens, reasoning 포함 | 200 | 107 |
| 위 output 중 reasoning tokens | 88 | 0 |
| Cached input tokens | 0 | 0 |
| TTFT median | 5.937 s | 3.484 s |
| Elapsed median | 6.951 s | 4.423 s |

동일 case의 input usage 차이는 두 쌍 모두 +5 tokens다. 전체 input 69,648 + output 307 = 69,955 tokens이며 reasoning 88은 output에 포함된다. Case·arm당 한 번의 관측으로 output·reasoning·시간 차이의 일반적인 우위는 판단하지 않는다.

## 2026-10-29 전체 6개 사례 확인 준비

통과한 revised core를 그대로 사용하고 N1·N2·E1·E2·C1·C2를 한 번씩 생성한다. [6회 protocol](source-fidelity-six-protocol.json)의 SHA-256은 `d7e4c1d17a1ed40908c571f15315b104f1a7b03b46f53ed830865fb6d7e665fc`이다. 이전 prompt·source·model·effort를 유지한다. N1의 필요조건, E1의 평가 범위, C1의 검증 범위, C2의 인과·제안 상태까지 case별 acceptance를 미리 기록했다.

기존 runner의 고정 experiment 목록에 한 항목만 추가했다. 다음 command는 revised만 6회 생성하며, 채택이나 추가 실험을 자동 수행하지 않는다.

```sh
python3 /Users/janghyunbin/dev/human-readable-writing/research/benchmark_layout.py \
  --experiment source-fidelity-six \
  --output /private/tmp/human-readable-fidelity-six-run-20261029
```

성공 시 `6회 생성 완료`가 출력된다. 기존 4회 결과 directory는 재사용하지 않는다. 오류 시 원본을 지우거나 재실행하기 전에 완료 event·부분 응답·usage를 확인한다.

전체 6개 모두 의미·형식에서 pass이고 실행 무결성이 맞을 때 기존 writing skill 반영 여부를 검토한다. Fail·uncertain·실행 불완전이면 채택을 보류한다. 모두 이미 본 사례이며 current와 비교하지 않는 확인이므로 독립 holdout이나 개선 효과 입증으로 취급하지 않는다.

새 six-case CLI test가 option 부재로 실패하는 것을 확인한 뒤 목록에 추가했다. 전체 offline test 23개가 통과했고, 새 6회 실제 전송 core·prompt·model·effort·hash와 완료 표시, 기존 12회·4회 및 hash 변조 거부를 확인했다. Synthetic test는 model을 호출하지 않는다. 실제 후속 generation은 현재 0/6이다. Agent 환경의 기존 app-server 권한 제한에 대해 새 실행을 반복하지 않았다.


Six-case 준비본을 같은 reviewer가 후속 read-only 검토했다. Revised core·6개 prompt·source·model·effort·schedule·case별 acceptance·hash·main 반영본이 일치하며 Critical·Important·Minor finding은 없었다. Runner는 registry 한 항목 추가 외에 이전 adapter와 AST가 동일함을 확인했다. Reviewer는 test를 재실행하지 않았으며, lead가 최종 main checkout에서 전체 23개 통과를 직접 확인했다. 실제 후속 6회는 미실행 상태다.

## 2026-10-29 Checkpoint 검토

미commit 연구자료를 보존하기 전에 전체 offline test 23개를 다시 실행하여 통과를 확인하였다. Fresh-context reviewer `checkpoint_review`는 runner·fixture·protocol과 12회·4회 archive를 read-only로 검토하였고 Critical·Important·Minor finding을 보고하지 않았다. 원본 directory와 결과·journal의 byte 일치, frozen hash, 실제 전송 내용·완료 event·usage·문서의 집계를 확인하였다.

Journal의 sent event에는 timestamp가 없어 각 TTFT·elapsed의 시작점을 journal만으로 독립 재계산할 수는 없다. 모든 trial에서 완료 시각과 첫 delta의 차이는 저장된 elapsed와 TTFT의 차이와 0.002 ms 이내로 일치하며, 계산 위치는 실행 당시 adapter에 보존하였다. Hook payload·외부 작업과 원본 stderr의 내용은 이번 검토 범위에 포함하지 않았다. 기존 계측의 이 한계를 숨기거나 과거 원본을 덮어쓰지 않는다.

후속 6-case 결과 directory는 아직 없으며 실제 생성은 0/6이다. 기존 계획에 따라 제한된 agent 환경에서 app-server를 재시도하지 않았다. 위 일반 Terminal command로 실행하고 완료된 뒤 결과·event·adapter를 보존하여 판정한다. 현재 61-token 전역 실사용 core와 명시적 skill 호출 설정은 유지한다.

기존 날짜별 연구 기록의 문체 검사에서는 182건이 검출되었으며, 검토 전 snapshot과 rule·위치·내용이 동일하였다. 전역의 날짜별 과거 문서 append-only 원칙에 따라 해당 기록을 일괄 재작성하지 않았다. 이번에 추가한 안내·출처·checkpoint 문단에서는 새 문체 지적이 없었고 번호·참조 검사는 통과하였다. 이를 전체 과거 문서의 문체 검사 통과로 보고하지 않는다.


## 2026-10-29 전체 6회 결과 — 의미·형식 6/6 pass

사용자가 일반 Terminal에서 후속 6회를 실행하였다. 시작은 `2026-10-29T08:23:52.607939+00:00`, 마지막 결과 기록은 `08:24:41.227809+00:00`이며 약 48.620 s가 걸렸다. 앞 절의 0/6은 실행 전 상태다. [Six-case audit](source-fidelity-six-audit.json)에 사례별 판정과 실행 기록의 한계를 함께 남겼다.

Lead와 별도 context의 reviewer `six_case_audit`가 frozen source·acceptance와 여섯 output을 따로 대조하였다. Reviewer는 lead 판정문이나 이전 audit을 읽지 않았으며, arm 이름은 보이는 agent 평가다.

| Case | 의미·Formal·문단 형식 | 확인한 핵심 |
|---|---|---|
| N1 | pass | worker, >7일 AND pinned false의 필요조건, 복원 가능성 미검증 |
| N2 | pass | controller의 허용 역할, 사전 승인, 최대 2회, 자동 승인 없음 |
| E1 | pass | 전체 80개 중 12개 제외, 68개의 median error 0.8 m, 제외 대상 error 미계산 |
| E2 | pass | timeout만으로 실패 확정 불가, 같은 ID 재시도, 다른 ID의 중복 방지 미검증 |
| C1 | pass | >=3 조건·재실행 부정, unit test 9개와 실제 traffic 미검증 |
| C2 | pass | 같은 replay의 48→36 ms 관측, 원인 미확인, holdout 평가 제안·일정 미정 |

문장 수는 2·3·2·3·2·3개이며 모두 완결된 문장마다 빈 줄을 유지하였다. N1의 “경우에만”은 필요조건을 충분조건으로 바꾸지 않았다. N2는 재시작 수행 주체로 바뀌지 않았으며, E2와 C2도 불확실성의 대상·강도 및 행동의 확정 여부를 보존하였다. 원문에 없는 검증 상태를 추가한 사례는 없었다.

### 원본 보존과 실행 확인

- [Six-case 결과](source-fidelity-six-results.jsonl): SHA-256 `ee9c2a6bc486907b35b58019f5423eb78604a1c6a4ed93af5deac1c40726b7b4`.
- [Event journal](source-fidelity-six-events.jsonl): SHA-256 `1f3385622b232c15622c3875e4367ec42fb4be2e412c1227077300ab6f9a37e2`.
- [실행 당시 adapter](source-fidelity-six-adapter.txt): SHA-256 `57f302303f26e8fc8288389f0b958245fc57bf9f5d88a0132f14629de505ce0e`.
- 원본 directory `/private/tmp/human-readable-fidelity-six-run-20261029`와 stderr를 유지하였다. Stderr SHA-256은 `ec221e36577af41c0f907d6d70882f3ef1afefaf3c7f3292601043e19498d418`이다.

Protocol·source·common runner·adapter hash, 순서, 실제 전송 core·prompt·model·effort, 여섯 완료 event·최종 응답·usage가 기록상 일치하였다. `complete: 6`이며 failure record는 없었다. 관측 item type은 agentMessage·reasoning·userMessage이고 tool item이나 item/tool call은 없었다.

다만 E2·C1·C2의 turn/start 단계에서 `thread/settings/updated`가 각각 한 번 관측되었다. Payload를 보존하지 않아 어떤 설정이 달라졌는지 또는 실질적인 변화가 없었는지 확인할 수 없다. Hook started/completed도 각각 12회이며 payload가 없다. 이를 protocol 위반의 증거로 취급하지 않지만, 기록된 전송 조건의 일치를 runtime 전체의 동일성 입증으로 확대하지 않는다. Sent timestamp 부재에 따른 기존 timing 재계산 한계도 그대로다.

Input 104,473 + output 700 = total 105,173 tokens다. Reasoning 377은 output에 포함되며 cached input은 0이다. TTFT median은 7.022 s, elapsed median은 8.059 s다. Current를 같이 생성하지 않았고 case당 한 번이므로 비용·속도 우위를 추정하지 않는다.

### 반영 여부 검토와 종료 범위

사전에 정한 출력 기준을 모두 통과하였으며, 확인 가능한 실행 기록도 일치하였다. 이번 4회→6회 확인 단계는 완료한다. 추가 generation을 자동으로 늘리지 않는다.

검토 결론은 명시적으로 호출하는 writing skill의 의미 보존 지침을 아래 범위에서 구체화할 근거를 확보하였다는 것이다.

1. 원문의 주체·동작·조건·이유와 제시된 검증 상태를 보존한다. 검증에 대한 언급이 없다는 사실을 “미검증”이라는 새 주장으로 바꾸지 않는다.
2. 불확실성의 대상과 강도를 유지한다. “중복 방지 여부 미검증”을 “위험이 확인되지 않음”으로 바꾸지 않는다.
3. 사용자가 선호한 짧은 기술 설명에서는 formal 문체와 문장별 문단 분리를 사용한다. 다른 길이·문서 형식의 효과까지 검증한 것으로 취급하지 않는다.

직접 전달한 revised core의 출력 준수 확인이므로 full MANIFEST에 통합했을 때의 동작, 기존 61-token global core, 사람의 이해도 개선은 별도 문제다. 직전 4회에서 current도 통과했으므로 revised의 우위는 미확인이다. 이번 결과 검토에서는 MANIFEST·SKILL·global core를 변경하지 않았다. 실제 반영 시에는 위 범위의 변경을 확인하고 실사용 문장에 대한 사용자 feedback으로 평가하는 것이 적절하다.

### 기존 manifest 적용 확인과 최종 판단

규칙을 추가하기 전에 별도 context의 `manifest_source_check`가 현재 SKILL·MANIFEST를 읽고 N2·E2 원문을 다시 작성하였다. Formal 문체와 문장별 빈 줄은 요청에 명시하였다. Research 기록이나 이전 판정은 제공하지 않았다. [Audit의 `manifest_application_check`](source-fidelity-six-audit.json)에 요청·원문·실제 output과 lead 판정을 보존하였다.

두 output 모두 의미를 보존하였다. N2는 controller의 허용 역할과 operator 승인·최대 2회·자동 승인 없음만 서술하였다. E2는 timeout의 의미와 재시도 조건, 다른 request_id의 중복 방지 여부 미검증을 유지하였다. 따라서 이 확인에서는 기존 manifest의 부족함을 재현하지 못하였으며, 작성 규칙이나 예시를 추가하지 않았다. 재사용 안내에 현재 61-token native pilot 상태를 기재하였다.

각 사례 한 번의 적용 확인이며, 기존 manifest의 일반적인 성공률이나 추가 지침의 불필요함을 입증하지 않는다. Frozen app-server 실험과 별도인 agent 확인이므로 token·timing 합계에도 포함하지 않는다. 다음 평가는 [실사용 pilot](native-pilot.md)의 실제 사례와 사용자 feedback으로 진행한다. 추가 generation이나 전역 core 교체는 수행하지 않았다.

이미 완료된 output directory를 같은 command로 다시 지정하면 `FileExistsError`로 중단된다. 이 경로에서는 app-server를 시작하기 전에 중단하므로 해당 실패로 추가 generation이 발생하지 않는다. 이번 directory는 `complete: 6`인 기존 결과를 보존하고 있어 재실행이 필요하지 않았다.
