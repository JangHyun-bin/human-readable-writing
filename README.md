<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing" width="100%">
</p>

<p align="center"><strong>English</strong> · <a href="README.ko.md">한국어</a></p>

Human-readable writing is a portable agent skill for technical prose. The project targets Claude Code, Codex, OpenCode, Pi, and oh-my-pi; verification coverage differs by runtime. Call it with a PR description, incident update, research note, or operational guide. Your agent then edits the text so that a reader can follow what happened, why a claim holds, and what to do next.

The skill is a set of Markdown instructions for the agent's model and contains no scripts. The instructions ask the model to rewrite compressed noun phrases as sentences that say who does what. They also ask it to keep technical terms and source facts, to place each condition and uncertainty next to the claim it limits, and to order information for the reader's task. When the source leaves a relationship unclear, the instructions tell the model to ask about it instead of inventing one.

The skill started as a personal writing tool, and its evaluation is limited. Recorded checks show that it loads in specific runtime versions and that a few outputs kept their source facts. Gains in human comprehension, reading time, or general writing quality have not been established.

## Example

This PR description is an illustration, written to show the intended edit. It is not output from a recorded run.

**Before**

> To prevent previous-user data from reappearing when a profile response arrives after logout, this change gates screen updates on a match between the `sessionVersion` captured when the request starts and its current value when the response arrives, with the value incremented on logout. In-flight requests are not cancelled, and the behavior has been checked only in a browser.

**After**

> A profile response that arrives after logout can put the previous user's data back on screen. This change prevents that by incrementing `sessionVersion` on logout. When a response arrives, the app updates the screen only if the version saved when the request started still matches the current version.
>
> In-flight requests are not cancelled. The behavior has been checked only in a browser.

The revision states the problem and the fix first. It then explains when the app saves, changes, and compares the version. The version-match condition, the uncancelled in-flight requests, and the browser-only check remain explicit.

The [examples page](examples/README.md) adds the request to type and the facts each revision kept. It also shows an incident update recorded in a dated runtime check, together with the limits of that check.

## Install

You need:

- An installed agent runtime. See the [target runtimes and current coverage](docs/tool-support.md).
- Node.js 22.20 or later if you use the [`skills` CLI](https://github.com/vercel-labs/skills). Run `node --version` to check. Manual installation does not require this CLI.

The following CLI example selects Codex and Claude Code. Run it from the root of the project where you want to use the skill:

```sh
npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code
```

This command installs the skill for that project only. Codex reads it from `.agents/skills/`, and Claude Code reads it from `.claude/skills/`. Keep only the `-a` options for agents you use.

For Pi, replace the agent options with `-a pi`; Pi also uses `.agents/skills/`. For oh-my-pi, use the [manual installation guide](docs/install.md). OpenCode is also a target, but its [current support is partial](docs/tool-support.md#opencode-limitation). The CLI supporting an agent does not establish that this skill works in every configuration. Start a fresh session after installing.

To install for your user account instead, so that every project can use the skill, add `-g`:

```sh
npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code -g
```

The 2026-11-02 runtime checks did not cover user-level installs. See [verification](docs/verification.md) for the current install checks.

The `skills` CLI sends anonymous usage data. For a public GitHub repository such as this one, the data includes the repository and skill names. To turn it off, set `DISABLE_TELEMETRY=1` when you run the CLI. The CLI's [telemetry notes](https://github.com/vercel-labs/skills/blob/main/docs/troubleshooting.md#telemetry) give details.

The [installation guide](docs/install.md) covers manual installation from a clone, updates, removal, and migration. Earlier instructions linked the repository root into a skills directory. The skill now lives in `skills/human-readable-writing/`, so replace those links as the guide describes.

## Use

Use your runtime's invocation from the table and include the text you want edited. The example below uses Claude Code; the writing instructions are shared across runtimes.

| Runtime | Command |
|---|---|
| Codex | `$human-readable-writing` |
| Claude Code | `/human-readable-writing` |
| Pi | `/skill:human-readable-writing` |
| oh-my-pi | `/skill:human-readable-writing` |
| OpenCode | Native skill selection; [CLI invocation is not reliably verified](docs/tool-support.md#opencode-limitation). |

```text
/human-readable-writing Revise this PR description for a maintainer.
Preserve the technical terms, facts, conditions, and uncertainty.

[Paste the description here.]
```

Use the skill explicitly; runtimes differ in how they select it. The instructions ask the model to follow the language and format you request and to keep identifiers, quantities, units, exclusions, negation, and uncertainty. They do not force one sentence per paragraph. One recorded OpenCode run changed a source condition, so compare each result with its source before you use it.

There are no runtime-specific copies of the writing rules. [Tool support](docs/tool-support.md) describes installation paths, observed behavior, and remaining compatibility work for all five targets.

## Runtime support

The current package was exercised with Claude Code 2.1.321 in project and user scopes, Pi 1.4.0, and oh-my-pi 18.18.6. Native Codex 0.167.0 could not be verified with the test account because its provider rejected the selected models. The [current verification record](docs/verification.md) records those errors, the checked models, and output limitations rather than treating them as passes.

On 2026-11-02, project installations of Codex 0.166.0, Claude Code 2.1.312, Pi 1.4.0, and oh-my-pi 18.15.0 passed bounded checks. In each runtime, the skill loaded for one English and one Korean request, the model read the required instruction files, and both outputs kept the checked source facts. In one control request per runtime that did not name the skill, the runtime did not load it. These checks linked the repository root at commit `4fff511` into disposable projects, before the skill moved to `skills/human-readable-writing/`. They did not test the current layout, the `skills` CLI, or user-level installs.

**OpenCode 2.2.1 is partially verified, with failures.** One English native load succeeded. CLI mentions did not reliably select the intended copy of the skill, supporting files did not always resolve, and one output changed a source condition.

[Tool support](docs/tool-support.md) lists the tested versions, models, paths, and limits. [Verification](docs/verification.md) records the checks of the current package and install commands. Neither record establishes general writing quality.

## Languages

The skill follows the language you request. Without a translation request, it keeps the source language. **English and Korean have equal priority for documentation and validation.** That priority does not limit which languages you can request. The English and Korean READMEs carry the same installation, use, support, and evidence facts.

The shared [writing principles](skills/human-readable-writing/MANIFEST.md) are in one English file. Korean writing and mixed Korean and English writing also use the [Korean guidance](skills/human-readable-writing/references/korean.md). The language of the instructions does not set the output language.

Existing translations: [Français](README.fr.md) · [中文（简体）](README.zh-CN.md) · [日本語](README.ja.md). They are translated guides, not validated language releases, and no development order is set among them. [Language support](skills/human-readable-writing/references/language-support.md) describes the scope and the recorded language checks.

## Evidence and limits

| Record | What was observed |
|---|---|
| [Native runtime checks, 2026-11-02](research/runtime-validation-20261102.json) | Four runtimes passed bounded checks, and OpenCode had mixed results. The record keeps versions, commands, outputs, file-read evidence, and limits. |
| [English and Korean workflow cases, 2026-11-01](skills/human-readable-writing/references/language-support.md#workflow-check) | Both instruction versions passed the agent's source-fidelity and format checks. No improvement or runtime-compatibility claim follows. |
| [Five Korean document comparisons](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | One user's preferences for paragraphs, tables, and information order. |
| [12 layout generations](research/layout-generation-pilot.md) | Unsupported verification claims and shifts in uncertainty led to deferring adoption. |
| [Four source-fidelity generations](research/source-fidelity-pilot.md) · [Six follow-up cases](research/source-fidelity-six-audit.json) | Both arms passed the four-generation comparison. The six-case follow-up had no concurrent comparison arm. Neither established superiority. |

These records concern the instruction versions they evaluated. Earlier token and timing results do not measure the current skill. Installing the skill does not install the maintainer's separate [global-core pilot](research/native-pilot.md).

## Report a problem

Open an issue with the form that matches the problem. You can write in English or Korean.

- Use the [install or invocation form](https://github.com/JangHyun-bin/human-readable-writing/issues/new?template=install-problem.yml) when the CLI fails, the runtime does not find the skill, or calling the skill does not load it.
- Use the [changed source meaning form](https://github.com/JangHyun-bin/human-readable-writing/issues/new?template=source-meaning-change.yml) when an edit changed a number, a condition, a negation, an exclusion, or the strength of a claim. Use it also when an edit added a relationship that the source did not state.

Issues are public. Remove credentials, personal data, and confidential text before you post. A short made-up source that shows the same change is enough.

The [contributing guide](CONTRIBUTING.md) explains how to propose changes.

## Further reading

- The [skill entry point](skills/human-readable-writing/SKILL.md) and the [writing principles](skills/human-readable-writing/MANIFEST.md).
- The [installation guide](docs/install.md), [tool support](docs/tool-support.md), [verification](docs/verification.md), and [language support](skills/human-readable-writing/references/language-support.md).
- The [validation history](VALIDATION.md), [literature review](research/related-literature.md), and [cost study](research/invocation-cost.md), in Korean.
- The [changelog](CHANGELOG.md).

## License

The material written for this project, including the skill instructions, documentation, and scripts, is available under the [MIT License](LICENSE). Quotations from third-party works and the cited works themselves keep their own terms. [NOTICE.md](NOTICE.md) lists those sources and explains how the license applies to model outputs kept in the research records.

This project began with an analysis of Clark, Martin, and Mahowald's [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1). The skill's guidance is a practical proposal. The paper's authors did not validate or endorse it.
