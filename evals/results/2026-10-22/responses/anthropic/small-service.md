Keep the existing application and PostgreSQL. With two developers, 15 peak requests/second, 2 GB of database data, and an acceptable four-hour outage, Kafka, Redis, microservices, and sharding would introduce operational costs without a demonstrated benefit.

```text
Employees → existing application → PostgreSQL (catalog, permissions)
                         └──────→ private file/object storage
```

Assume the catalog requires metadata CRUD, access control, and ordinary search. Keep these as modules in one deployable service. Store file references and ownership in PostgreSQL; store the 40 GB of files in durable private storage with authenticated downloads. Use PostgreSQL indexes and, if needed, its full-text search before introducing a separate search service. Validate authorization on every operation.

For long-running imports or indexing, start with a database-backed job table processed by the application or one worker. Jobs need durable status, bounded retries, and idempotent processing. Add this only if synchronous work causes unacceptable request latency.

Use migrations, structured logs, latency/error dashboards, database connection limits, and automated backups. Test restoration of both metadata and files. Four hours of acceptable downtime defines a recovery-time target, not acceptable data loss: establish the recovery-point target separately. Choose backup frequency and PostgreSQL recovery facilities accordingly. Verify restoration actually fits four hours.

Reconsider choices based on evidence:

- Redis: repeated expensive reads dominate latency despite query/index improvements, and a measured cache-hit opportunity justifies invalidation complexity.
- Kafka: multiple independent consumers need durable replay or sustained event throughput exceeds a simpler job queue's capabilities.
- Microservices: independently owned components require separate release cycles, failure isolation, or materially different scaling. A two-person team is unlikely to benefit initially.
- Sharding: measured database limits persist after query tuning, suitable hardware, archiving, and other simpler options. The present data size does not justify it.
- Additional application instances or database redundancy: availability requirements tighten or measured resource saturation demands them.

Load-test representative queries near and above peak traffic, and review slow queries and capacity trends. The trade-off is deliberately accepting a larger application failure boundary and limited independent scaling in exchange for lower cost, simpler debugging, and faster delivery.
