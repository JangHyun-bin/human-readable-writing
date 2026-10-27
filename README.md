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

평소 답변은 기존 기본 instructions로 바로 작성한다. 이 skill을 위한 상시 지침이나 skill·manifest를 자동으로 읽는 절차는 두지 않는다.

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

용어 표기의 정본은 `~/.agents/TERMINOLOGY.md`이다. 이 정본에서 skill을 매번 읽으라는 지시를 제거하였다. 세 조건의 비교에서 기본 답변도 의미 보존 검토를 통과하였고 축약 지침의 추가 효과가 확인되지 않아, 축약 지침도 상시 추가하지 않았다. Codex의 `~/.codex/AGENTS.md`와 Claude Code의 `~/.claude/CLAUDE.md`가 참조하는 기존 정본은 유지한다.

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
