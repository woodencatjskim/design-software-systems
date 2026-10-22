The proposal violates both promises.

- Replying `sent` before a durable write accepts a message that disappears if the chat process crashes.
- An in-memory Kafka outage buffer cannot survive process failure. Dropping its oldest entries explicitly loses accepted messages.
- Redis Pub/Sub has no durable replay; an offline or disconnected subscriber can miss delivery.
- Waiting for a five-second Cassandra batch before delivery cannot provide online delivery under 500 ms.

Minimal repair:

```text
Sender → gateway → durable Kafka acknowledgement → sender accepted ACK
                       └→ delivery consumer → recipient connection → device ACK
                       └→ Cassandra history consumer
```

Define `accepted` as durably recorded, and distinguish it from device delivery and read receipts. Publish before sending the acceptance response. Configure Kafka acknowledgements, replication, and minimum in-sync replicas to match the intended failure tolerance; disable settings that permit acknowledged data loss. A chat-process crash must leave the accepted record available for another consumer.

When Kafka cannot durably accept a message, apply bounded backpressure or return a retryable unavailable response. Never acknowledge messages stored only in memory. If an acknowledgement is lost after persistence, the client retries using a stable message ID; consumers and storage deduplicate that ID. Do not promise exactly-once transport.

Deliver directly from the durable log without waiting for Cassandra batches. Cassandra can remain the asynchronous history store. Redis Pub/Sub may remain a low-latency routing hint, but durable replay or a catch-up path must recover missed notifications. Track recipient/device delivery progress and resend unacknowledged messages after connection loss. Consumer progress must not discard the only retrievable copy before downstream storage or delivery recovery is safe.

Set retention long enough to cover database lag and the supported recovery window. Alert before lag threatens retention. Cassandra failures must not silently age messages out of Kafka.

The latency promise needs a measurable boundary: sender submission to online recipient receipt, with a defined percentile and network conditions. Allocate the 500 ms budget across durable append, consumption, routing, and client delivery; benchmark it. No architecture can guarantee this for arbitrary network delay or an unavailable persistence service. Negotiate a bounded SLO and report acceptance failures separately rather than hiding them.

Verify process kills immediately before and after durable append/ACK, Kafka unavailability, full buffers, lost Pub/Sub notifications, recipient reconnects, duplicate retries, Cassandra lag, and load-test tail latency. Revisit partitions, routing capacity, and storage throughput when measurements show saturation; the first repair is contract correctness, not more components.
