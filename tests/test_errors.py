"""Tests for goalie._errors module."""

import pickle

import pytest

import goalie
from goalie import CheckError, CheckTypeError, CheckValueError


class TestCheckError:
    """Tests for `CheckError`."""

    def test_message_without_name(self) -> None:
        """Message omits the name when none is given."""
        err = CheckError(1, "a string")
        assert str(err) == "Expected a string, got 1."

    def test_message_with_name(self) -> None:
        """Message includes the name when given."""
        err = CheckError(1, "a string", name="prefix")
        assert str(err) == "prefix must be a string, got 1."

    def test_attributes(self) -> None:
        """Constructor arguments are stored as attributes."""
        err = CheckError(1, "a string", name="prefix")
        assert err.value == 1
        assert err.expected == "a string"
        assert err.name == "prefix"

    def test_pickle_round_trip(self) -> None:
        """Pickling and unpickling preserves the message."""
        err = CheckError(1, "a string", name="prefix")
        restored = pickle.loads(pickle.dumps(err))
        assert str(restored) == str(err)
        assert restored.value == err.value


class TestCheckTypeError:
    """Tests for `CheckTypeError`."""

    def test_is_type_error(self) -> None:
        """`CheckTypeError` is caught by `except TypeError`."""
        with pytest.raises(TypeError):
            raise CheckTypeError(1, "a string")

    def test_is_check_error(self) -> None:
        """`CheckTypeError` is also caught by `except CheckError`."""
        with pytest.raises(CheckError):
            raise CheckTypeError(1, "a string")

    def test_pickle_round_trip(self) -> None:
        """Pickling and unpickling preserves the message."""
        err = CheckTypeError(1, "a string", name="prefix")
        restored = pickle.loads(pickle.dumps(err))
        assert str(restored) == str(err)


class TestCheckValueError:
    """Tests for `CheckValueError`."""

    def test_is_value_error(self) -> None:
        """`CheckValueError` is caught by `except ValueError`."""
        with pytest.raises(ValueError, match="color must be a hex color code"):
            raise CheckValueError("red", "a hex color code", name="color")

    def test_is_check_error(self) -> None:
        """`CheckValueError` is also caught by `except CheckError`."""
        with pytest.raises(CheckError):
            raise CheckValueError("red", "a hex color code", name="color")

    def test_pickle_round_trip(self) -> None:
        """Pickling and unpickling preserves the message."""
        err = CheckValueError("red", "a hex color code", name="color")
        restored = pickle.loads(pickle.dumps(err))
        assert str(restored) == str(err)


def _validate_color(color: object) -> None:
    """Represent the intended `if not check: raise` call-site pattern."""
    if not goalie.is_hex_color(color):
        raise CheckValueError(color, "a hex color code", name="color")


def test_raise_pattern() -> None:
    """The intended `if not check: raise` call-site pattern works end to end."""
    with pytest.raises(CheckValueError, match="color must be a hex color code"):
        _validate_color("red")
