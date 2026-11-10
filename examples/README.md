# Examples

English · [한국어](README.ko.md)

Each example shows the request, the source text, the revision, and the facts the revision kept. A label says where the revision came from:

- **Illustration.** Written to show the intended edit. It is not output from a recorded run.
- **Recorded output.** Copied unchanged from a dated run record. Another run, model, or instruction version can produce different text.

Neither kind shows that readers understand the revision better. The [README](../README.md) explains how to install and call the skill.

## PR description (illustration)

**Request**

```text
$human-readable-writing Revise this PR description for a maintainer.
Preserve the technical terms, facts, conditions, and uncertainty.
```

**Source**

> To prevent previous-user data from reappearing when a profile response arrives after logout, this change gates screen updates on a match between the `sessionVersion` captured when the request starts and its current value when the response arrives, with the value incremented on logout. In-flight requests are not cancelled, and the behavior has been checked only in a browser.

**Revision**

> A profile response that arrives after logout can put the previous user's data back on screen. This change prevents that by incrementing `sessionVersion` on logout. When a response arrives, the app updates the screen only if the version saved when the request started still matches the current version.
>
> In-flight requests are not cancelled. The behavior has been checked only in a browser.

**Facts kept**

- A profile response that arrives after logout can show the previous user's data.
- Logout increments `sessionVersion`.
- The app updates the screen only if the version saved at request start matches the current version.
- In-flight requests are not cancelled.
- The behavior was checked only in a browser.

## Incident update (recorded output)

Claude Code 2.1.312 produced this output on 2026-11-02 with the `claude-sonnet-5-5` model, in a disposable project. The skill instructions were the version at commit `4fff511`. The [runtime record](../research/runtime-validation-20261102.json) keeps the full command, the files that the runtime read, and the outputs that Codex, Pi, oh-my-pi, and OpenCode produced for the same source.

**Request**, sent with the source in the same message

```text
/human-readable-writing Edit the following incident update in English for an engineering team. Return only the revised prose, in at most two paragraphs. Preserve all facts, numbers, units, negation, conditions, and uncertainty.
```

**Source**

> Between 09:10 and 09:25 UTC, the gateway returned HTTP 503 for 18 of 240 requests. The other 222 requests succeeded. Retried requests were not included in these counts; their outcomes are unknown. If the gateway retry limit is zero, the client does not retry automatically. A cache restart happened before recovery, but causation has not been established. p95 latency for successful requests was 820 ms; latency for failed requests was not measured. A separate replay is proposed, not approved or completed.

**Output**

> Between 09:10 and 09:25 UTC, the gateway returned HTTP 503 for 18 of 240 requests, and the other 222 succeeded. These counts exclude retried requests, whose outcomes are unknown. If the gateway retry limit is zero, the client does not retry automatically.
>
> A cache restart happened before recovery, but we have not established that it caused the recovery. The p95 latency for successful requests was 820 ms. We did not measure latency for failed requests. A separate replay has been proposed; it is neither approved nor completed.

**Facts kept**

The record's manual review marked each of these as kept:

- English, in at most two paragraphs.
- The window from 09:10 to 09:25 UTC.
- HTTP 503 for 18 of 240 requests, and success for the other 222.
- Retried requests excluded from the counts, with unknown outcomes.
- No automatic client retry if the gateway retry limit is zero.
- A cache restart before recovery, with causation not established.
- A p95 latency of 820 ms for successful requests, and no latency measurement for failed requests.
- A separate replay that was proposed but not approved or completed.

This check tested loading and source fidelity, not readability. The same record includes a control in which Claude Code received this request without the skill. That output also kept every checked fact, so one pair of outputs cannot show what the skill changed.

## More records

The [workflow cases from 2026-11-01](../research/english-first-checks.json) add an English PR description, an incident update, a research note, an ambiguous requirement, and a Korean operational notice. In those cases, agents read the skill files directly instead of loading the skill through a runtime. The previous and revised instructions both passed.
