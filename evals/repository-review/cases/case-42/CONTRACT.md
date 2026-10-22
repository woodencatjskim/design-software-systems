# Inventory service

The public API and the enabled nightly partner import share this database. Accepted orders must never allocate more units than capacity. Rejected partner orders remain pending upstream. The supplied schema is the complete deployed inventory schema; there are no additional triggers, writers, or database policies in this snapshot. Review allocation behavior, not authentication or payment processing.
