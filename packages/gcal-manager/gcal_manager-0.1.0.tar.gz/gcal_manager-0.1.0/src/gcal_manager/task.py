"""Store and retrieve task templates."""

from __future__ import annotations


class Task:
    """A class to represent a task template."""


def get() -> list[Task]:
    """Return all task templates."""


def search() -> list[Task]:
    """Return all task templates matching search criteria."""


def create(task: Task) -> None:
    """Add task template to available templates."""


def delete(task: Task) -> None:
    """Remove task template for available templates."""
