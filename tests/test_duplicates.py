"""Tests for goalie._duplicates module."""

import goalie


class TestHasDuplicates:
    """Tests for `has_duplicates`."""

    def test_with_dups(self) -> None:
        """List with duplicate elements returns True."""
        assert goalie.has_duplicates([1, 1, 2])

    def test_no_dups(self) -> None:
        """List with all unique elements returns False."""
        assert not goalie.has_duplicates([1, 2, 3])

    def test_strings(self) -> None:
        """String list with duplicates returns True."""
        assert goalie.has_duplicates(["a", "b", "a"])


class TestHasNoDuplicates:
    """Tests for `has_no_duplicates`."""

    def test_unique(self) -> None:
        """List with all unique elements returns True."""
        assert goalie.has_no_duplicates([1, 2, 3])

    def test_with_dups(self) -> None:
        """List with duplicates returns False."""
        assert not goalie.has_no_duplicates([1, 1, 2])

    def test_empty(self) -> None:
        """Empty list returns True."""
        assert goalie.has_no_duplicates([])


class TestIsDuplicate:
    """Tests for `is_duplicate`."""

    def test_with_dups(self) -> None:
        """Elements appearing more than once are marked True."""
        result = goalie.is_duplicate([1, 2, 1, 3])
        assert result == [True, False, True, False]

    def test_no_dups(self) -> None:
        """All unique elements are marked False."""
        result = goalie.is_duplicate([1, 2, 3])
        assert result == [False, False, False]

    def test_all_dups(self) -> None:
        """All duplicate elements are marked True."""
        result = goalie.is_duplicate([1, 1, 1])
        assert result == [True, True, True]

    def test_empty(self) -> None:
        """Empty list returns empty list."""
        assert goalie.is_duplicate([]) == []
