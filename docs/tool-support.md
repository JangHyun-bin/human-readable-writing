# Tool compatibility

Checked on 2026-11-02 against skill commit `4fff511`. [Commands, inputs, outputs, file-read evidence, hashes, and judgments](../research/runtime-validation-20261102.json) accompany these bounded observations. A pass means the stated cases worked in the recorded configuration, not that every model, installation scope, or writing task is supported.

## Observed results

| Runtime | Model | Tested project entry point | Result |
|---|---|---|---|
| Codex 0.166.0 | Configured default `gpt-6-astra` | `.agents/skills/human-readable-writing` → `$human-readable-writing` | Pass: English/Korean invocation, manifest and Korean-reference reads; no target load in one uninvoked control. |
| Claude Code 2.1.312 | `claude-sonnet-5-5` | `.claude/skills/human-readable-writing` → `/human-readable-writing` | Pass: same checks; registered slash command remained available; the uninvoked control made no tool calls. |
| Pi 1.4.0 (`@earendil-works/pi-coding-agent`) | `openai/gpt-5.4-mini` | `.agents/skills/human-readable-writing` → `/skill:human-readable-writing` | Pass: same checks; native command expansion was present in the recorded user message. |
| oh-my-pi 18.15.0 (`@oh-my-pi/pi-coding-agent`, Bun 1.4.4) | `openai/gpt-5.4-mini` | `.omp/skills/human-readable-writing` → `/skill:human-readable-writing` | Pass in print mode: registered `skill://` reads, manifest and Korean reference; no target load in one uninvoked control. Interactive completion was not tested. |
| OpenCode 2.2.1 | `venice/deepseek-v4-1-flash-1017-uncensored` | `.opencode/skills/human-readable-writing` → `@human-readable-writing`; experimental native activation also checked | Partial, with failures: an English native load passed; CLI mentions did not reliably select the correct copy. Native activation loaded Korean references after searching but failed to resolve English references in another run, whose output also changed a condition. |

The four passing runtimes retained the source language, quantities, units, exclusions, negation, conditions, and uncertainty in one English and one Korean incident update. No external authentication blocker remained. There were no human-reader evaluations or repeated statistical trials. Codex's Korean run also loaded the existing `korean-report-style` skill; this is compatibility evidence, not an isolated measurement of this skill's effect. Codex's model name comes from configuration, not its JSON event stream.

## Install and invoke

Keep the **complete skill directory**, including `MANIFEST.md`, `references/`, and `agents/`. Keep its directory name `human-readable-writing`. Use one authoritative checkout; do not create runtime-specific writing rules.

The README documents user-level links for Codex (`~/.agents/skills`) and Claude Code (`~/.claude/skills`). This check exercised the project-local equivalents in the table, not those global links. For a project-local installation, run the following from the project where you will use the skill, replacing the checkout path with your actual checkout:

```sh
# Codex or Pi
mkdir -p .agents/skills
ln -s /absolute/path/to/human-readable-writing .agents/skills/human-readable-writing

# Claude Code
mkdir -p .claude/skills
ln -s /absolute/path/to/human-readable-writing .claude/skills/human-readable-writing

# oh-my-pi
mkdir -p .omp/skills
ln -s /absolute/path/to/human-readable-writing .omp/skills/human-readable-writing
```

Choose the block for your runtime. Each destination must be unoccupied; inspect existing entries rather than overwriting them. Start a fresh session in that project, then use the invocation in the table and append your text. Test sessions used symlinks for these four runtimes. Pi and oh-my-pi were installed into temporary directories; global packages and user configuration were not replaced.

The executable forms used in the checks were `codex exec`, `claude -p`, `pi --print --mode json`, and `omp --print --mode json`. The evidence record retains the complete argument lists, restrictions, prompts, and outputs. Pi/oh-my-pi used the existing OpenAI API environment; Codex/Claude used existing authentication. Credentials are excluded from the record.

## Explicit invocation policy

`agents/openai.yaml` keeps Codex's `allow_implicit_invocation: false`. Shared `SKILL.md` now includes `disable-model-invocation: true`, which the other runtimes document as hiding a skill from automatic selection while retaining explicit use. No additional Claude Code `skillOverrides` entry was used in the passing checks. Existing user overrides can still affect behavior; preserve unrelated settings.

Claude’s initialization inventory listed the skill both before and after the metadata change. That inventory does not establish whether the model was shown its description. Neither the baseline nor post-change uninvoked control loaded the skill, and explicit slash invocation loaded the manifest after the change. No unwanted automatic invocation was demonstrated.

One uninvoked control per runtime produced no target skill tool load. This is a limited observation, not a proof that every host configuration prevents implicit use. A model can follow similar writing advice without loading this skill.

## OpenCode limitation and follow-up

The first `opencode run --standalone --format json '@human-readable-writing …'` sessions did not use the intended project skill and found older copies elsewhere. They do not count as validation of this revision. Setting a session's `location.directory` explicitly and using a physical copy allowed one English request to call the native `skill` tool and read the correct manifest, but the equivalent Korean request again found another checkout.

The documented experimental `session.skill` API successfully activated the installed skill by ID. In the subsequent English request, relative reads failed and the manifest was not read. Its output also replaced “if the retry limit is zero, the client does not retry” with an unsupported restriction to limits above zero. The Korean API case eventually read both intended files and preserved the source. These mixed results do not justify advertising reliable `@` invocation or a generally working API workaround. The directory changes were diagnostic attempts, not proof that symlinks caused the failure.

For now, use one of the four checked runtimes. Before relying on OpenCode, verify the active project and selected skill copy in a fresh session, then repeat both language cases and the uninvoked control. A different model or interactive skill selector needs its own evidence; neither was tested here. OpenCode 1 is outside this review.

## Official references

- [Codex skills](https://learn.chatgpt.com/docs/build-skills): discovery, explicit invocation, and `allow_implicit_invocation`.
- [Claude Code skills](https://code.claude.com/docs/en/skills): slash commands and `disable-model-invocation`.
- [OpenCode 2 skills](https://opencode.ai/v2/docs/skills/), [CLI](https://opencode.ai/v2/docs/cli/), and [API](https://opencode.ai/v2/docs/api): project paths, mentions, session location, and native activation.
- [Pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md): `.agents/skills`, `/skill:name`, and explicit-only metadata.
- [oh-my-pi skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md): native `.omp/skills`, `skill://` resources, and interactive `skills.enableSkillCommands`. Foreign user-level providers are opt-in; a shared user link alone is not sufficient evidence of discovery.

## 한국어 요약

Codex·Claude Code·Pi·oh-my-pi는 기록된 버전·모델·프로젝트 설치에서 한·영 호출, 필요한 참조 파일 읽기, 원문 충실도 검사를 통과했다. 도구별 호출 없는 비교 요청 한 건에서는 대상 스킬을 읽지 않았다. 사용자 전역 설치와 대화형 선택기는 별도로 검증하지 않았다.

OpenCode 2는 일부 네이티브 호출이 성공했지만 잘못된 사본 선택, 참조 경로 처리 실패, 조건 의미 변경이 관찰되어 부분 검증으로 남긴다. 네 도구 중 하나를 사용하거나 OpenCode의 프로젝트·스킬 선택을 확인한 뒤 같은 검사를 다시 수행해야 한다. 현재 결과만으로 안정적인 우회 방법을 보장하지 않는다.

공통 `disable-model-invocation: true`를 적용했고 Codex의 기존 정책도 유지했다. 검증한 Claude Code에는 추가 `skillOverrides` 설정이 필요하지 않다. 설치·명령·입출력과 로딩 근거는 위 기록에 있으며, 인증정보는 포함하지 않는다. 실행 호환성과 제한된 원문 보존 검사는 사람의 이해도나 글쓰기 품질 향상 검증과 구분한다.
