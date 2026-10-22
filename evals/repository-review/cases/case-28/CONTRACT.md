# Document search

Authenticated middleware supplies api.search with a trusted tenant_id. Users may see only their own tenant's titles, categories, and counts. The UI renders every returned field. This is the complete projection schema and query path; no database row policies or response filters exist outside this snapshot. Review the search response, not authentication implementation or indexing lag.
