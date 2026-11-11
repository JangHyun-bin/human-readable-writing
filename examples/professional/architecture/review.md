# Architecture source-fidelity review

The review checks whether both native revisions preserve the fictional ADR's source facts and bounded design judgment. Source parity passes. English passes A01 through A10. Korean passes A01 through A10. No material source-fidelity issue or unsupported added claim was found.

## Evidence examined

Examined the complete English and Korean `before` drafts, `sources.md`, current `facts.json`, frozen `remaining-run/architecture/facts.json`, and each language's full `request.md`, `output.md`, and `attempt.json` under `verification/professional-examples-20261111/remaining-run/architecture/`.

The English and Korean source drafts express the same selected facts, conditions, and exclusions. The frozen and current fact ledgers contain the same facts and review checks; their JSON formatting differs. Both requests contain the corresponding complete source draft and an instruction to preserve facts and judgment strength without additions. The source, request, and output SHA-256 values were computed with `shasum -a 256`. Source and request hashes match each attempt's recorded `input_sha256` and `request_sha256`.

Both attempt records report `capture_status=captured`, exit code 0, observed and requested model `claude-sonnet-5-5`, and runtime `2.1.322 (Claude Code)`. Each records a successful read of `.claude/skills/human-readable-writing/MANIFEST.md` and `manifest_read=true`. Korean additionally records a successful read of `.claude/skills/human-readable-writing/references/korean.md` and `korean_reference_read=true`. English records `korean_reference_read=false`. These are inspected derived tool-read records, not an independent inspection of unpublished raw execution streams. Capture success is not the basis of the fidelity verdict.

The computed output hashes match the attempt records:

| Language | Output SHA-256 |
| --- | --- |
| English | `deacba2f25ffe66bda73097fe061fd8703d0b52fc08791d2d471d8dcf936418f` |
| Korean | `fdad8d22ff6441be1dd88b7b858d00627adb6081530414dcf68d62a220d6d70a` |

## Findings

Both outputs preserve the ADR context, decision, alternatives, and consequences. Added lists, subheadings, and alternative tables change presentation without changing the decision.

A01 through A03 retain unordered delivery, second-level timestamp limits, the distinction between repeated delivery and separate duplicate Events, and the qualified object-ID/type recommendation. Neither output turns duplicate handling into suppression of future updates.

A04 through A08 retain raw-body signature verification before durable receipt, durable receipt before successful acknowledgment, and receipt as distinct from business completion. The four arrivals remain E2, E2 again, late E1, and distinct duplicate paid E3. Both retain the three Event IDs, two types, one invoice and order, distinct receipt and operation keys, configured account context, and all identifier mappings. Repeated E2 creates no new work even while pending; it neither discards nor completes that row. Committed receipt work survives a crash before acknowledgment.

A09 retains the single ACID database, concurrency constraints, and atomic ledger insertion, entitlement mutation, and inbox completion. The business transaction cannot commit only completion. E3 can finish its own receipt without a second grant.

A10 retains retrieval, confirmed paid status, matching existing order, pending on failure, and no reversal from late created E1. The eventual one-local-grant conclusion remains conditional on successful processing, database assumptions, and retained records. Both preserve pending retries, contention and recovery costs, and the exclusion of refunds, disputes, subscription changes, external fulfillment, and outbound payment API idempotency. Neither claims global exactly-once execution or implemented Stripe behavior. The application and version remain fictional scenario assumptions, not a live deployment or tested endpoint.

Only text and recorded-evidence review was performed. No native rerun, live Stripe call, build, lint, test, formatter, or reader study was performed. Fact-by-fact verdicts are in `review.json`.
