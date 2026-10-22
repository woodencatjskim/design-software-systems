"""Search endpoint called with tenant identity from authenticated middleware."""

import sqlite3

from .repository import facets, result_page


def search(connection: sqlite3.Connection, tenant_id: str) -> dict:
    """Return a tenant's document page and category summary.

    Args:
        connection: Open search projection database connection.
        tenant_id: Tenant derived from the authenticated session.

    Returns:
        Document titles and category counts shown by the client.
    """
    if not isinstance(tenant_id, str) or not tenant_id:
        raise ValueError("An authenticated tenant is required")
    return {"documents": result_page(connection, tenant_id), "facets": facets(connection, tenant_id)}
