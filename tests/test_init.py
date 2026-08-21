"""Test goalie package initialization."""

import goalie


def test_import() -> None:
    """Test that goalie can be imported."""
    assert goalie is not None


def test_all_exports_resolve() -> None:
    """Every name in `__all__` resolves to an attribute of the package."""
    assert len(goalie.__all__) == 30
    for name in goalie.__all__:
        assert hasattr(goalie, name)
