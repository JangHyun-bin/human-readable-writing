# ADR 01. Durable invoice-event receipt and local entitlement grants

## Context

This proposed ADR describes a fictional application design. It is not a Stripe change, an API change, or a production change. It assumes one account, one environment, snapshot `invoice.created` and `invoice.paid` events at version `2026-10-28.preview`, existing invoice-to-order mappings, and one non-revocable local entitlement per invoice.

Stripe documents [unordered delivery](https://docs.stripe.com/webhooks#event-ordering) and [duplicate events](https://docs.stripe.com/webhooks#handle-duplicate-events). Snapshot `created` values have second-level precision, so they establish neither order nor uniqueness. Two cases must be kept apart: repeated delivery of one Event, and separate duplicate Event objects. For the second case, Stripe recommends using `data.object.id` together with `event.type`. It does not recommend blanket suppression of future object updates.

The fictional arrival trace has four deliveries for one invoice and order, in this order:

1. `invoice.paid` E2
2. A repeat of E2
3. A late `invoice.created` E1
4. A distinct duplicate `invoice.paid` E3

The four deliveries contain three Event IDs and two event types. E1 was generated before E2, possibly within the same timestamp second.

## Decision

**Inbox.** Use a durable inbox as the work queue, without external queue publication. Store the payload, the receipt time, and a `pending` or `completed` state under a unique `(account_id, event_id)` key.

- `account_id` is configured account context, not an assumed payload field.
- `event_id`, `event_type`, and `invoice_id` come from `Event.id`, `Event.type`, and `data.object.id`.
- The business-operation key is `(account_id, invoice_id, operation_kind=grant_entitlement)`, not the Event ID.

**Receipt.** Following Stripe's [handler guidance](https://docs.stripe.com/webhooks#create-a-handler), verify the signature against the unmodified raw body. Then commit the inbox row, or confirm that a durable earlier row exists, before promptly returning `2xx`. If persistence fails, the handler does not return a success response. Receipt acknowledges delivery, not business completion.

- A repeated E2 adds no work, including when its existing row is still pending. The repeat neither discards that row nor marks it completed.
- If a crash occurs after the receipt commit but before the acknowledgment, the committed work remains available when the event is redelivered.

**Processing.** One ACID database holds the inbox, the operation ledger, and the entitlement. Locks and unique constraints handle concurrent workers.

- Paid processing retrieves the invoice. It requires a confirmed `status=paid` and a matching existing `order_id`. If retrieval fails or either condition is unmet, the work stays pending.
- For a new operation, the ledger insertion, the entitlement mutation, and the inbox completion commit atomically.
- If the operation already exists, the worker may complete the inbox row without another grant. This includes E3.
- A transaction crash cannot commit only the completion.
- Created processing completes its receipt without resetting the entitlement, so a late E1 cannot undo a grant.

## Alternatives

| Alternative | Limit |
| --- | --- |
| Event-ID-only deduplication | Misses E3. |
| Acknowledgment before persistence | Risks losing work. |
| Timestamp sorting | Cannot establish order. |

None of these replaces business-operation uniqueness.

## Consequences and limits

Database contention and pending-work recovery are costs. Pending rows remain retryable. Inbox and operation records are not pruned within this example.

Under these database and retention assumptions, the following together produce one local grant for this trace: eventual successful receipt, worker retries, retrieval, paid confirmation, and order matching. This is not global exactly-once execution.

Refunds, disputes, subscription changes, external fulfillment, and outbound payment API idempotency are excluded.