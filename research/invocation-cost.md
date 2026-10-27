# Writing skill 호출 비용 비교

측정일: 2026-10-27 · 기준 commit: `aefe5a8` · Codex CLI: `0.164.0`

## 1. 채택한 형태

평소 답변은 기존 기본 instructions로 바로 작성한다. 이 skill을 위한 상시 지침은 추가하지 않는다. 전역의 자동 읽기 지시를 제거하고, 상세 manifest는 사용자가 명시적으로 호출한 문장 검토에서만 읽는다.

축약 지침을 추가하는 후보도 비교하였지만, 기본 답변과의 의미 보존 차이를 이번 sample에서 확인하지 못하였다. 모든 요청에 추가 context를 사용하는 것을 정당화할 근거가 확보되지 않아 이 후보는 채택하지 않았다. 이는 기존 model의 작성 능력을 사용하는 선택이며 model weights를 변경한 구현은 아니다.

## 2. 세 조건과 측정 방법

| 조건 | 추가 동작 |
|---|---|
| `baseline` | 이 skill을 적용하는 별도 동작 없이 기본 답변 작성 |
| `loaded` | 고정한 기존 `SKILL.md`·`MANIFEST.md`를 한 번 읽고 작성 |
| `native` | 핵심 원칙을 developer instructions에 직접 포함하여 작성한 후보 |

Model은 local config의 `gpt-6-astra`, reasoning effort는 `high`로 고정하였다. Coding 결과 보고·PR 설명·연구 해석의 가상 과제 세 개를 사용하였다. 각 조건·과제를 한 번씩 실행하여 총 9회 측정하였다. 과제별 조건 순서는 Latin square로 교차 배치하였다.

Codex app-server의 ephemeral thread를 각 실행마다 새로 생성하였다. 별도 API key는 사용하지 않았고 기존 Codex 인증으로 실행하였다. Skill catalog는 모든 조건에서 제외하고, 다른 skill을 실행하지 않도록 동일한 developer 지시를 적용하였다. 이 지시는 공통으로 포함되는 전역 skill 활성화 지시보다 우선한다. 따라서 `baseline`은 같은 Codex host에서 이 skill의 적용을 생략한 조건이며, 아무 지침도 없는 순수 model은 아니다.

`loaded`는 별도의 read-only tool로 동결한 두 문서를 한 번에 반환하였다. Tool 정의는 모든 조건에서 동일하게 제공하였다. 실제 filesystem bridge 자체의 지연이나 두 문서를 따로 읽는 경우의 두 번째 왕복은 측정하지 않았다. `native`에는 benchmark script의 `CORE`만 추가하였다. 나머지 host instructions와 도구 구성은 동일하다.

`turn/start`를 보낸 시각부터 마지막 답변의 첫 `item/agentMessage/delta`까지를 TTFT로 측정하였다. Commentary의 첫 글자는 제외하였다. 전체 시간은 `turn/completed`까지이며, app-server와 thread 생성 시간은 제외하였다. Input·cached input·output·reasoning tokens는 `thread/tokenUsage/updated`의 누적 usage를 기록하였다. Model request 수 자체는 protocol에서 직접 측정하지 않았고 tool 왕복 수만 측정하였다.

## 3. 실측 결과

각 조건의 세 실행에 대한 중앙값이다. Token은 각 실행 안의 model 호출을 합한 usage이다.

| 조건 | Input tokens | Cached input | Output tokens | Reasoning tokens | TTFT | 전체 시간 | Tool 왕복 |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | 18,079 | 0 | 455 | 291 | 13.58 s | 16.36 s | 0 |
| loaded | 38,272 | 17,920 | 288 | 119 | 9.63 s | 11.58 s | 1 |
| native 후보 | 18,140 | 13,184 | 375 | 216 | 16.06 s | 17.45 s | 0 |

Input 중앙값은 `loaded`가 `baseline`의 약 2.12배였다. 문서 내용의 추가뿐 아니라 tool 이후 model을 재개할 때 공통 context가 다시 포함되는 영향이 있다. Cached input도 별도로 보고하므로 이 비율을 실제 요금 비율로 해석하지 않는다. 이번 비교에서는 별도 billing 금액을 산출하지 않았다.

모든 과제에서 `native` 후보의 input은 해당 baseline보다 정확히 61 tokens 많았다. Tool 왕복은 두 조건 모두 0이었다. 이 61 tokens는 축약 원칙 본문의 비용이며, 전역 지침에 제목까지 포함해 배치하는 후보는 reference tokenizer 기준 76 tokens였다.

시간은 input 수와 같은 방향으로 움직이지 않았다. `loaded`가 더 빠른 과제가 있었고, 조건별 cache hit과 reasoning·output 양도 달랐다. 따라서 native 또는 기본 경로가 특정 비율만큼 빨라진다는 결론을 내리지 않는다. 이 pilot에서 확인한 것은 tool 왕복과 누적 input 차이이며, 지연에 대한 안정적인 인과 효과는 미확인이다.

## 4. 의미 보존 확인

동일한 과제 안에서 세 output을 원문과 직접 대조하였다. 평가자는 조건을 알고 있었으며 blind human reader 평가가 아니다.

| 과제 | 확인한 항목 | 결과 |
|---|---|---|
| Coding 보고 | 20 ms, p95 2.4 m→1.8 m, 전체 150·성공 135·실패 15, 동일 data의 threshold 선택, independent holdout 부재, iOS·현장 미검증, 후속 평가가 제안임을 보존 | 세 조건 모두 보존 |
| PR 설명 | 같은 account만 직렬화, 다른 account는 병렬 유지, unit test 6개 통과, 부하·배포 미수행, 단일 process 범위와 여러 process의 미검증 | 세 조건 모두 보존 |
| 연구 해석 | 영어 corpus의 관찰, 두 trained that alternation·KL 없음·>98%, far transfer 1/4와 genitive, forced choice, frontier 원인·인간 독해·한국어 효과 미검증 | 세 조건 모두 보존 |

이 결과는 sample의 사실 보존 확인이다. 같은 품질의 글을 항상 생성한다거나 인간이 더 빨리 이해한다는 근거는 아니다. 첫 coding 보고처럼 배치가 달라지는 경우도 있었으나, 독자의 선호나 이해 시간을 측정하지 않았다.

## 5. Context 비용의 구분

`o200k_base`로 문서 자체를 별도 계수한 reference 값은 다음과 같다. Provider usage와 동일한 값이라고 가정하지 않는다.

| 항목 | Reference tokens | 배포 판단 |
|---|---:|---|
| 기존 전역 자동 읽기 절 | 121 | 제거 |
| 기존 skill file + 전체 manifest | 2,044 | 명시적으로 호출한 검토에서만 읽기 |
| 전역에 추가하는 축약 후보 | 76 | 미채택 |
| 이번 skill을 위한 새 상시 원칙 | 0 | 기존 기본 작성 지침 유지 |

Codex는 `agents/openai.yaml`의 `allow_implicit_invocation: false`를 사용하고, Claude Code는 `skillOverrides`의 `user-invocable-only`를 사용한다. 자동 context에서 실제로 제외되는지는 각 runtime의 설정·prompt 확인 결과와 구분하여 기록한다. 동작의 근거는 [OpenAI 공식 skill 문서](https://learn.chatgpt.com/docs/build-skills)와 [Claude Code의 invocation 제어 문서](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill)이다.

배포 후 실제 symlink가 가리키는 checkout에서 다음을 확인하였다. 이 확인에는 추가 model 요청을 사용하지 않았다.

- `codex debug prompt-input`의 기본 skills 목록에서 `human-readable-writing` 항목이 변경 전에는 있었고 변경 후에는 없었다. Description도 기본 prompt에 포함되지 않았다.
- 같은 prompt에서 전역 자동 읽기 절이 제거되었음을 확인하였다. 다른 언어·인증·CI 지침의 본문은 보존하였다.
- App-server의 `skills/list`에는 같은 skill이 `enabled: true`로 남아 있었다. 기본 prompt에서의 노출과 명시적 호출을 위한 등록을 구분하였다.
- Claude Code `2.1.311`의 local settings에서 `user-invocable-only`를 확인하였고 다른 setting 값은 그대로 유지하였다. Claude의 실제 model 응답이나 prompt 구성은 이번에 측정하지 않았다.

## 6. 재실행과 한계

원본 기록과 실제 output은 [invocation-pilot.jsonl](invocation-pilot.jsonl)에 있다. 측정 도구는 [benchmark_writing.py](benchmark_writing.py)이며, 마지막 답변의 첫 token을 commentary와 구분하는 검사 등 세 개는 [test_benchmark_writing.py](test_benchmark_writing.py)에 있다.

```sh
python3 -m unittest discover -s research -p 'test_*.py' -v
python3 research/benchmark_writing.py --output /private/tmp/writing-pilot-new.jsonl
```

Benchmark는 실제 Codex model 요청을 최대 9회 실행한다. 새 output 경로를 사용해야 하며 기존 결과를 덮어쓰지 않는다. 초기 문서의 reference commit이 local git history에 있어야 한다. Model·effort는 실행 시점의 local Codex config에서 읽으므로 재비교 시 동일하게 고정되었는지 확인한다.

각 cell을 한 번만 측정한 작은 pilot이며 p95나 통계적 유의성을 추정하지 않았다. Cache 상태를 강제로 동일하게 만들지 않았고, 실제 다중 turn coding 작업·Claude Code의 model 응답·인간 독해는 측정하지 않았다. 이미 문서를 읽은 긴 session의 context 비용이 이 설정 변경만으로 제거된다고 가정하지 않는다.
