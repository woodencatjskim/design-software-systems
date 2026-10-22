Each message has 299 destination devices:

`99 other members × 3 devices + 2 sender devices = 299`

At 100 new messages/second, that is **29,900 logical device deliveries/second**. With decimal 1 KB bodies, payload delivery bandwidth is **29,900,000 bytes/second = 29.9 MB/s = 239.2 Mb/s**. This excludes message envelopes, encryption expansion, transport headers, acknowledgements, retransmissions, and internal replication. The originating device's upload is a separate 100 KB/s payload ingress stream.

```text
100 message appends/s → group stream → 299 destinations/message
                                      → 29,900 deliveries/s
```

Storing each body once creates 100 logical body writes/second and 100 KB/s of raw body storage growth. That is 8.64 GB/day or 259.2 GB for 30 days, assuming sustained traffic. Replication, indexes, backups, and metadata increase physical storage beyond this figure.

Other write rates depend on the delivery model and cannot be inferred from body storage alone:

- One message reference per member would add 10,000 reference writes/second if the sender's member history is included.
- Persisting one work item per destination device would add 29,900 delivery-work writes/second.
- An ACK for every delivery yields up to 29,900 logical ACK events/second on the first successful pass. Batching or cumulative device cursors can substantially reduce database updates.
- A shared group log with per-device cursors avoids duplicating bodies or necessarily creating a database row for every delivery. Membership authorization and membership-history semantics still require explicit handling.

These are alternative implementation choices, not necessarily costs that should all be added together. Replicas and retries further affect physical write rates.

**Deleting the only server message record after the first device ACK does not support 30-day offline sync.** That ACK proves receipt by one device; the other 298 may still need the message. Keep the body and sufficient group history retrievable for at least the promised sync window, regardless of another device's acknowledgement. Deletion of a transient routing record is safe only if a durable, authorized replay source remains.

Track device progress independently, with explicit policy for new, revoked, and long-offline devices. Define the 30-day boundary precisely and return a clear history-gap result when a device exceeds it.

Load-test 29,900 deliveries/second plus reconnect bursts, retransmissions, and encryption overhead. Revisit fanout workers, batching, and partitioning based on measured CPU, egress, queue delay, and storage growth; body-write throughput alone is not the scaling driver.
