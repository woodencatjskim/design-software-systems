"""Queries backing document search and its category panel."""

import sqlite3


def result_page(connection: sqlite3.Connection, tenant_id: str) -> list[tuple]:
    """Read the tenant's document titles.

    Args:
        connection: Open projection database connection.
        tenant_id: Authenticated tenant identity.

    Returns:
        Document identifiers and titles visible to this tenant.
    """
    if not isinstance(tenant_id, str) or not tenant_id:
        raise ValueError("A tenant is required")
    return connection.execute(
        "SELECT id, title FROM documents WHERE tenant_id = ? ORDER BY id", (tenant_id,),
    ).fetchall()


def facets(connection: sqlite3.Connection, tenant_id: str) -> list[tuple]:
    """Read category counts for the search panel.

    Args:
        connection: Open projection database connection.
        tenant_id: Authenticated tenant identity.

    Returns:
        Categories and matching document counts.
    """
    if not isinstance(tenant_id, str) or not tenant_id:
        raise ValueError("A tenant is required")
    return connection.execute(
        "SELECT category, COUNT(*) FROM documents GROUP BY category ORDER BY category",
    ).fetchall()
