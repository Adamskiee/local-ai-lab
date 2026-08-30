"""Fake database connection module for testing."""


def get_connection():
    raise RuntimeError("Database not available in test environment")
