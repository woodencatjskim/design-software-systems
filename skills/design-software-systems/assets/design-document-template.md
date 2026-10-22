# System design: [name]

<!-- Use only relevant sections. Bracketed fields are authoring prompts, not claims. -->

## Recommendation

[Proposed structure, the requirements it satisfies, and its principal trade-off.]

## Scope and evidence

[Actors, essential journeys, excluded work, observed repository facts, assumptions, unknowns.]

## Requirements and invariants

| Operation or invariant | Target / failure scope | Enforcement | Verification |
|---|---|---|---|
| [Requirement] | [Measurable condition] | [Responsible component and mechanism] | [Evidence or experiment] |

## Workload

| Input / derivation | Value and unit | Provenance | Excluded overhead |
|---|---|---|---|
| [Calculation] | [Estimate] | [Fact or assumption] | [What remains to size] |

## Data and contracts

[Entities, keys, ownership, access patterns, retention, API/events, authorization, errors, idempotency.]

## Components and flows

[Minimal structure; authoritative stores and derived views; representative read/write; acceptance boundary; partial failure and recovery. Add a diagram only when useful.]

## Decisions

| Pressure | Choice | Viable alternative | Accepted cost | Revisit condition |
|---|---|---|---|---|
| [Requirement/evidence] | [Mechanism] | [Alternative] | [Trade-off] | [Observation] |

## Operation and evolution

[Bottlenecks, overload behavior, observability, restore path, compatibility/deployment order, rollback limits.]

## Verification and remaining work

[Concrete success/failure experiments, what actually ran, remaining uncertainty, and implementation tasks.]
