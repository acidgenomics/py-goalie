"""Tests for goalie._sets module."""

import goalie


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


class TestIsSuperset:
    """Tests for `is_superset`."""

    def test_true(self) -> None:
        """True when first set is a superset of second."""
        assert goalie.is_superset({1, 2, 3}, {1, 2})

    def test_false(self) -> None:
        """False when first set is not a superset of second."""
        assert not goalie.is_superset({1, 2}, {1, 2, 3})


class TestAreDisjointSets:
    """Tests for `are_disjoint_sets`."""

    def test_disjoint(self) -> None:
        """True when sets have no common elements."""
        assert goalie.are_disjoint_sets({1, 2}, {3, 4})

    def test_overlap(self) -> None:
        """False when sets share elements."""
        assert not goalie.are_disjoint_sets({1, 2}, {2, 3})


class TestAreIntersectingSets:
    """Tests for `are_intersecting_sets`."""

    def test_overlap(self) -> None:
        """True when sets share elements."""
        assert goalie.are_intersecting_sets({1, 2}, {2, 3})

    def test_disjoint(self) -> None:
        """False when sets have no common elements."""
        assert not goalie.are_intersecting_sets({1, 2}, {3, 4})


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
