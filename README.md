<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing — 용어는 보존하고, 관계는 풀어 쓴다." width="100%">
</p>

<p align="center">
  <strong>기술적 의미를 보존하는 Codex · Claude Code writing skill</strong>
</p>

<p align="center">
  <a href="#바로-사용하기">사용법</a> ·
  <a href="MANIFEST.md">작성 원칙</a> ·
  <a href="#설치">설치</a> ·
  <a href="#검증과-한계">검증 근거</a>
</p>

---

Technical term은 그대로 두고, 누가 무엇을 했는지와 어떤 조건에서 결과가 성립하는지를 분명하게 쓴다. PR 설명·기술 조사·업무 안내·연구 해석에 적용한다.

## 같은 사실, 더 분명한 관계

아래는 문장 구조와 문단 배치를 비교하는 **가상 예시**다.

**원문**

> evaluator는 전체 80 session 중, timeout이 발생한 12 session을 제외한, 68 session의 median error를 0.8 m로 보고했다. timeout이 발생한 session의 error는 계산하지 않았다.

**개정**

> evaluator는 전체 80 session 중 timeout이 발생한 12 session을 제외하고, 나머지 68 session의 median error를 0.8 m로 보고했다.
>
> timeout이 발생한 12 session의 error는 계산하지 않았다.

수치와 측정 범위를 유지하면서 삽입 설명을 풀고, 계산하지 않은 대상을 별도 문단에 둔다. [예시 출처와 사용자 선호 기록](research/structure-layout-responses.json)

## 바로 사용하기

설치한 뒤, 문장이나 문서를 붙여 넣고 skill을 명시적으로 호출한다.

**Codex**

```text
$human-readable-writing 이 PR 설명을 다듬어줘.
Technical term과 수치·조건·불확실성은 보존해.
```

**Claude Code**

```text
/human-readable-writing 이 기술 설명을 다듬어줘.
관찰한 사실과 가설, 아직 확인하지 않은 부분을 구분해.
```

호출한 작업에서 [MANIFEST.md](MANIFEST.md)의 상세 지침과 필요한 예시를 읽는다. 이미 context에 있는 내용은 재사용한다.

## 무엇을 바꾸는가

| 검토할 부분 | 작성 방향 |
|---|---|
| 명사가 이어진 문장 | 주체·동작·대상 사이의 관계를 풀어 쓴다. |
| 조건이 끼어든 설명 | 핵심 서술을 가까이 두고, 밀접한 동작·조건을 함께 묶는다. |
| 여러 조건의 수치 비교 | 기준·단위·범위를 유지한 표로 비교한다. |
| 실행 안내 | 현재 상태와 필요한 판단·행동을 먼저 제시하고 이유를 잇는다. |
| 연구 결과 해석 | 관측 내용 뒤에 판단과 한계를 둔다. |

**보존할 것:** technical term, 식별자, 수치·단위·범위, 조건·부정, 불확실성의 대상과 강도. 원문에 없는 사실이나 관계는 추측으로 채우지 않는다.

## 설치

Repository에 접근할 수 있는 계정으로 clone한 뒤 **repo root에서** 설치한다. 대상 skill 경로가 비어 있을 때 사용하는 command다.

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD" "$HOME/.agents/skills/human-readable-writing"
ln -s "$PWD" "$HOME/.claude/skills/human-readable-writing"
```

두 skill directory가 같은 checkout을 가리키므로 상세 지침은 한 곳에서 관리한다. 이미 clone했다면 해당 directory에서 `mkdir`와 `ln` 단계만 수행한다.

<details>
<summary><strong>Runtime별 호출 설정</strong></summary>

| Runtime | 진입점 | 명시적 호출 설정 |
|---|---|---|
| Codex | `~/.agents/skills/human-readable-writing/SKILL.md` | 이 repo의 `agents/openai.yaml`에 `allow_implicit_invocation: false` 포함 |
| Claude Code | `~/.claude/skills/human-readable-writing/SKILL.md` | 아래 `skillOverrides`를 기존 설정에 병합 |

Claude Code의 `~/.claude/settings.json`에서 기존 설정을 보존하면서 다음 항목을 병합한다.

```json
{
  "skillOverrides": {
    "human-readable-writing": "user-invocable-only"
  }
}
```

Local skill directory를 읽지 않는 cloud session에는 별도 설치가 필요하다. 설치 경로와 symlink 지원은 [OpenAI 공식 문서](https://learn.chatgpt.com/docs/build-skills)와 [Claude Code 공식 문서](https://code.claude.com/docs/en/skills)의 personal skill 범위를 따른다.

</details>

<details>
<summary><strong>현재 개인 환경의 global core pilot</strong></summary>

현재 개인 환경에서는 기존 61-token core를 기본 instructions에 포함하고, 상세 skill은 명시적으로 호출한다. 위 symlink 설치만으로 global core까지 추가되지는 않는다.

2026-10-29 사용자가 core를 `~/.agents/TERMINOLOGY.md`에 적용하였고 상태 조회에서 `enabled`를 확인하였다. Codex의 `~/.codex/AGENTS.md`와 Claude Code의 `~/.claude/CLAUDE.md`가 참조하는 기존 정본은 유지하였다. 61 tokens는 `o200k_base` 기준 core 본문의 reference 값이며 모든 요청의 청구량을 뜻하지 않는다.

[Pilot 기록](research/native-pilot.md)에 적용·확인·되돌리기 command와 기존 설치 경로의 이력이 있다. 상세 지침은 2026-10-30 사용자 선호를 반영했고, 기존 global core와 호출 정책은 유지하였다.

</details>

## 검증과 한계

**현재 단계는 개인 실사용 pilot이다.** 문헌에서 얻은 아이디어와 이 사용자의 표현 선호를 작성 지침에 반영하였다. 사람의 이해도·읽기 시간 개선이나 일반적인 성능 우위는 아직 입증하지 않았다.

| 확인한 내용 | 결과와 해석 범위 |
|---|---|
| [실제 문서 다섯 쌍의 A/B 선호](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | 개인의 문단·표·정보 순서 선호를 상세 지침에 반영. Core 효과나 이해도 측정과 구분한다. |
| [Layout generation 12회](research/layout-generation-pilot.md) | 원문 밖 검증 상태 추가와 불확실성 재해석이 발견되어 채택을 보류했다. |
| [문제 사례 비교 4회](research/source-fidelity-pilot.md) | 두 arm 모두 pass. 보완안의 우위는 확인하지 못했다. |
| [Revised core의 6개 사례](research/source-fidelity-six-audit.json) | Agent의 의미·형식 기준은 6/6 pass. 기존 core와의 비교 실험은 아니다. |

실험의 revised core는 93 reference tokens이며, 현재 global pilot의 original core 61 tokens와 구분한다. 기존 MANIFEST를 적용한 문제 사례 두 개도 의미를 보존하였다. [전체 검증 기록](VALIDATION.md)

## 더 읽기

| 목적 | 문서 |
|---|---|
| 작성 원칙과 적용 예시 | [MANIFEST](MANIFEST.md) · [Skill 진입점](SKILL.md) |
| 출발점이 된 논문의 설계·결과·한계 | [논문 분석](ANALYSIS.md) · [원문 근거 검토](research/evidence-review.md) |
| 관련 연구와 적용 아이디어 | [관련 문헌](research/related-literature.md) · [두 논문 적용 제안](research/two-paper-application.md) |
| 문장 구조·문단 배치의 사용자 선호 | [선호 기록](research/structure-layout-pilot.md) |
| Input 비용과 응답 시간 | [호출 비용 비교](research/invocation-cost.md) · [동일 budget 비교](research/core-refinement.md) · [Blind 답변](research/core-refinement-blind.md) |

기본 instructions도 input tokens를 사용한다. 추가 file 조회가 없다는 사실이 비용이 전혀 없다는 뜻은 아니다.

---

[arXiv:2610.29162v1](https://arxiv.org/abs/2610.29162v1)의 분석에서 시작하였다. 논문은 영어 corpus의 언어적 특성과 작은 model의 length-penalty 실험을 보고했으며, 이 skill의 한국어 작성 지침은 실무 제안이다.

원논문은 CC BY 4.0으로 제공된다. 저자·출처·변경 내역은 [NOTICE.md](NOTICE.md)에 있다. **이 repository 자체의 배포 license는 아직 별도로 지정하지 않았다.**
