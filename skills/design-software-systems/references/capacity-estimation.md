# Capacity and cost estimation

Use estimates to choose or reject mechanisms, not to decorate the document. Mark every example number as an assumption.

## Workload worksheet

| Quantity | Derivation | Caveat |
|---|---|---|
| Average operations/s | daily active users × actions/day ÷ 86,400 | Registered users are not DAU |
| Peak operations/s | average × justified peak factor | Check bursts and skew separately |
| Logical bytes/day | new records/day × encoded record size | State excluded indexes and metadata |
| Retained logical bytes | sum of surviving cohorts over retention | Not every event survives the full TTL |
| Physical bytes | retained bytes × replicas + indexes/versions/backups | Avoid counting a replica twice |
| Client deliveries | events × recipients/event × devices/recipient | Group fanout and sender sync add work |
| Network bytes | transfer count × bytes/transfer | Distinguish client egress and origin traffic |
| Connection memory | concurrent connections × measured bytes/connection | Idle sockets still consume resources |
| Queue growth/s | arrival rate − successful drain rate | A retry can increase arrivals during failure |
| Recovery time floor | bytes to restore ÷ sustainable restore bytes/s | Add setup, log replay, validation, cutover |

Use bit/s for bitrate and byte/s for storage/egress: 8 bits = 1 byte. State decimal GB/TB or binary GiB/TiB. Separate rates from accumulated volumes and room-nights from reservations.

## Worked examples

These are educational assumptions, not vendor throughput limits or real company statistics.

- Audio: 30,000,000 tracks × 3 MB = 90 TB of logical audio. Three retained full copies would be 270 TB before versions and other overhead.
- Booking: 1,100,000,000 room-nights/year ÷ 2 nights/booking ÷ 365 ÷ 86,400 ≈ 17.44 bookings/s. Inventory, payment, history, and event writes can make the database write rate higher.
- Messaging: 500,000,000 DAU × 20 messages/day ÷ 86,400 ≈ 115,741 new messages/s. A 3–5× peak is about 347,222–578,704/s before fanout and retries.
- At 1 KB/message, that messaging example creates 10 TB/day. Keeping every message for 30 days would retain 300 TB logically; delivered-message deletion changes this estimate.

## Choose from evidence

Do not infer a database's limit from row count or QPS alone. Identify query shape, working set, indexes, transaction length, contention, hardware, and latency target. Plan representative measurement before asserting a capacity ceiling.

Before sharding, evaluate indexing, query simplification, connection use, retention, vertical capacity, replicas where freshness permits, and workload-specific isolation. These are options, not a mandatory progression. A hot inventory row can remain hot after adding shards.

Name the shard key's effects on locality, range queries, cross-shard transactions, hot tenants, and rebalancing. Modulo partitioning and consistent hashing have different movement costs; neither guarantees balanced traffic when keys are hot.

For cost, identify the dominant drivers and a sensitivity range: storage copies, retention, network egress, idle capacity, managed service minimums, and operating effort. Use current documented prices only when available; otherwise provide quantities and unresolved price inputs. Do not invent precise monthly costs.

## Evidence needed for a load claim

Record environment, dataset, query/request mix, concurrency, warm/cold state, duration, percentiles, errors, saturation, and recovery after overload. A formula is not a load test. A test on a small fixture is not production proof.
