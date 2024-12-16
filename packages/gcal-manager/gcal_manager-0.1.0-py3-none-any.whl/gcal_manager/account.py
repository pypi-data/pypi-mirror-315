"""Store and retrieve Google Account information."""

from __future__ import annotations


class Account:
    """A class to represent a Google Account."""


def get() -> list[Account]:
    """Return accounts that have been registered."""


def register(account: Account) -> None:
    """Add account to the set of known accounts."""


def remove(account: Account) -> None:
    """Remove account from the set of known accounts."""
