Use the existing application service and PostgreSQL as a modular monolith. Store catalog metadata, access rules, and basic search fields in PostgreSQL; keep files in private object storage or the existing backed-up file store, with database references. Use PostgreSQL full-text search if ordinary text search is needed. Fifteen requests per second, 2 GB of database data, and 40 GB of files provide no evidence that distribution is necessary.

Do not add Kafka, Redis, microservices, or sharding now. Each creates deployment, failure recovery, and consistency work for two developers. Use ordinary transactions for catalog changes. If asynchronous file processing becomes necessary, a small database-backed job queue and worker can be sufficient; make jobs retryable and idempotent.

Operate one deployable application with health checks, structured logs, request latency/error metrics, database query monitoring, and tested backups. Define acceptable data loss separately from the four-hour downtime allowance. Keep database and file backups consistent enough to recover references, test restoring them, and verify that the actual recovery procedure fits four hours. Do not add high availability solely by assumption, but consider it if measured recovery cannot meet that target.

Change the architecture in response to evidence:

- Slow requests: inspect query plans and add appropriate indexes before introducing a cache. Consider Redis when repeated expensive reads dominate and tolerable staleness and invalidation rules are clear.
- Independent consumers, replay requirements, or sustained asynchronous throughput beyond a simple queue: evaluate a durable event broker such as Kafka.
- Independently owned domains requiring different deployment or scaling cycles: consider extracting a service when that benefit exceeds coordination costs.
- Database capacity: first tune queries, remove contention, scale the database, and consider replicas for reads. Shard only after measured write/storage constraints exceed practical single-database options and a viable partition key is established.

Measure representative load, deployment recovery, and restore time. Employee count and raw file size alone are not scaling triggers.
