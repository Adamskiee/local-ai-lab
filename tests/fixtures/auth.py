"""Fake authentication module for testing."""


def verify_token(token: str) -> bool:
    if not token:
        return False
    return token.startswith("Bearer ")
