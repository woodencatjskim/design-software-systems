"""Nightly partner orders use the same inventory database as the API."""

import sqlite3


def import_order(connection: sqlite3.Connection, sku: str, quantity: int) -> bool:
    """Allocate a partner order from the scheduled import.

    Args:
        connection: Open inventory database connection.
        sku: Partner SKU after input mapping.
        quantity: Positive requested quantity.

    Returns:
        Whether the order was allocated; rejected orders remain pending upstream.
    """
    if not isinstance(sku, str) or not sku or type(quantity) is not int or quantity <= 0:
        raise ValueError("A nonempty SKU and positive integer quantity are required")
    try:
        with connection:
            cursor = connection.execute(
                "UPDATE inventory SET allocated = allocated + ? WHERE sku = ?",
                (quantity, sku),
            )
        return cursor.rowcount == 1
    except sqlite3.IntegrityError:
        # The scheduler retains rejected orders for business resolution.
        return False
