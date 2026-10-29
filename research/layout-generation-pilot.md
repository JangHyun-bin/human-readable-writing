# Layout 지침 generation 검증

검토일: 2026-10-28. **완료된 답변 0/12개. 실행 환경의 권한 오류로 generation 검증은 미완료다.** User 선호 기록과 실제 generation 결과를 구분한다.

## 검증 대상

[개인 선호 pilot](structure-layout-pilot.md)에서 사용자는 formal한 N1 source를 선호했고, 그 문구를 문단으로 나눈 조합에도 긍정적으로 답했다. N2의 세 문장과 API 설명의 네 문장에서는 문장마다 빈 줄을 둔 배치를 선택했다. 따라서 후속 후보의 동작을 아래처럼 정의했다.

> Formal한 문체와 technical term을 유지한다.
>
> 짧은 기술 설명은 문장마다 빈 줄로 구분한다.

이는 이 사용자의 짧은 기술 설명에 대한 후속 검증 지침이다. 문장 구조를 casual하게 바꾸거나 명사형을 일괄 제거하도록 지시하지 않는다. 장문·표·code·인용문의 형식에 적용한 검증은 없다.

## 동결한 비교

[Protocol](layout-generation-protocol.json)의 SHA-256은 `a0573f11039be65b0462217ce5c41ef498b4518c2d7bcfe85256e748f5986331`이다. Source 6개와 질문 문구, core, model, effort, 실행 순서를 첫 시도 전에 고정했다.

| Arm | 지침 | Local reference count |
|---|---|---:|
| formal | 기존 B + formal한 문체·technical term 유지 | 72 tokens |
| formal_layout | formal + 문장마다 빈 줄로 구분 | 88 tokens |

두 arm은 문단 분리 지시 한 문장만 다르다. Formal 유지 조건도 추가했으므로 `formal`을 과거 B와 동일한 arm으로 취급하지 않는다. 기존 B의 수치·단위·범위·부정·불확실성·인과 보존 지침은 두 arm에 모두 남아 있다.

위 수치는 설치된 `tiktoken`의 `o200k_base`와 기존 local encoding cache로 core 본문만 센 값이다. 문단 분리 지시의 차이는 16 tokens이며, provider의 실제 input usage·비용은 아직 측정하지 못했다.

Model은 기존 실험과 같은 `gpt-6-astra`, effort는 `high`로 지정했다. 새 가상 사례 6개 × 2 arm × 1회, 총 12회이며 먼저 실행하는 arm을 사례마다 교대했다. 기존 24회 B/C 제안에서 선택된 layout 동작의 준수 여부를 확인하는 범위로 줄였다. 한 번씩 생성하는 비교로 선호·이해도·latency 우위를 주장하지 않는다.

## 실행과 중단

기존 `benchmark_writing.Client`를 재사용하는 임시 Python 실행에서 `receive`를 감싸 모든 관측 event method와 item type을 기록하도록 준비했다. `commandExecution`과 dynamic tool event가 기록에 남는지 assert로 확인했다. 실제 답변에서 관측한 tool 수가 0이라는 결과는 아직 없으며, 계측 코드의 준비와 실제 계측을 구분한다.

| 시도 | 실행 환경 | 결과 |
|---|---|---|
| 1 | 기존 app-server 설정 | `~/.codex` 아래 SQLite state 초기화 실패. 완성된 답변 0개 |
| 2 | 이번 process에만 `sqlite_home`을 새 `/private/tmp` directory로 지정 | app-server가 `Operation not permitted (os error 1)`로 종료. 완성된 답변 0개 |

`sqlite_home`은 runtime state DB의 경로를 지정하는 공식 설정이다. 설치된 binary에서도 해당 설정 이름을 확인했다. 두 번째 시도는 허용된 임시 directory에 state를 저장하도록 한 것이며, sandbox나 영구 설정을 변경하지 않았다. [OpenAI Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)

첫 시도 진단은 `/private/tmp/writing-layout-pilot-frv7y6gs`, 두 번째는 `/private/tmp/writing-layout-pilot-30v8a9ie`에 남아 있다. 두 번째 오류의 세부 시스템 호출은 확인하지 못했으므로 network·인증·model 문제로 단정하지 않는다. 빈 output 파일도 해당 임시 directory로 옮겼으며, repository에 성공한 결과처럼 보이는 빈 JSONL은 두지 않는다.

## 현재 판단

사용자의 형식 선호는 기록했으나, 해당 instruction의 generation 준수율·사실 보존·provider usage·TTFT·전체 시간은 미측정이다. 지침 실패로 채점하거나 성공한 사례로 보고하지 않는다.

기존 runner code·core·manifest·invocation 설정과 원래 21개 benchmark record는 변경하지 않았다. Runtime 실행 제한이 없는 환경에서 동결한 12회 비교를 실행한 뒤에 자동 적용 여부를 판단할 수 있다.

## 2026-10-28 재현 가능한 runner와 독립 검토

사용자의 진행 승인 후 [별도 runner](benchmark_layout.py)를 구현했다. 기존 `benchmark_writing.Client`의 transport를 재사용하고, 새 adapter의 측정·기록 loop는 별도로 둔다. 기존 Client 파일과 frozen protocol의 hash는 유지한다. 새 adapter hash도 각 실행의 journal에 기록하므로 과거 runner와 같은 측정 구현으로 취급하지 않는다.

실행 가능한 환경에서 아래 command를 사용한다. Output directory는 새 경로여야 하며, 이미 존재하면 process 시작 전에 거부한다.

```sh
python3 /Users/janghyunbin/dev/human-readable-writing/research/benchmark_layout.py --output /private/tmp/human-readable-layout-run-20261028
```

`results.jsonl`에는 완료된 trial만, `events.jsonl`에는 실제 실행 command·전송 instruction·관측 method/item type·partial text/usage·실패 단계가 남는다. Child stderr는 `app-server.stderr`에 별도로 보존한다. Delta 없이 final만 도착하면 output은 보존하고 TTFT는 null로 기록한다. 실패나 중단 시 남은 trial을 자동 재시도하지 않는다. 실제 완료 결과와 incomplete attempt의 관측 usage를 구분하고, 누락된 usage를 0으로 처리하지 않는다.

### 결과를 보기 전에 고정한 판정 기준

- 12개 record가 frozen 순서·source·core·prompt·model·effort와 일치해야 experiment 완료다.
- 두 arm 모두 모든 source 사실과 4문장 상한을 확인한다. Baseline의 문단 묶음은 그 자체로 failure가 아니다.
- Candidate 6개 모두 formal register와 paragraph당 완결된 한 문장을 충족해야 해당 형식을 채택할 수 있다. 특정 명사형 구문 자체를 강제하지 않는다.
- N1의 `> 7일 AND pinned == false`는 필요조건이며 충분조건으로 강화하면 실패다. E2에서 timeout으로 성공·실패 또는 same-ID 중복 방지의 검증까지 추론하면 실패다. C1의 `>= 3`과 실제 traffic 미검증, C2의 제안·일정 미정도 보존해야 한다.
- Source와 다른 의미, unknown item/method, 실패한 attempt는 숨기거나 결과에서 조용히 제외하지 않는다. Literal 일치만으로 의미 보존을 통과시키지 않는다.
- Cached input은 input의 부분이며 reasoning output도 output과 별도로 다시 더하지 않는다. 이 1회 반복의 token·timing 기록으로 비용·latency 우위를 일반화하지 않는다.

### 검토와 확인 결과

구현 전 fresh-context reviewer 두 명이 같은 원본 protocol·source·code·실패 자료를 독립 검토했다. `runtime_review_v1`은 두 번째 EPERM의 원인이 미확정임을 지적했고, `validity_review_v1`은 partial evidence·실패 stage·전체 event 종류 기록과 명시적인 4문장 상한이 필요하다고 판단했다. 두 판단을 반영했으며 source나 scope를 바꾸지는 않았다.

추가 원인 조사는 최대 3 checks·5분으로 제한했다. 기존 `logs_2.sqlite`의 immutable read-only 조회에서는 WARN/ERROR row가 없었다. 두 진단 directory에 command manifest/stdout trace가 없음을 확인했고, 해당 시간대의 codex denial만 조회한 macOS log command는 `Cannot run while sandboxed`로 거부됐다. 종료 조건에 따라 현재 환경의 실제 runtime 재시도는 중단했다. 원인 미확정을 network·인증·model 실패로 바꾸어 기록하지 않는다.

구현 뒤 별도의 fresh-context code reviewer `layout_runner_code_review`가 검토했다. Initialize 중단 시 child가 남고 failure record가 빠지는 Important finding 1개를 synthetic process로 재현했다. Startup 중단과 partial output 이후 중단의 regression test를 먼저 실패시킨 뒤 adapter에서 cleanup과 failure 기록을 보완했다. Minor finding은 없었다.

최종 확인 command:

```sh
python3 -m unittest discover -s research -p 'test_*.py' -v
```

원래 test 4개와 새 runner test 10개, 총 14개가 통과했다. [Synthetic fixture](fixtures/layout_app_server.py)는 model을 호출하지 않으며, 그 응답을 실제 pilot 결과에 포함하지 않았다. Frozen hash 변조 거부, 전체 12개 전송 조건, overwrite 거부, unknown event/item 기록, EOF·timeout·중단 시 evidence 및 child cleanup, final-only output을 확인했다.

현재 **runner 구현·offline 검증은 완료**, **실제 generation은 0/12로 미완료**다. 실제 app-server compatibility, 새 output의 사실·형식 준수, writing 지침 채택은 확인하지 않았다. 사람의 이해도·일반적 품질·latency 우위는 이 pilot의 판정 범위가 아니다. 기존 active core·manifest·invocation 설정은 유지한다.

## 2026-10-29 실제 결과 확인 — generation 12/12 완료, 채택 보류

사용자가 일반 Terminal에서 절대 경로 command를 실행했고, 시작 timestamp `2026-10-28T05:45:49.795205+00:00`의 실행에서 12개 답변과 `complete: 12` 기록이 생성됐다. 같은 output 경로로 다시 실행했을 때의 `FileExistsError`는 원본 덮어쓰기를 막은 것이며, 기존 결과는 손상되지 않았다. 앞 절의 0/12는 agent sandbox 안에서의 이전 상태다. 새로운 결과는 일반 Terminal에서 실행한 것이므로 sandbox 내부의 권한 오류를 해결했다고 주장하지 않는다.

완료 메시지가 없어 사용자가 재실행한 점을 확인하고 CLI에 성공 종료 후 결과 경로를 출력하는 한 줄을 추가했다. 실제 측정에 사용된 adapter 원본은 변경 전에 [snapshot](layout-generation-adapter.txt)으로 보존했다. 이 출력 문구 변경은 생성·계측 loop를 바꾸지 않는다.

### 원본과 실행 무결성

- [결과 12개](layout-generation-results.jsonl): SHA-256 `62d75ad83dc396a70cff7aeb36cebbaf0a6418de224d1fab2e7891b22ea789b1`.
- [Event journal](layout-generation-events.jsonl): SHA-256 `720f8e7beb0ea1db0eb61ffa2612c101d967a71f7ab56fe7bcd817809cf8fed7`.
- [실행 당시 adapter](layout-generation-adapter.txt): SHA-256 `bba3c6888673792d80e72646d38d6ea53d4287403de7e8aac3c5d035e0ac4891`.
- 원본 directory `/private/tmp/human-readable-layout-run-20261028`는 그대로 유지했다. Stderr는 해당 directory에 보존하며 SHA-256은 `9760eb0c71c00262f0fa3de99159b7908067e75347843c31a02e50050b2d3cad`이다.

Protocol·source·기존 Client·실행 adapter hash가 journal과 일치함을 확인했다. 12개 schedule, 실제 전송 prompt·core·model·effort, 각 turn의 완료 event와 최종 usage도 일치했다. 이 실행의 failure record는 없었다. 이전 두 incomplete attempt는 별도 기록으로 남아 있으며 이번 usage와 섞지 않는다.

관측 item type은 `agentMessage`, `reasoning`, `userMessage`뿐이고 tool item이나 `item/tool/call`은 없었다. 다만 `hook/started`와 `hook/completed`가 각각 24회 있었으며 그 payload는 journal에 보존하지 않았다. 따라서 model의 tool item 부재와 모든 hook·외부 작업 부재를 같은 주장으로 취급하지 않는다. `mcpServer/startupStatus/updated` 등의 runtime notification도 관측됐다.

### 내용 audit

Fresh-context agent `layout_results_audit`가 source·facts와 12개 output을 독립 대조했고, lead도 별도로 내용을 확인했다. [사례별 판정](layout-generation-audit.json)은 agent audit이며 human comprehension 측정이 아니다.

| Case | formal | formal_layout | 주요 근거 |
|---|---|---|---|
| N1 | pass | pass | AND 필요조건, `> 7일`, worker, 복원 미검증 유지 |
| N2 | fail | fail | 두 arm 모두 source에 없는 검증 상태를 추가. Candidate는 controller의 허용 역할도 재시작 가능 표현으로 바꿈 |
| E1 | pass | pass | 80/12/68, 0.8 m, timeout error 미계산과 평가 범위 유지 |
| E2 | pass | uncertain | Candidate의 “중복 처리 위험은 확인되지 않았다”가 원래 방지 여부 미검증보다 다르게 읽힐 수 있음 |
| C1 | pass | pass | `>= 3`, 재실행 부정, unit test 9개, 실제 traffic 미검증 유지 |
| C2 | pass | pass | 48→36 ms, 원인 미확인, holdout 제안·일정 미정 유지 |

모든 12개가 formal register와 4문장 상한을 충족했고, candidate 6개 모두 paragraph당 완결된 한 문장을 지켰다. 의미 보존은 formal 5 pass/1 fail, formal_layout 4 pass/1 fail/1 uncertain이다.

N2 candidate의 “실제 동작은 별도로 검증하지 않았습니다”와 formal의 “실제 구현이 이 조건을 준수하는지는 확인하지 않았습니다”는 source에 없는 검증 상태다. 해당 내용이 현실에서 거짓이라고 입증한 것이 아니라, 주어진 사실만 보존하는 이번 acceptance를 충족하지 못한 것이다. 두 arm에 공통으로 나타났으므로 문단 분리 지시가 원인이라고 단정하지 않는다.

E2 candidate는 원래 세 사실을 유지했지만, 추가한 “중복 처리 위험은 확인되지 않았다”가 위험 여부 미확인 또는 확인된 위험 없음으로 읽힐 수 있다. 불확실한 판정을 pass로 바꾸지 않고 채택 기준에 미달한 것으로 남긴다.

### Usage와 timing

| 측정값 | formal, 6회 | formal_layout, 6회 |
|---|---:|---:|
| Input tokens 합계 | 107,839 | 107,935 |
| Output tokens 합계, reasoning 포함 | 1,485 | 1,188 |
| 위 output 중 reasoning tokens | 1,080 | 805 |
| Cached input tokens | 0 | 0 |
| TTFT median | 12.121 s | 10.623 s |
| 전체 시간 median | 13.125 s | 11.533 s |

동일 case의 input usage 차이는 여섯 쌍 모두 **+16 tokens**로 local reference count와 일치했다. 두 arm 합계는 input 215,774 + output 2,673 = total 218,447 tokens이며 reasoning 1,885는 output에 포함된 부분이다. 한 번씩 생성한 관측이므로 output·reasoning·시간의 차이를 지침의 일반적인 비용·속도 개선으로 해석하지 않는다.

### 판단

**Generation 실행은 완료했으며, 문장별 문단 분리의 관측 준수율은 6/6이다. 전체 writing 지침의 채택 기준은 충족하지 못했다.** 의미 보존 기준을 사후 완화하거나 실패한 N2를 제외하지 않는다.

다음 개선 범위는 source에 없는 검증 상태를 덧붙이는 공통 동작과 불확실성의 재해석이다. 이것이 core·harness·model의 어느 부분에서 비롯됐는지는 이번 비교만으로 확정할 수 없다. 이번 turn에서는 추가 generation을 실행하거나 core·manifest·global 설정을 변경하지 않았다. 기존 결과를 같은 directory에서 다시 생성할 필요도 없다.

CLI 완료 메시지 추가 뒤 기존 관련 test 14개는 통과했다. 같은 discovery에서 작업 중 새로 나타난 `test_native_pilot.py`가 존재하지 않는 `native_pilot`을 import하여 전체 suite는 `ModuleNotFoundError`로 실패했다. 이 파일의 mtime은 `2026-10-29T02:20:14.124529+00:00`이며 이번 변경에 포함하지 않았다. 전체 suite가 통과했다고 보고하지 않으며, 기존 결과·event archive·adapter snapshot의 byte/hash 일치는 별도로 확인했다.


## 2026-10-29 후속 준비

별도 native pilot 작업이 반영된 현재 checkout에서 기존 전체 test 20개가 통과하여 앞서 기록한 `native_pilot` import 실패는 재현되지 않았다. 사용자가 승인한 [N2·E2 보완안 4회 비교](source-fidelity-pilot.md)를 준비했고, runner 선택 기능을 포함한 전체 test 22개도 통과했다. 기존 결과와 frozen input은 유지하며, 새 실험의 실제 generation은 아직 0/4다.
