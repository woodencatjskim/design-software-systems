Exercise: booking

Use PostgreSQL as the inventory and booking authority. For every `(hotel_id, room_type_id, night)`, enforce `confirmed_quantity + held_quantity <= capacity`. A stay consumes `[check_in, check_out)`. Assume quantity is positive and inventory rows are prepopulated; reject missing nights.

Store nightly inventory, holds with expiry and allocation rows, reservations, scoped idempotency records, payment attempts, and durable payment/refund work. Payment state is separate from reservation state.

For `POST /holds`, authenticate the guest and validate dates, quantity, and quote. In one short transaction, claim the caller/operation/idempotency key, record a canonical request fingerprint, lock every affected inventory row in deterministic order, verify all nights, allocate the entire stay, and record the hold and response. Commit before acknowledging success. A sold-out night rolls everything back. Bound whole-transaction retries for deadlocks or serialization failures.

The same key and request return the original hold, including its current lifecycle status; concurrent duplicates wait within a deadline or receive an explicit in-progress response. Reusing a key with different arguments returns conflict. Retain keys through the documented client retry period and payment reconciliation window; expired holds must not become fresh allocations through retries. Different guests with different keys still contend on inventory locks.

Persist a payment attempt and its stable provider idempotency key before dispatch. A worker calls the provider outside inventory transactions. A timeout means unknown: query by the stable payment identifier or retry with the same supported provider key. Do not create a new charge merely because the response was lost. A scheduled reconciler covers missed callbacks and unresolved attempts.

Choose this expiry policy: confirmation must win the authoritative transaction before the ten-minute deadline. Confirmation and expiration lock the same hold and inventory rows in a consistent order. Confirmation verifies provider success, hold state, and database time, then converts held quantities to confirmed quantities atomically. Expiration releases all nights exactly once. An authenticated, deduplicated success callback arriving after expiry does not revive the hold; record a durable void/refund obligation. If that compensation times out, reconcile it with the provider using its stable identifier. Escalate unresolved compensation after bounded retries.

Verify:

- Two guests compete for the final room: exactly one allocation succeeds.
- Concurrent duplicate keys: one hold and one logical charge; changed payload returns conflict.
- A middle night is unavailable or absent: no partial allocation remains.
- Crash immediately after commit but before response: retry returns the committed hold.
- Provider charges then times out: reconciliation confirms without another charge.
- Callback and expiry race, including callback after reallocation: no overselling; late payment creates one compensation obligation.
- Duplicate callbacks/refund responses and worker restarts converge to one final result.

These are proposed verification scenarios, not completed tests.
