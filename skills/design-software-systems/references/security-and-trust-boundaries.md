# Security at architecture boundaries

Use only for boundaries involved in the request: tenant or object access, external inputs, private data, resource abuse, and access revocation. This is a focused design review, not a compliance certification or a requirement to audit every subsystem.

## Trace identity to every observable result

Identify where user, tenant, service, and object identities originate and which boundary authenticates and authorizes them. Distinguish authenticated identity from client-supplied routing fields. Trace checks through all relevant reads and writes, including background jobs and derived views. An opaque identifier is not authorization.

For search and reporting, inspect result bodies, counts, facets, snippets, exports, and pagination independently. Filtering a displayed list does not necessarily restrict earlier aggregation or a cached response. Verify cache keys and ownership policy against the actual data sensitivity. A shared policy or database enforcement may cover these outputs: inspect it before reporting a missing check.

## External events and capabilities

For webhooks or completion callbacks, identify source verification, operation/tenant binding, duplicate handling, and the permitted state transition. An authentic event can still refer to an expired or differently owned operation. A retry must not create a new authority or logical side effect.

For signed URLs and other capabilities, state operation, object/version, lifetime, and sharing/reuse behavior. Authorization at issuance does not necessarily provide immediate revocation. Check publication and later replacement together; use [content-delivery.md](content-delivery.md) for upload-specific details.

## Retention, revocation, and abuse

Trace private data into authoritative stores, indexes, caches, logs, exports, and backups only where those copies exist. Define when deletion or revocation takes effect at each surface, including previously issued capabilities. Explain retained backups and previously downloaded copies without promising instant erasure everywhere.

When one actor can consume shared resources, identify the expensive operation, admission/quota owner, resource bound, and behavior under exhaustion. Check retries and asynchronous fanout as amplification paths. Do not prescribe a universal rate limit without a workload and product contract.

For each material concern, connect **asset and trust boundary → reachable misuse → existing protection → residual consequence → correction → verification**. Exercise both unauthorized rejection and legitimate access so a proposed fix does not simply disable the feature. Label unavailable policy or configuration as unresolved evidence.

This structure is informed by [OWASP threat modeling](https://owasp.org/www-community/Threat_Modeling). Product-specific guarantees still require documentation for the deployed version.
