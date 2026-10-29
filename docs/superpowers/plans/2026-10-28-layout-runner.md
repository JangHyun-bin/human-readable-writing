# Layout generation runner implementation plan

> **For agentic workers:** Use superpowers:executing-plans. User가 승인한 재현 가능한 runner와 동결된 pilot 범위 안에서 lead가 구현한다.

**Goal:** 동결된 12-turn 비교를 실행하고 성공·실패 evidence를 보존하는 command를 제공한다.

**Architecture:** 기존 `benchmark_writing.Client`의 transport를 재사용한다. 별도 layout runner가 관측 event와 partial output을 즉시 기록하고, frozen input을 확인한 뒤 각 trial을 순차 실행한다.

**Tech Stack:** Python standard library와 설치된 Codex CLI. 새 dependency 없음.

**Spec:** `research/layout-generation-protocol.json`과 `research/structure-layout-source.json`.

## Global constraints

- 기존 공통 Client·protocol·source·benchmark 원본 hash를 유지한다.
- `gpt-6-astra`, `high`, 고정된 12개 schedule·core·prompt를 변경하지 않는다.
- 현재 runtime 원인 조사 3 checks를 종료했다. 이 환경에서 추가 app-server 실행은 하지 않는다. Offline fixture는 generation이 아니다.
- Partial evidence와 미확인 usage를 보존하고, 미확인 값은 null로 둔다. 기존 output directory는 덮어쓰지 않는다.
- 실제 generation·지침 채택은 12개 실제 output 및 의미 audit 전에는 완료로 표시하지 않는다.

## Review focus

- Core가 arm 이름 때문에 누락되지 않도록 실제 전송 instruction을 확인한다.
- Unknown item·method와 실패 전 partial output·usage를 journal에 보존한다.
- Final-only 응답에서 TTFT를 만들어 내지 않는다.
- EOF·오류·timeout에서 실패 stage를 남기고 child process를 닫는다.
- Frozen input 변조·기존 output이 있으면 process 시작 전에 거부한다.

## Task 1: Durable runner

**Files:** `research/benchmark_layout.py`, `research/test_benchmark_layout.py`, `research/fixtures/layout_app_server.py`.

**Interfaces:** `load_protocol(root: Path) -> dict`, `run(output: Path) -> None`, CLI `python3 research/benchmark_layout.py --output <new-directory>`.

- [x] External app-server만 synthetic child process로 대체하는 test를 작성하고 RED 확인.
- [x] 기존 Client를 변경하지 않는 runner 구현. Journal·results·stderr는 하나의 새 directory에 저장.
- [x] `python3 -m unittest discover -s research -p 'test_*.py' -v` 전체 GREEN 확인.
- [x] 독립 code review와 새 evidence에 따른 판단을 기록. 필요하면 실패 test와 함께 지적 사항 fix.
- [x] Command·acceptance·현재 runtime 제한을 원래 research 기록에 연결한다.

Acceptance: 실제 12개 record가 없으면 generation 미완료다. 후보 6개 모두 사실·조건·부정·불확실성·formal register·문장별 paragraph·4문장 상한을 충족해야 채택할 수 있다. Baseline의 paragraph 묶음은 그 자체로 failure가 아니다. 사람의 이해도·일반적 품질·latency 우위는 이 pilot로 판정하지 않는다.

Runner 구현·offline 검증·code review 완료. 실제 generation은 runtime 권한 제한으로 0/12이며 지침 채택은 미완료다.
