# Human-readable writing

기술적 의미를 보존하면서 사람이 이해할 수 있도록 작성하는 원칙이다. [arXiv:2610.29162v1](https://arxiv.org/abs/2610.29162v1)을 분석하여 작성하였다. **용어는 보존하고, 관계는 풀어 쓴다.**

## 구성

| 문서 | 내용 |
|---|---|
| [SKILL.md](SKILL.md) | Agent가 발견하고 호출하는 진입점 |
| [MANIFEST.md](MANIFEST.md) | 작성 원칙·의미 보존 확인·적용 예시의 정본 |
| [ANALYSIS.md](ANALYSIS.md) | 논문 설계·결과·한계와 실무 적용 판단 |
| [VALIDATION.md](VALIDATION.md) | 적용 확인과 배포 검증 기록 |
| [원문 근거 검토](research/evidence-review.md) | 독립 검토의 section·line별 근거 |

## 사용

실사용 pilot 기간에는 61-token core를 기본 instructions에 직접 포함하여 답변을 작성한다. 상세 skill·manifest는 명시적으로 호출할 때만 읽는다.

2026-10-29 사용자가 일반 Terminal에서 core를 적용하였고 상태 조회에서 `enabled`를 확인하였다. [실사용 pilot](research/native-pilot.md)에 적용·확인·되돌리기 command와 5–10개 사례의 기록 기준이 있다. 상세 skill의 명시적 호출 정책은 유지한다.

문장 개선·문서 검토가 필요하면 Codex에서는 `$human-readable-writing`, Claude Code에서는 `/human-readable-writing`으로 명시적으로 호출한다. 호출한 작업에서만 상세 manifest와 필요한 예시를 읽는다. 이미 현재 context에 있는 내용은 재사용한다.

```text
human-readable-writing을 적용해서 이 설명을 작성해줘.
Technical term과 수치·조건·불확실성은 보존해.
```

## 이 Mac의 전역 설치

Codex와 Claude Code가 같은 checkout을 읽도록 다음 위치를 연결하였다.

| Runtime | 진입점 |
|---|---|
| Codex | `~/.agents/skills/human-readable-writing/SKILL.md` |
| Claude Code | `~/.claude/skills/human-readable-writing/SKILL.md` |

두 skill directory는 이 repository를 가리키는 symlink이다. 상세 지침은 이 repository에서 한 번 변경한다. Codex는 `agents/openai.yaml`의 `allow_implicit_invocation: false`를 사용한다. Claude Code는 `~/.claude/settings.json`의 `skillOverrides`에서 이 skill을 `user-invocable-only`로 설정한다.

용어 표기의 정본은 `~/.agents/TERMINOLOGY.md`이다. 최초 비용 비교 후 이 정본에서 skill을 매번 읽으라는 지시를 제거하였고 축약 지침도 상시 추가하지 않았다. 2026-10-29에는 사용자가 승인한 실사용 pilot을 위해 core 본문만 정본에 직접 추가하였다. Codex의 `~/.codex/AGENTS.md`와 Claude Code의 `~/.claude/CLAUDE.md`가 참조하는 기존 정본은 유지한다.

다른 machine에서는 이 private repository를 clone한 뒤 **repo root에서**, 대상 경로가 비어 있을 때 다음과 같이 설치할 수 있다.

```sh
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD" "$HOME/.agents/skills/human-readable-writing"
ln -s "$PWD" "$HOME/.claude/skills/human-readable-writing"
```

Claude Code의 `~/.claude/settings.json`에서는 기존 설정을 보존하면서 다음 항목을 병합한다.

```json
{
  "skillOverrides": {
    "human-readable-writing": "user-invocable-only"
  }
}
```

Local skill directory를 읽지 않는 cloud session에는 별도 설치가 필요하다. 설치 경로와 symlink 지원은 [OpenAI 공식 문서](https://learn.chatgpt.com/docs/build-skills)와 [Claude Code 공식 문서](https://code.claude.com/docs/en/skills)의 personal skill 범위를 따른다.

## 근거의 범위

논문은 영어 corpus의 언어적 특성과 작은 model의 length-penalty 실험을 보고하였다. 이 skill의 한국어 작성 원칙은 실무 제안이며, 사람의 독해 개선 효과를 검증한 결과는 아니다.

원논문은 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)으로 제공된다. 저자·출처·변경 내역과 적용 범위는 [NOTICE.md](NOTICE.md)에 명시하였다. 이 repository 자체의 배포 license는 아직 별도로 지정하지 않았다.

호출 방식과 token·응답 시간의 비교 결과는 [비용 비교](research/invocation-cost.md)를 참조한다. 기본 instructions도 input tokens를 사용하므로, 추가 file 조회가 없다는 사실을 비용이 전혀 없다는 의미로 해석하지 않는다.

기존 축약 core와 같은 token budget의 후보를 비교한 후속 실험은 [고도화 비교](research/core-refinement.md), 조건 이름을 가린 실제 답변은 [blind 비교](research/core-refinement-blind.md)에 있다. 해당 실험 직후에는 기본 적용 설정을 유지하였으며, 이후 시작한 실사용 pilot의 현재 상태는 위 사용 절에 명시하였다.

## 후속 연구와 검증 상태

| 자료 | 2026-10-29 확인 상태 |
|---|---|
| [관련 문헌](research/related-literature.md) · [두 논문 적용 제안](research/two-paper-application.md) | 연구 근거와 독립적인 적용 가설을 구분하여 기록 |
| [문장 구조·줄바꿈 선호](research/structure-layout-pilot.md) | 사용자의 formal 문체·문장별 문단 선호 기록. 이해도 측정과 구분 |
| [Layout generation](research/layout-generation-pilot.md) | 12/12 생성 완료. 원문 밖 검증 상태 추가와 불확실성 재해석으로 채택 보류 |
| [Source fidelity](research/source-fidelity-pilot.md) | 문제 사례의 4/4 비교 완료. 두 arm 모두 pass로 보완 효과는 미확정 |
| [전체 6개 사례 protocol](research/source-fidelity-six-protocol.json) · [audit](research/source-fidelity-six-audit.json) | 6/6 생성 완료. Agent의 의미·형식 기준 모두 pass |

별도 실험의 revised core는 93 reference tokens이며, 전역 실사용 pilot의 original CORE 61 tokens와 구분한다. 여섯 사례는 revised만 한 번씩 확인한 결과로, 기존 core보다 낫다는 근거는 아니다. 기존 manifest를 적용한 문제 사례 두 개도 의미를 보존하여 작성 규칙을 추가하지 않았다. 전역 core와 명시적 skill 호출 정책을 유지하고, 다음 평가는 실사용 pilot의 사용자 feedback으로 진행한다.


2026-10-30 실제 문서 다섯 쌍에 대한 사용자 선택을 반영하여 [MANIFEST](MANIFEST.md)의 짧은 설명 문단 배치·수치 비교 표·목적별 정보 순서를 구체화하였다. 명시적으로 skill을 호출할 때 이 상세 지침을 읽는다. 기존 61-token core와 호출 정책은 유지하며, 이번 변경은 개인 선호의 반영이지 일반적인 독해 개선 효과의 입증은 아니다.
