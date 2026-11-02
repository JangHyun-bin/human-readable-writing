<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing" width="100%">
</p>

<p align="center"><a href="README.md">English</a> · <strong>한국어</strong></p>

독자가 기술 설명의 흐름을 따라갈 수 있도록 다듬는 글쓰기 스킬입니다. 무엇이 일어났는지, 어떤 근거로 판단하는지, 다음에 무엇을 해야 하는지를 분명하게 설명합니다. PR 설명, 장애 보고, 연구 메모, 업무 안내에 사용할 수 있습니다.

여러 용어로 압축된 설명은 주체와 동작이 드러나는 문장으로 풀고, 조건과 불확실성은 해당 주장 곁에 둡니다. 문서의 목적에 맞게 정보 순서를 정리하면서 기술 용어와 사실을 보존합니다. 원문에 필요한 관계가 빠져 있으면 확인할 내용을 질문합니다.

## 예시

PR 설명에서는 어떤 문제를 어떻게 해결하는지, 어디까지 확인했는지가 드러나야 합니다.

**원문**

> 로그아웃 후 도착한 프로필 응답으로 인한 이전 사용자 정보 재표시를 막기 위해, 요청 시작 시 저장한 `sessionVersion`과 응답 수신 시 현재 값의 일치 여부에 따라 화면 갱신을 결정하도록 변경하고 로그아웃 시에는 이 값을 증가시키도록 했습니다. 이미 전송된 요청은 취소하지 않으며 브라우저 환경에서만 동작을 확인했습니다.

**개정**

> 로그아웃 후에 프로필 응답이 도착하면 이전 사용자 정보가 화면에 다시 표시될 수 있습니다. 이를 막기 위해 로그아웃할 때 `sessionVersion`을 증가시킵니다. 응답을 받으면 요청을 시작할 때 저장한 값과 현재 값을 비교하고, 두 값이 같을 때만 화면을 갱신합니다.
>
> 이미 전송된 요청은 취소하지 않습니다. 동작은 브라우저 환경에서만 확인했습니다.

문제와 해결 동작을 먼저 설명하고, 값의 저장·변경·비교 시점을 따라갈 수 있도록 순서를 정리했습니다. 값이 같아야 한다는 조건, 요청을 취소하지 않는다는 동작, 브라우저에 한정된 확인 범위도 유지했습니다. 설명용 가상 사례이며, 실제 실행 결과와 평가 범위는 아래 [검증 기록](#검증과-한계)에서 확인하실 수 있습니다.

## 설치

저장소를 한 번 복제한 뒤 로컬 스킬 경로에 연결합니다. **저장소 루트에서, 두 대상 경로가 비어 있을 때** 실행해 주세요. 경로가 이미 있다면 연결 대상을 먼저 확인해 주세요.

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD" "$HOME/.agents/skills/human-readable-writing"
ln -s "$PWD" "$HOME/.claude/skills/human-readable-writing"
```

이미 복제하셨다면 해당 디렉터리에서 `mkdir`와 `ln` 단계만 수행해 주세요. `SKILL.md`가 `MANIFEST.md`와 한국어용 `references/korean.md`를 읽으므로 디렉터리 전체를 유지해 주세요.

Codex의 명시적 호출 설정은 `agents/openai.yaml`에 포함되어 있습니다. 공통 `SKILL.md`에는 Claude Code 등 호환 도구를 위한 `disable-model-invocation: true`가 포함되어 있습니다. 검증한 Claude Code 버전에는 별도의 `skillOverrides` 추가가 필요하지 않습니다. 기존의 다른 설정은 유지해 주세요.

위 방법은 로컬 세션용입니다. 이 경로를 읽을 수 없는 환경에서는 [Codex](https://learn.chatgpt.com/docs/build-skills) 또는 [Claude Code](https://code.claude.com/docs/en/skills)의 개인 스킬 설치 안내를 따라 주세요.

## 사용

스킬을 명시적으로 호출하고 다듬을 원문을 함께 넣어 주세요.

| 도구 | 요청 앞에 붙일 명령 |
|---|---|
| Codex | `$human-readable-writing` |
| Claude Code | `/human-readable-writing` |

```text
$human-readable-writing 이 PR 설명을 유지보수자가 읽기 좋게 다듬어 주세요.
기술 용어와 사실·조건·불확실성은 보존해 주세요.

[이곳에 원문을 붙여 넣어 주세요.]
```

사용자가 지정한 언어와 형식을 따릅니다. 번역을 요청하지 않았다면 원문의 언어를 유지합니다. 식별자, 수치·단위, 제외 조건, 부정과 불확실성을 보존하며, 원문에 없는 관계는 추측으로 채우지 않고 확인합니다. 문단과 표는 문서의 목적에 맞게 사용하고, 문장마다 문단을 나누는 규칙은 강제하지 않습니다.

## 도구 지원

2026-11-02에 **Codex 0.166.0, Claude Code 2.1.312, Pi 1.4.0, oh-my-pi 18.15.0**의 프로젝트 로컬 설치에서 제한된 한·영 호출·참조 파일 로딩 검사를 통과했습니다. 도구별 호출 없는 비교 요청 한 건에서는 이 스킬을 읽지 않았습니다. 임시 프로젝트에서 검사했으며, 위 사용자 전역 설치 경로를 별도로 시험한 것은 아닙니다.

**OpenCode 2.2.1은 부분 검증 상태이며 실패가 있습니다.** 영어 네이티브 로딩 한 건은 성공했지만 CLI 멘션과 참조 파일 경로 처리가 일관되지 않았습니다. 추가 출력에서는 원문의 조건도 바뀌었습니다. Pi·oh-my-pi 사용법을 포함한 [검증 경로·명령·모델·제약](docs/tool-support.md)을 참고해 주세요. 이 관찰은 일반적인 글쓰기 품질을 입증하지 않습니다.

## 언어

스킬은 요청하신 언어를 따르며, 번역을 요청하지 않으시면 원문의 언어를 유지합니다. **한국어와 영어는 문서 관리와 검증의 공동 우선 대상입니다.** 사용하실 언어를 이 두 언어로 제한하지는 않습니다. 두 README에서 설치·사용 방법, 지원 상태, 검증 근거를 함께 관리합니다. 예시는 각 언어에서 자연스럽게 작성하되, 공통 정보가 바뀌면 두 문서에 반영합니다.

공통 [작성 원칙](MANIFEST.md)은 영어 파일 하나로 유지합니다. 한국어 및 한·영 혼용 문서에는 [한국어 보완 지침](references/korean.md)을 함께 적용합니다. 지침 파일의 언어가 출력 언어를 정하지는 않습니다.

기존 번역 문서: [Français](README.fr.md) · [中文（简体）](README.zh-CN.md) · [日本語](README.ja.md). 번역 안내를 제공하는 상태이며 해당 언어의 출력 품질 검증을 뜻하지 않습니다. 세 언어 사이에 개발 순위를 두지 않고, 실제 사용 수요와 언어별 검토 여건에 따라 후속 작업을 정합니다. [언어 지원과 검증 기록](docs/language-support.md)에 상세 범위를 정리했습니다.

## 검증과 한계

제한적인 검증을 거친 개인 글쓰기 도구입니다. 사람의 이해도·읽기 시간 개선이나 일반적인 글쓰기 품질 우위는 입증하지 않았습니다.

| 기록 | 확인한 내용 |
|---|---|
| [네이티브 호출 검사, 2026-11-02](research/runtime-validation-20261102.json) | 네 도구는 제한된 검사를 통과했고 OpenCode는 성공·실패가 섞였습니다. 버전·명령·출력·파일 로딩 근거와 제약을 기록했습니다. |
| [영어·한국어 작업 사례](docs/language-support.md#workflow-check) | 두 지침 버전 모두 에이전트의 원문 충실도·형식 점검을 통과했습니다. 개선 효과나 도구 호환성을 입증한 결과는 아닙니다. |
| [한국어 문서 다섯 쌍 비교](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | 한 사용자의 문단·표·정보 순서 선호를 기록했습니다. |
| [문단 배치 생성 12회](research/layout-generation-pilot.md) | 근거 없는 검증 상태 추가와 불확실성 변경이 발견되어 채택을 보류했습니다. |
| [원문 충실도 생성 4회](research/source-fidelity-pilot.md) · [후속 사례 6개](research/source-fidelity-six-audit.json) | 4회 비교는 두 조건 모두 통과했고, 후속 6개 사례에는 동시 비교 조건이 없었습니다. 두 기록 모두 우위를 입증하지 않았습니다. |

각 기록은 당시 평가한 지침 버전에 한정됩니다. 과거 토큰·응답 시간 측정값은 현재 스킬의 비용을 나타내지 않습니다. 위 설치 과정은 유지보수자의 별도 [전역 지침 실험](research/native-pilot.md)을 설치하지 않습니다.

## 더 읽기

- [작성 원칙](MANIFEST.md)과 [스킬 진입점](SKILL.md).
- [언어 정책·검증 기준](docs/language-support.md)과 [도구별 호환성](docs/tool-support.md).
- [검증 이력](VALIDATION.md), [관련 문헌 검토](research/related-literature.md), [호출 비용 비교](research/invocation-cost.md).

Clark·Martin·Mahowald의 [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1) 분석에서 시작한 프로젝트입니다. 스킬의 작성 지침은 실무 제안이며, 원논문의 저자가 검증하거나 보증한 방법이 아닙니다. 원논문은 CC BY 4.0으로 제공되며 출처와 개별 라이선스는 [NOTICE.md](NOTICE.md)에 기록했습니다.

## 라이선스

프로젝트에서 별도로 작성한 코드·스킬 지침·문서는 기여자가 관련 권리를 보유한 범위에서 [MIT License](LICENSE)로 제공합니다. 제3자 인용문과 재사용 자료에는 각 자료의 기존 조건이 적용됩니다. [NOTICE.md](NOTICE.md)를 참고해 주세요. 이 MIT License는 참고 논문의 라이선스를 변경하지 않습니다.

## 개발 계획

[설계 제안](docs/superpowers/specs/2026-11-02-writing-stack-design.md)과 [구현 계획](docs/superpowers/plans/2026-11-02-writing-stack.md)에 Core, 작업별 지침, 언어·사용자 프로필, 검증 도구, 평가 실행기, 배포 검사를 정리했습니다. 향후 작업 계획이며, 현재 배포물의 기능이나 품질 검증 결과를 뜻하지 않습니다.
