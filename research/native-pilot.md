# Native writing core 실사용 pilot

## 적용 상태

2026-10-29 사용자 승인에 따라 기존 61-token core의 실사용 pilot을 준비하였다. 현재 session의 filesystem 정책은 `~/.agents/TERMINOLOGY.md`의 쓰기를 허용하지 않아 전역 적용은 미완료이다. 실제 사례는 아직 수집하지 않았다.

## 고정한 core

이번 대화에서 합의한 기존 축약 지침은 [benchmark_writing.py의 CORE](benchmark_writing.py)이다. 해당 상수를 설치와 되돌리기에서 함께 사용한다. [기존 후속 실험](core-refinement.md)과 구분하여 실사용 사례를 기록한다.

```text
기술 설명은 명사 연쇄의 관계와 주체·행동·조건을 분명하게 쓴다. 수치·단위·범위·부정·불확실성을 보존하고 관찰·가설·확인한 인과를 구분한다.
```

Core 본문은 `o200k_base` 기준 61 tokens이다. 현재 정본의 원문에 앞뒤 newline과 core 본문만 추가한 전체 문서의 reference token 증가량도 61이었다. 실제 provider usage는 session의 다른 내용과 함께 결정되므로 이 값을 모든 요청의 청구량이나 총비용으로 간주하지 않는다.

## 적용과 되돌리기

이 Mac의 Codex global `AGENTS.md`는 `~/.agents/TERMINOLOGY.md`를 가리키고, Claude Code global `CLAUDE.md`는 같은 정본을 읽도록 설정되어 있다. 정본에 core 본문을 직접 추가하여 기존 instruction 경로로 전달한다. 상세 skill은 명시적 호출을 유지한다.

일반 Terminal에서 다음 command로 적용한다.

```sh
python3 /Users/janghyunbin/dev/human-readable-writing/research/native_pilot.py enable
```

적용 여부 확인과 되돌리기는 다음과 같다.

```sh
python3 /Users/janghyunbin/dev/human-readable-writing/research/native_pilot.py status
python3 /Users/janghyunbin/dev/human-readable-writing/research/native_pilot.py disable
```

Installer는 core가 이미 있으면 다시 추가하지 않는다. 기존 문서의 원문과 permission을 보존하여 atomic replacement하고, 되돌릴 때는 추가한 문구와 정확히 일치하는 block만 제거한다. Pilot 중 core를 직접 바꾸면 원본과 다른 문구는 자동으로 제거하지 않는다. 문구를 바꾸기 전 `disable`로 기존 core를 먼저 제거한다.

Codex는 run 시작 시 instruction chain을 구성하므로 적용 후 새 session에서 확인한다. 기존 global file보다 우선하는 override가 있으면 해당 경로를 별도로 확인해야 한다. 이 Mac에서는 준비 시점에 global `AGENTS.override.md`가 없음을 확인하였다. [OpenAI 공식 문서](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

## 실사용 기록

PR 설명·coding 결과·연구 해석의 실제 답변 5–10개를 확인한다. 전역 적용을 마친 새 session에서는 첫 생성에 core를 포함한다. 기록은 사용자가 feedback을 제공하거나 별도 검토를 요청한 시점에 작성한다. 별도 benchmark generation이나 답변별 자동 기록을 설치하지 않는다.

| 사례 | 유형 | 사용자 평가 | 누락·중복·이유 연결 | 후속 판단 |
|---|---|---|---|---|
| 01 | 미수집 | — | — | — |
| 02 | 미수집 | — | — | — |
| 03 | 미수집 | — | — | — |
| 04 | 미수집 | — | — | — |
| 05 | 미수집 | — | — | — |
| 06 | 미수집 | — | — | — |
| 07 | 미수집 | — | — | — |
| 08 | 미수집 | — | — | — |
| 09 | 미수집 | — | — | — |
| 10 | 미수집 | — | — | — |

사용자 평가는 더 쉽게 이해됨·차이 없음·개선 필요로 구분한다. 수치·조건·불확실성 누락은 별도로 기록한다. 의미 손실이 반복되면 pilot을 중단하고 core를 제거한다. 읽기 선호가 이어지면 유지하고, 이점이 확인되지 않으면 기본 경로로 되돌린다. 이 판단을 인간 이해도나 latency 개선의 일반적 입증으로 확대하지 않는다.

## 검증 범위

임시 문서에서 중복 설치 방지, byte 단위 복원, 후속 편집 보존, read-only status, symlink·permission 보존, 실패 시 원문 보존을 검사한다. 실제 전역 enable과 새 session의 동작, 사람의 이해도·실사용 latency는 아직 미검증이다. 이 session에서는 전역 file 쓰기와 추가 model 요청을 수행하지 않았다.
