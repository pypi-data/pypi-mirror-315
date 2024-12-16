"""Store and retrieve Google Calendar events."""

from __future__ import annotations


class Event:
    """A class to represent an event on a Google Calendar."""


def get() -> list[Event]:
    """Return all events."""


def search() -> list[Event]:
    """Return all events matching search criteria."""


def create(event: Event) -> None:
    """Add event to Google Calendar."""


def delete(event: Event) -> None:
    """Remove event from Google Calendar."""
