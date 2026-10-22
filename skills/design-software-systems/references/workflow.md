# Scope, evidence, and decisions

Use for a substantial design, a repository change, or an architecture review. Adapt depth to the request.

## Discover the contract

Capture a small set of essential journeys: actor, trigger, expected result, unacceptable result. For each non-functional requirement, name the operation, measurement boundary, percentile or tolerance, and workload. "Fast" is not a latency target; "available" is not a defined failure contract.

Keep three lists:

- **Observed:** source and scope, such as a schema constraint or a traced call.
- **Assumed:** value, why it is reasonable, and which decision changes if it is false.
- **Unknown:** missing evidence and the smallest question or experiment that resolves it.

An unanswered question may block a final recommendation without blocking an explicitly conditional design. Do not turn a hypothetical into a production fact.

## Existing systems

Trace one critical journey through entry point, validation/authorization, state change, external effects, and response. Inspect callers and migrations before proposing interface changes. Check relevant recent changes, tests, incidents, or ADRs when available; do not invent an incident history.

Prefer a targeted extension when it meets the contract. A new requirement does not imply a rewrite. If code and docs disagree, describe the discrepancy and ask which behavior is intended when it affects correctness.

For a migration, specify:

1. Which old and new readers/writers coexist.
2. The compatible schema or protocol expansion.
3. Backfill scope, idempotency, checkpoints, and reconciliation.
4. Cutover conditions and monitoring.
5. How to stop or roll back, including data that cannot be reversed safely.
6. When old fields or paths can be retired.

Do not call a destructive migration reversible just because application code can be redeployed.

## Compare decisions

| Field | Required reasoning |
|---|---|
| Pressure | Requirement, workload, invariant, or operational constraint |
| Choice | Mechanism and the boundary where it applies |
| Alternative | A viable option and why it was not selected |
| Cost | Complexity, latency, availability, money, or maintenance |
| Revisit | Observable condition that would change the choice |
| Verification | Evidence or experiment that tests the claim |

A modular monolith can have clear ownership without independent deployments. Microservices require a reason for separate deployment or scaling plus the ability to operate the resulting network and data boundaries. Team size alone is not a decision rule. Introduce domain layering only where it improves change isolation or testability; avoid mandatory interfaces for every function.

If an ADR is requested, record context, considered options, decision, consequences, status, and evidence. Proposed is different from accepted. Do not silently supersede an existing decision.

## Review findings

Prioritize consequences: correctness/data loss, availability or latency, operational cost, then maintainability. A finding needs a concrete scenario and evidence. "No Kafka" is not a defect. "An acknowledged request exists only in process memory and the contract requires survival of process loss" is a testable conflict.

Distinguish observed defects, contradictions within a proposal, and missing evidence. Include counterevidence and residual uncertainty. Give actionable remedies rather than a universal numeric architecture score.
