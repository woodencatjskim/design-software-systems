# Architecture review: [scope]

<!-- Use for substantial reviews. Omit fields that do not affect the repair decision. -->

## Scope and evidence

[Contract, inspected snapshot/commit and working-tree changes, entry points, unavailable sources.]

## Finding: [concrete consequence]

- **Disposition:** [demonstrated defect / conditional risk / unresolved check]
- **Requirement and impact:** [What breaks, who is affected, and under which failure scope.]
- **Reachable path:** [Entry point → caller → enforcement/effect, with source locations.]
- **Failure sequence:** [Preconditions and ordered actions ending in the invalid observation.]
- **Counterevidence:** [Safeguards inspected and why they block or permit the sequence.]
- **Smallest correction:** [Change, compatibility implications, and accepted cost.]
- **Verification:** [Before/after observation; executed check and result, or explicitly proposed check.]

## Concerns ruled out and remaining checks

[Useful negative findings, unresolved preconditions, and the next evidence needed. An empty confirmed-finding list is valid.]
