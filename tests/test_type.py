"""Tests for goalie._type module."""

import goalie


class TestIsAll:
    """Tests for `is_all`."""

    def test_int(self) -> None:
        """True when object is an instance of the single listed class."""
        assert goalie.is_all(42, classes=(int,))

    def test_wrong_type(self) -> None:
        """False when object does not match the listed class."""
        assert not goalie.is_all("hello", classes=(int,))

    def test_multi_class_must_be_all(self) -> None:
        """is_all requires x to be an instance of ALL listed classes."""
        assert not goalie.is_all(42, classes=(int, float))

    def test_single_class_match(self) -> None:
        """True when object is an instance of all listed classes."""
        assert goalie.is_all(True, classes=(bool, int))

    def test_list_all_match(self) -> None:
        """True when a list matches the single listed class."""
        assert goalie.is_all([1, 2, 3], classes=(list,))


class TestIsAny:
    """Tests for `is_any`."""

    def test_match(self) -> None:
        """True when object matches one of the listed classes."""
        assert goalie.is_any(42, classes=(int, str))

    def test_no_match(self) -> None:
        """False when object matches none of the listed classes."""
        assert not goalie.is_any("hello", classes=(int, float))


class TestIsVectorish:
    """Tests for `is_vectorish`."""

    def test_list(self) -> None:
        """True for a list."""
        assert goalie.is_vectorish([1, 2, 3])

    def test_tuple(self) -> None:
        """True for a tuple."""
        assert goalie.is_vectorish((1, 2))

    def test_str_fails(self) -> None:
        """False for a string."""
        assert not goalie.is_vectorish("hello")

    def test_int_fails(self) -> None:
        """False for an int."""
        assert not goalie.is_vectorish(42)

    def test_dict_fails(self) -> None:
        """False for a dict."""
        assert not goalie.is_vectorish({"a": 1})
