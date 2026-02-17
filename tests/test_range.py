"""Tests for goalie._range module."""

import goalie


class TestIsInRange:
    """Tests for `is_in_range`."""

    def test_in_range(self) -> None:
        """Value within range returns True."""
        assert goalie.is_in_range(0.5, lower=0, upper=1)

    def test_at_lower_closed(self) -> None:
        """Value at lower bound of closed range returns True."""
        assert goalie.is_in_range(0, lower=0, upper=1)

    def test_at_upper_closed(self) -> None:
        """Value at upper bound of closed range returns True."""
        assert goalie.is_in_range(1, lower=0, upper=1)

    def test_too_low(self) -> None:
        """Value below range returns False."""
        assert not goalie.is_in_range(-1, lower=0, upper=1)

    def test_too_high(self) -> None:
        """Value above range returns False."""
        assert not goalie.is_in_range(2, lower=0, upper=1)

    def test_not_numeric(self) -> None:
        """Non-numeric value returns False."""
        assert not goalie.is_in_range("hello", lower=0, upper=1)

    def test_bool_fails(self) -> None:
        """Boolean value returns False."""
        assert not goalie.is_in_range(True, lower=0, upper=1)


class TestIsInOpenRange:
    """Tests for `is_in_open_range`."""

    def test_in_range(self) -> None:
        """Value within open range returns True."""
        assert goalie.is_in_open_range(0.5, lower=0, upper=1)

    def test_at_boundary_fails(self) -> None:
        """Values at boundaries of open range return False."""
        assert not goalie.is_in_open_range(1, lower=0, upper=1)
        assert not goalie.is_in_open_range(0, lower=0, upper=1)


class TestIsInLeftOpenRange:
    """Tests for `is_in_left_open_range`."""

    def test_at_upper(self) -> None:
        """Value at upper bound returns True."""
        assert goalie.is_in_left_open_range(1, lower=0, upper=1)

    def test_at_lower_fails(self) -> None:
        """Value at lower bound returns False."""
        assert not goalie.is_in_left_open_range(0, lower=0, upper=1)


class TestIsInRightOpenRange:
    """Tests for `is_in_right_open_range`."""

    def test_at_lower(self) -> None:
        """Value at lower bound returns True."""
        assert goalie.is_in_right_open_range(0, lower=0, upper=1)

    def test_at_upper_fails(self) -> None:
        """Value at upper bound returns False."""
        assert not goalie.is_in_right_open_range(1, lower=0, upper=1)


class TestIsNegative:
    """Tests for `is_negative`."""

    def test_negative(self) -> None:
        """Negative value returns True."""
        assert goalie.is_negative(-1)

    def test_zero_fails(self) -> None:
        """Zero returns False."""
        assert not goalie.is_negative(0)

    def test_positive_fails(self) -> None:
        """Positive value returns False."""
        assert not goalie.is_negative(1)


class TestIsPositive:
    """Tests for `is_positive`."""

    def test_positive(self) -> None:
        """Positive value returns True."""
        assert goalie.is_positive(1)

    def test_zero_fails(self) -> None:
        """Zero returns False."""
        assert not goalie.is_positive(0)

    def test_negative_fails(self) -> None:
        """Negative value returns False."""
        assert not goalie.is_positive(-1)


class TestIsNonNegative:
    """Tests for `is_non_negative`."""

    def test_positive(self) -> None:
        """Positive value returns True."""
        assert goalie.is_non_negative(1)

    def test_zero(self) -> None:
        """Zero returns True."""
        assert goalie.is_non_negative(0)

    def test_negative_fails(self) -> None:
        """Negative value returns False."""
        assert not goalie.is_non_negative(-1)


class TestIsNonPositive:
    """Tests for `is_non_positive`."""

    def test_negative(self) -> None:
        """Negative value returns True."""
        assert goalie.is_non_positive(-1)

    def test_zero(self) -> None:
        """Zero returns True."""
        assert goalie.is_non_positive(0)

    def test_positive_fails(self) -> None:
        """Positive value returns False."""
        assert not goalie.is_non_positive(1)


class TestIsPercentage:
    """Tests for `is_percentage`."""

    def test_valid(self) -> None:
        """Value within 0-100 returns True."""
        assert goalie.is_percentage(50)

    def test_zero(self) -> None:
        """Zero returns True."""
        assert goalie.is_percentage(0)

    def test_hundred(self) -> None:
        """One hundred returns True."""
        assert goalie.is_percentage(100)

    def test_too_high(self) -> None:
        """Value above 100 returns False."""
        assert not goalie.is_percentage(110)

    def test_negative(self) -> None:
        """Negative value returns False."""
        assert not goalie.is_percentage(-10)


class TestIsProportion:
    """Tests for `is_proportion`."""

    def test_valid(self) -> None:
        """Value within 0-1 returns True."""
        assert goalie.is_proportion(0.5)

    def test_zero(self) -> None:
        """Zero returns True."""
        assert goalie.is_proportion(0)

    def test_one(self) -> None:
        """One returns True."""
        assert goalie.is_proportion(1)

    def test_too_high(self) -> None:
        """Value above 1 returns False."""
        assert not goalie.is_proportion(1.1)
