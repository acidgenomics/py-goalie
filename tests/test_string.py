"""Tests for goalie._string module."""

import goalie


class TestIsHexColor:
    """Tests for `is_hex_color`."""

    def test_six_digit(self) -> None:
        """Six-digit hex color is valid."""
        assert goalie.is_hex_color("#FF0000")

    def test_lowercase(self) -> None:
        """Lowercase hex color is valid."""
        assert goalie.is_hex_color("#ff0000")

    def test_eight_digit_alpha(self) -> None:
        """Eight-digit hex color with alpha channel is valid."""
        assert goalie.is_hex_color("#FF0000FF")

    def test_no_hash(self) -> None:
        """Hex color without leading hash is invalid."""
        assert not goalie.is_hex_color("FF0000")

    def test_wrong_length(self) -> None:
        """Hex color with wrong length is invalid."""
        assert not goalie.is_hex_color("#FFF")

    def test_invalid_chars(self) -> None:
        """Hex color with non-hex characters is invalid."""
        assert not goalie.is_hex_color("#GGGGGG")

    def test_non_string(self) -> None:
        """Non-string input is invalid."""
        assert not goalie.is_hex_color(42)


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
