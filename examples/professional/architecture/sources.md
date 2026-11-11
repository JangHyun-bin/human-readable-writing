# Architecture source packet

## Topic, reader, and purpose

This packet supplies an English and Korean architecture decision record for backend implementers and architecture reviewers. The question is whether durable receipt and a local business-operation key can prevent duplicate entitlement grants when invoice events arrive repeatedly and out of order. The application and delivery trace are fictional. This is a professional-writing source example, not an implementation, production proposal, deployment record, or recorded model output.

`facts.json` selects ten groups, A01 through A10. Both `before` drafts contain all ten. The groups separate public webhook constraints from application assumptions and the author's bounded design judgment.

## Official sources and locators

Sources were read on 2026-11-11. The following hashes identify separately retrieved complete response bodies, requested with `Accept: text/markdown`, with retrieval completed at 2026-11-11T08:24:58Z. All four responses reported `text/markdown; charset=utf-8`. These are hashes of dynamic documentation responses, not stable publication editions or hashes of excerpts. No full third-party response body is distributed in this packet.

### S1. Stripe webhook documentation

URL: https://docs.stripe.com/webhooks

SHA-256: `23ec0d42e0618b33a13503b31d0e7c9a3938ad9b48d692ab21ed88e973c35f44`

Response length: 48,050 bytes.

Relevant sections:

- [Event ordering](https://docs.stripe.com/webhooks#event-ordering). Delivery need not follow generation order. Snapshot `created` timestamps are in seconds, may collide, and are unsuitable for event ordering or duplicate identification. The section also permits retrieval of missing objects when `invoice.paid` arrives first.
- [Handle duplicate events](https://docs.stripe.com/webhooks#handle-duplicate-events). The same Event may be delivered repeatedly. Separate Event objects may also be duplicates, for which Stripe recommends the object ID in `data.object` together with `event.type`.
- [Create a handler](https://docs.stripe.com/webhooks#create-a-handler). Signature verification requires the unchanged raw request body. Prompt successful acknowledgment precedes complex business work. The snapshot-handler subsection distinguishes event-time data from a retrieved current resource.
- [Handle events asynchronously](https://docs.stripe.com/webhooks#handle-events-asynchronously) and [Quickly return a 2xx response](https://docs.stripe.com/webhooks#quickly-return-a-2xx-response). These support the separation of receipt from business completion. They do not prescribe this packet's database schema, retention, or transaction design.
- The snapshot event-destination registration example uses `Stripe-Version: 2026-10-28.preview`. This is the documented version chosen as the fictional scenario's version assumption. No endpoint registration was performed.

A01 through A04 paraphrase S1. The qualification in A03 rejects an overgeneralization of the documented duplicate rule. Stripe does not prescribe a permanent suppression policy for every future update to an object.

### S2. Stripe Event object

URL: https://docs.stripe.com/api/events/object

SHA-256: `81768fc3868ada2555aa2aedc6e26e5d475b364cc5059a6d405a9758b9d16abc`

Response length: 2,975 bytes.

Relevant attributes are `id`, `type`, `data`, `created`, `account`, `api_version`, and `pending_webhooks`. `created` is measured in seconds since the Unix epoch. `api_version` identifies the version used to render the event's data, which does not change after creation. `account` describes a connected account and is nullable. Consequently, the fictional single-account application obtains its local `account_id` from configured account context rather than assuming that every payload contains `account`.

The draft's local names map `event_id` to `Event.id`, `event_type` to `Event.type`, and `invoice_id` to the invoice's `data.object.id`. `order_id` and `operation_kind` are application identifiers, not Stripe Event fields. The configured-account choice and composite database keys are original design assumptions, not vendor requirements.

### S3. Stripe snapshot event types

URL: https://docs.stripe.com/api/events/types

SHA-256: `1bfb1e526e1a4e01d687da97a2652a276bd38e08bb397a5542f99779b255fb88`

Response length: 51,696 bytes.

The `invoice.created` entry describes creation of an invoice. The `invoice.paid` entry describes a successful invoice payment attempt or an invoice marked paid out of band. Both carry an invoice in `data.object`. The selected ADR uses only their names and invoice relationship. It does not infer that `invoice.paid` proves a particular charge, cash-settlement method, or external fulfillment result.

### S4. Stripe Invoice object

URL: https://docs.stripe.com/api/invoices/object

SHA-256: `feea3905740bbebbddafecec1cf7cd45ba72fc6f7c06f0f9cafe4376808c4ff3`

Response length: 21,234 bytes.

The `id` and `status` attributes support identifying the invoice and checking for `status=paid`. Current documentation lists `draft`, `open`, `paid`, `uncollectible`, and `void` as statuses. The other statuses are background only, not selected claims requiring reproduction in the drafts. The decision to retrieve the invoice before granting and to require a matching local order belongs to the fictional application.

## Application assumptions and bounded judgment

A05 through A09 define the fictional application. A10 is the author's assessment of the consequences under those assumptions, not a Stripe guarantee. The version `2026-10-28.preview` is a documented version string used to bound the hypothetical snapshot schema. It is not a claim that a live account is configured to that version. No version-specific request, historical payload, API response, or SDK compatibility was tested. The packet uses only the documented identifier, timestamp, type, and invoice-status fields, not a purported complete executable payload.

The scenario has one account and one environment. The latter prevents the local account key from silently merging independent test and live namespaces. Invoice-to-order mappings already exist. A grant is local and non-revocable within the scenario. The inbox, operation ledger, and entitlement share one ACID database. The inbox itself supplies durable queued work, so no acknowledgment-to-external-queue publication gap is assumed. Inbox and operation records remain retained throughout the example.

The acknowledgment protocol and transaction boundary are proposed application rules. Stripe's prompt-response guidance is not a guarantee that receipt is durable, and its duplicate guidance is not a guarantee that the application's operation has completed. These distinctions are the writing example's central reasoning.

## Relationships for editorial review

The trace is a fixture, not observed Stripe traffic. No timestamps, throughput, latency, or error rates were measured.

| Arrival | Event | Meaning | Required local interpretation |
| --- | --- | --- | --- |
| 1 | E2 | `invoice.paid` for the one invoice | Durable receipt creates pending work. The paid conditions control any grant. |
| 2 | E2 again | Another delivery of the same Event | The account/event key finds the existing row. No new work is created, including when the row is pending. |
| 3 | E1 | Late `invoice.created` for the same invoice | It is a distinct receipt. Completing it never resets an existing grant. |
| 4 | E3 | Separate duplicate `invoice.paid` Event for the same invoice | It retains its own inbox row. The business-operation key prevents another grant. |

The fixture therefore has four deliveries, three Event IDs, two event types, one invoice, one order, and one grant operation. E1 was generated before E2, although their second-precision `created` values may be equal. Arrival order is not a worker scheduling guarantee. Whichever eligible paid worker wins the operation key may perform the grant. Processing the other paid Event completes its receipt without another grant.

Receipt uniqueness is `(account_id, event_id)`. Operation uniqueness is `(account_id, invoice_id, operation_kind=grant_entitlement)`. An invoice ID alone is neither a receipt ID nor a universal rule for suppressing all later invoice activity.

The endpoint verifies the raw-body signature before persisting or confirming a durable receipt and before returning `2xx`. A committed pending row remains work, not evidence of business completion. If persistence fails, the endpoint does not return successful acceptance. If the process crashes after the receipt commit and before acknowledgment, redelivery finds the retained row rather than creating new work or losing the committed work.

For a new grant, ledger insertion, entitlement mutation, and inbox completion commit together. A business-transaction crash therefore cannot leave only the completion marker committed. Locks and unique constraints arbitrate concurrent workers. A worker that finds the operation already committed completes its own inbox receipt without mutating the grant again. The ADR does not specify lock syntax, isolation-level details, retry scheduling, or a general worker algorithm.

The at-most-one local grant argument depends on operation uniqueness, atomicity, retained records, and non-revocation. Reaching one grant also requires eventual successful receipt and worker processing, invoice retrieval, confirmed paid status, and order matching. Retrieval failure or an unmet condition leaves pending work. Neither successful receipt nor uniqueness alone supplies this eventual-processing condition. Permanently failed retrieval, stopped workers, or a permanently unmatched order do not justify a completion claim.

The alternatives preserve distinct reasons for rejection. Event-ID-only handling misses the separate duplicate E3. Acknowledgment before persistence risks lost work. Timestamp sorting cannot establish generation order or uniqueness. The proposal carries database contention and pending-work recovery costs rather than eliminating failure handling.

## Excluded claims and uncertainty

There is no global exactly-once guarantee, ordering guarantee, or general claim that all future invoice updates can be ignored. Refunds, disputes, subscription changes, external fulfillment, and outbound payment API idempotency are excluded. An external email, shipment, payment call, or another database would need a different effect-delivery design. No such design is supplied or implied here.

Retry duration, manual replay windows, automatic invoice-finalization timing, and the full set of snapshot payload fields are background, not selected draft facts. No production Stripe account, actual event, or business transaction was inspected. The source constraints were checked against the public documentation, while the version-specific behavior of an implemented endpoint remains untested because no endpoint is part of the assignment.

## Rights and attribution

Both drafts, the fictional identifiers and trace, the selected fact descriptions, and the editorial analysis are original project-authored text. Public-source facts are paraphrased and attributed to Stripe. Stripe documentation redistribution permission has not been established. Citation does not place Stripe's wording, code, figures, tables, or documentation under this repository's MIT license. No third-party figure, table, sample payload, source code, or long quotation is reproduced.

## Specialized terminology

| English | Korean | Meaning in this packet |
| --- | --- | --- |
| Architecture decision record, ADR | 설계 결정 기록, ADR | Context, decision, alternatives, and consequences of one bounded choice. |
| Snapshot Event | 스냅샷 Event | The documented Event format, not a thin event notification. |
| Event ID | 이벤트 ID | The identity of an Event object, not the grant operation. |
| Duplicate delivery | 중복 전달 | Another receipt of the same Event. |
| Separate duplicate Event object | 별개의 중복 Event 객체 | An Event with a distinct ID that describes the same grant-triggering business occurrence here. |
| Business-operation key | 업무 연산 키 | Account, invoice, and `grant_entitlement` together. |
| Acknowledgment | 수신 확인 응답 | Successful delivery response, not business completion. |
| Durable inbox | 영속 inbox | Retained receipt records that also constitute the work queue. |
| Pending | 처리 대기, `pending` | Received work that has not completed. |
| Completed | 처리 완료, `completed` | The inbox receipt's processing is complete, including a duplicate-operation no-op. |
| Operation ledger | 연산 원장 | Local record of committed grant operations. |
| Entitlement | 이용 권한 | One non-revocable local grant per invoice in the fictional application. |
| Out-of-order delivery | 생성 순서와 다른 전달 | Arrival order differs from generation order. |
| Idempotency | 멱등성 | Repetition does not add a grant within the named local operation boundary. |

## Editorial rationale

Both drafts preserve the ADR structure, delivery trace, receipt/completion distinction, crash boundaries and conditional guarantee. English and Korean use their own sentence flow with the same selected facts.

## Recorded outputs

The [English attempt](../../../verification/professional-examples-20261111/remaining-run/architecture/en/attempt.json) and [Korean attempt](../../../verification/professional-examples-20261111/remaining-run/architecture/ko/attempt.json) record actual requests, model, package hashes and observed reference reads. The [fidelity review](review.md) covers A01–A10. No live Stripe call or production implementation was performed.
