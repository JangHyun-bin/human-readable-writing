# Install, update, and remove the skill

[English README](../README.md) · [한국어 README](../README.ko.md)

Use an agent you already have access to. Installing this skill does not install an agent runtime, provide a model account, or make the skill available in a hosted chat application. The instructions below do not require changing your existing agent settings.

## Choose an installation scope

The `skills` CLI requires Node.js 22.20 or later and `npx`. Check the [CLI documentation](https://github.com/vercel-labs/skills) when upgrading the installer. The [current verification record](verification.md) distinguishes what was actually tested from historical compatibility checks.

Claude Code, Codex, OpenCode, Pi, and oh-my-pi are all target runtimes. The CLI examples below select Codex and Claude Code. For Pi, replace those agent options with `-a pi`; oh-my-pi uses the manual `.omp/skills` path below. OpenCode retains its [partial-support limitations](tool-support.md#opencode-limitation). Targeting a runtime does not mean every installation or invocation path has passed verification.

For the current project, run from that project's directory:

```sh
npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code
```

Choose only the agents you use by removing the other `-a` option. To make it available across projects for your user instead, add `-g`:

```sh
npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code -g
```

Do not install into both scopes unless you intend to manage both copies. An existing skill with the same name may be replaced by the installer. Inspect existing entries and retain local edits before proceeding. Do not use `sudo`.

The CLI collects installation telemetry. Prefix a command with `DISABLE_TELEMETRY=1` to opt out, for example:

```sh
DISABLE_TELEMETRY=1 npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code
```

The CLI's list of supported agents is not this project's compatibility claim. See [tested runtimes and limits](tool-support.md).

## Start a fresh agent session

In Codex, begin the request with `$human-readable-writing`; in Claude Code, use `/human-readable-writing`; in Pi and oh-my-pi, use `/skill:human-readable-writing`. For OpenCode, consult the [native activation and CLI limitations](tool-support.md#opencode-limitation) rather than assuming a reliable command. Include the source text and the intended reader. These are prompts inside the agent, not shell commands.

```text
$human-readable-writing Revise this PR description for a maintainer.
Preserve technical terms, facts, numbers, conditions, and uncertainty.
Return only the revised description.

[Paste the description here.]
```

Use `/human-readable-writing` instead for Claude Code. Without a translation request the skill keeps the source language. Compare the result with the source before publishing it; a writing instruction is not a guarantee that a model preserves every fact.

## Update a CLI-managed installation

Run the project command from the project where you installed the skill. The `-p` and `-g` flags select different installations:

```sh
# Current project
npx skills update human-readable-writing -p

# Your user-level installation
npx skills update human-readable-writing -g
```

Use the same installer that created the installation. A manually linked checkout is updated with Git, not by assuming it is tracked by the CLI. Start a new agent session after updating.

## Remove a CLI-managed installation

For the current project:

```sh
npx skills remove human-readable-writing -a codex -a claude-code
```

For your user-level installation:

```sh
npx skills remove human-readable-writing -a codex -a claude-code -g
```

Remove the `-a` option for an agent you did not install to. Do not use `--all`, delete a shared skills directory, or delete your source checkout to uninstall one skill.

## Install manually from a checkout

If you do not use Node.js, clone the repository and link only the installable subdirectory. Run these commands from the checkout root. The destination paths must be unoccupied:

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

skill="$PWD/skills/human-readable-writing"
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$skill" "$HOME/.agents/skills/human-readable-writing"
ln -s "$skill" "$HOME/.claude/skills/human-readable-writing"
```

Already cloned? Start with the `skill=` line from the checkout root. Keep the entire `skills/human-readable-writing` directory. It contains the manifest, Korean guidance, optional language-support reference, agent metadata, license, and source notices. Linking only `SKILL.md` is insufficient.

For a manual project-local installation, run the following from the project where you will use the skill, replacing the checkout path:

```sh
skill="/absolute/path/to/human-readable-writing/skills/human-readable-writing"
mkdir -p .agents/skills .claude/skills
ln -s "$skill" .agents/skills/human-readable-writing
ln -s "$skill" .claude/skills/human-readable-writing
```

Use only the link for your agent. Pi uses `.agents/skills`; oh-my-pi uses `.omp/skills`. Their invocation is `/skill:human-readable-writing`. See [tool support](tool-support.md) for the bounded checks and runtime-specific restrictions. An agent-wide default or third-party provider may change discovery, so verify the selected copy in a fresh session.

To update a manually linked installation, run `git pull --ff-only` from the checkout, inspect the changes, and start a fresh agent session. If Git refuses because you have local changes or a different branch history, resolve that in the checkout rather than overwriting your edits.

## Move an existing root-level link

Older instructions linked the checkout root. That root is no longer a skill. Run this block from your existing checkout root after updating it. It replaces only the two user-level symlinks that point exactly to that checkout. Files, directories, relative links, and links to another checkout are reported and left unchanged:

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

For project-local root links, apply the same check to that project's `.agents/skills/human-readable-writing` or `.claude/skills/human-readable-writing`. If you copied files instead of creating symlinks, retain your local edits and replace only that skill directory with the complete new subdirectory. Do not merge an old root-level copy with the new layout.

## Remove a manual symlink

Run from the checkout root. The following removes only links to this checkout's installed subdirectory, not the checkout, other skills, or another installation:

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

Project-local symlinks can be removed with the same target check using their project paths. If a destination is a regular directory rather than a symlink, inspect it before changing it. The commands above deliberately do not recursively delete directories.

## Troubleshoot discovery

- Start a fresh session after installing or updating.
- Check that you installed into the project where the agent is running, or intentionally selected `-g`.
- Inspect any existing same-named installation before installing another copy. Do not infer that the nearest README is the copy the agent loaded.
- Confirm that the installed directory contains `SKILL.md`, `MANIFEST.md`, `references/`, and `agents/`.
- Keep explicit invocation enabled. Codex metadata sets `allow_implicit_invocation: false`; `SKILL.md` sets `disable-model-invocation: true` for compatible runtimes. No user settings change is required by these instructions.
- For OpenCode, retain the documented partial-support warning. A CLI installer supporting OpenCode does not fix the recorded loading and source-fidelity failures.

Report installation failures or changed source meaning through the repository's [issue forms](https://github.com/JangHyun-bin/human-readable-writing/issues/new/choose). Remove credentials, private paths, and confidential source text first.

## 한국어 안내

프로젝트 설치는 사용할 프로젝트에서 실행하고, 사용자 전역 설치는 `-g`를 추가합니다. 두 범위에 모두 설치했다면 업데이트와 삭제도 범위별로 관리해야 합니다. Codex에서는 `$human-readable-writing`, Claude Code에서는 `/human-readable-writing`으로 명시적으로 호출합니다.

수동 설치는 저장소 루트가 아니라 `skills/human-readable-writing` 디렉터리를 연결합니다. 기존 루트 링크를 옮길 때는 위 이동 절차처럼 대상이 해당 checkout과 일치하는 링크만 바꿉니다. 다른 디렉터리나 파일을 강제로 덮어쓰지 않습니다. 모델에 보낼 원문에 비밀정보가 포함돼 있는지 확인하고, 결과의 수치·조건·부정·불확실성을 원문과 대조해 주세요.
