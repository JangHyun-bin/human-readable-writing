# Human-readable technical writing

## Purpose and scope

Help readers understand what happened, why a claim is warranted, and what decision or action follows. Apply this guidance to technical explanations, pull request descriptions, incident updates, research notes, and instructions.

Keep the requested language, register, spelling variety, and document format. Write idiomatically in that language. Preserve code, identifiers, paths, commands, API names, quotations, and established technical terms. Follow the user's glossary; explain an unfamiliar term when the intended reader needs it.

## Writing principles

1. **Establish the facts before editing the wording.** Identify the actor, action, conditions, observations, and unresolved questions. When the source leaves a relationship unclear, state what needs clarification instead of inventing a connection.
2. **Keep technical names; explain their relationships.** Unpack noun clusters with verbs and explicit links between concepts. Distinguish an established term from a compressed label created for the document.
3. **Keep the main statement easy to follow.** Bring the subject and its action together. Move lengthy interruptions into a separate sentence when that clarifies the relationship. Group closely related actions and conditions; use paragraph breaks at meaningful shifts. Follow a requested layout rather than imposing one sentence per paragraph.
4. **Describe concrete events and actions.** If a metaphor or improvised verb hides what failed, changed, or was prevented, name that event. Keep conventional technical usage.
5. **Preserve the strength and scope of the evidence.** Keep numbers, units, denominators, exclusions, conditions, negation, exceptions, and uncertainty next to the claims they qualify. Distinguish observations, hypotheses, and established causes. Use a table when it makes a comparison easier to inspect, retaining the basis and limits of that comparison.
6. **Order information for the reader's task.** In operational guidance, lead with the current state and the decision or action needed, then explain why. In research interpretation, connect observations to the judgment and its limits. Follow any requested ordering. Use an example where it clarifies a relationship, and remove repetition that adds no meaning.

## Final check

Read the revised text on its own, then compare it with the source:

- Is it clear who or what acts, and under which conditions?
- Can the reader connect each claim to its evidence and limits?
- Are quantities, exclusions, negation, and the target and strength of uncertainty intact?
- Does the text separate what happened, what might explain it, and what has been established?
- If an action is needed, is its owner and completion condition clear from the supplied information?

Revise the unclear parts. If required information is absent, ask a focused question or mark the gap. Sentence length, word count, and noun density are clues to inspect, not pass/fail thresholds.

## Examples

These are illustrative writing examples, not measurements from this project.

### Clarify a compressed label without inventing its meaning

**Source:** `holdout regression dilution mitigation gate`

The label alone does not establish what is measured, whether mitigation has happened, or what permits the next step. Ask for that relationship before rewriting it as a release requirement.

**If the source explanation confirms that progress requires remeasuring the effect of label noise on an independent holdout:**

> Remeasure the effect of label noise on an independent holdout before proceeding.

The relationship comes from the supplied explanation, not from expanding the label by guesswork.

### Preserve exclusions and uncertainty

**Source facts:** A replay analysis reported a drop in median error from 1.4 m to 1.1 m. It included 96 successful sessions out of 120 and excluded 24 failed sessions. The same replay data was used to select the threshold. Android timestamps were snapped to a 10 ms grid. Additional label noise and regression dilution are possible explanations, not established causes. iOS and field performance have not been verified.

**Revised:**

> Median error fell from 1.4 m to 1.1 m across the 96 successful sessions in the replay analysis. The analysis excluded 24 failed sessions out of 120 and used the same data to select the threshold, so this is not an independent holdout result.
>
> Snapping Android timestamps to a 10 ms grid may have introduced label noise. Whether regression dilution explains the result remains unconfirmed. iOS and field performance have not been verified.

The revision retains the denominator, exclusions, selection procedure, and uncertainty. A proposed follow-up evaluation would need to be labeled as a proposal, not as work already agreed or completed.

### Preserve the boundary between a study and an application

**Overstatement:**

> Reasoning training makes AI writing hard to understand, so longer sentences solve the problem.

**Revised:**

> The paper observed linguistic features associated with reading difficulty in English AI-generated text. In a controlled experiment with smaller models, a length penalty increased preference for some shorter grammatical forms. The study did not establish the causes in frontier-model training or show that this writing guidance improves human comprehension.

An observation, a limited experiment, and a proposed writing intervention support different claims.

## Language and user preferences

English is the canonical language of these instructions. Output follows the user's requested language and audience. For Korean and Korean–English writing, use the scoped guidance in [references/korean.md](references/korean.md). A project's language priority does not override an explicit request to write in another language.

The maintainer's earlier preferences for short paragraphs, comparison tables, and observation-first research notes came from five Korean document comparisons. They inform optional layout choices; they are not evidence of a universal rule for English or other languages. Keep tightly connected reasoning together when that reads more naturally.

## Reuse and evidence

Invoke [SKILL.md](SKILL.md) for a writing task. To reuse it in another repository, reference this manifest at its existing accessible location or copy the complete skill directory so its relative references still resolve. Keep this file as the single source for the shared principles. This guidance does not authorize changes to technical behavior or historical evidence.

The starting point was Clark, Martin, and Mahowald's [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1). The writing principles and examples are practical proposals, not an intervention validated by the paper's authors. That study did not directly measure human comprehension of this skill's outputs.

See [language coverage and validation](references/language-support.md) for current scope, and the original [analysis](https://github.com/JangHyun-bin/human-readable-writing/blob/main/ANALYSIS.md), [validation history](https://github.com/JangHyun-bin/human-readable-writing/blob/main/VALIDATION.md), and [attribution record](NOTICE.md) for archived evidence in Korean. The maintainer's separate 61-token global core remains unchanged by this skill.
