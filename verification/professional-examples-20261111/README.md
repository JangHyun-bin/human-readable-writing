# Professional writing examples — 2026-11-11

Five professional genres now have English and Korean source drafts and recorded native revisions: [examples](../../examples/professional/README.md) · [한국어](../../examples/professional/README.ko.md).

Ten initial calls produced nine revisions accepted by separate agent source-fidelity reviews and one rejected Korean finance revision. A separately requested correction addressed that failure; its review was performed by the integration owner. The ten selected revisions therefore include one feedback-corrected result, not ten first-pass successes. All eleven native outputs remain unchanged.

## Snapshot and execution

- Baseline commit: `a0d872b26fe32942e4e5be6080735352b771bddd`. The executed skill includes subsequent working-tree introduction changes; this is not a claim that the snapshot is on the default branch.
- Runtime: Claude Code **2.1.322**. Requested and observed model: **`claude-sonnet-5-5`** for all eleven calls.
- Seven installed-package file hashes are recorded in each attempt and in [summary.json](summary.json). The same package was used for every call, including the correction.
- Each call used a complete skill copy in a disposable project's `.claude/skills/human-readable-writing/`. No existing skill installation or user configuration was replaced.
- Requests explicitly named the skill. Read and Skill were the only tools enabled. Hooks, external MCP servers, and persistent sessions were disabled for these projects.
- All ten initial calls successfully read `MANIFEST.md`; all five Korean calls also read `references/korean.md`. The separate Korean correction read both files too.

The initial commands were:

```sh
python3 verification/run_professional_examples.py --case research --output verification/professional-examples-20261111/research-run --model claude-sonnet-5-5 --workers 2
python3 verification/run_professional_examples.py --case finance --case capex --case policy --case architecture --output verification/professional-examples-20261111/remaining-run --model claude-sonnet-5-5 --workers 5
```

The exact helper used for those initial batches is archived as [runner-source.txt](runner-source.txt), SHA-256 `78170a67fac79639b483f183b9d80a49e6a92fc9413e8fa3abcb72c65a26ab0e`. It is an execution-method snapshot, not a runnable replacement at its archived location. The current [capture helper](../run_professional_examples.py) additionally pins the resolved executable per batch and supports explicit correction requests. It refuses an existing output directory; new runs need a fresh destination.

The two initial manifests are [research](research-run/manifest.json) and [remaining cases](remaining-run/manifest.json). Their original `fidelity_status: not_reviewed` describes capture-time status and is preserved. Subsequent review outcomes are separate records, linked in [summary.json](summary.json).

## Inputs, review and selection

Each case has a fact ledger, independently authored English and Korean originals, source/rights notes, and a separate agent review. Public paper or agency prose was not relabeled a bad draft. Finance and capex data are fictional; the architecture case combines documented webhook constraints with a fictional local system.

Reviews compare the complete original and output against every selected fact, including numbers, units, conditions, uncertainty, actor/identifier distinctions and unsupported additions. This is an agent source-fidelity judgment, not independent professional certification or a human-reader experiment.

The Korean finance failure added “가정했기 때문이다”, creating a causal explanation between two separate assumptions. The [failed review](../../examples/professional/finance/review.md) and [failed output](remaining-run/finance/ko/output.md) are retained. A fresh session received the original, failed revision and explicit feedback through:

```sh
python3 verification/professional-examples-20261111/correct_finance.py
```

The [correction provenance](finance-correction/provenance.json), [feedback](finance-correction/feedback.md), [actual request](finance-correction/finance/ko/request.md), [raw output](finance-correction/finance/ko/output.md), and [integration-owner review](finance-correction/review.md) distinguish that correction from the first attempt. Its helper snapshot is preserved separately in the correction directory. The correction script also refuses to overwrite the recorded attempt.

The [catalog](../../examples/professional/catalog.json) explicitly selects one revision per case/language. This command checks input/request/output hashes, fact-ledger equality, runtime/model/package consistency, complete review coverage, and the selected verdicts, then assembles the English/Korean indexes and summary:

```sh
python3 verification/professional-examples-20261111/assemble.py
```

It does not run models, rewrite captured attempts, decide semantic fidelity, or turn a failed review into a pass. The fact ledgers in run folders are JSON-reserialized snapshots; equality of their content is checked rather than equality of whitespace.

## Published evidence and limits

The records retain exact requests, unedited final document outputs, sanitized stderr, relevant successful file-read evidence, and stream hashes. Full initialization event streams are not published because they can contain local paths and session metadata. Authentication/account details and unrelated user-skill listings are not part of this corpus. Public author/source attribution remains in each case's notes.

This snapshot exercises explicit invocation in Claude Code project copies only. It does not repeat installer update/removal/migration, user-scope installs, uninvoked controls, or checks in Codex, OpenCode, Pi or oh-my-pi. The earlier [distribution record](../../docs/verification.md) retains its own package snapshot and results. Writing-principles text, Korean guidance and explicit-invocation policy were not changed for these examples.

No reader study, reading-time comparison, randomized no-skill comparison, or general success-rate estimate was performed. Source-fidelity acceptance does not establish that the revision is clearer or that the underlying financial, policy, equipment or system proposal has been validated. No live equipment, Stripe integration, landing UI change or deployment was performed in this stage.

## Repository checks

[checks.json](checks.json) records the executed capture-parser tests, corpus assembly, deliberately mismatched-case rejection, local-link check, package-hash comparison, and protected-file comparison against the baseline. These integrity checks supplement, rather than replace, the separate textual reviews.
