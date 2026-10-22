Exercise: small-service

Keep the existing application and PostgreSQL. Use modules within the application for catalog, authorization, and file handling. The supplied scale—80 employees, 15 peak requests/second, 2 GB of database data, and 40 GB of files—does not justify Kafka, Redis, microservices, or sharding. Actual query cost and reliability still need verification.

Store document metadata and permissions in PostgreSQL with indexes supporting the catalog's real filters and sorting. Store files in private durable file/object storage, with stable object identifiers in metadata; authorize access through the application. Publish a document only after its file exists and validation completes. Reconcile failed uploads and orphaned files. Use ordinary database queries initially, adding PostgreSQL search facilities if search is required.

Deploy one application service using the current operational setup. A database-backed job table and a worker in the existing deployment are sufficient if asynchronous indexing or cleanup is needed. Do not add that worker merely for architectural completeness. Keep database migrations, backups, basic request/error monitoring, disk alerts, and a tested restore procedure. Four hours of acceptable downtime does not specify acceptable data loss: assume committed catalog changes require durable storage, and define backup RPO separately. Measure restoration of both metadata and files against the four-hour RTO.

Reconsider components only with specific evidence:

- Redis: repeated expensive reads dominate latency after query/index improvements, and an explicit staleness policy permits caching.
- Kafka: independently operated consumers need durable replay or stream throughput the simpler job approach cannot meet.
- Microservices: a module requires independent releases, isolation, or scaling that outweighs network and operational costs for two developers.
- Sharding: representative tests show the database cannot satisfy requirements after addressing queries, contention, and practical capacity options; a workable partition key preserves required transactions.

Run a representative 15 requests/second workload with realistic queries, file transfers, and a burst margin. Record latency percentiles, errors, database utilization, lock waits, and connection counts. These measurements and a restore exercise would validate the proposal; neither has been performed here.
