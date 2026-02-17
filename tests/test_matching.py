"""Tests for goalie._matching module."""

import goalie


class TestIsMatchingRegex:
    """Tests for `is_matching_regex`."""

    def test_match(self) -> None:
        """String matching regex pattern returns True."""
        assert goalie.is_matching_regex("hello world", r"^hello")

    def test_no_match(self) -> None:
        """String not matching regex pattern returns False."""
        assert not goalie.is_matching_regex("goodbye", r"^hello")

    def test_complex_pattern(self) -> None:
        """Complex regex pattern matches correctly."""
        assert goalie.is_matching_regex("abc123", r"\d+")

    def test_non_string(self) -> None:
        """Non-string input returns False."""
        assert not goalie.is_matching_regex(42, r"\d+")


class TestIsMatchingFixed:
    """Tests for `is_matching_fixed`."""

    def test_match(self) -> None:
        """String containing fixed substring returns True."""
        assert goalie.is_matching_fixed("hello world", "hello")

    def test_no_match(self) -> None:
        """String not containing fixed substring returns False."""
        assert not goalie.is_matching_fixed("goodbye", "hello")

    def test_non_string(self) -> None:
        """Non-string input returns False."""
        assert not goalie.is_matching_fixed(42, "hello")


class TestIsNotMatchingRegex:
    """Tests for `is_not_matching_regex`."""

    def test_no_match(self) -> None:
        """String not matching regex pattern returns True."""
        assert goalie.is_not_matching_regex("goodbye", r"^hello")

    def test_has_match(self) -> None:
        """String matching regex pattern returns False."""
        assert not goalie.is_not_matching_regex("hello world", r"^hello")


class TestIsNotMatchingFixed:
    """Tests for `is_not_matching_fixed`."""

    def test_no_match(self) -> None:
        """String not containing fixed substring returns True."""
        assert goalie.is_not_matching_fixed("goodbye", "hello")

    def test_has_match(self) -> None:
        """String containing fixed substring returns False."""
        assert not goalie.is_not_matching_fixed("hello world", "hello")
