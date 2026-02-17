"""Tests for goalie._scalar module."""

import goalie


class TestIsScalar:
    """Tests for `is_scalar`."""

    def test_string(self) -> None:
        """String is scalar."""
        assert goalie.is_scalar("a")

    def test_int(self) -> None:
        """Integer is scalar."""
        assert goalie.is_scalar(1)

    def test_float(self) -> None:
        """Float is scalar."""
        assert goalie.is_scalar(1.5)

    def test_bool(self) -> None:
        """Boolean is scalar."""
        assert goalie.is_scalar(True)

    def test_none_fails(self) -> None:
        """None is not scalar by default."""
        assert not goalie.is_scalar(None)

    def test_none_ok(self) -> None:
        """None is scalar when none_ok is True."""
        assert goalie.is_scalar(None, none_ok=True)

    def test_list_of_two(self) -> None:
        """List of two elements is not scalar."""
        assert not goalie.is_scalar(["a", "b"])

    def test_list_of_one(self) -> None:
        """Single-element list is scalar."""
        assert goalie.is_scalar([1])


class TestIsScalarBool:
    """Tests for `is_scalar_bool`."""

    def test_true(self) -> None:
        """True is a scalar bool."""
        assert goalie.is_scalar_bool(True)

    def test_false(self) -> None:
        """False is a scalar bool."""
        assert goalie.is_scalar_bool(False)

    def test_int_fails(self) -> None:
        """Integer is not a scalar bool."""
        assert not goalie.is_scalar_bool(1)


class TestIsScalarInteger:
    """Tests for `is_scalar_integer`."""

    def test_int(self) -> None:
        """Integer is a scalar integer."""
        assert goalie.is_scalar_integer(1)

    def test_bool_fails(self) -> None:
        """Boolean is not a scalar integer."""
        assert not goalie.is_scalar_integer(True)

    def test_float_fails(self) -> None:
        """Float is not a scalar integer."""
        assert not goalie.is_scalar_integer(1.0)


class TestIsScalarFloat:
    """Tests for `is_scalar_float`."""

    def test_float(self) -> None:
        """Float is a scalar float."""
        assert goalie.is_scalar_float(1.0)

    def test_int_fails(self) -> None:
        """Integer is not a scalar float."""
        assert not goalie.is_scalar_float(1)


class TestIsScalarIntegerish:
    """Tests for `is_scalar_integerish`."""

    def test_int(self) -> None:
        """Integer is scalar integerish."""
        assert goalie.is_scalar_integerish(1)

    def test_float_whole(self) -> None:
        """Whole float is scalar integerish."""
        assert goalie.is_scalar_integerish(1.0)

    def test_float_fractional(self) -> None:
        """Fractional float is not scalar integerish."""
        assert not goalie.is_scalar_integerish(1.5)

    def test_bool_fails(self) -> None:
        """Boolean is not scalar integerish."""
        assert not goalie.is_scalar_integerish(True)


class TestIsScalarNumeric:
    """Tests for `is_scalar_numeric`."""

    def test_int(self) -> None:
        """Integer is scalar numeric."""
        assert goalie.is_scalar_numeric(1)

    def test_float(self) -> None:
        """Float is scalar numeric."""
        assert goalie.is_scalar_numeric(1.5)

    def test_bool_fails(self) -> None:
        """Boolean is not scalar numeric."""
        assert not goalie.is_scalar_numeric(True)

    def test_str_fails(self) -> None:
        """String is not scalar numeric."""
        assert not goalie.is_scalar_numeric("1")


class TestIsScalarStr:
    """Tests for `is_scalar_str`."""

    def test_str(self) -> None:
        """String is a scalar string."""
        assert goalie.is_scalar_str("hello")

    def test_empty_str(self) -> None:
        """Empty string is a scalar string."""
        assert goalie.is_scalar_str("")

    def test_int_fails(self) -> None:
        """Integer is not a scalar string."""
        assert not goalie.is_scalar_str(1)


class TestIsScalarList:
    """Tests for `is_scalar_list`."""

    def test_single_element(self) -> None:
        """Single-element list is a scalar list."""
        assert goalie.is_scalar_list([1])

    def test_two_elements(self) -> None:
        """Two-element list is not a scalar list."""
        assert not goalie.is_scalar_list([1, 2])

    def test_not_list(self) -> None:
        """Tuple is not a scalar list."""
        assert not goalie.is_scalar_list((1,))


class TestIsScalarSequence:
    """Tests for `is_scalar_sequence`."""

    def test_list_one(self) -> None:
        """Single-element list is a scalar sequence."""
        assert goalie.is_scalar_sequence([1])

    def test_tuple_one(self) -> None:
        """Single-element tuple is a scalar sequence."""
        assert goalie.is_scalar_sequence((1,))

    def test_str_fails(self) -> None:
        """String is not a scalar sequence."""
        assert not goalie.is_scalar_sequence("a")


class TestIsScalarAtomic:
    """Tests for `is_scalar_atomic`."""

    def test_str(self) -> None:
        """String is scalar atomic."""
        assert goalie.is_scalar_atomic("hello")

    def test_int(self) -> None:
        """Integer is scalar atomic."""
        assert goalie.is_scalar_atomic(42)

    def test_list_fails(self) -> None:
        """List is not scalar atomic."""
        assert not goalie.is_scalar_atomic([1])


class TestIsNonScalar:
    """Tests for `is_non_scalar`."""

    def test_list_of_two(self) -> None:
        """Multi-element list is non-scalar."""
        assert goalie.is_non_scalar([1, 2])

    def test_scalar_fails(self) -> None:
        """Scalar string is not non-scalar."""
        assert not goalie.is_non_scalar("a")


class TestIsFlag:
    """Tests for `is_flag`."""

    def test_true(self) -> None:
        """True is a valid flag."""
        assert goalie.is_flag(True)

    def test_false(self) -> None:
        """False is a valid flag."""
        assert goalie.is_flag(False)

    def test_int_fails(self) -> None:
        """Integer is not a valid flag."""
        assert not goalie.is_flag(1)

    def test_none_fails(self) -> None:
        """None is not a valid flag."""
        assert not goalie.is_flag(None)


class TestIsString:
    """Tests for `is_string`."""

    def test_string(self) -> None:
        """Non-empty string is a valid string."""
        assert goalie.is_string("hello")

    def test_empty_fails(self) -> None:
        """Empty string is not a valid string."""
        assert not goalie.is_string("")

    def test_int_fails(self) -> None:
        """Integer is not a valid string."""
        assert not goalie.is_string(1)

    def test_none_ok(self) -> None:
        """None is valid when none_ok is True."""
        assert goalie.is_string(None, none_ok=True)


class TestIsNumber:
    """Tests for `is_number`."""

    def test_int(self) -> None:
        """Integer is a valid number."""
        assert goalie.is_number(42)

    def test_float(self) -> None:
        """Float is a valid number."""
        assert goalie.is_number(3.14)

    def test_str_fails(self) -> None:
        """String is not a valid number."""
        assert not goalie.is_number("42")


class TestIsCharacter:
    """Tests for `is_character`."""

    def test_str(self) -> None:
        """Non-empty string is a valid character."""
        assert goalie.is_character("hello")

    def test_list_of_str(self) -> None:
        """List of strings is a valid character."""
        assert goalie.is_character(["a", "b"])

    def test_empty_str_fails(self) -> None:
        """Empty string is not a valid character."""
        assert not goalie.is_character("")

    def test_empty_list_fails(self) -> None:
        """Empty list is not a valid character."""
        assert not goalie.is_character([])

    def test_none_ok(self) -> None:
        """None is valid when none_ok is True."""
        assert goalie.is_character(None, none_ok=True)

    def test_mixed_list_fails(self) -> None:
        """Mixed-type list is not a valid character."""
        assert not goalie.is_character(["a", 1])
