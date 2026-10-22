"""Storage progress for the streaming endpoint."""

import sqlite3
from collections.abc import Iterator


def append(connection: sqlite3.Connection, message_id: str, body: str) -> Iterator[str]:
    """Append one message and expose progress to the caller.

    Args:
        connection: Open connection using explicit transactions.
        message_id: Identifier of a new message.
        body: Nonempty message body.

    Yields:
        An acceptance event for the caller to forward immediately.
    """
    if not isinstance(message_id, str) or not message_id or not isinstance(body, str) or not body:
        raise ValueError("A message identifier and body are required")
    connection.execute("BEGIN IMMEDIATE")
    connection.execute("INSERT INTO messages VALUES (?, ?)", (message_id, body))
    connection.commit()
    yield "accepted"
