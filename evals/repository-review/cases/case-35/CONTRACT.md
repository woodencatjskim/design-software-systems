# Message ingestion

Each event yielded by api.submit is transmitted immediately. An accepted message must remain readable after the writer process is lost. Connections use explicit transactions (isolation_level=None) against a local SQLite database with synchronous=FULL; committed data is recoverable after process loss. The database is the only recovery source. Host/disk loss, retries, media, and recipient delivery are outside this contract. The shown endpoint and storage adapter are the complete active path.
