"""Public reservation writer; all identities are authenticated upstream."""

import sqlite3


def reserve(connection: sqlite3.Connection, sku: str, quantity: int) -> bool:
    """Allocate stock through the public API.

    Args:
        connection: Open inventory database connection.
        sku: Validated inventory identifier.
        quantity: Positive requested quantity.

    Returns:
        Whether the allocation committed.
    """
    if not isinstance(sku, str) or not sku or type(quantity) is not int or quantity <= 0:
        raise ValueError("A nonempty SKU and positive integer quantity are required")
    with connection:
        cursor = connection.execute(
            "UPDATE inventory SET allocated = allocated + ? "
            "WHERE sku = ? AND allocated + ? <= capacity", (quantity, sku, quantity),
        )
    return cursor.rowcount == 1
