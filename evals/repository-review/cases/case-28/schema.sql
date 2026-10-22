-- Search projection; titles and categories are tenant-private.
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL
);
INSERT INTO documents VALUES (1, 'alpha', 'Team handbook', 'handbook');
INSERT INTO documents VALUES (2, 'beta', 'Unannounced acquisition', 'acquisition');
INSERT INTO documents VALUES (3, 'beta', 'Confidential budget', 'finance');
