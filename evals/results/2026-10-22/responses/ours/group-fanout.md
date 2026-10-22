Exercise: group-fanout

Each message needs `99 other members × 3 devices + 2 sender devices = 299` deliveries. Therefore `100 messages/second × 299 = 29,900 device deliveries/second`. This excludes the originating device, which already has its submitted message.

At decimal `1 KB = 1,000 bytes`, delivery body payload is `29,900 × 1,000 = 29,900,000 bytes/second`: **29.9 MB/s or 239.2 Mb/s** of client egress. This excludes envelopes, encryption overhead, protocol headers, retransmissions, acknowledgements, notifications, and server-to-server replication. Incoming body payload is another `100 × 1,000 = 100,000 bytes/second`, or 0.1 MB/s.

Storing each body once means 100 logical body inserts/second and 100 KB/s of new body data, not 29,900 body copies/second. If this rate is sustained continuously and all bodies are retained for 30 days, logical body storage is `100,000 × 86,400 × 30 = 259,200,000,000 bytes`, or **259.2 GB**, before replicas, indexes, metadata, backups, and versions. The supplied rate is not labeled average or peak; this retention number assumes it is the sustained average.

Other writes depend on the delivery model:

- Conversation log/sequence entries and idempotency records scale with 100 new messages/second.
- Per-member inbox fanout could produce `100 × 100 = 10,000` logical inbox records/second if sender synchronization uses the same inbox model. A shared conversation log can avoid these records.
- Per-device delivery records would imply up to 29,900 logical delivery-state entries/second. Device ACK processing can also reach 29,900 events/second before retries.
- Cursor coalescing and batching can reduce database writes; ACK events, rows changed, and database transactions are different quantities. Membership checks, indexes, archival writes, and replication add further work.

Do not delete the only server body after the first device ACK. That ACK says only one device received the message; other online devices can still be missing it, and offline devices cannot later reconstruct it. This violates a 30-day offline sync promise unless another durable copy remains available for the full promised window.

Retain a shared authoritative message history for at least that window and track each device's synchronization cursor separately. Acknowledge progress per device, replay gaps with message-ID deduplication, and define authorization and history behavior for new or returning devices. After retention expiry, report missing history explicitly. The exact meaning of “30-day offline sync” should distinguish messages created during the last 30 days from any previously undelivered history owed to a device that returns within 30 days.
