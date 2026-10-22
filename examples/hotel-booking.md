# Example: hotel booking with uncertain payment results

**Illustrative design and proposed checks; no payment system is executed here.**

## Recommendation and invariant

Use one transactional authority for nightly inventory, holds, and reservations. For every hotel, room type, and night:

`held_quantity + confirmed_quantity <= capacity`

A stay consumes `[check_in, check_out)`. An unavailable or missing night rejects the entire allocation. Holds last ten minutes. This example chooses refund/void compensation for successful payments discovered after expiry.

## Critical flow

1. Validate identity, dates, quantity, and the request fingerprint. Claim a caller/operation-scoped idempotency key under a unique constraint.
2. In one short transaction, lock every nightly inventory row in deterministic order, check availability, allocate all nights, create the hold, and persist the response. Commit before acknowledging the hold.
3. Persist a stable payment-attempt identity and durable work item. Call the provider outside inventory locks, using the provider's supported idempotency mechanism.
4. A timeout leaves the payment **unknown**. Query or retry that same attempt identity and reconcile missed callbacks. A new charge is not a timeout recovery strategy.
5. Confirmation and expiry lock the same authoritative hold/inventory state. Confirmation before expiry transfers held capacity to confirmed capacity atomically. Expiry releases all nights exactly once.
6. A late successful payment never resurrects an expired allocation. Persist one compensation obligation and reconcile refund/void outcomes, including compensation timeouts.

Concurrent identical requests serialize on the key; changed arguments with the same key produce conflict. Different guests use different keys and still compete through inventory enforcement. Retain keys for the supported retry and reconciliation horizon.

## Failure matrix

| Failure | Required observable result |
|---|---|
| Two guests request the last room | One allocation succeeds |
| The middle night is full | No partial stay remains allocated |
| Commit succeeds but response disappears | Retry returns the existing hold |
| Provider charges and times out | Reconciliation discovers that charge without starting another |
| Expiry races confirmation | One valid lifecycle transition wins |
| Late callback after another guest books | Compensation is recorded; inventory remains valid |
| Compensation worker restarts | Stable identifiers prevent repeated financial effects |

Provider semantics, retry retention, transaction isolation, and recovery settings require implementation-specific verification. Exhausted retries need an observable unresolved state and operational owner; they must not silently mark an unknown payment as failed.
