# Realtime delivery and synchronization

Use when persistent connections, offline delivery, fanout, or multiple devices matter. Polling can be sufficient for low-frequency updates; justify a persistent connection by the product's latency and interaction needs.

## Connection state is not message durability

A connection directory maps user/device/session to a live server, with expiration and stale-entry handling. Authoritative messages and delivery progress need a recoverable path independent of that directory.

Define the meaning of each state:

| State | Evidence |
|---|---|
| Pending | Sender has a local operation awaiting acceptance |
| Accepted | Server has met its stated durable-admission contract |
| Delivered | Target device has acknowledged receipt |
| Read | Product-defined user action has produced a read receipt |
| Failed/expired | Admission failed or a declared retention policy ended |

Do not use "sent" to hide whether the server merely received bytes or durably accepted them. A push notification is not proof of message delivery.

## Delivery and replay

Assign one stable identifier per logical message; keep it on retry. Enforce authorization and size limits before durable admission. Persist or durably log before an acknowledgement that promises survival. Route to online devices or retain recoverable pending work for offline devices.

Track delivery acknowledgements and replay unacknowledged work with duplicate suppression. Deduplicate by message/operation identity, not text content: two identical texts can be two legitimate messages. Redis Pub/Sub may accelerate live routing but needs a durable recovery path for missed publications.

Choose ordering scope, usually a conversation or sender stream. Specify the ordering authority, sequence/cursor, gap detection, and repair. A timestamp alone does not prove a total order across devices.

## Multiple devices and groups

Separate the message body, recipient/user delivery state, and device sync cursors. State whether delivery means any device, every active device, or another policy. One device's receipt must not erase the only copy another entitled device still needs.

For long-offline/new devices, define history bootstrap, incremental sync, retention expiry, and missing-history behavior. Read status should merge according to a deliberate monotonic rule rather than letting an older receipt regress it.

Group fanout multiplies deliveries, inbox records, and receipt handling even if the body is stored once. Include membership authorization at send time and define what membership changes mean for history. State whether the sender's other devices also synchronize the message.

## Latency and overload

Separate durable admission, live delivery, archival writes, and analytics. A five-second buffer on the synchronous delivery path cannot meet a 500 ms end-to-end target. If batching is off-path, explain how durability and online delivery are secured before the batch completes.

Bound offline backlogs, retries, connection counts, and reconnect rates. During durable-store outage, reject or explicitly defer new work instead of silently dropping accepted messages. Use backoff/jitter for reconnects and a resync cursor after reattachment.

WebSocket does not imply L4-only load balancing: some L7 load balancers support upgrades. Evaluate support, timeouts, connection draining, capacity, and routing requirements. [AWS ALB WebSocket support](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html)

## Encryption changes the architecture

If end-to-end encryption prevents the server from seeing plaintext, server-side plaintext search, mention parsing, and link preview extraction cannot simply remain in the pipeline. Move applicable work to clients or explicitly change the privacy contract. Include encrypted media, device enrollment/revocation, history sharing, and key distribution in the model.

Use established protocols and libraries. Do not invent encryption where a public key can decrypt every message: key agreement and per-message key evolution have different roles. [Signal X3DH](https://signal.org/docs/specifications/x3dh/), [Double Ratchet](https://signal.org/docs/specifications/doubleratchet/)

## Evidence to collect

Observe admission failures, delivery percentiles, oldest pending age, duplicate handling, reconnect rate, hot partitions, and per-device sync lag. Test loss of a chat process after ACK, lost live notifications, directory failure, offline recipients, late receipts, and retention expiry.
