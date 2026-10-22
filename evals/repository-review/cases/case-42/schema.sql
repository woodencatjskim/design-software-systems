-- The allocation count is the authoritative inventory state.
CREATE TABLE inventory (
    sku TEXT PRIMARY KEY,
    capacity INTEGER NOT NULL CHECK (capacity >= 0),
    allocated INTEGER NOT NULL CHECK (allocated >= 0),
    CHECK (allocated <= capacity)
);
INSERT INTO inventory VALUES ('desk', 1, 0);
