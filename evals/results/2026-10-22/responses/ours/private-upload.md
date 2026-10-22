Exercise: private-upload

Use the existing application, PostgreSQL, and private S3 storage. Start with direct authorized S3 transfers; there is no measured reason to add a CDN for this regional application.

Both claims are incorrect. A presigned URL is generally a reusable bearer capability until its validity ends; it is not automatically single-use. Issuing an upload URL neither uploads bytes nor publishes a file in the application. An uploaded object may become retrievable through an applicable object-store permission before application publication, so keep download authorization gated by metadata state. Exact URL and storage-policy behavior must be checked against the deployed S3 configuration; no online verification was performed here.

Authenticate a tenant member and authorize the specific parent record before creating an attachment. In PostgreSQL, create a pending upload record containing an opaque attachment ID, tenant ID, generated staging key, expected constraints, and expiry. Commit that record before issuing a short-lived upload capability restricted to that key and operation. Enforce size/checksum constraints where supported and validate actual results. Clients never choose another tenant's object key. Keep buckets private and server storage credentials constrained.

The client transfers bytes directly to S3. An authenticated completion request or storage event triggers an idempotent completion handler. Treat callbacks as hints: load the upload record, verify the actual object, size, integrity, and allowed format, then publish through a conditional state transition to `ready`. A repeated callback returns the existing outcome. Object storage and PostgreSQL do not share a transaction, so publication needs reconciliation.

Prevent reusable upload URLs from replacing published bytes. For example, enable versioning on staging uploads, pin the validated version, and copy that exact version to a server-only final key. Publish the final key/version only after the copy is verified. Downloads always address the recorded immutable version. Repeated completion must never switch a ready attachment to later bytes. This adds a copy but keeps publication independent of a still-valid upload capability.

If upload or copy succeeds but metadata update fails, keep the object private and retry/reconcile using the durable upload identity. Periodic cleanup finds expired pending uploads, unreferenced staging/final objects, and incomplete multipart uploads. Use a grace period and recheck references before deletion; coordinate cleanup with completion so it cannot delete a newly published object. Bound retries and surface persistently stuck records. If initial metadata creation fails, issue no URL.

For downloads, authorize tenant membership and attachment access, require `ready`, then issue a short-lived URL for the exact final version. Previously issued URLs may remain usable until expiration; immediate revocation requires an access proxy or another explicit mechanism.

Test cross-tenant access, repeated callbacks, upload overwrite attempts, metadata failures after upload/copy, cleanup races, and expired URLs. Reconsider a CDN after measuring geographic latency, repeated downloads, origin traffic, and cost, including private-content authorization and cache invalidation requirements.
