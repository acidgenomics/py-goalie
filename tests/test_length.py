"""Tests for goalie._length module."""

import goalie


class TestHasLength:
    """Tests for `has_length`."""

    def test_list(self) -> None:
        """List with elements has length."""
        assert goalie.has_length([1, 2, 3])

    def test_empty_fails(self) -> None:
        """Empty list has no length."""
        assert not goalie.has_length([])

    def test_specific_n(self) -> None:
        """List matches expected length n."""
        assert goalie.has_length([1, 2], n=2)

    def test_wrong_n(self) -> None:
        """List does not match wrong length n."""
        assert not goalie.has_length([1], n=2)

    def test_str(self) -> None:
        """Non-empty string has length."""
        assert goalie.has_length("hello")


class TestHasElements:
    """Tests for `has_elements`."""

    def test_has(self) -> None:
        """Non-empty string has elements."""
        assert goalie.has_elements("hello")

    def test_specific_n(self) -> None:
        """List matches expected element count n."""
        assert goalie.has_elements([1, 2], n=2)

    def test_empty(self) -> None:
        """Empty list has no elements."""
        assert not goalie.has_elements([])


class TestNElements:
    """Tests for `n_elements`."""

    def test_list(self) -> None:
        """Count elements in a flat list."""
        assert goalie.n_elements([1, 2, 3]) == 3

    def test_nested(self) -> None:
        """Count elements recursively in nested structure."""
        assert goalie.n_elements({"a": [1, 2], "b": [3]}) == 3

    def test_scalar(self) -> None:
        """Scalar value counts as one element."""
        assert goalie.n_elements(42) == 1


class TestAreSameLength:
    """Tests for `are_same_length`."""

    def test_same(self) -> None:
        """Two lists with equal length match."""
        assert goalie.are_same_length([1, 2], [3, 4])

    def test_different(self) -> None:
        """Two lists with different lengths do not match."""
        assert not goalie.are_same_length([1], [2, 3])


class TestAllAreAtomic:
    """Tests for `all_are_atomic`."""

    def test_dict_atomic(self) -> None:
        """Dict with all atomic values passes."""
        assert goalie.all_are_atomic({"a": "foo", "b": "bar"})

    def test_list_atomic(self) -> None:
        """List with all atomic values passes."""
        assert goalie.all_are_atomic(["a", 1, 2.0])

    def test_nested_fails(self) -> None:
        """Dict containing a nested collection fails."""
        assert not goalie.all_are_atomic({"a": "x", "b": []})

    def test_empty_fails(self) -> None:
        """Empty dict fails."""
        assert not goalie.all_are_atomic({})
