"""Store and retrieve Google Calendar information."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gcal_manager.account import Account


class Calendar:
    """A class to represent a Google Calendar."""


def get(account: Account) -> list[Calendar]:
    """Return all calendars associated with an account."""


def remove(calendar: Calendar) -> None:
    """Remove calendar from the set of known calendars."""
