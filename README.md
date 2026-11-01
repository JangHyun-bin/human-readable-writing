<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing" width="100%">
</p>

<p align="center"><strong>English</strong> · <a href="README.ko.md">한국어</a></p>

A skill for editing technical prose in English and Korean. It clarifies who did what, under which conditions, while preserving facts, technical terms, and uncertainty. Use it for PR descriptions, incident updates, research notes, and operational guidance.

## Example

**Before**

> The evaluator reported a median error of 0.8 m across 68 of the 80 sessions, excluding the 12 that timed out; errors for the timed-out sessions were not calculated.

**After**

> Of the 80 sessions, 12 timed out. The evaluator reported a median error of 0.8 m across the remaining 68 sessions.
>
> Errors were not calculated for the 12 timed-out sessions.

The measured and excluded groups are easier to distinguish; the numbers and limits stay intact. This illustrative example is adapted from a [recorded Korean editing case](research/structure-layout-responses.json), not a measurement of reader comprehension.

## Installation

Clone the repository once, then link the checkout to the local skill directories. Run these commands from the repository root with both destination paths unoccupied. If a path already exists, inspect it before changing it.

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD" "$HOME/.agents/skills/human-readable-writing"
ln -s "$PWD" "$HOME/.claude/skills/human-readable-writing"
```

Already cloned? Run only the `mkdir` and `ln` commands from that checkout. Keep the complete directory: `SKILL.md` reads `MANIFEST.md` and, for Korean writing, `references/korean.md`.

Codex's explicit-invocation policy is included in `agents/openai.yaml`. The shared `SKILL.md` includes `disable-model-invocation: true` for compatible runtimes, including Claude Code; no additional `skillOverrides` entry is needed for the tested Claude Code version. Keep existing unrelated settings.

These instructions cover local sessions. For environments that cannot read these directories, follow the personal-skill instructions for [Codex](https://learn.chatgpt.com/docs/build-skills) or [Claude Code](https://code.claude.com/docs/en/skills).

## Use

Invoke the skill and include the text you want to edit:

| Tool | Start your request with |
|---|---|
| Codex | `$human-readable-writing` |
| Claude Code | `/human-readable-writing` |

```text
$human-readable-writing Revise this PR description for a maintainer.
Preserve the technical terms, facts, conditions, and uncertainty.

[Paste the description here.]
```

The skill follows your requested language and format. Without a translation request, it keeps the source language. It preserves identifiers, quantities, units, exclusions, negation, and uncertainty; it asks about missing relationships instead of inventing them. Paragraphs and tables serve the document's purpose, with no fixed sentence-per-paragraph rule.

## Runtime support

On 2026-11-02, project-local installations passed the bounded English/Korean invocation and reference-loading checks in **Codex 0.166.0, Claude Code 2.1.312, Pi 1.4.0, and oh-my-pi 18.15.0**. One uninvoked control per tool did not load this skill. These checks used disposable projects; the user-level installation above was not independently exercised.

**OpenCode 2.2.1 is partially verified, with failures.** An English native load succeeded, but CLI mentions and supporting-file resolution were inconsistent. An additional output changed a source condition. See [tested installation paths, commands, models, and limitations](docs/tool-support.md), including Pi and oh-my-pi usage. These observations do not establish general writing quality.

## Languages

**English and Korean are equal primary languages.** Both READMEs cover installation, use, support status, and evidence. Examples should read naturally in their own language; changes to these shared facts belong in both documents.

The common [writing principles](MANIFEST.md) stay in one English file. Korean and mixed Korean–English writing also use the [Korean guidance](references/korean.md). The language of the instructions does not dictate the output language.

Existing translations: [Français](README.fr.md) · [中文（简体）](README.zh-CN.md) · [日本語](README.ja.md). These are translated guides, not validated language releases. No development order is assigned among them; further work depends on actual use and language-specific review. See [language support and evidence](docs/language-support.md).

## Evidence and limits

This is a personal writing tool with limited evaluation. Improved human comprehension, reading time, and general writing quality have not been established.

| Record | What was observed |
|---|---|
| [Native runtime checks, 2026-11-02](research/runtime-validation-20261102.json) | Four runtimes passed bounded checks; OpenCode had mixed results. Versions, commands, outputs, file-read evidence, and limits are recorded. |
| [English and Korean workflow cases](docs/language-support.md#workflow-check) | Both instruction versions passed the agent's source-fidelity and format checks. No improvement or runtime-compatibility claim follows. |
| [Five Korean document comparisons](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | One user's preferences for paragraphs, tables, and information order. |
| [12 layout generations](research/layout-generation-pilot.md) | Unsupported verification claims and shifts in uncertainty led to deferring adoption. |
| [Four source-fidelity generations](research/source-fidelity-pilot.md) · [Six follow-up cases](research/source-fidelity-six-audit.json) | Both arms passed the four-generation comparison; the six-case follow-up had no concurrent comparison arm. Neither established superiority. |

These records concern the instruction versions they evaluated. Earlier token and timing results do not measure the current skill. Installing it does not install the maintainer's separate [global-core pilot](research/native-pilot.md).

## Further reading

- [Writing principles](MANIFEST.md) and [skill entry point](SKILL.md).
- [Language policy and validation](docs/language-support.md) and [tool compatibility](docs/tool-support.md).
- [Validation history](VALIDATION.md), [literature review](research/related-literature.md), and [cost study](research/invocation-cost.md), in Korean.

This project began with an analysis of Clark, Martin, and Mahowald's [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1). The skill's guidance is a practical proposal, not an intervention validated or endorsed by the paper's authors. The paper is available under CC BY 4.0; [NOTICE.md](NOTICE.md) records attribution and separate source licenses. **This repository has no separate distribution license.**
