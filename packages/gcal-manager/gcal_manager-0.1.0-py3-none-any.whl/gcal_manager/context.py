"""Store and retrieve contexts."""

from __future__ import annotations


class Context:
    """A class to represent a context."""


def get(context: str | None = None) -> list[Context]:
    """Return contexts."""


def register(context: Context) -> None:
    """Add context to the set of known contexts."""


def remove(context: Context) -> None:
    """Remove context from the set of known contexts."""
