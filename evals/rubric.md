# Behavioral evaluation protocol

This is a small development regression suite, not a leaderboard or proof of production correctness. Freeze prompts and criteria before running a comparison. Do not give this rubric to the agent answering the prompts.

## Procedure

1. Use `prompts.json` without suggested answers. Keep the same language, tool access, model configuration, and response budget across conditions.
2. Conditions: ordinary agent without an additional architecture skill; this skill including its selectively loaded references; a named reference skill at a recorded revision or content hash.
3. Prefer a fresh session per case. If a condition runs all cases in one session, disclose the shared context; that is a smoke comparison, not an independent-per-case benchmark.
4. Save unedited responses, the condition instructions, source hashes, and actual execution date. Do not expose answer keys to the answerer.
5. A reviewer scores each criterion as pass, fail, or unverified, citing an excerpt or location in the response. Do not infer omitted mechanisms. Report critical failures separately from totals.
6. Repeat only failures affected by a change, and retain the earlier evidence. Do not silently replace inconvenient results.

## Criteria: four per case

| Case | A | B | C | D |
|---|---|---|---|---|
| small-service | Keeps the existing simple service/DB | Does not mandate Kafka/cache/sharding | Separates files from catalog metadata | Names evidence-based revisit and recovery conditions |
| booking | All stay dates allocated atomically with authoritative checks | Server-enforced concurrent idempotency | Unknown payments reconciled without blind new charges | Expiration vs late callback is serialized with a stated compensation policy |
| message-ack | Identifies ACK before durability as unsafe | Rejects silent buffer eviction as loss | Pub/Sub has a replay/recovery path | Resolves five-second pre-delivery batching vs 500 ms |
| encrypted-search | Identifies plaintext processing conflict | Gives a privacy-consistent alternative or explicit requirement change | Addresses encrypted media | Addresses per-device key/history access without invented crypto |
| group-fanout | 299 deliveries/message and 29,900/s | 29.9 MB/s payload with exclusions | Separates body storage from other writes | First-device ACK does not justify deletion before offline entitlement is resolved |
| schema-evolution | Does not invent repository evidence | Preserves old response/state meaning or explicitly identifies an unresolved contract | States mixed-version rollout and backfill verification | Explains cutover/rollback limits and a real inventory enforcement boundary |
| private-upload | Enforces tenant/object authorization | Does not treat presigned URLs as automatically single-use | Validated publication plus idempotent completion/orphan recovery | CDN is conditional on workload evidence |
| bounded-question | Answers the concept correctly | Two short paragraphs | No unnecessary design workflow/files | Does not claim a key alone guarantees every external side effect |

Critical failures include approving overselling, acknowledged-message loss, blind duplicate charges, cross-tenant access, or plaintext server processing under the unchanged E2EE requirement. A high total does not offset a critical failure.

## Limits

Static package checks do not run these tasks. Model responses are design suggestions, not executed booking/message systems. Human or model-assisted grading can be wrong; publish raw responses so the judgment can be challenged. A small favorable sample does not establish superiority over another skill or generalize to other agents/models.
