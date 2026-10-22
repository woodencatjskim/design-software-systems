-- This database is the only authoritative copy; there is no upstream durable log.
CREATE TABLE messages (id TEXT PRIMARY KEY, body TEXT NOT NULL);
