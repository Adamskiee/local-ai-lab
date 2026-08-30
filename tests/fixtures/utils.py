"""Fake utility functions for testing."""


def slugify(text: str) -> str:
    return text.lower().replace(" ", "-")
