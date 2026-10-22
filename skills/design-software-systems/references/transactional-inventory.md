# Reservations and scarce inventory

Use for booking, stock allocation, ticketing, or similar claims on a limited resource. Model the allocated unit before choosing concurrency control.

## Define the invariant

For a hotel example, inventory can be keyed by `(hotel_id, room_type_id, stay_date)`. A stay uses `[check_in, check_out)`: checkout does not consume another night. Validate date order, quantity, and presence of every required inventory row.

For every affected date:

```text
confirmed quantity + active held quantity + new quantity <= authorized capacity
```

Business-approved overbooking changes authorized capacity; it does not excuse a race condition. Default to no overbooking unless the product contract permits it. Physical room assignment may occur later and is a separate concern.

## Separate two problems

| Problem | Protection |
|---|---|
| One logical request is submitted again | Server-enforced idempotency with stable result and request identity |
| Different users compete for the same last resource | Atomic validation and allocation at the inventory authority |

Disabling a button or generating a UUID does not enforce either condition at the authoritative store by itself.

## Transaction example

For a multi-night reservation using pre-existing inventory rows:

1. Validate the caller, request, dates, quantity, and price/quote policy.
2. Reserve the scoped idempotency key atomically; define how another in-flight request waits or receives pending/conflict.
3. Lock all required inventory rows in a deterministic order, or use an equivalent correct transaction/conditional-write scheme.
4. Confirm all expected dates exist and all have sufficient capacity.
5. Update every date and create the hold/reservation in one transaction; record an outbox entry here if an event is required.
6. Commit before reporting the committed outcome. On failure, roll back the entire allocation, including the idempotency claim if it was not committed.

For conditional updates across dates, partial success must still roll back as a unit. Locking nonexistent rows is not sufficient: define prepopulation, missing-row rejection, or another mechanism that protects creation. Keep transactions short and do not wait on an external payment call while holding inventory locks.

## Payments and expiration

Use a durable reservation/payment lifecycle with stable identifiers. Possible states include held, payment-pending, confirmed, expired, canceled, and reconciliation-required. Track payment attempts and refunds separately from the reservation.

Payment timeout is an unknown result. Query or retry using the provider's idempotency mechanism before issuing a new charge. Authenticate callbacks and make their processing idempotent. Reconcile missed callbacks.

Serialize hold expiration and payment confirmation against the same authoritative state. A late payment cannot silently revive expired inventory already allocated to someone else. Choose a documented policy: attempt a fresh allocation, refund/void the payment, or send the case to reconciliation. Record compensations durably and retry them safely.

## Search and scale

Search results and cached availability are advisory. Final allocation must recheck the authority. Propagate changes through an explicit path and tolerate stale candidates without allowing overselling.

Sharding by hotel/resource can preserve transaction locality but does not eliminate contention on one popular resource. Measure lock waits, conflict/retry rates, allocation latency, expiration backlog, and payment reconciliation age before selecting additional machinery.

## Acceptance scenarios

- Two callers compete for the last unit: at most the authorized quantity succeeds.
- Two identical requests run concurrently: one logical allocation and a stable result.
- One night is sold out or missing: no other nights remain partially consumed.
- Payment succeeds while confirmation times out: reconcile without a second charge.
- Payment arrives after hold expiration: no silent oversell; compensation follows policy.
