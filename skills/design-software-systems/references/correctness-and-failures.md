# Correctness across failure boundaries

Read the sections relevant to the system's promises. Do not add every distributed mechanism to every design.

## Invariants and concurrent writes

Express the business rule, the authority that enforces it, and the atomic boundary. A read followed by an unrelated write is not protection against concurrency. Choose a unique constraint, atomic conditional update, locking transaction, or serializable transaction according to the invariant and database semantics.

PostgreSQL Serializable can run concurrent transactions and reject unsafe executions; it is not a global single-file execution queue. A serialization retry must repeat the entire transaction with bounded attempts. Order multi-row locks consistently and handle timeouts/deadlocks. [PostgreSQL isolation](https://www.postgresql.org/docs/18/transaction-iso.html)

## Idempotency and ambiguous outcomes

A client-generated identifier is useful only if the effect owner enforces it. Scope the key to the caller and operation; store a request fingerprint and outcome, define concurrent-in-flight behavior and retention, and reject the same key used for a different request. Commit the deduplication record and local effect atomically where possible.

A timeout after dispatch means the result may be unknown, not necessarily failed. Retry with the same effect key when the destination supports it; otherwise reconcile using a stable business identifier. Local deduplication cannot guarantee an external payment or email is idempotent.

## Acceptance and durability

Distinguish received, admitted, durably accepted, delivered, and applied. State whether success survives process loss, host/disk loss, availability-zone loss, or region loss.

- Memory alone does not survive a process crash.
- A local write-ahead log can survive process loss under its flush guarantees, but not loss of its only disk.
- Replicated acknowledgement depends on configured replicas, failure independence, and what each acknowledgement means.

If durable admission is unavailable, return a retryable failure or an explicitly pending result according to the product contract. Do not acknowledge durable success and silently evict accepted work when a buffer fills.

## Events, queues, and derived views

For a DB write plus event publication, account for either half failing. A transactional outbox or appropriate CDC can connect committed state to asynchronous work; consumers still need replay and duplicate handling. [AWS outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)

Specify message identity, ordering scope, retention, retry owner, maximum delay/backlog, poison-message handling, and how a DLQ item returns to service. Advance a consumer checkpoint only after the required effect is secured. Kafka producer idempotence or transactions do not automatically cover an unrelated database or external API.

Redis Pub/Sub is at-most-once; it cannot be the sole recovery path for accepted messages. Keep recoverable state and a resynchronization mechanism if loss is unacceptable. [Redis delivery semantics](https://redis.io/docs/latest/develop/pubsub/)

Search indexes and caches are derived views. Name their source, propagation mechanism, freshness tolerance, rebuild procedure, and authoritative validation at commit time. A cache outage fallback must protect the origin from a sudden request surge.

## Availability and recovery

Partition tolerance is a failure condition to plan for, not a third option to discard in a distributed system. Decide per operation what happens when the required authority or quorum is unreachable: reject, wait, or serve explicitly stale/limited results.

Read replicas may lag. Identify reads that require read-after-write and route or synchronize them accordingly. Replicas are not backups against replicated deletion or corruption. Tie each failure scope to a recovery source, RPO, RTO, and a restore exercise.

Give dependency calls deadlines and bounded retry budgets, with backoff/jitter where appropriate. Avoid multiple layers independently multiplying retries. State overload admission, degraded behavior, and conditions for returning to normal service.

## Product-specific cautions

- Ordinary B-tree indexes do not automatically implement typo tolerance. PostgreSQL has specialized search options; `LIKE` does not universally imply a full scan. [pg_trgm](https://www.postgresql.org/docs/17/pgtrgm.html)
- Cassandra BATCH is not a universal bulk-ingest acceleration technique. Cross-partition batches add costs and do not have SQL-style isolation across all partitions. [Cassandra BATCH](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html#batch)
- Cassandra's peer architecture is not a single-primary/read-follower model. Model the chosen database's actual replication and consistency. [Cassandra basics](https://cassandra.apache.org/_/cassandra-basics.html)

Consult the deployed product version for implementation decisions. Keep unsupported claims conditional.

## Verify the promise

Choose failure experiments that can falsify the design: concurrent final-resource allocation; duplicate request while the first is in flight; process termination immediately after ACK; lost event publication; stale replica read; delayed webhook; full queue; cache failure under peak load; restore from a retained backup. State expected observations, not just "test resilience."
