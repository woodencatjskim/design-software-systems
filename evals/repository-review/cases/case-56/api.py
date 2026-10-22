"""Job submission delegates persistence to a deployment-provided adapter."""

from typing import Protocol


class Adapter(Protocol):
    """Adapter surface; durability semantics are absent from this snapshot."""

    def append(self, job_id: str, payload: str) -> None:
        """Submit data to the configured adapter.

        Args:
            job_id: New job identifier.
            payload: Serialized job body.
        """
        ...


def submit(adapter: Adapter, job_id: str, payload: str) -> str:
    """Return acceptance after the adapter call returns.

    Args:
        adapter: Deployment-provided storage adapter.
        job_id: Nonempty job identifier.
        payload: Nonempty serialized body.

    Returns:
        The acceptance event exposed to the caller.
    """
    if not isinstance(job_id, str) or not job_id or not isinstance(payload, str) or not payload:
        raise ValueError("A job identifier and payload are required")
    adapter.append(job_id, payload)
    return "accepted"
