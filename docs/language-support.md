# Language support and validation

Korean and English are equal primary languages of this project. Maintain a complete user path in both: documentation, invocation examples, writing guidance, and language-appropriate evaluation tasks. This is a maintenance priority, not a claim that native-level quality or human comprehension gains have been validated.

The requested output language always takes precedence. Editing without a language instruction preserves the source language. Shared instructions are written in English; that does not require translating other requests into English.

## Current scope

| Maintenance scope | Language | Available material | Remaining work |
|---|---|---|---|
| Primary | Korean | [Korean README](../README.ko.md), scoped language guidance, workflow checks, and personal editing records | Bounded runtime checks recorded; continued reader feedback on real work |
| Primary | English | [English README](../README.md), shared instructions, original English workflow requests, and validation summary | Bounded runtime checks recorded; further native-reader review of real work |
| Translation | French | [French README](../README.fr.md) | Output validation and language-specific guidance where needed; no scheduled priority |
| Translation | Simplified Chinese | [Simplified Chinese README](../README.zh-CN.md) | Output validation and language-specific guidance where needed; no scheduled priority. Traditional Chinese documentation is not provided |
| Translation | Japanese | [Japanese README](../README.ja.md) | Output validation and language-specific guidance where needed; no scheduled priority |
| Unscheduled | Other languages | No maintained documentation or language-specific evaluation | Establish a use case and review capacity before adding a language |

French, Chinese, and Japanese are not labeled as validated language releases. A model's ability to produce those languages does not establish that this skill has been evaluated for them.

The Korean and English READMEs are maintained together. Installation, invocation, support status, and evidence must agree; examples and wording can differ to suit each language. Keep existing translations accessible and correct shared facts when they change, without promising equal editorial coverage. Further language work depends on actual use and review capacity, not a fixed ranking among French, Chinese, and Japanese.

The shared skill instructions remain in one English manifest. Add language-specific guidance only where it changes a concrete writing decision. The dated checks below retain the policy and instruction versions used at the time; current maintenance gives Korean and English equal priority.

## What native support requires

- **A complete user path.** A reader can discover, install, invoke, and understand the skill in the language being supported.
- **Language-appropriate writing.** Examples and tasks originate in that language and use natural terminology, sentence structure, and paragraph flow. A translated README alone is insufficient.
- **Source fidelity.** Quantities, exclusions, conditions, negation, and uncertainty survive the edit. Missing relationships remain unresolved until the source supplies them.
- **Separate quality evidence.** Check instruction compliance and source fidelity, then obtain native-reader judgments on clarity and naturalness. Record personal preference separately from comprehension or reading-time measurements.

Keep shared semantic rules in [MANIFEST.md](../MANIFEST.md). Add language-specific references only where they change a concrete writing decision. English tasks do not load the [Korean guidance](../references/korean.md). The maintainer's earlier short-paragraph preference is scoped to that user's Korean work rather than treated as a universal language rule.

## Workflow check

On 2026-11-01, five requests were fixed before the instruction revision: an English PR description, an incident update, a research note, an ambiguous release requirement, and a Korean operational notice. The English requests were authored in English rather than translated from the earlier Korean benchmark.

One fresh agent context used the previous skill from commit `88ec41b0cda9c48fa78ecd71d0a4b85bcb24218b`. A separate fresh context used the revised skill. Each agent processed the same five requests in one context and returned the requested prose. The lead agent compared all ten outputs with the source facts and requested formats.

| Check | Previous skill | Revised skill |
|---|---|---|
| English PR: write outcome, client-only scope, test coverage, untested logout overlap; one paragraph | Pass | Pass |
| English incident: time window, counts, status code, possible cause, sequence without causal proof, unknown retries | Pass | Pass |
| English research: medians, overlapping ranges, excluded timeouts, missing latency measurements, limited conclusion | Pass | Pass |
| English ambiguous requirement: request the missing relationship without inventing a release condition | Pass | Pass |
| Korean notice: correct output language, existing results, failure before app-server startup, no extra generation | Pass | Pass |

[Requests, verbatim outputs, source checks, and file hashes](../research/english-first-checks.json) are retained. Both instruction versions passed these checks. No improvement claim follows from this result.

A subsequent document review clarified that copying the complete skill directory preserves the Korean reference path. The outputs were not regenerated for that reuse-instruction edit; the evidence file records the evaluated and published instruction hashes separately.

Each instruction version was checked on five cases, with one output per case. Within each version, the same agent context handled all five cases. This was a small, unblinded check. It included no comparison against unguided outputs, no repeated statistical comparison, and no independent human review.

Agents were told to read the skill files. The check did not exercise normal runtime discovery, a new Codex session, or invocation in Claude Code.

For this revision, native-level English quality, human comprehension, reading time, token cost, and latency remain unmeasured.

## Earlier evidence

The earlier [validation history](../VALIDATION.md), [literature notes](../research/related-literature.md), and [personal preference record](../research/native-pilot.md) remain in their original Korean form. They are historical evidence, not new English-language trials.

- The five document comparisons recorded one user's layout preferences.
- The 12-generation layout pilot exposed unsupported verification claims and changes to uncertainty; adoption was deferred.
- The four-generation source-fidelity comparison passed in both arms and did not establish superiority.
- The six-case follow-up checked the revised core alone and passed the agent's meaning and format criteria.

The old 61-token global core, 93-token experimental core, frozen protocols, and benchmark runner remain unchanged. Earlier token and timing results do not measure the instruction revision evaluated on 2026-11-01.

The work draws on Clark, Martin, and Mahowald's [AI-language analysis](https://arxiv.org/abs/2610.29162v1), Reinhart et al.'s [human/LLM style comparison](https://arxiv.org/abs/2410.16107), and Martínez, Mollica, and Gibson's [legal-language study](https://www.pure.ed.ac.uk/ws/files/256304933/Poor_Writing_MARTINEZ_DOA17022022_VOR_CC_BY_NC_ND.pdf). These sources motivate writing ideas; none validates this skill's outputs. The original [attribution record](../NOTICE.md) distinguishes the sources and their licenses.

## Real-document reading preference

On 2026-11-01, the maintainer compared the original limitations paragraph above with an edited version in the existing conversation and a side-by-side HTML page, then selected B (the edit). [The preference record](../research/english-document-preference-20261101.json) retains both presented texts and the exact response. No reason was given. Wording, information order, and paragraph breaks changed together, so this is a preference for the whole passage.

The document adopts B’s three-paragraph structure with one fidelity correction: the middle paragraph removes an unsupported causal link and keeps the three untested runtime items explicit. That corrected wording was not separately rated. This single comparison does not establish a general English writing rule, an isolated skill effect, or completed native-reader validation.

## Next validation work

Use real Korean and English PR descriptions, incident updates, and research notes under the shared manifest. Include mixed Korean–English terminology and requests that must preserve uncertainty or ask about a missing relationship. Retain the original requests and outputs, check meaning separately, and collect reader feedback on wording and flow in each language.

The [2026-11-02 runtime checks](../research/runtime-validation-20261102.json) cover fresh-session invocation and reference loading for four runtimes, with mixed OpenCode results. See [tool compatibility](tool-support.md) for tested versions, models, paths, and remaining limitations. Repeat the checks when runtime behavior or skill instructions change. A successful load is not a writing-quality evaluation, and the dated writing checks above do not validate later instruction revisions. Further language evaluation remains unscheduled until there is a concrete use case and a reviewer for that language.
