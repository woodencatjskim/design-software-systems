Exercise: bounded-question

An idempotency key is an identifier a client attaches to one intended operation so the service can recognize retries. If you submit a payment and the response disappears, you can retry with the same key: the service should recognize the original operation and return its recorded outcome instead of creating another payment. A genuinely new payment gets a new key.

The key works only when the service actually enforces that behavior; a random identifier alone prevents nothing. Reusing the same key with different payment details should be rejected, and the service needs a defined period during which it remembers keys. Idempotency addresses repeated attempts at the same operation; it does not by itself prevent two different customers from competing for the same last item.
