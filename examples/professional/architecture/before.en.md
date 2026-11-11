# ADR 01. Durable invoice-event receipt and local entitlement grants

## Context

This proposed ADR is a fictional application design, not a Stripe, API, or production change. It assumes one account, one environment, snapshot `invoice.created` and `invoice.paid` events at version `2026-10-28.preview`, existing invoice-to-order mappings, and one non-revocable local entitlement per invoice.

Stripe documents [unordered delivery](https://docs.stripe.com/webhooks#event-ordering) and [duplicate events](https://docs.stripe.com/webhooks#handle-duplicate-events). Snapshot `created` values have second-level precision and establish neither order nor uniqueness. Repeated delivery of one Event and separate duplicate Event objects differ. Stripe recommends `data.object.id` with `event.type` for the latter, not blanket suppression of future object updates.

The fictional arrival trace is `invoice.paid` E2, repeated E2, late `invoice.created` E1, and distinct duplicate `invoice.paid` E3. These four deliveries contain three Event IDs and two types for one invoice and order. E1 was generated before E2, possibly within the same timestamp second.

## Decision

Use a durable inbox as the work queue, without external queue publication. Store payload, receipt time, and `pending` or `completed` state under a unique `(account_id, event_id)` key. `account_id` is configured account context, not an assumed payload field. `event_id`, `event_type`, and `invoice_id` come from `Event.id`, `Event.type`, and `data.object.id`. The business-operation key is `(account_id, invoice_id, operation_kind=grant_entitlement)`, not the Event ID.

Following Stripe's [handler guidance](https://docs.stripe.com/webhooks#create-a-handler), verify the signature against the unmodified raw body. Commit the inbox row or confirm its durable predecessor before promptly returning `2xx`. Persistence failure receives no success response. Receipt acknowledges delivery, not business completion. Repeated E2 adds no work, including when its existing row is still pending. It neither discards that row nor marks it completed. A crash after receipt commit but before acknowledgment leaves the committed work available on redelivery.

One ACID database holds inbox, operation ledger, and entitlement, with locks and unique constraints for concurrent workers. Paid processing retrieves the invoice and requires confirmed `status=paid` and its matching existing `order_id`. Retrieval failure or an unmet condition leaves work pending. For a new operation, ledger insertion, entitlement mutation, and inbox completion commit atomically. An existing operation permits completion without another grant, including for E3. A transaction crash cannot commit only completion. Created processing completes its receipt without resetting entitlement, so late E1 cannot undo a grant.

## Alternatives

Event-ID-only deduplication misses E3. Acknowledgment before persistence risks losing work. Timestamp sorting cannot establish order. None replaces business-operation uniqueness.

## Consequences and limits

Database contention and pending-work recovery are costs. Pending rows remain retryable, and inbox and operation records are not pruned within this example. Under these database and retention assumptions, eventual successful receipt, worker retries, retrieval, paid confirmation, and order matching produce one local grant for this trace, not global exactly-once execution. Refunds, disputes, subscription changes, external fulfillment, and outbound payment API idempotency are excluded.
