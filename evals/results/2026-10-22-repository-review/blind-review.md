# Blinded evidence review

All 14 answers satisfy the four frozen properties: disposition, evidence, reasoning/counterevidence, and repair decision. All seven comparisons are ties on material correctness and usefulness. No unsupported material defect was found. There is no blocking issue for this source-based evaluation.

This judgment does **not** authenticate reported experiments. Twelve answers describe completed probes, but no execution provenance is supplied. Their causal conclusions are independently supported by the supplied code; their claimed runs, environments and precise observed outputs remain unverified. The two case-56 answers explicitly present future verification instead.

| Case | X: disposition / evidence / reasoning / repair | Y: disposition / evidence / reasoning / repair | Preference |
|---|---|---|---|
| case-17 | pass / pass / pass / pass | pass / pass / pass / pass | tie |
| case-42 | pass / pass / pass / pass | pass / pass / pass / pass | tie |
| case-28 | pass / pass / pass / pass | pass / pass / pass / pass | tie |
| case-63 | pass / pass / pass / pass | pass / pass / pass / pass | tie |
| case-35 | pass / pass / pass / pass | pass / pass / pass / pass | tie |
| case-91 | pass / pass / pass / pass | pass / pass / pass / pass | tie |
| case-56 | pass / pass / pass / pass | pass / pass / pass / pass | tie |

The per-answer, per-property excerpts/source locations and rationales are recorded in review.json. Answer references below identify lines in answers/<case-id>/X.md or Y.md; source references identify files within cases/<case-id>.

## Inventory: case-17 and case-42

For case-17, X:3-5 and Y:3-7 correctly trace the enabled job (schedule.json:1) to the unconditional increment (jobs.py:22), contrast the API predicate (api.py:21-22), and inspect the complete nonnegative-only schema (schema.sql:4-5). Starting from schema.sql:7, accepting the API's one unit and then importing one more produces allocation 2 at capacity 1. Transaction serialization and the IntegrityError handler do not supply a missing capacity check. Both answers give a guarded update, optional authoritative CHECK, migration reconciliation and tests covering accepted and rejected orders. Their local-reproduction claims are unverified; the defect itself follows from source. Neither warrants a preference.

For case-42, X:3-5 and Y:3-5 correctly identify schema.sql:6's `CHECK (allocated <= capacity)` as shared enforcement. jobs.py:19-28 rolls back the violating update and returns False, while api.py:19-24 accepts valid reservations. X's reverse-order scenario explicitly includes a successful import; Y requests both writer orderings as verification. Both avoid requiring redundant application enforcement and label an importer predicate optional. Their scheduler-retention and contention questions are qualified integration checks, not claims that rejected orders are lost. Reported probe differences, including Y's concurrency test and runtime version, cannot decide preference without provenance.

## Search: case-28 and case-63

For case-28, X:5-10 and Y:3-5 trace both fields from api.py:20 to repository.py:18-20 and 35-38. Both SQL paths use the trusted tenant identity; facets filter before grouping. Thus even a category shared with another tenant cannot acquire that tenant's contribution. Both discuss legitimate alpha/beta responses and empty/shared-category checks, respect CONTRACT.md:3's trusted middleware premise, and avoid unnecessary repair. Their reported executions are unverified but consistent with the source.

For case-63, X:3-5 and Y:3-7 correctly identify the separate unfiltered facet path at repository.py:33-37. api.py:20 exposes it directly; schema.sql:8-10 supplies alpha's handbook and beta's acquisition/finance. Beta-only categories and shared-category contributions leak, while titles remain protected by repository.py:19. Both propose the tenant predicate before grouping and exact endpoint checks for valid private/shared/empty-tenant results. Y additionally explains why filtering category labels afterward is insufficient; X's proposed repair already operates at the correct boundary. Neither has a material repair advantage.

## Acceptance: case-35 and case-91

For case-35, X:3 and Y:3 correctly connect immediate forwarding at api.py:22 with storage.py:20-23: BEGIN, INSERT, yield, then commit. The generator suspends before commit, so writer loss after the acceptance event can lose the only uncommitted copy. CONTRACT.md:3's committed-data recovery premise and synchronous=FULL do not protect this interval. Both include normal complete consumption as successful counterevidence, propose commit-before-yield, and require first-event process-loss and failure-without-acceptance verification. The described child-process experiments are not independently authenticated.

X:9 raises a further transaction-lifetime issue absent from the answer key. It is defensible: closing the generator while suspended at the first event skips commit, and storage.py:20-23 has no cleanup. A narrow reviewer-run in-memory check against the unchanged supplied append function confirmed `in_transaction=True` both immediately after the first yield and after close. Consequences for other writers or connection reuse depend on the connection remaining open, which X explicitly qualifies. This is an implementation concern, not a separate demonstrated breach of a broader availability contract. It is not a false positive. Y:9-11 already incorporates transaction cleanup and subsequent-use verification, so this additional discussion does not materially change the repair decision.

For case-91, X:3-5 and Y:3-7 correctly cite the opposite ordering: storage.py:22 commits before line 23 yields, under the precise recoverability assumptions of CONTRACT.md:3. Failure before commit cannot yield acceptance, and a committed but unacknowledged message is compatible with the one-way promise. Both avoid demanding host/disk resilience or another recovery service. Their claimed process-kill tests remain unverified. The reviewer's narrow check found `in_transaction=False` at the first event and after close; this is not a substitute for authenticating their reported kill tests.

X:9's missing-rollback discussion is explicitly conditional on ownership, reuse and caller cleanup. The source lacks rollback, but the failed invocation emits no acceptance, and no production connection lifecycle is supplied. This is a reasonable evidence request, not a false accepted-message-loss finding or an unnecessary mandatory repair. Both answers correctly preserve the protected acceptance path.

## Missing adapter evidence: case-56

X:3-5 and Y:3-5 correctly distinguish normal completion of api.py:32 from durable storage: api.py:33 returns acceptance only afterward, but api.py:6-16 provides no durability semantics. Both a worker-memory implementation and a recoverably persistent implementation fit that interface. CONTRACT.md:3 expressly withholds the adapter, configuration and recovery source. Neither safety nor acknowledged loss is established.

Both answers request the concrete implementation/version, effective durability and buffering settings, return/commit boundary, data lifetime and restart discovery path. Both make changes conditional on finding early acknowledgement, and propose real-adapter worker-loss verification with externally recorded accepted IDs. Requests to recover or resume accepted work are treated as recovery checks, not new recipient-delivery guarantees. Neither answer claims to have executed these tests.

## Citation and evaluation limits

Most answers cite `service/<file>:line`, while the supplied review bundle stores those files at `cases/<case-id>/<file>`. I normalized that common packaging prefix to the unique matching source and verified line contents; it is a path-format discrepancy, not a missing call path. case-42 X and case-56 Y already use unprefixed references. All decisive ranges identify the claimed source operations.

This is a blinded source-based judgment using the frozen rubric and key, not an independent external audit or deployment assessment. No condition identities were sought or guessed, and no network, installation, delegation, service edits or answer edits were used. Reviewer execution was limited to the two small transaction-state checks described above. Production behavior and author execution provenance remain outside the supplied evidence.
