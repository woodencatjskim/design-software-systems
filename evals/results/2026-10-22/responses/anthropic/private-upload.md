A presigned URL is a bearer capability valid under its signing conditions and lifetime; it is not automatically single-use. Issuing an upload URL neither uploads a file nor makes it published in the application. S3 object accessibility and application publication are separate decisions.

```text
Client → API: create upload intent → PostgreSQL pending attachment
Client → S3: upload via scoped URL
Client/event → API: verify object → mark ready
Client → API: authorize download → short-lived S3 download URL
```

Authenticate the user and derive tenant identity from trusted session context. Create the pending metadata record before issuing a URL. Generate an unpredictable object key bound to the tenant and upload intent. Keep the bucket private with public access blocked and tightly scoped IAM. A tenant prefix helps organization but does not replace application authorization.

Issue short-lived upload permission restricted to that exact destination and expected constraints. Apply upload size limits where supported, and verify size, checksum, and content requirements before publication. Do not trust a client completion claim alone: inspect the stored object. If scanning is required, keep the attachment quarantined until it passes.

A reusable upload URL can overwrite its target during validity. Bind publication to an immutable object version, or promote a verified staging upload into a separate immutable final key. With versioning, verify and publish the exact version identifier and use that version for downloads. This prevents a later upload from changing already-approved content.

Completion processing authenticates the caller/event source and checks the intent, tenant, object key, and exact version. A unique upload identifier and guarded `pending → ready` transition make duplicate callbacks harmless. Publish only after verified object state and metadata commit succeed. A failed metadata transaction remains retryable; reconciliation can discover uploaded pending objects later.

For failures before metadata creation, return an error without issuing the upload capability. For orphaned objects from other failure paths, run a reconciler and lifecycle cleanup after a defined grace period. Coordinate cleanup with finalization so cleanup first claims/abandons a pending intent transactionally, preventing it from subsequently becoming ready. Delete only abandoned or unreferenced versions after rechecking; do not apply a blanket age rule to published attachments. Expire incomplete multipart uploads separately.

On download, authorize tenant membership and attachment access from PostgreSQL before issuing a short-lived URL for the published version. Anyone holding that URL can use it until expiry; immediate revocation requires a different access path or stronger controls.

A CDN is not presently justified. Start with regional S3 downloads and measure latency, geographical distribution, cache reuse, and egress cost. Add private CDN delivery only if those measurements justify its caching and authorization complexity. Verify cross-tenant access denial, repeated callbacks, upload/commit failure, object replacement, and cleanup/finalization races.
