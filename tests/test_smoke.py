"""Smoke test: replace with real tests."""

import batterway


def test_imports() -> None:
    """The package imports."""
    assert batterway.__name__ == "batterway"
