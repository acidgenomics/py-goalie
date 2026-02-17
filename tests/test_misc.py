"""Tests for goalie._misc module."""

import goalie


class TestIsAlpha:
    """Tests for `is_alpha`."""

    def test_valid(self) -> None:
        """Valid alpha value is accepted."""
        assert goalie.is_alpha(0.05)

    def test_zero_fails(self) -> None:
        """Zero is not a valid alpha."""
        assert not goalie.is_alpha(0.0)

    def test_one_fails(self) -> None:
        """One is not a valid alpha."""
        assert not goalie.is_alpha(1.0)

    def test_negative_fails(self) -> None:
        """Negative value is not a valid alpha."""
        assert not goalie.is_alpha(-0.1)

    def test_string_fails(self) -> None:
        """String input is not a valid alpha."""
        assert not goalie.is_alpha("0.05")


class TestIsHeaderLevel:
    """Tests for `is_header_level`."""

    def test_valid_1(self) -> None:
        """Header level 1 is valid."""
        assert goalie.is_header_level(1)

    def test_valid_7(self) -> None:
        """Header level 7 is valid."""
        assert goalie.is_header_level(7)

    def test_zero_fails(self) -> None:
        """Zero is not a valid header level."""
        assert not goalie.is_header_level(0)

    def test_eight_fails(self) -> None:
        """Eight is not a valid header level."""
        assert not goalie.is_header_level(8)


class TestIsOrganism:
    """Tests for `is_organism`."""

    def test_human(self) -> None:
        """Homo sapiens is a valid organism."""
        assert goalie.is_organism("Homo sapiens")

    def test_mouse(self) -> None:
        """Mus musculus is a valid organism."""
        assert goalie.is_organism("Mus musculus")

    def test_lowercase_fails(self) -> None:
        """Lowercase organism name is rejected."""
        assert not goalie.is_organism("homo sapiens")

    def test_single_word_fails(self) -> None:
        """Single word is not a valid organism name."""
        assert not goalie.is_organism("Human")


class TestIsDark:
    """Tests for `is_dark`."""

    def test_returns_result(self) -> None:
        """Returns a boolean or check result."""
        result = goalie.is_dark()
        assert isinstance(result, bool) or hasattr(result, "cause")


class TestFormalCompress:
    """Tests for `formal_compress`."""

    def test_gzip(self) -> None:
        """Gzip is a valid compression format."""
        assert goalie.formal_compress("gzip")

    def test_bz2(self) -> None:
        """Bz2 is a valid compression format."""
        assert goalie.formal_compress("bz2")

    def test_xz(self) -> None:
        """Xz is a valid compression format."""
        assert goalie.formal_compress("xz")

    def test_invalid(self) -> None:
        """Invalid string is not a valid compression format."""
        assert not goalie.formal_compress("invalid")

    def test_none_fails(self) -> None:
        """None is not a valid compression format."""
        assert not goalie.formal_compress(None)
