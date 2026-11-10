# Tool compatibility

Keep the complete installable directory at `skills/human-readable-writing`. Required guidance and agent metadata ship together; research logs and repository documentation do not need to be installed. [Installation, updates, removal, and migration](install.md) describe the current layout.

## Current distribution checks

The current native first-use path is verified with Claude Code 2.1.321 in project and user scopes. Pi 1.4.0 and oh-my-pi 18.18.6 also loaded the package in bounded project checks. Native Codex 0.167.0 was blocked by provider version/account errors with the test account. These are different outcomes, not four current passes. The verification record also notes a formatting failure and unsupported additions in some outputs.

See the [current verification record](verification.md) for tests of this layout, installer lifecycle, exact runtime versions, and installation scopes. A previous successful load does not validate a later layout, runtime, model, or installation scope. Neither runtime compatibility nor a source-fidelity check establishes improved human comprehension or general writing quality.

Claude Code, Codex, OpenCode, Pi, and oh-my-pi are all target runtimes. The latest test results describe observed coverage, not the project's full support goal. CLI instructions cover Codex, Claude Code, and Pi; oh-my-pi also has a manual path. OpenCode support remains partial. The installer supporting an agent is not evidence that this skill works reliably in that agent, and completing OpenCode compatibility remains part of the support goal.

## Historical observations, 2026-11-02

The following records apply to skill commit `4fff511` and its then-current root-level layout. [Commands, inputs, outputs, file-read evidence, hashes, and judgments](../research/runtime-validation-20261102.json) are preserved unchanged. These observations are not silently relabeled as tests of the new layout.

| Runtime | Model | Tested project entry point | Recorded result |
|---|---|---|---|
| Codex 0.166.0 | Configured default `gpt-6-astra` | `.agents/skills/human-readable-writing` → `$human-readable-writing` | Pass in bounded English/Korean invocation and reference-loading checks; no target load in one uninvoked control. |
| Claude Code 2.1.312 | `claude-sonnet-5-5` | `.claude/skills/human-readable-writing` → `/human-readable-writing` | Pass in the same bounded checks; explicit slash invocation remained available. |
| Pi 1.4.0 | `openai/gpt-5.4-mini` | `.agents/skills/human-readable-writing` → `/skill:human-readable-writing` | Pass in the same bounded checks. |
| oh-my-pi 18.15.0 | `openai/gpt-5.4-mini` | `.omp/skills/human-readable-writing` → `/skill:human-readable-writing` | Pass in print mode; interactive completion was not tested. |
| OpenCode 2.2.1 | `venice/deepseek-v4-1-flash-1017-uncensored` | `.opencode/skills/human-readable-writing` with CLI mentions and experimental native activation | Partial, with failures selecting the intended copy, resolving references, and preserving a source condition. |

The four passing runtimes retained language, quantities, units, exclusions, negation, conditions, and uncertainty in one English and one Korean incident update. There were no human-reader evaluations or repeated statistical trials. Codex's Korean run also loaded a pre-existing `korean-report-style` skill, so this was not an isolated estimate of this skill's effect. Codex's historical model name came from configuration, not its JSON event stream. Historical user-global installations were not independently tested.

## Current manual project paths

From the project where you will use the skill, set the actual checkout path and run only the block for your agent. Each destination must be unoccupied:

```sh
skill="/absolute/path/to/human-readable-writing/skills/human-readable-writing"

# Codex or Pi
mkdir -p .agents/skills
ln -s "$skill" .agents/skills/human-readable-writing

# Claude Code
mkdir -p .claude/skills
ln -s "$skill" .claude/skills/human-readable-writing

# oh-my-pi
mkdir -p .omp/skills
ln -s "$skill" .omp/skills/human-readable-writing
```

Start a fresh session in that project and invoke the skill using the table's syntax. To test an independent copy instead, copy the complete installable directory, not the repository root or `SKILL.md` alone. Instructions for user-global Codex and Claude Code links, collision checks, and removal are in the [installation guide](install.md).

## Explicit invocation policy

Packaged `agents/openai.yaml` keeps Codex's `allow_implicit_invocation: false`. Packaged `SKILL.md` keeps `disable-model-invocation: true` for runtimes that support it. Do not remove these fields merely to make a generic Agent Skills validator accept its narrower frontmatter schema. No user-level `skillOverrides` change is required by this project's instructions.

The 2026-11-02 record observed no target skill tool load in one uninvoked control per runtime. That is not proof that every host configuration prevents implicit use. Claude's initialization inventory listed the skill both before and after the metadata change, which did not establish whether the model was shown its description. Explicit slash invocation loaded the manifest after the change. Existing user overrides and other skills can still affect behavior.

## OpenCode limitation

In the historical checks, CLI `@human-readable-writing` requests found older copies or did not select the intended project skill consistently. Explicit session location and a physical copy helped one English case, not the equivalent Korean request. Experimental native activation loaded Korean references after searching but failed English reference resolution in another run. That output also replaced “if the retry limit is zero, the client does not retry” with an unsupported restriction to positive limits.

These results do not justify advertising a generally reliable CLI mention or API workaround. Moving files or using a CLI installer is not a demonstrated fix. Before relying on OpenCode, verify the selected copy and repeat both language cases and an uninvoked control in a fresh session. OpenCode 1 is outside these records.

## Official references

- [Codex skills](https://learn.chatgpt.com/docs/build-skills).
- [Claude Code skills](https://code.claude.com/docs/en/skills).
- [Pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md).
- [oh-my-pi skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md).
- [OpenCode 2 skills](https://opencode.ai/v2/docs/skills/), [CLI](https://opencode.ai/v2/docs/cli/), and [API](https://opencode.ai/v2/docs/api).

## 한국어 요약

현재 설치물은 `skills/human-readable-writing`이며, [설치 안내](install.md)의 새 경로를 사용합니다. 이번 구조·설치 범위의 검증은 [현재 검증 기록](verification.md)에서 확인합니다. 이전 프로젝트 로컬 검증을 새 구조나 사용자 전역 설치의 검증으로 간주하지 않습니다.

과거 Codex·Claude Code·Pi·oh-my-pi 검증은 제한된 사례의 호출·참조 로딩과 원문 보존 관찰입니다. 사람의 이해도나 일반적인 글쓰기 품질 향상을 입증하지 않습니다. OpenCode의 사본 선택·참조 로딩·조건 변경 문제는 이번 문서·배포 정리에서 해결했다고 주장하지 않습니다.
