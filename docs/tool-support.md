# Tool compatibility

Documentation review: 2026-11-02. This records compatibility candidates and remaining work, not completed runtime tests. Keep one complete skill directory so references to `MANIFEST.md` and `references/korean.md` resolve.

## Current status

| Tool | Explicit invocation in its documentation | Project status |
|---|---|---|
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `$human-readable-writing` | Installation documented; `agents/openai.yaml` sets `allow_implicit_invocation: false`. Fresh-session discovery and invocation checks remain pending. |
| [Claude Code](https://code.claude.com/docs/en/skills) | `/human-readable-writing` | Installation documented; README instructs users to set the `user-invocable-only` override. Fresh-session discovery and invocation checks remain pending. |
| [OpenCode 2](https://opencode.ai/v2/docs/skills/) | `@human-readable-writing` | Documentation reviewed; project runtime checks pending. This review does not cover OpenCode 1. |
| [Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md) | `/skill:human-readable-writing` | Documentation reviewed; project runtime checks pending. |
| [oh-my-pi](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md) | `/skill:human-readable-writing` | Documentation reviewed; project runtime checks pending. Interactive commands depend on `skills.enableSkillCommands`. |

The local version check found Codex 0.166.0, Claude Code 2.1.312, and OpenCode 2.2.1. `pi` and `omp` were not found on PATH. Version and help output do not demonstrate that a skill loads or that a model follows it. The earlier [writing workflow check](language-support.md#workflow-check) told agents to read the files directly.

## Proposed integration

OpenCode 2 and Pi document discovery through `~/.agents/skills`, already used by the Codex installation. Claude Code has its own documented link. oh-my-pi's foreign user-level providers are opt-in, so that shared link alone is insufficient to promise discovery; verify a native skill location or the selected provider and active profile.

Claude Code, OpenCode 2, Pi, and oh-my-pi document `disable-model-invocation: true`. Adding it to the shared `SKILL.md` is a candidate for enforcing explicit invocation across these tools, while retaining Codex's existing policy. **That field has not been added in this documentation revision.** The prose instruction to invoke explicitly does not by itself disable a runtime's automatic selection. Claude Code's existing override remains the documented installation step.

Keep the directory name and skill name `human-readable-writing` aligned. Link or copy the full directory rather than distributing a lone `SKILL.md`. Verify which copy wins when a runtime can discover the same skill through multiple paths. No runtime-specific copy of the writing principles or package wrapper is needed for this approach.

## Checks before advertising support

For each runtime, record its version, model, skill revision, installation path, and any relevant settings. Start fresh sessions and retain inputs, outputs, and evidence of skill loading.

1. Confirm that the expected skill is discovered, without a stale or conflicting copy.
2. Invoke it through the documented user command on one English and one Korean editing request. Confirm that it reads the shared manifest and, for Korean, the Korean reference.
3. Check that an ordinary writing request without the command does not automatically load the skill.
4. Check source fidelity in the two outputs: language, numbers, exclusions, negation, and uncertainty. Report these limited checks separately from reader judgments or comprehension measurements.

Run these checks in a disposable project or isolated configuration. Do not change the user's global instructions to conduct them. Mark each runtime independently; a pass in one does not establish support in another.

## 한국어 요약

Codex와 Claude Code는 설치 안내와 명시적 호출 설정을 제공한다. OpenCode 2·Pi·oh-my-pi는 공식 문서의 호환 형식을 확인한 단계다. 다섯 도구 모두 이번 개정에 대한 새 세션의 탐색·호출 검증은 아직 하지 않았다.

공통 지침은 한 벌로 유지한다. 도구를 추가할 때는 설치 경로, 명시적 호출, 한국어 참조 파일 로딩, 자동 호출 억제를 각각 확인해야 한다. 위에서 제안한 `disable-model-invocation: true`는 아직 적용하지 않았으며 기존 Claude Code 설정 안내도 유지한다. 도구에서 스킬을 읽었다는 사실과 글쓰기 품질을 검증했다는 주장은 구분한다.
