# 스킬 설치·업데이트·삭제

[한국어 README](../README.ko.md) · [English guide](install.md)

이미 사용 중인 에이전트에 설치합니다. 이 스킬을 설치해도 에이전트 도구나 모델 계정이 제공되지는 않으며, 웹 채팅 앱에 자동으로 추가되지 않습니다. 아래 절차를 위해 기존 에이전트 설정을 바꿀 필요는 없습니다.

## 설치 범위 선택

`skills` CLI에는 Node.js 22.20 이상과 `npx`가 필요합니다. 설치 도구를 업그레이드할 때는 [공식 CLI 안내](https://github.com/vercel-labs/skills)를 확인합니다. 실제로 시험한 버전과 설치 범위는 [현재 검증 기록](verification.md)에 구분합니다.

Claude Code, Codex, OpenCode, Pi, oh-my-pi는 모두 지원 대상입니다. 아래 CLI 예시는 Codex와 Claude Code를 선택합니다. Pi는 해당 에이전트 옵션을 `-a pi`로 바꾸며, oh-my-pi는 아래 수동 `.omp/skills` 경로를 사용합니다. OpenCode의 [부분 지원 제약](tool-support.md#opencode-limitation)은 유지합니다. 지원 대상으로 삼는다는 뜻이 모든 설치·호출 경로의 검증 통과를 의미하지는 않습니다.

현재 프로젝트에서만 사용하려면 사용할 프로젝트의 디렉터리에서 실행합니다.

```sh
npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code
```

사용하지 않는 도구의 `-a` 옵션은 빼도 됩니다. 여러 프로젝트에서 사용할 사용자 전역 설치는 `-g`를 추가합니다.

```sh
npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code -g
```

두 범위의 사본을 따로 관리할 의도가 없다면 한 범위에만 설치합니다. 설치 도구가 같은 이름의 기존 스킬을 교체할 수 있으므로 먼저 기존 항목과 직접 수정한 내용을 확인합니다. `sudo`는 사용하지 않습니다.

CLI는 설치 telemetry를 수집합니다. 다음처럼 명령 앞에 `DISABLE_TELEMETRY=1`을 붙이면 비활성화할 수 있습니다.

```sh
DISABLE_TELEMETRY=1 npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code
```

CLI가 지원하는 모든 에이전트에서 이 스킬의 동작을 검증했다는 의미는 아닙니다. [도구별 지원 범위](tool-support.md)를 확인합니다.

## 새 세션에서 호출

Codex에서는 `$human-readable-writing`, Claude Code에서는 `/human-readable-writing`, Pi와 oh-my-pi에서는 `/skill:human-readable-writing`으로 요청을 시작합니다. OpenCode는 안정적인 명령이 있다고 가정하지 말고 [네이티브 활성화와 CLI 제약](tool-support.md#opencode-limitation)을 확인합니다. 다듬을 원문과 대상 독자를 함께 전달합니다. 다음은 셸 명령이 아니라 에이전트에 보내는 요청입니다.

```text
$human-readable-writing 이 PR 설명을 유지보수자가 읽기 좋게 다듬어 주세요.
기술 용어와 사실·수치·조건·불확실성을 보존하고, 개정문만 반환해 주세요.

[이곳에 원문을 붙여 넣어 주세요.]
```

Claude Code에서는 첫 명령만 `/human-readable-writing`으로 바꿉니다. 번역을 요청하지 않았다면 원문의 언어를 유지합니다. 모델이 모든 사실을 보존한다고 보장하지 않으므로 결과를 공개하기 전에 원문과 대조합니다.

## CLI로 설치한 사본 업데이트

프로젝트 설치는 설치했던 프로젝트에서 실행합니다. `-p`와 `-g`는 서로 다른 설치 범위를 선택합니다.

```sh
# 현재 프로젝트
npx skills update human-readable-writing -p

# 사용자 전역 설치
npx skills update human-readable-writing -g
```

설치에 사용한 도구로 업데이트합니다. 수동 링크한 checkout은 Git으로 업데이트하며 CLI가 관리하는 설치라고 가정하지 않습니다. 업데이트 후 새 에이전트 세션을 시작합니다.

## CLI로 설치한 사본 삭제

현재 프로젝트의 사본은 다음 명령으로 삭제합니다.

```sh
npx skills remove human-readable-writing -a codex -a claude-code
```

사용자 전역 사본에는 `-g`를 추가합니다.

```sh
npx skills remove human-readable-writing -a codex -a claude-code -g
```

설치하지 않은 도구의 `-a` 옵션은 뺍니다. 한 스킬을 삭제하기 위해 `--all`을 쓰거나, 공용 skills 디렉터리 또는 원본 checkout을 삭제하지 않습니다.

## Checkout에서 수동 설치

Node.js를 사용하지 않는다면 저장소를 복제한 뒤 설치용 하위 디렉터리만 연결합니다. 링크 생성은 checkout 루트에서 실행하며 두 대상 경로가 비어 있어야 합니다.

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

skill="$PWD/skills/human-readable-writing"
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$skill" "$HOME/.agents/skills/human-readable-writing"
ln -s "$skill" "$HOME/.claude/skills/human-readable-writing"
```

이미 복제했다면 checkout 루트에서 `skill=` 줄부터 실행합니다. 사용할 도구의 링크만 생성해도 됩니다. `skills/human-readable-writing`에는 manifest, 한국어 지침, 언어 지원 참조, 에이전트 메타데이터, 라이선스와 출처 고지가 있으므로 디렉터리 전체를 유지합니다. `SKILL.md` 파일만 연결하면 충분하지 않습니다.

수동 프로젝트 설치는 사용할 프로젝트에서 실제 checkout 경로를 지정합니다.

```sh
skill="/absolute/path/to/human-readable-writing/skills/human-readable-writing"
mkdir -p .agents/skills .claude/skills
ln -s "$skill" .agents/skills/human-readable-writing
ln -s "$skill" .claude/skills/human-readable-writing
```

Pi는 `.agents/skills`, oh-my-pi는 `.omp/skills`를 사용하며 `/skill:human-readable-writing`으로 호출합니다. 해당 도구의 제한된 검증 범위는 [도구 지원 문서](tool-support.md)를 확인합니다. 사용자 설정이나 다른 skill provider가 사본 선택에 영향을 줄 수 있으므로 새 세션에서 실제로 선택한 경로를 확인합니다.

수동 링크한 사본을 업데이트하려면 checkout에서 `git pull --ff-only`를 실행하고 변경 사항을 확인한 뒤 새 에이전트 세션을 시작합니다. 직접 수정한 내용이나 브랜치 이력 때문에 Git이 거부하면 먼저 그 문제를 해결합니다. 로컬 변경을 강제로 덮어쓰지 않습니다.

## 기존 루트 링크 이전

이전 설치 안내는 checkout 루트 자체를 연결했습니다. 이제 루트는 스킬이 아니므로 새 하위 디렉터리를 연결해야 합니다. 업데이트한 checkout 루트에서 다음을 실행합니다. 정확히 이 checkout을 가리키는 두 사용자 전역 심볼릭 링크만 교체합니다. 일반 파일·디렉터리, 상대 경로 링크, 다른 checkout을 가리키는 링크는 그대로 두고 확인할 경로를 출력합니다.

```sh
checkout="$PWD"
skill="$checkout/skills/human-readable-writing"
if [ ! -f "$skill/SKILL.md" ]; then
  printf '%s\n' 'Run this from the updated checkout root.' >&2
  exit 1
fi
for base in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
  link="$base/human-readable-writing"
  if [ -L "$link" ] && [ "$(readlink "$link")" = "$checkout" ]; then
    unlink "$link"
    ln -s "$skill" "$link" || exit 1
    printf 'Updated %s\n' "$link"
  else
    printf 'Unchanged; inspect if needed: %s\n' "$link"
  fi
done
```

프로젝트 로컬 루트 링크도 해당 프로젝트의 `.agents/skills/human-readable-writing` 또는 `.claude/skills/human-readable-writing`을 대상으로 같은 확인을 적용합니다. 심볼릭 링크가 아니라 파일을 복사했다면 로컬 수정 사항을 보관한 뒤 해당 스킬 디렉터리만 새 설치물 전체로 교체합니다. 예전 루트 사본과 새 구조를 섞지 않습니다.

## 수동 링크 삭제

Checkout 루트에서 실행합니다. 다음은 이 checkout의 새 설치용 하위 디렉터리를 가리키는 링크만 삭제합니다. Checkout과 다른 스킬, 다른 설치의 링크는 삭제하지 않습니다.

```sh
skill="$PWD/skills/human-readable-writing"
for base in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
  link="$base/human-readable-writing"
  if [ -L "$link" ] && [ "$(readlink "$link")" = "$skill" ]; then
    unlink "$link"
    printf 'Removed %s\n' "$link"
  else
    printf 'Unchanged; inspect if needed: %s\n' "$link"
  fi
done
```

프로젝트 로컬 링크도 해당 경로에서 같은 대상 확인을 적용합니다. 일반 디렉터리라면 수정 전에 내용을 확인합니다. 위 절차는 디렉터리를 재귀 삭제하지 않습니다.

## 스킬이 보이지 않을 때

- 설치·업데이트 후 새 세션을 시작합니다.
- 현재 프로젝트에 설치했는지, 의도적으로 사용자 전역 `-g`를 선택했는지 확인합니다.
- 같은 이름의 기존 설치를 먼저 확인합니다. 가까이에 있는 README와 에이전트가 읽은 사본이 같다고 추정하지 않습니다.
- 설치된 디렉터리에 `SKILL.md`, `MANIFEST.md`, `references/`, `agents/`가 있는지 확인합니다.
- 명시적 호출 정책을 유지합니다. Codex는 `allow_implicit_invocation: false`, 호환 도구는 `disable-model-invocation: true`를 사용하며 별도 사용자 설정 변경은 요구하지 않습니다.
- OpenCode의 부분 지원 경고를 유지합니다. CLI가 OpenCode 설치를 지원해도 기록된 사본 선택·참조 로딩·원문 조건 변경 문제가 해결된 것은 아닙니다.

설치 실패나 원문 의미 변경은 [issue 양식](https://github.com/JangHyun-bin/human-readable-writing/issues/new/choose)으로 보고합니다. 인증정보, 개인 경로, 회사 문서나 비공개 원문은 제거합니다.
