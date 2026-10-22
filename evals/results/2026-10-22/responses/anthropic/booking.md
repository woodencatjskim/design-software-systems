Use one PostgreSQL transaction boundary for inventory and booking state; external payment cannot participate in that transaction.

```text
Client → Booking API → PostgreSQL → durable payment jobs → provider
                            ↑──────── callbacks/reconciliation ──┘
```

Maintain inventory rows keyed by `(hotel_id, room_type, night)`, with capacity and allocated quantity. A hold allocates every night in `[check_in, check_out)`. Booking, booking-night allocations, idempotency records, and payment attempts belong in the same database. Inventory includes active holds and confirmed reservations.

Creating a hold locks all required inventory rows in deterministic date order, checks every night, and increments allocations atomically. If any night is unavailable, roll back the entire stay. Persist the hold, its expiry, and the response before committing. Enforce nonnegative quantities and allocations not exceeding capacity. Do not release inventory just because a read observes an expired timestamp; release it through a guarded state transition.

Scope client idempotency keys to caller and operation. Uniquely store the key, request fingerprint, and outcome. A retry with the same payload returns the existing booking/result; changed payload with the same key is rejected. Concurrent duplicates serialize through that unique record. Retain keys across the supported retry horizon.

Create a stable provider idempotency key per payment attempt and a durable job in the hold transaction. A timeout means payment outcome is unknown. Retry/query using that same attempt identity; do not issue a fresh charge. Verify callback authenticity and deduplicate provider events. Reconcile unresolved attempts periodically, including callbacks that never arrive.

Payment completion and expiry both lock the booking and relevant inventory in one consistent order. Completion confirms only an active, unexpired hold. Expiry transitions a hold once and releases all allocations once. If successful payment arrives after expiry, record the financial outcome but never confirm against released inventory. Queue an idempotent refund and reconcile it until terminal; make this customer-visible. This chooses predictable compensation over trying to resurrect a sold room. Provider success and reservation confirmation are separate states.

Verify:

- Two guests racing for the last room produce exactly one allocation.
- A multi-night request with one full night changes no inventory.
- Concurrent retries and response loss create one hold and one charge attempt.
- Charge succeeds but times out: reconciliation discovers success without charging twice.
- Expiry racing with callbacks cannot double-release or confirm expired inventory.
- A late successful callback after resale triggers one refund, never overbooking.
- Duplicate callbacks, worker crashes, and refund timeouts converge without repeated effects.

Monitor inventory invariants, overdue holds, unknown payments, and outstanding refunds. Revisit locking contention and provider reconciliation capacity as booking volume grows.
