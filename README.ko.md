<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing" width="100%">
</p>

<p align="center"><a href="README.md">English</a> · <strong>한국어</strong></p>

Human-readable writing은 기술 문서를 다듬는 범용 에이전트 스킬입니다. Claude Code, Codex, OpenCode, Pi, oh-my-pi를 모두 지원 대상으로 삼으며, 도구마다 검증 범위는 다릅니다. PR 설명, 장애 안내, 연구 메모, 업무 안내를 넣고 호출하면 에이전트가 글을 다듬습니다. 독자가 무엇이 일어났는지, 어떤 근거로 판단하는지, 다음에 무엇을 해야 하는지를 따라갈 수 있게 하는 것이 목적입니다.

스킬은 에이전트의 모델이 따르는 Markdown 지침이며 스크립트를 포함하지 않습니다. 지침은 모델에게 여러 용어로 압축된 표현을 주체와 동작이 드러나는 문장으로 풀고, 조건과 불확실성을 해당 주장 곁에 두고, 독자의 작업에 맞게 정보 순서를 정하도록 요청합니다. 기술 용어와 원문의 사실은 유지하고, 원문에 없는 관계는 지어내지 말고 질문하도록 합니다.

개인 글쓰기 도구로 시작했으며 검증 범위가 제한적입니다. 기록된 검사는 특정 도구 버전에서 스킬이 로딩되는지와 소수의 출력이 원문 사실을 유지했는지를 확인했습니다. 사람의 이해도·읽기 시간 개선이나 일반적인 글쓰기 품질 향상은 입증하지 않았습니다.

## 예시

아래 PR 설명은 스킬이 지향하는 편집을 보여 드리기 위한 설명용 가상 사례이며, 기록된 실행의 출력이 아닙니다.

**원문**

> 로그아웃 후 도착한 프로필 응답으로 인한 이전 사용자 정보 재표시를 막기 위해, 요청 시작 시 저장한 `sessionVersion`과 응답 수신 시 현재 값의 일치 여부에 따라 화면 갱신을 결정하도록 변경하고 로그아웃 시에는 이 값을 증가시키도록 했습니다. 이미 전송된 요청은 취소하지 않으며 브라우저 환경에서만 동작을 확인했습니다.

**개정**

> 로그아웃 후에 프로필 응답이 도착하면 이전 사용자 정보가 화면에 다시 표시될 수 있습니다. 이를 막기 위해 로그아웃할 때 `sessionVersion`을 증가시킵니다. 응답을 받으면 요청을 시작할 때 저장한 값과 현재 값을 비교하고, 두 값이 같을 때만 화면을 갱신합니다.
>
> 이미 전송된 요청은 취소하지 않습니다. 동작은 브라우저 환경에서만 확인했습니다.

문제와 해결 동작을 먼저 설명하고, 값을 저장·변경·비교하는 시점을 따라갈 수 있도록 순서를 정리했습니다. 값이 같아야 한다는 조건, 요청을 취소하지 않는다는 동작, 브라우저에 한정된 확인 범위도 유지했습니다.

[예시 모음](examples/README.ko.md)에는 입력할 요청과 각 개정에서 유지한 사실을 함께 정리했습니다. 날짜가 기록된 도구 검사에서 나온 장애 안내 출력과 그 검사의 한계도 실었습니다.

## 설치

다음이 필요합니다.

- 설치된 에이전트 도구. [지원 대상과 현재 검증 범위](docs/tool-support.md)를 확인해 주세요.
- [`skills` CLI](https://github.com/vercel-labs/skills)를 사용한다면 Node.js 22.20 이상. `node --version`으로 확인하실 수 있습니다. 수동 설치에는 이 CLI가 필요하지 않습니다.

다음 CLI 예시는 Codex와 Claude Code를 선택합니다. 스킬을 사용할 프로젝트의 루트에서 실행해 주세요.

```sh
npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code
```

이 명령은 해당 프로젝트에만 스킬을 설치합니다. Codex는 `.agents/skills/`에서, Claude Code는 `.claude/skills/`에서 스킬을 읽습니다. 사용할 도구의 `-a` 옵션만 남겨 주세요.

Pi에서는 에이전트 옵션을 `-a pi`로 바꾸며, Pi도 `.agents/skills/`를 사용합니다. oh-my-pi는 [수동 설치 안내](docs/install.ko.md)를 따릅니다. OpenCode도 지원 대상이지만 [현재 지원은 부분적](docs/tool-support.md#opencode-limitation)입니다. CLI가 해당 도구에 설치할 수 있다는 사실만으로 모든 설정에서 이 스킬이 동작한다고 보장하지 않습니다. 설치 후에는 새 세션을 시작해 주세요.

프로젝트마다 설치하지 않고 사용자 계정에 한 번 설치해 모든 프로젝트에서 사용하려면 `-g`를 추가해 주세요.

```sh
npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code -g
```

2026-11-02 도구 검사는 사용자 전역 설치를 다루지 않았습니다. 현재 설치 검사는 [검증 기록](docs/verification.md)에서 확인하실 수 있습니다.

`skills` CLI는 익명 사용 데이터를 전송합니다. 이 저장소처럼 공개된 GitHub 저장소라면 저장소와 스킬 이름도 포함됩니다. 전송을 끄려면 CLI를 실행할 때 `DISABLE_TELEMETRY=1`을 설정해 주세요. 자세한 내용은 CLI의 [telemetry 안내](https://github.com/vercel-labs/skills/blob/main/docs/troubleshooting.md#telemetry)에 있습니다.

수동 설치, 업데이트, 제거, 이전 설치에서 옮기는 방법은 [설치 안내](docs/install.ko.md)에 있습니다. 예전 안내는 저장소 루트를 스킬 디렉터리에 연결했습니다. 스킬은 이제 `skills/human-readable-writing/`에 있으므로, 설치 안내에 따라 기존 링크를 바꿔 주세요.

## 사용

아래 표에서 사용하는 도구의 호출 방식을 선택하고, 다듬을 원문을 함께 넣어 주세요. 아래 예시는 Claude Code용이며, 작성 지침은 도구에 관계없이 공유합니다.

| 도구 | 명령 |
|---|---|
| Codex | `$human-readable-writing` |
| Claude Code | `/human-readable-writing` |
| Pi | `/skill:human-readable-writing` |
| oh-my-pi | `/skill:human-readable-writing` |
| OpenCode | 네이티브 스킬 선택. [CLI 호출은 안정적으로 검증되지 않았습니다.](docs/tool-support.md#opencode-limitation) |

```text
/human-readable-writing 이 PR 설명을 유지보수자가 읽기 좋게 다듬어 주세요.
기술 용어와 사실·조건·불확실성은 보존해 주세요.

[이곳에 원문을 붙여 넣어 주세요.]
```

스킬은 명시적으로 호출하며, 도구마다 선택 방식이 다릅니다. 지침은 모델에게 요청하신 언어와 형식을 따르고 식별자, 수치·단위, 제외 조건, 부정, 불확실성을 보존하도록 요구합니다. 문장마다 문단을 나누는 규칙은 강제하지 않습니다. 기록된 OpenCode 실행 한 건에서 원문의 조건이 바뀌었으므로, 결과를 사용하기 전에 원문과 비교해 주세요.

도구마다 별도의 작성 규칙 사본을 두지 않습니다. 다섯 지원 대상의 설치 경로, 실제 관찰 결과, 남은 호환성 작업은 [도구 호환성](docs/tool-support.md)에 정리했습니다.

## 도구 지원

현재 패키지는 Claude Code 2.1.321의 프로젝트·사용자 전역 설치, Pi 1.4.0, oh-my-pi 18.18.6에서 실행했습니다. 테스트 계정의 네이티브 Codex 0.167.0은 선택한 모델을 제공자가 거부해 호출을 검증하지 못했습니다. 해당 오류와 모델, 출력의 제약은 통과로 간주하지 않고 [현재 검증 기록](docs/verification.md)에 구분했습니다.

2026-11-02에 Codex 0.166.0, Claude Code 2.1.312, Pi 1.4.0, oh-my-pi 18.15.0의 프로젝트 설치가 제한된 검사를 통과했습니다. 도구마다 영어와 한국어 요청을 한 건씩 실행했고, 스킬이 로딩되어 모델이 필요한 지침 파일을 읽었으며, 두 출력 모두 검사한 원문 사실을 유지했습니다. 도구별로 스킬을 호출하지 않은 비교 요청 한 건에서는 스킬을 읽지 않았습니다. 이 검사는 스킬이 `skills/human-readable-writing/`으로 옮겨지기 전, 커밋 `4fff511`의 저장소 루트를 임시 프로젝트에 직접 연결해 진행했습니다. 현재 구조, `skills` CLI, 사용자 전역 설치는 시험하지 않았습니다.

**OpenCode 2.2.1은 부분 검증 상태이며 실패가 있습니다.** 영어 네이티브 로딩 한 건은 성공했습니다. 그러나 CLI 멘션은 의도한 스킬 사본을 안정적으로 선택하지 못했고, 참조 파일 경로도 항상 해석되지는 않았으며, 한 출력에서는 원문의 조건이 바뀌었습니다.

검사한 버전·모델·경로·제약은 [도구 호환성](docs/tool-support.md)에, 현재 패키지와 설치 명령에 대한 검사는 [검증 기록](docs/verification.md)에 있습니다. 두 문서 모두 일반적인 글쓰기 품질을 입증하지 않습니다.

## 언어

스킬은 요청하신 언어를 따르며, 번역을 요청하지 않으시면 원문의 언어를 유지합니다. **한국어와 영어는 문서 관리와 검증의 공동 우선 대상입니다.** 사용하실 언어를 이 두 언어로 제한하지는 않습니다. 한국어와 영어 README는 설치·사용 방법, 지원 상태, 검증 근거를 같은 내용으로 관리합니다.

공통 [작성 원칙](skills/human-readable-writing/MANIFEST.md)은 영어 파일 하나로 유지합니다. 한국어 및 한·영 혼용 문서에는 [한국어 보완 지침](skills/human-readable-writing/references/korean.md)을 함께 적용합니다. 지침 파일의 언어가 출력 언어를 정하지는 않습니다.

기존 번역 문서: [Français](README.fr.md) · [中文（简体）](README.zh-CN.md) · [日本語](README.ja.md). 번역 안내를 제공하는 상태이며 해당 언어의 출력 품질 검증을 뜻하지 않습니다. 세 언어 사이에 개발 순위는 두지 않습니다. [언어 지원과 검증 기록](skills/human-readable-writing/references/language-support.md)에 상세 범위를 정리했습니다.

## 검증과 한계

| 기록 | 확인한 내용 |
|---|---|
| [네이티브 호출 검사, 2026-11-02](research/runtime-validation-20261102.json) | 네 도구는 제한된 검사를 통과했고 OpenCode는 성공·실패가 섞였습니다. 버전·명령·출력·파일 로딩 근거와 제약을 기록했습니다. |
| [영어·한국어 작업 사례, 2026-11-01](skills/human-readable-writing/references/language-support.md#workflow-check) | 두 지침 버전 모두 에이전트의 원문 충실도·형식 점검을 통과했습니다. 개선 효과나 도구 호환성을 입증한 결과는 아닙니다. |
| [한국어 문서 다섯 쌍 비교](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | 한 사용자의 문단·표·정보 순서 선호를 기록했습니다. |
| [문단 배치 생성 12회](research/layout-generation-pilot.md) | 근거 없는 검증 상태 추가와 불확실성 변경이 발견되어 채택을 보류했습니다. |
| [원문 충실도 생성 4회](research/source-fidelity-pilot.md) · [후속 사례 6개](research/source-fidelity-six-audit.json) | 4회 비교는 두 조건 모두 통과했고, 후속 6개 사례에는 동시 비교 조건이 없었습니다. 두 기록 모두 우위를 입증하지 않았습니다. |

각 기록은 당시 평가한 지침 버전에 한정됩니다. 과거 토큰·응답 시간 측정값은 현재 스킬의 비용을 나타내지 않습니다. 이 스킬을 설치해도 유지보수자의 별도 [전역 지침 실험](research/native-pilot.md)은 설치되지 않습니다.

## 문제 알리기

문제에 맞는 양식으로 issue를 열어 주세요. 영어나 한국어로 작성하실 수 있습니다.

- CLI 설치가 실패하거나, 도구가 스킬을 찾지 못하거나, 호출해도 스킬이 로딩되지 않으면 [설치·호출 문제 양식](https://github.com/JangHyun-bin/human-readable-writing/issues/new?template=install-problem.yml)을 사용해 주세요.
- 개정 결과에서 수치, 조건, 부정, 제외 조건, 주장의 강도가 바뀌었거나 원문에 없는 관계가 추가되었다면 [원문 의미 변경 양식](https://github.com/JangHyun-bin/human-readable-writing/issues/new?template=source-meaning-change.yml)을 사용해 주세요.

Issue는 공개됩니다. 올리기 전에 인증정보, 개인정보, 기밀 문서를 지워 주세요. 같은 변경을 보여 주는 짧은 가상 원문이면 충분합니다.

변경을 제안하는 방법은 [기여 안내](CONTRIBUTING.md)에 있습니다.

## 더 읽기

- [스킬 진입점](skills/human-readable-writing/SKILL.md)과 [작성 원칙](skills/human-readable-writing/MANIFEST.md).
- [설치 안내](docs/install.ko.md), [도구 호환성](docs/tool-support.md), [검증 기록](docs/verification.md), [언어 지원](skills/human-readable-writing/references/language-support.md).
- [검증 이력](VALIDATION.md), [관련 문헌 검토](research/related-literature.md), [호출 비용 비교](research/invocation-cost.md).
- [변경 기록](CHANGELOG.md).

## 라이선스

스킬 지침, 문서, 스크립트를 포함해 이 프로젝트를 위해 작성한 자료는 [MIT License](LICENSE)로 제공합니다. 제3자 저작물의 인용문과 인용한 저작물 자체에는 각각의 조건이 그대로 적용됩니다. [NOTICE.md](NOTICE.md)에 출처와 license, 그리고 연구 기록에 남은 모델 출력에 license가 적용되는 범위를 정리했습니다.

Clark·Martin·Mahowald의 [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1) 분석에서 시작한 프로젝트입니다. 스킬의 작성 지침은 실무 제안이며, 원논문의 저자가 검증하거나 보증한 방법이 아닙니다.
