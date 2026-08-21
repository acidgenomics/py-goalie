"""Tests for goalie._collection module."""

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

    def test_empty(self) -> None:
        """Empty list returns False."""
        assert not goalie.has_duplicates([])


class TestIsSubset:
    """Tests for `is_subset`."""

    def test_true(self) -> None:
        """True when first set is a subset of second."""
        assert goalie.is_subset({1, 2}, {1, 2, 3})

    def test_false(self) -> None:
        """False when first set is not a subset of second."""
        assert not goalie.is_subset({1, 4}, {1, 2, 3})

    def test_equal(self) -> None:
        """True when sets are equal."""
        assert goalie.is_subset({1, 2}, {1, 2})


class TestAreSetEqual:
    """Tests for `are_set_equal`."""

    def test_equal(self) -> None:
        """True when sets contain the same elements."""
        assert goalie.are_set_equal({1, 2}, {2, 1})

    def test_not_equal(self) -> None:
        """False when sets differ."""
        assert not goalie.are_set_equal({1, 2}, {1, 3})

    def test_list_input(self) -> None:
        """True when list inputs are set-equal despite duplicates."""
        assert goalie.are_set_equal([1, 2, 2], [2, 1])
