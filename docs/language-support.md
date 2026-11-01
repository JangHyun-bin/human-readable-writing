# Language support and validation

English is the primary authoring language of this project. The goal is an end-to-end English experience: documentation, invocation prompts, writing guidance, examples, and evaluation tasks written naturally in English.

The requested output language always takes precedence. Editing without a language instruction preserves the source language. English-first development does not mean translating Korean, French, or other requests into English.

## Development order

| Priority | Language | Implemented scope | Remaining work |
|---|---|---|---|
| 1 | English | Canonical README, skill entry point, manifest, UI prompt, original English workflow requests, and English validation summary | Fresh-session runtime checks and native-reader review of real work |
| 2 | Korean | Localized README, scoped language guidance, and the earlier personal pilot | Continued real-work feedback under the shared manifest |
| 3 | French | Roadmap only | French-authored tasks, language-specific guidance where needed, and native-reader review |
| 4 | Chinese, Japanese, and other languages | Roadmap only | Define the relevant locale/script and audience, then author tasks and validate each language separately |

French, Chinese, and Japanese are not labeled as validated language releases. A model's ability to produce those languages does not establish that this skill has been evaluated for them.

## What native support requires

- **A complete user path.** A reader can discover, install, invoke, and understand the skill in the language being supported.
- **Language-appropriate writing.** Examples and tasks originate in that language and use natural terminology, sentence structure, and paragraph flow. A translated README alone is insufficient.
- **Source fidelity.** Quantities, exclusions, conditions, negation, and uncertainty survive the edit. Missing relationships remain unresolved until the source supplies them.
- **Separate quality evidence.** Check instruction compliance and source fidelity, then obtain native-reader judgments on clarity and naturalness. Record personal preference separately from comprehension or reading-time measurements.

Keep shared semantic rules in [MANIFEST.md](../MANIFEST.md). Add language-specific references only where they change a concrete writing decision. English tasks do not load the [Korean guidance](../references/korean.md). The maintainer's earlier short-paragraph preference is scoped to that user's Korean work rather than treated as a universal language rule.

## Workflow check

On 2026-11-01, five requests were fixed before the instruction revision: an English PR description, an incident update, a research note, an ambiguous release requirement, and a Korean operational notice. The English requests were authored in English rather than translated from the earlier Korean benchmark.

One fresh agent context used the previous skill from commit `88ec41b0cda9c48fa78ecd71d0a4b85bcb24218b`. A separate fresh context used the English-first skill. Each agent processed the same five requests in one context and returned the requested prose. The lead agent compared all ten outputs with the source facts and requested formats.

| Check | Previous skill | English-first skill |
|---|---|---|
| English PR: write outcome, client-only scope, test coverage, untested logout overlap; one paragraph | Pass | Pass |
| English incident: time window, counts, status code, possible cause, sequence without causal proof, unknown retries | Pass | Pass |
| English research: medians, overlapping ranges, excluded timeouts, missing latency measurements, limited conclusion | Pass | Pass |
| English ambiguous requirement: request the missing relationship without inventing a release condition | Pass | Pass |
| Korean notice: correct output language, existing results, failure before app-server startup, no extra generation | Pass | Pass |

[Requests, verbatim outputs, source checks, and file hashes](../research/english-first-checks.json) are retained. Both instruction versions passed these checks. No improvement claim follows from this result.

A subsequent document review clarified that copying the complete skill directory preserves the Korean reference path. The outputs were not regenerated for that reuse-instruction edit; the evidence file records the evaluated and published instruction hashes separately.

This was a small, unblinded agent check with one output per case and version. It was not a no-guidance experiment, a repeated statistical comparison, or an independent human review. The five outputs within each arm shared a context. Agents were directed to read the skill files; normal runtime discovery, a new Codex session, and a Claude Code invocation were not exercised. Native-level English quality, human comprehension, reading time, token cost, and latency remain unmeasured for this revision.

## Earlier evidence

The earlier [validation history](../VALIDATION.md), [literature notes](../research/related-literature.md), and [personal preference record](../research/native-pilot.md) remain in their original Korean form. They are historical evidence, not new English-language trials.

- The five document comparisons recorded one user's layout preferences.
- The 12-generation layout pilot exposed unsupported verification claims and changes to uncertainty; adoption was deferred.
- The four-case source-fidelity comparison passed in both arms and did not establish superiority.
- The six-case follow-up checked the revised core alone and passed the agent's meaning and format criteria.

The old 61-token global core, 93-token experimental core, frozen protocols, and benchmark runner remain unchanged. Earlier token and timing results do not measure this English-first revision.

The work draws on Clark, Martin, and Mahowald's [AI-language analysis](https://arxiv.org/abs/2610.29162v1), Reinhart et al.'s [human/LLM style comparison](https://arxiv.org/abs/2410.16107), and Martínez, Mollica, and Gibson's [legal-language study](https://www.pure.ed.ac.uk/ws/files/256304933/Poor_Writing_MARTINEZ_DOA17022022_VOR_CC_BY_NC_ND.pdf). These sources motivate writing ideas; none validates this skill's outputs. The original [attribution record](../NOTICE.md) distinguishes the sources and their licenses.

## Next English milestone

Use the explicit skill in a new session on real English PR descriptions, incident updates, and research notes. Retain the original requests and outputs, check meaning separately, and collect native-reader feedback on wording and flow. Keep the English-first foundation distinct from a claim that native-reader validation has been completed. Extend the language-specific evaluation to Korean, then French, before Chinese, Japanese, and other languages.
