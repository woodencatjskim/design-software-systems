The excerpt establishes only the existing response shape and two status values. It does not establish whether old clients tolerate additional fields, how inventory is represented, whether reservations span multiple units, or whether clients depend on immediate confirmation. I have inspected no repository. Those unknowns prevent a safe assumption that old clients can understand a new `payment_pending` status.

Preserve the existing endpoint and its `reserved`/`canceled` meanings. Introduce an explicitly versioned contract for payment-pending holds, with documented expiry and confirmation behavior. Do not report an unconfirmed hold as `reserved` merely to preserve the enum. If mandatory payment prevents immediate reservations for old clients, either preserve a compatible business path for the 60-day overlap or obtain agreement on a supported failure/upgrade experience; additive columns cannot solve that semantic conflict.

Use an expand-and-contract migration:

1. **Expand:** Add separate hold, payment-attempt, inventory-allocation, and idempotency storage as needed. Holds should remain outside legacy reservation queries until confirmed. Keep the existing reservation schema and enum valid. Define the actual inventory key only after identifying what is reserved.
2. **Unify writes:** Route both API versions through one transactional inventory allocator. It locks relevant inventory, checks capacity, and atomically creates allocations. The old path creates a confirmed reservation; the new path first creates an expiring hold. Confirmation and expiry serialize against the same allocation state. Database safeguards must cover every writer.
3. **Backfill:** Map existing active reservations to inventory using authoritative information. The excerpt lacks the fields needed to derive that mapping, so do not invent it. Reconcile existing overselling explicitly; backfill cannot undo it. For online backfill, capture concurrent changes and prove convergence, or use a bounded write pause for final reconciliation.
4. **Cut over:** Deploy compatibility code before enabling new behavior. Drain old application binaries or block their unsafe writes before making the allocator authoritative. A feature flag alone does not prevent an old writer from overselling. Enable new clients gradually, retaining the original response contract throughout overlap.

```text
Legacy API ─┐
            ├→ shared transactional allocator → authoritative inventory
New API ────┘              └→ holds/payment lifecycle
```

Verify legacy contract tests, strict enum parsing, mixed-version concurrent requests for the last unit, retry duplication, backfill reconciliation, hold expiry/payment races, and old-writer exclusion. Monitor allocation invariants and rollout error rates.

Rollback can stop new hold creation while keeping workers running to resolve existing holds/payments. Rolling back to code that bypasses allocation is unsafe; dropping new tables or converting pending holds into confirmed reservations is also unsafe. Schema contraction waits until clients and outstanding lifecycle records no longer need compatibility. Revisit indexing and lock contention after measuring the new workload.
