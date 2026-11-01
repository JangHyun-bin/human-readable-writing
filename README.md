<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing" width="100%">
</p>

<p align="center">
  <strong>A writing skill for clear, precise technical prose.</strong><br>
  Built for Codex and Claude Code.
</p>

<p align="center">
  <strong>English</strong> · <a href="README.ko.md">한국어</a> · <a href="README.fr.md">Français</a> · <a href="README.zh-CN.md">中文（简体）</a> · <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="MANIFEST.md">Writing principles</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#languages">Languages</a> ·
  <a href="#evidence-and-limits">Evidence</a>
</p>

---

Make it clear who did what, under which conditions, and what the evidence supports. Use this skill for pull request descriptions, incident updates, research notes, and operational guidance.

## The same facts, easier to follow

An illustrative example adapted from a [preserved Korean writing case](research/structure-layout-responses.json). It is not a new measurement or an English preference test.

**Before**

> The evaluator reported a median error of 0.8 m across 68 of the 80 sessions, excluding the 12 that timed out; errors for the timed-out sessions were not calculated.

**After**

> Of the 80 sessions, 12 timed out. The evaluator reported a median error of 0.8 m across the remaining 68 sessions.
>
> Errors were not calculated for the 12 timed-out sessions.

The revision makes the measured group and the excluded group explicit while keeping the numbers and limits intact.

## Quick start

After installing the skill, invoke it and include the text you want to revise.

**Codex**

```text
$human-readable-writing Revise this pull request description for a maintainer.
Preserve the technical terms, facts, conditions, and uncertainty.
```

**Claude Code**

```text
/human-readable-writing Clarify this incident update.
Keep observations, possible causes, and unverified claims distinct.
```

The skill reads [MANIFEST.md](MANIFEST.md) when invoked and reuses guidance already in context. The output follows the requested language; editing preserves the source language unless you ask for a translation.

## What it changes

| What to inspect | How to improve it |
|---|---|
| Dense noun clusters | Make the actors, actions, and relationships explicit. |
| Interruptions and nested conditions | Keep the main statement easy to follow and related conditions together. |
| Comparisons across several conditions | Use a table when it clarifies the comparison; retain units, scope, and caveats. |
| Operational guidance | Lead with the current state and the decision or action needed, then explain why. |
| Research interpretation | Connect observations to the judgment and its limits. |

**What stays intact:** technical names, identifiers, quantities, units, exclusions, negation, and the target and strength of uncertainty. Missing relationships stay unresolved until the source supports them.

Paragraphs follow the reasoning and the requested format. A preference for one sentence per paragraph is not imposed across languages or document types.

## Installation

Clone with an account that can access this repository. Run the linking commands **from the repository root**, with both destination skill paths unoccupied.

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD" "$HOME/.agents/skills/human-readable-writing"
ln -s "$PWD" "$HOME/.claude/skills/human-readable-writing"
```

Both runtimes read the same checkout. If you have already cloned it, run only the `mkdir` and `ln` commands from that directory.

<details>
<summary><strong>Runtime settings and explicit invocation</strong></summary>

| Runtime | Entry point | Invocation policy |
|---|---|---|
| Codex | `~/.agents/skills/human-readable-writing/SKILL.md` | `agents/openai.yaml` includes `allow_implicit_invocation: false`. |
| Claude Code | `~/.claude/skills/human-readable-writing/SKILL.md` | Merge the `skillOverrides` setting below into the existing settings file. |

Preserve other settings in `~/.claude/settings.json` when adding:

```json
{
  "skillOverrides": {
    "human-readable-writing": "user-invocable-only"
  }
}
```

Cloud sessions that cannot read local skill directories need a separate installation. See the personal-skill guidance for [Codex](https://learn.chatgpt.com/docs/build-skills) and [Claude Code](https://code.claude.com/docs/en/skills).

</details>

<details>
<summary><strong>The maintainer's separate global-core pilot</strong></summary>

The maintainer's personal environment also includes an earlier, compact Korean core in the global instructions. Installing the symlinks above does not install that core.

The core was enabled on 2026-10-29 in `~/.agents/TERMINOLOGY.md`, through the existing Codex and Claude Code instruction paths. It remains unchanged. Its 61-token size is a reference count using `o200k_base`, not a promise about total request usage.

The [original pilot record](research/native-pilot.md) contains the local installation history and reversal commands in Korean. The English-first skill is a separate, explicitly invoked layer.

</details>

## Languages

English is the primary language for authoring the skill, its examples, and its public-facing documentation. Language priority governs development and validation; it does not override the language you request.

| Priority | Language | Current scope |
|---|---|---|
| 1 | English | Canonical instructions, documentation, examples, and workflow checks. Native-reader evaluation is pending. |
| 2 | Korean | [Korean guide](README.ko.md), scoped language guidance, and the existing personal pilot evidence. |
| 3 | French | [French README](README.fr.md) available. Language-specific guidance and output validation are still planned. |
| 4 | Simplified Chinese | [Simplified Chinese README](README.zh-CN.md) available. Language-specific guidance and output validation are still planned. |
| 4 | Japanese | [Japanese README](README.ja.md) available. Language-specific guidance and output validation are still planned. |
| 4 | Other languages | Planned; localized documentation and language-specific validation have not been completed. |

The five READMEs cover the same installation and usage path. Shared agent instructions remain in English; localized documentation does not establish native-level output quality.

[Language support and validation criteria](docs/language-support.md) distinguish translated documentation, observed agent behavior, and native-reader validation.

## Evidence and limits

**This is an evolving personal writing tool.** The guidance combines literature-informed ideas with recorded editing preferences. Improvements in human comprehension or reading time have not been established.

| Evidence | What it supports |
|---|---|
| [English-first workflow check](docs/language-support.md#workflow-check) | Limited checks of language choice, requested format, and source fidelity; not proof of native-level quality. |
| [Five Korean document comparisons](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | One user's preferences for paragraphs, tables, and information order. |
| [12 layout generations](research/layout-generation-pilot.md) | Adoption was deferred after unsupported verification claims and shifts in uncertainty were found. |
| [Four source-fidelity generations](research/source-fidelity-pilot.md) | Both arms passed; superiority of the revised version was not established. |
| [Six revised-core cases](research/source-fidelity-six-audit.json) | All six met the agent's meaning and format criteria; there was no concurrent comparison arm. |

The earlier generation studies used Korean technical prose. Their experimental 93-token revised core is distinct from the 61-token global core and the full manifest. Results from those studies do not validate the new English-first skill.

## Further reading

| Purpose | Documents |
|---|---|
| Shared writing guidance | [Manifest](MANIFEST.md) · [Skill entry point](SKILL.md) |
| Language-specific guidance | [Korean](references/korean.md) · [Coverage and validation](docs/language-support.md) |
| Original paper analysis, in Korean | [Analysis](ANALYSIS.md) · [Evidence review](research/evidence-review.md) |
| Related literature and applications, in Korean | [Literature notes](research/related-literature.md) · [Two-paper application](research/two-paper-application.md) |
| Earlier cost and timing studies, in Korean | [Invocation cost](research/invocation-cost.md) · [Fixed-budget comparison](research/core-refinement.md) · [Blinded outputs](research/core-refinement-blind.md) |
| Historical validation and preferences, in Korean | [Validation log](VALIDATION.md) · [Layout preferences](research/structure-layout-pilot.md) |

Instructions consume input tokens even when they require no additional file reads. Earlier token and latency measurements do not measure the cost of this revision.

---

This project began with an analysis of Thomas Hikaru Clark, Matias B. Martin, and Kyle Mahowald's [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1). Its writing guidance and examples are separate practical proposals, not interventions validated or endorsed by the paper's authors.

The original paper is available under CC BY 4.0. The [attribution record](NOTICE.md), in Korean, identifies sources and their separate licenses. **This repository does not yet have a separate distribution license.**
