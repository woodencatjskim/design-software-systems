---
name: design-software-systems
description: Design software systems, review architecture proposals, and plan changes to existing systems from requirements, workload estimates, and repository evidence. Produce proportionate design documents with data/API contracts, explicit trade-offs, correctness invariants, failure recovery, and verification criteria. Use for system design, capacity planning, service boundaries, consistency decisions, or architecture reviews; not for isolated bug fixes, terminology explanations, or diagram styling alone.
license: MIT
metadata:
  author: woodencatjskim
  version: "0.1.0"
---

# Design Software Systems

Turn a software problem into an implementable, reviewable design. Preserve the user's scope and language. A design is a proposal until implementation or measurements establish its claims.

## Match the work to the request

| Request | Approach | Deliverable |
|---|---|---|
| New system or significant feature | Clarify the product contract, estimate the relevant load, design the smallest sufficient structure | Design and verification plan |
| Change to an existing system | Trace current behavior first; explain what changes and how to migrate | Evidence-based evolution plan |
| Review of a proposal | Test its requirements, decisions, and failure claims; prioritize concrete findings | Findings with evidence, consequences, remedies, and unknowns |
| Bounded architecture question | Answer directly when the supplied constraints settle it | Short decision with rationale and revisit condition |

Do not force a full document onto a small question. Do not turn an ordinary design task into an exhaustive audit. Create files when requested or appropriate to the workspace; otherwise answer in the conversation. Preserve existing user-authored documents and use their conventions.

## Working procedure

### 1. Establish what is known

Separate facts, assumptions, and unresolved questions. Identify the actors, essential user journeys, excluded features, and constraints that change the decision: latency, load, durability, retention, cost, team, deployment environment, and existing interfaces.

In a repository, inspect relevant docs, schemas, configuration, entry points, callers, and state-changing paths. Follow the critical flow rather than reading every dependency. Cite file locations for conclusions about existing behavior. Record disagreements between code and design intent; do not silently treat either as an authorized change to the product contract.

For a repository architecture review or a change affecting multiple writers, readers, or trust boundaries, use [repository-review.md](references/repository-review.md). Trace the other paths that can change or expose the same data, then look for enforcement that could disprove a suspected defect. Keep a bounded architecture answer bounded.

Ask only questions whose answers materially change correctness or the architecture. Reuse information already provided. Where reasonable, proceed with explicit assumptions and describe their consequences. Do not require approval at every stage.

### 2. Define the guarantees and size the workload

Write the invariants before selecting technology. Examples: a reservation cannot exceed authorized inventory; an accepted message survives the stated failure scope; one logical payment does not cause two charges.

Estimate only quantities that affect decisions. Show inputs, units, formulas, average versus peak, skew, and excluded overhead. Distinguish business operations from database operations and deliveries. Do not claim a database needs sharding from a user-count or QPS threshold alone.

Read [capacity-estimation.md](references/capacity-estimation.md) when sizing matters. Read [workflow.md](references/workflow.md) for unclear scope, repository evolution, or a formal design/review deliverable.

### 3. Connect the data, contracts, and structure

Define key entities, access patterns, ownership, identifiers, indexes, consistency needs, and retention. Define the important APIs or events, including authorization, validation, pagination where relevant, errors, and retry semantics. State which store is authoritative and which views are derived.

Draw or describe the smallest sufficient architecture and trace a representative read and write end to end. Data/API design and component design may be developed in either order. Include failure branches for operations that can lose data or duplicate effects.

For each critical write, identify the transaction boundary and the exact point at which success is acknowledged. For a cross-system effect, explain how an unknown outcome is reconciled. State where ordering is required rather than assuming a global order.

### 4. Challenge the design

Read [correctness-and-failures.md](references/correctness-and-failures.md) when the design changes authoritative state, crosses failure boundaries, or makes delivery/durability claims. Select only the relevant domain material:

| Pressure | Reference |
|---|---|
| Large files, media delivery, object access, CDN | [content-delivery.md](references/content-delivery.md) |
| Reservations, stock, scarce resources, payment coordination | [transactional-inventory.md](references/transactional-inventory.md) |
| Persistent connections, offline delivery, groups, multiple devices | [realtime-messaging.md](references/realtime-messaging.md) |
| Tenant isolation, external callbacks, private data or access revocation | [security-and-trust-boundaries.md](references/security-and-trust-boundaries.md) |

Add a component only to address a named requirement, measured constraint, or plausible failure with stated impact. For substantial decisions, compare viable alternatives and explain the accepted cost. Do not invent alternatives merely to fill a comparison table.

Consider the failure modes that threaten the contract: concurrent changes, duplicate submits, timeout after commit, stale reads, lost notifications, dependency overload, reconnect storms, and partial recovery. Give retries a responsible owner and a stopping condition. Give queued work a capacity or age bound and an overload behavior.

For existing systems, preserve public interfaces and data outside the requested change. Include compatibility direction, deployment order, backfill/reconciliation, and rollback limits where schemas or protocols change.

### 5. Deliver the decision and its verification

Lead with the recommendation. Include the evidence, assumptions, accepted trade-offs, unresolved risks, and what measurement would change the recommendation. Use [the design template](assets/design-document-template.md) for substantial work, omitting irrelevant sections. Diagrams are optional; use the user's preferred format or portable Mermaid/text when useful. No renderer or other skill is required.

For a review, report each finding as: violated requirement or claim → reachable path and evidence → concrete failure sequence → counterevidence checked → impact → correction → verification. Distinguish a demonstrated defect, a conditional risk, and an unresolved check. A missing source is neither proof of failure nor proof of safety. Use [the finding template](assets/review-finding-template.md) when a substantial review needs a durable record; do not require it for every answer.

Before handing over, check:

- Every critical journey reaches a named final or durable effect.
- Each invariant has an enforcement mechanism and an observable verification condition.
- Success responses, retention, replication, and recovery agree on what can be lost.
- Repeated requests and ambiguous outcomes do not silently create repeated effects.
- Important estimates include units, amplification, and explicit assumptions.
- Component choices account for operational cost, not only scalability.
- Evolution plans account for mixed versions and irreversible changes.
- Facts, proposals, measurements, and unverified claims remain distinguishable.

## Evidence and portability

Use repository evidence and available tools, without requiring a specific shell, agent, cloud, MCP server, or web access. If a calculation tool is available, verify consequential arithmetic. Without it, show the calculation and its uncertainty.

Verify product-specific guarantees against the deployed version's official documentation when available. If unavailable, state the uncertainty and avoid turning remembered limits into facts. Do not describe a proposed load test, restore, or deployment as completed.

Use the user's language for explanations and preserve API names and identifiers. Respect their existing technology choices unless a concrete conflict needs discussion. Architecture work does not itself authorize deploying infrastructure, changing production data, or publishing documents.
