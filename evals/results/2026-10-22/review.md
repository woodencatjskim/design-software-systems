# Evidence review

Criteria A–D refer to the four columns of [the frozen rubric](../../rubric.md). Each row links to the complete unedited response. Quoted fragments locate the evidence; judgments concern the stated criteria, not every possible correctness property. All cells pass except the explicitly marked formatting failure. No critical failure in the rubric was observed.

## Small service

| Response | A: existing service | B: no forced infrastructure | C: files versus metadata | D: revisit and recovery |
|---|---|---|---|---|
| [Baseline](responses/baseline/small-service.md) | “existing application service and PostgreSQL” | “Do not add Kafka, Redis, microservices, or sharding now” | “keep files in private object storage” | “test restoring them”; “measured write/storage constraints” |
| [Ours](responses/ours/small-service.md) | “Keep the existing application and PostgreSQL” | “does not justify Kafka, Redis, microservices, or sharding” | “Store document metadata and permissions in PostgreSQL”; separate files | “Measure restoration”; “representative tests” |
| [Anthropic](responses/anthropic/small-service.md) | “Keep the existing application and PostgreSQL” | “without a demonstrated benefit” | “Store file references and ownership in PostgreSQL” | “Verify restoration actually fits four hours”; evidence list |

## Booking

| Response | A: all dates atomic | B: concurrent idempotency | C: unknown payment | D: expiry and compensation |
|---|---|---|---|---|
| [Baseline](responses/baseline/booking.md) | “allocate all nights, and create the hold atomically” | “A unique constraint serializes competing identical requests” | “timeout means unknown outcome” | “lock the same reservation and inventory state”; refund/void late success |
| [Ours](responses/ours/booking.md) | “A sold-out night rolls everything back” | same-key duplicates “wait within a deadline” or in-progress | stable provider key and “scheduled reconciler” | same hold/inventory locks; “durable void/refund obligation” |
| [Anthropic](responses/anthropic/booking.md) | “roll back the entire stay” | “Concurrent duplicates serialize through that unique record” | “do not issue a fresh charge” | shared locks; “Queue an idempotent refund” |

## Message acknowledgement

| Response | A: premature ACK | B: eviction | C: replay | D: batching latency |
|---|---|---|---|---|
| [Baseline](responses/baseline/message-ack.md) | crash “loses an accepted message” | “explicitly destroys already accepted work” | “durable consumer/replay path” | “Remove Cassandra's five-second batch from the delivery critical path” |
| [Ours](responses/ours/message-ack.md) | “leaving the only copy in process memory” | “Never evict acknowledged work” | “conversation sequence and device cursor” | “make Cassandra archival writes asynchronous” |
| [Anthropic](responses/anthropic/message-ack.md) | “disappears if the chat process crashes” | “Never acknowledge messages stored only in memory” | “durable replay or a catch-up path” | “Deliver directly from the durable log” |

## Encryption conflict

| Response | A: conflict | B: feasible alternative | C: media | D: devices/history |
|---|---|---|---|---|
| [Baseline](responses/baseline/encrypted-search.md) | “The requirements conflict” | “Move content features onto authorized devices” | “Encrypt media on the client” | authenticated enrollment and encrypted history transfer |
| [Ours](responses/ours/encrypted-search.md) | “Do not present server decryption as end-to-end encryption” | local indexes and client previews | attachment ciphertext and encrypted decryption material | supported enrollment; old history not implied by future keys |
| [Anthropic](responses/anthropic/encrypted-search.md) | “changes the end-to-end encryption trust boundary” | local indexes and previews | “Encrypt media on the sending device” | authenticated linking and supported history transfer |

## Group fanout

| Response | A: deliveries | B: bandwidth | C: other writes | D: retention |
|---|---|---|---|---|
| [Baseline](responses/baseline/group-fanout.md) | 299/message; 29,900/s | 29.9 MB/s; explicit exclusions | queue entries, cursor updates, shared log alternatives | “does not support a 30-day offline sync promise” |
| [Ours](responses/ours/group-fanout.md) | 299/message; 29,900/s | 29.9 MB/s; explicit exclusions | distinguishes events, changed rows, transactions | “Do not delete the only server body after the first device ACK” |
| [Anthropic](responses/anthropic/group-fanout.md) | 299/message; 29,900/s | 29.9 MB/s; explicit exclusions | alternative fanout costs, not summed indiscriminately | “other 298 may still need the message” |

## Schema evolution

| Response | A: evidence honesty | B: legacy meaning | C: rollout/backfill | D: enforcement/rollback |
|---|---|---|---|---|
| [Baseline](responses/baseline/schema-evolution.md) | “I cannot infer inspected implementation” | never maps pending to reserved; explicit business conflict | shared safe writer; restartable backfill and concurrent change handling | transactional allocation; rollback retains outstanding holds |
| [Ours](responses/ours/schema-evolution.md) | “There is no inspected implementation” | “Do not silently change reserved to mean pending” | every writer upgraded; checkpointed reconciliation | atomic allocation; no rollback to unchecked writer |
| [Anthropic](responses/anthropic/schema-evolution.md) | “I have inspected no repository” | preserves enum meanings; explicit compatibility conflict | expand, unify, backfill, cutover; old writer exclusion | allocator locks; unsafe rollback and early table removal rejected |

## Private uploads

| Response | A: tenant authorization | B: URL reuse | C: publication/recovery | D: CDN |
|---|---|---|---|---|
| [Baseline](responses/baseline/private-upload.md) | upload/download application authorization | “not automatically single-use” | validated immutable promotion, idempotent completion, reconciliation | “not justified without measurements” |
| [Ours](responses/ours/private-upload.md) | tenant/parent and ready-attachment checks | “reusable bearer capability” | version-pinned final copy, guarded publication, cleanup race handling | “no measured reason to add a CDN” |
| [Anthropic](responses/anthropic/private-upload.md) | trusted tenant session and attachment checks | “not automatically single-use” | guarded transition and transactionally abandoned cleanup intent | “not presently justified” |

## Bounded explanation

| Response | A: concept | B: two paragraphs | C: bounded scope | D: key is insufficient alone |
|---|---|---|---|---|
| [Baseline](responses/baseline/bounded-question.md) | recognizes retries of one action | Pass: two paragraphs | no workflow or implementation | “the label alone provides no guarantee” |
| [Ours](responses/ours/bounded-question.md) | recognizes original payment attempt | **Fail:** extra `Exercise: bounded-question` paragraph precedes two explanatory paragraphs | no architecture workflow or implementation | “a random identifier alone prevents nothing” |
| [Anthropic](responses/anthropic/bounded-question.md) | recognizes the same action | Pass: two paragraphs | no workflow or implementation | “the key alone does not make every side effect safe to repeat” |

## Interpretation

Baseline: 32 pass, 0 fail. This skill: 31 pass, 1 format failure. Anthropic: 32 pass, 0 fail. No unverified rubric cells, but all runtime guarantees remain unverified because these are written answers. The format label is not an architecture safety defect; it is still recorded rather than edited away.

This sample shows no incremental quality benefit from the new skill. The evaluation did not test automatic activation or real repository analysis, and shared context within each condition limits independence. A stronger future comparison should test underspecified requests, supplied code that contradicts a design, migration integration points, and smaller models, with fresh per-case sessions and a blinded independent reviewer.
