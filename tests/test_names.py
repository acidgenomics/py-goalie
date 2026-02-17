"""Tests for goalie._names module."""

import goalie


class TestHasNames:
    """Tests for `has_names`."""

    def test_dict(self) -> None:
        """Dict with keys has names."""
        assert goalie.has_names({"a": 1})

    def test_empty_dict(self) -> None:
        """Empty dict has no names."""
        assert not goalie.has_names({})

    def test_list_fails(self) -> None:
        """List does not have names."""
        assert not goalie.has_names([1, 2])


class TestHasValidNames:
    """Tests for `has_valid_names`."""

    def test_valid(self) -> None:
        """Dict with non-empty unique keys is valid."""
        assert goalie.has_valid_names({"foo": 1, "bar": 2})

    def test_invalid(self) -> None:
        """Dict with empty key is invalid."""
        assert not goalie.has_valid_names({"": 1})

    def test_duplicate_fails(self) -> None:
        """Duplicate names are invalid."""
        assert not goalie.has_valid_names(["a", "a"])


class TestValidNames:
    """Tests for `valid_names`."""

    def test_valid(self) -> None:
        """List of unique non-empty strings is valid."""
        assert goalie.valid_names(["foo", "bar"])

    def test_empty_str(self) -> None:
        """Empty string in list is invalid."""
        assert not goalie.valid_names(["foo", ""])

    def test_duplicate_fails(self) -> None:
        """Duplicate names are invalid."""
        assert not goalie.valid_names(["a", "a"])


class TestHasRownames:
    """Tests for `has_rownames`."""

    def test_no_index(self) -> None:
        """Dict without index has no rownames."""
        assert not goalie.has_rownames({"a": 1})
