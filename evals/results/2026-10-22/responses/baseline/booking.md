Make one database transaction the authority for availability across every night of a stay. Represent inventory by hotel, room type, and date, with capacity and allocated quantity; holds and confirmed bookings both consume allocation. Store the reservation, its nightly allocations, expiration, state, and payment attempts. Lock every required inventory row in a consistent date order, verify capacity on all nights, allocate all nights, and create the hold atomically. Roll back everything if any night is unavailable. A database constraint can additionally enforce allocation between zero and capacity.

Persist the client idempotency key scoped to caller and operation, together with a request fingerprint and reservation/result reference. A unique constraint serializes competing identical requests. The same key and request return the original result; a different request with that key is rejected. A retry must never create another hold or extend the original expiration implicitly.

Do not hold database locks while calling the payment provider. Commit a payment command/outbox entry with the hold, then call the provider using a stable payment-attempt idempotency key. A timeout means unknown outcome, not failure. Query the provider or consume authenticated callbacks until the attempt is reconciled; avoid another charge with a new key merely because a response was lost. Persist provider transaction identifiers and deduplicate callback events, while also making state transitions idempotent against duplicate events with different identifiers.

Expiration and confirmation must lock the same reservation and inventory state. Define the deadline by database time: confirmation may consume the existing hold only if it remains live before its deadline. Expiration atomically releases all nights. A payment callback after expiration cannot simply confirm: another guest may already own the inventory. Choose a clear policy: refund/void the late successful payment and leave the reservation expired. Record that compensation durably, retry it idempotently, and reconcile unresolved charges/refunds with operational alerts. Callback order cannot resurrect an expired reservation or undo a confirmed one. Authorization followed by capture can reduce refunds if supported, but external uncertainty still requires reconciliation.

Verify:

- Two guests race for the last room: exactly one acquires a hold.
- A multi-night stay lacks one night: no night is partially allocated.
- Concurrent identical retries create one reservation and one payment attempt; changed payloads fail.
- Crashes before and after database commit, provider charge, and callback processing recover without duplicate allocation or charge.
- Payment times out after charging: reconciliation discovers success.
- Expiration races confirmation at the deadline: exactly one valid transition wins.
- A late callback after released inventory is rebooked triggers refund, never overbooking.
- Repeated/out-of-order callbacks and repeated refund commands preserve final state.
