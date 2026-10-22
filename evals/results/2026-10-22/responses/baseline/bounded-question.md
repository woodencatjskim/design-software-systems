An idempotency key is a unique label for one intended operation. If a client sends a request and loses the response, it can retry using the same key. The service recognizes that retry as the same operation and avoids performing its effect twice—for example, charging a card twice.

Use a new key for a genuinely new operation and reuse the original key for retries of the same request. The service must support and remember these keys for a defined period; the label alone provides no guarantee. Reusing a key with different request details should be treated as a conflict, not as a new operation.
