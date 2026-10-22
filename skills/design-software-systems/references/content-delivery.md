# Large-file and media delivery

Use when object size, delivery bandwidth, access control, or media retention shapes the design. A small private attachment feature may need only an origin and an authorization flow.

## Separate the paths

Keep metadata/control operations distinct from large-byte transfers when bandwidth or isolation justifies it. Describe:

1. Who can request an upload or download.
2. Which service authorizes the specific object and operation.
3. How the client transfers bytes to the origin or CDN.
4. How completion and validation make an object visible.
5. What happens to partial uploads and orphaned metadata or objects.

Authentication is not authorization to every object. Scope capabilities to the object, operation, lifetime, and any enforceable upload constraints. Validate completion, size, format, and integrity before publishing content. An upload URL is not evidence that an upload completed.

## Consistent publication

Object storage and the metadata DB usually do not share one transaction. A possible lifecycle is pending → uploaded → validated → ready, with explicit failed/expired states. Make completion callbacks idempotent and reconcile incomplete records. The exact states depend on the workload; do not require transcoding for ordinary file uploads.

Use a stable object key or version identifier in metadata; issue access URLs as needed. S3 presigned URLs generally remain reusable until expiration and can overwrite an existing key for permitted uploads. One-time use or immutable versions require additional application/storage policy. [S3 presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)

## Add a CDN for a reason

Compare direct delivery and edge caching using geography, repeat access, latency, origin load, authorization, and cost. Account for cache keys, expiration, invalidation/versioned objects, cache miss surges, and private-content access. Do not assume every encrypted or personalized object will have useful cache reuse.

Specify whether range requests, resumable uploads, or multiple quality encodings are requirements. Estimate their copies and egress separately. CDN hit rate can lower origin traffic without removing client egress.

## Questions that expose failures

- Metadata commits but the object upload fails: can a user see a broken resource?
- Object upload succeeds but metadata fails: how is the orphan reclaimed?
- A URL expires during or before a retry: how is authorized access renewed?
- An object changes: can old caches return an inconsistent version?
- A user loses access: what can previously issued URLs still permit?
- A deletion is requested: what retention remains in replicas, caches, and backups?

Explain the actual policy instead of claiming instant global deletion or revocation without a mechanism.
