"""Streaming endpoint: each yielded event is immediately sent to the client."""

import sqlite3
from collections.abc import Iterator

from .storage import append


def submit(connection: sqlite3.Connection, message_id: str, body: str) -> Iterator[str]:
    """Forward storage progress events to the connected sender.

    Args:
        connection: Open explicit-transaction database connection.
        message_id: Identifier of a new message.
        body: Nonempty message body.

    Yields:
        Events the transport sends immediately without buffering.
    """
    if not isinstance(message_id, str) or not message_id or not isinstance(body, str) or not body:
        raise ValueError("A message identifier and body are required")
    yield from append(connection, message_id, body)
