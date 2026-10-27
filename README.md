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

Codex에서는 `$human-readable-writing`, Claude Code에서는 `/human-readable-writing`으로 호출한다. 기술 설명·PR 설명·진행 보고·연구 해석·agent 지시를 작성하거나 개정할 때 자동 선택할 수 있도록 description을 설정하였다.

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

두 skill directory는 이 repository를 가리키는 symlink이다. 변경은 이 repository에서 한 번 수행한다. 적용 시점은 `~/.agents/TERMINOLOGY.md`의 전역 지침에도 명시하였다. Codex의 `~/.codex/AGENTS.md`와 Claude Code의 `~/.claude/CLAUDE.md`가 이 정본을 참조한다.

다른 machine에서는 이 private repository를 clone한 뒤 **repo root에서**, 대상 경로가 비어 있을 때 다음과 같이 설치할 수 있다.

```sh
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD" "$HOME/.agents/skills/human-readable-writing"
ln -s "$PWD" "$HOME/.claude/skills/human-readable-writing"
```

Local skill directory를 읽지 않는 cloud session에는 별도 설치가 필요하다. 설치 경로와 symlink 지원은 [OpenAI 공식 문서](https://learn.chatgpt.com/docs/build-skills)와 [Claude Code 공식 문서](https://code.claude.com/docs/en/skills)의 personal skill 범위를 따른다.

## 근거의 범위

논문은 영어 corpus의 언어적 특성과 작은 model의 length-penalty 실험을 보고하였다. 이 skill의 한국어 작성 원칙은 실무 제안이며, 사람의 독해 개선 효과를 검증한 결과는 아니다.
