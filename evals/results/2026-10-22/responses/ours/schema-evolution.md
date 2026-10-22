Exercise: schema-evolution

Use an additive hold API and preserve the legacy reservation response and status vocabulary during the 60-day coexistence window. Merely adding `payment_pending` to the existing status column can break old clients; mapping an unconfirmed hold to `reserved` would misrepresent the outcome.

Observed evidence is limited to the supplied endpoint and table. There is no inspected implementation. Unknowns include reservation resource/date/quantity mappings, inventory authority, legacy success semantics, cancellation behavior, and whether payment is mandatory for old-client bookings. Those uncertainties prevent a complete inventory backfill or a proven compatibility claim.

Proposed expansion:

1. Add separate holds, hold allocations, payment attempts, and scoped idempotency records. Add inventory rows keyed by the actual allocated unit—hotel/type/night only if this is a hotel system. Keep `reservations.status` as `reserved` or `canceled`; add nullable linkage fields only if existing readers tolerate them.
2. Introduce `/holds` with explicit pending/expired/confirmed semantics for new clients. Confirmation creates or links a legacy-compatible reservation only after successful inventory/payment coordination. Keep existing reservation IDs stable.
3. Route both old and new booking writers through one allocation authority before enabling holds. For each multi-unit allocation, lock all inventory rows in consistent order, check capacity, and commit the full allocation atomically. Hold expiration, confirmation, and cancellations use the same authority. Application prechecks alone do not stop overselling.

Mixed-version deployment must include old server instances and background writers, not just mobile clients. Deploy schema expansion first, then a server compatibility release for every writer, then enable new-client holds. Prevent unconverted writers from bypassing enforcement through routing, permissions, or retiring those instances. A feature flag does not protect inventory if an old writer can still allocate independently.

Legacy clients may continue immediate reservations only if that remains an authorized product behavior. If all bookings now require payment-pending interaction that old clients cannot represent, the requirements cannot both be met transparently: provide a compatible supported payment journey or require upgrade/reject the affected operation using a documented legacy error. Do not silently change `reserved` to mean pending.

Backfill confirmed allocations from authoritative reservation resource data, with checkpoints and idempotent writes. The provided schema alone lacks that data. Capture concurrent changes and reconcile counts before cutover; use a brief booking-write pause if needed to close the race. Existing oversold inventory requires explicit business resolution, not invented capacity.

Cut over only after allocation reconciliation, old/new client contract tests, final-unit concurrency tests, duplicate requests, expiry/payment races, and writer coverage pass. Monitor capacity violations, lock failures, expiry backlog, and payment reconciliation age.

Rollback disables new holds but retains inventory enforcement and processes or expires existing holds. Reverting to an old unchecked writer can reintroduce overselling. Confirmed allocations and external charges cannot be erased by reverting code; compensate payments explicitly. Retire old compatibility paths only after the 60-day window and evidence that required clients have migrated.
