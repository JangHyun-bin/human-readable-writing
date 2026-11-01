<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing" width="100%">
</p>

<p align="center"><a href="README.md">English</a> · <strong>한국어</strong></p>

한국어와 영어 기술 문서를 다듬는 스킬이다. 사실·기술 용어·불확실성을 보존하면서 누가 무엇을 했는지, 어떤 조건에서 결과가 성립하는지를 분명하게 쓴다. PR 설명, 장애 보고, 연구 메모, 업무 안내에 적용한다.

## 예시

**원문**

> evaluator는 전체 80 session 중, timeout이 발생한 12 session을 제외한, 68 session의 median error를 0.8 m로 보고했다. timeout이 발생한 session의 error는 계산하지 않았다.

**개정**

> evaluator는 전체 80 session 중 timeout이 발생한 12 session을 제외하고, 나머지 68 session의 median error를 0.8 m로 보고했다.
>
> timeout이 발생한 12 session의 error는 계산하지 않았다.

수치와 조건을 유지하면서 집계 대상과 제외 대상을 구분했다. [기존 편집 사례](research/structure-layout-responses.json)에 기록된 가상 예시이며, 사람의 이해도 개선을 측정한 결과는 아니다.

## 설치

저장소를 한 번 복제한 뒤 로컬 스킬 경로에 연결한다. **저장소 루트에서, 두 대상 경로가 비어 있을 때** 실행한다. 경로가 이미 있다면 연결 대상을 먼저 확인한다.

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD" "$HOME/.agents/skills/human-readable-writing"
ln -s "$PWD" "$HOME/.claude/skills/human-readable-writing"
```

이미 복제했다면 해당 디렉터리에서 `mkdir`와 `ln` 단계만 수행한다. `SKILL.md`가 `MANIFEST.md`와 한국어용 `references/korean.md`를 읽으므로 디렉터리 전체를 유지해야 한다.

Codex의 명시적 호출 설정은 `agents/openai.yaml`에 포함되어 있다. 공통 `SKILL.md`에는 Claude Code 등 호환 도구를 위한 `disable-model-invocation: true`가 포함되어 있다. 검증한 Claude Code 버전에는 별도의 `skillOverrides` 추가가 필요하지 않다. 기존의 다른 설정은 유지한다.

위 방법은 로컬 세션용이다. 이 경로를 읽을 수 없는 환경에서는 [Codex](https://learn.chatgpt.com/docs/build-skills) 또는 [Claude Code](https://code.claude.com/docs/en/skills)의 개인 스킬 설치 안내를 따른다.

## 사용

스킬을 명시적으로 호출하고 다듬을 원문을 함께 넣는다.

| 도구 | 요청 앞에 붙일 명령 |
|---|---|
| Codex | `$human-readable-writing` |
| Claude Code | `/human-readable-writing` |

```text
$human-readable-writing 이 PR 설명을 유지보수자가 읽기 좋게 다듬어줘.
기술 용어와 사실·조건·불확실성은 보존해.

[이곳에 원문을 붙여 넣는다.]
```

사용자가 지정한 언어와 형식을 따른다. 번역을 요청하지 않았다면 원문의 언어를 유지한다. 식별자, 수치·단위, 제외 조건, 부정과 불확실성을 보존하며, 원문에 없는 관계는 추측으로 채우지 않고 확인한다. 문단과 표는 문서의 목적에 맞게 사용하고, 문장마다 문단을 나누는 규칙은 강제하지 않는다.

## 도구 지원

2026-11-02에 **Codex 0.166.0, Claude Code 2.1.312, Pi 1.4.0, oh-my-pi 18.15.0**의 프로젝트 로컬 설치에서 제한된 한·영 호출·참조 파일 로딩 검사를 통과했다. 도구별 호출 없는 비교 요청 한 건에서는 이 스킬을 읽지 않았다. 임시 프로젝트에서 검사했으며, 위 사용자 전역 설치 경로를 별도로 시험한 것은 아니다.

**OpenCode 2.2.1은 부분 검증 상태이며 실패가 있다.** 영어 네이티브 로딩 한 건은 성공했지만 CLI 멘션과 참조 파일 경로 처리가 일관되지 않았다. 추가 출력에서는 원문의 조건도 바뀌었다. Pi·oh-my-pi 사용법을 포함한 [검증 경로·명령·모델·제약](docs/tool-support.md)을 참고한다. 이 관찰은 일반적인 글쓰기 품질을 입증하지 않는다.

## 언어

**한국어와 영어를 동등한 주 지원 언어로 둔다.** 두 README에서 설치·사용 방법, 지원 상태, 검증 근거를 함께 관리한다. 예시는 각 언어에서 자연스럽게 작성하되, 공통 정보가 바뀌면 두 문서에 반영한다.

공통 [작성 원칙](MANIFEST.md)은 영어 파일 하나로 유지한다. 한국어 및 한·영 혼용 문서에는 [한국어 보완 지침](references/korean.md)을 함께 적용한다. 지침 파일의 언어가 출력 언어를 정하지는 않는다.

기존 번역 문서: [Français](README.fr.md) · [中文（简体）](README.zh-CN.md) · [日本語](README.ja.md). 번역 안내를 제공하는 상태이며 해당 언어의 출력 품질 검증을 뜻하지 않는다. 세 언어 사이에 개발 순위를 두지 않고, 실제 사용 수요와 언어별 검토 여건에 따라 후속 작업을 정한다. [언어 지원과 검증 기록](docs/language-support.md)에 상세 범위를 정리했다.

## 검증과 한계

제한적인 검증을 거친 개인 글쓰기 도구다. 사람의 이해도·읽기 시간 개선이나 일반적인 글쓰기 품질 우위는 입증하지 않았다.

| 기록 | 확인한 내용 |
|---|---|
| [네이티브 호출 검사, 2026-11-02](research/runtime-validation-20261102.json) | 네 도구는 제한된 검사를 통과했고 OpenCode는 성공·실패가 섞였다. 버전·명령·출력·파일 로딩 근거와 제약을 기록했다. |
| [영어·한국어 작업 사례](docs/language-support.md#workflow-check) | 두 지침 버전 모두 에이전트의 원문 충실도·형식 점검을 통과했다. 개선 효과나 도구 호환성을 입증한 결과는 아니다. |
| [한국어 문서 다섯 쌍 비교](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | 한 사용자의 문단·표·정보 순서 선호를 기록했다. |
| [문단 배치 생성 12회](research/layout-generation-pilot.md) | 근거 없는 검증 상태 추가와 불확실성 변경이 발견되어 채택을 보류했다. |
| [원문 충실도 생성 4회](research/source-fidelity-pilot.md) · [후속 사례 6개](research/source-fidelity-six-audit.json) | 4회 비교는 두 조건 모두 통과했고, 후속 6개 사례에는 동시 비교 조건이 없었다. 두 기록 모두 우위를 입증하지 않았다. |

각 기록은 당시 평가한 지침 버전에 한정된다. 과거 토큰·응답 시간 측정값은 현재 스킬의 비용을 나타내지 않는다. 위 설치 과정은 유지보수자의 별도 [전역 지침 실험](research/native-pilot.md)을 설치하지 않는다.

## 더 읽기

- [작성 원칙](MANIFEST.md)과 [스킬 진입점](SKILL.md).
- [언어 정책·검증 기준](docs/language-support.md)과 [도구별 호환성](docs/tool-support.md).
- [검증 이력](VALIDATION.md), [관련 문헌 검토](research/related-literature.md), [호출 비용 비교](research/invocation-cost.md).

Clark·Martin·Mahowald의 [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1) 분석에서 시작한 프로젝트다. 스킬의 작성 지침은 실무 제안이며, 원논문의 저자가 검증하거나 보증한 방법이 아니다. 원논문은 CC BY 4.0으로 제공되며 출처와 개별 라이선스는 [NOTICE.md](NOTICE.md)에 기록했다. **이 저장소 자체의 배포 라이선스는 별도로 지정하지 않았다.**
