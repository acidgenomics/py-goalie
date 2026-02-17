"""Tests for goalie._compare module."""

import goalie


class TestIsEqualTo:
    """Tests for `is_equal_to`."""

    def test_equal_int(self) -> None:
        """Equal integers return True."""
        assert goalie.is_equal_to(1, 1)

    def test_equal_float(self) -> None:
        """Equal int and float return True."""
        assert goalie.is_equal_to(1.0, 1)

    def test_not_equal(self) -> None:
        """Unequal values return False."""
        assert not goalie.is_equal_to(1, 2)

    def test_tolerance(self) -> None:
        """Values within tolerance return True."""
        assert goalie.is_equal_to(1.0, 1.0 + 1e-10)

    def test_beyond_tolerance(self) -> None:
        """Values beyond tolerance return False."""
        assert not goalie.is_equal_to(1.0, 1.1)


class TestIsNotEqualTo:
    """Tests for `is_not_equal_to`."""

    def test_not_equal(self) -> None:
        """Unequal values return True."""
        assert goalie.is_not_equal_to(2, 1)

    def test_equal_fails(self) -> None:
        """Equal values return False."""
        assert not goalie.is_not_equal_to(1, 1)


class TestIsGreaterThan:
    """Tests for `is_greater_than`."""

    def test_greater(self) -> None:
        """Greater value returns True."""
        assert goalie.is_greater_than(2, 1)

    def test_equal_fails(self) -> None:
        """Equal value returns False."""
        assert not goalie.is_greater_than(1, 1)

    def test_less_fails(self) -> None:
        """Lesser value returns False."""
        assert not goalie.is_greater_than(0, 1)


class TestIsGreaterThanOrEqualTo:
    """Tests for `is_greater_than_or_equal_to`."""

    def test_greater(self) -> None:
        """Greater value returns True."""
        assert goalie.is_greater_than_or_equal_to(2, 1)

    def test_equal(self) -> None:
        """Equal value returns True."""
        assert goalie.is_greater_than_or_equal_to(1, 1)

    def test_less_fails(self) -> None:
        """Lesser value returns False."""
        assert not goalie.is_greater_than_or_equal_to(0, 1)


class TestIsLessThan:
    """Tests for `is_less_than`."""

    def test_less(self) -> None:
        """Lesser value returns True."""
        assert goalie.is_less_than(-1, 0)

    def test_equal_fails(self) -> None:
        """Equal value returns False."""
        assert not goalie.is_less_than(0, 0)


class TestIsLessThanOrEqualTo:
    """Tests for `is_less_than_or_equal_to`."""

    def test_less(self) -> None:
        """Lesser value returns True."""
        assert goalie.is_less_than_or_equal_to(1, 3)

    def test_equal(self) -> None:
        """Equal value returns True."""
        assert goalie.is_less_than_or_equal_to(3, 3)

    def test_greater_fails(self) -> None:
        """Greater value returns False."""
        assert not goalie.is_less_than_or_equal_to(4, 3)
