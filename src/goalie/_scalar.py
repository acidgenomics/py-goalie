"""Scalar type check functions.

Converted from R check-scalar-isScalar.R, check-scalar-isFlag.R,
check-scalar-isString.R, check-scalar-isNumber.R,
check-scalar-isCharacter.R.
"""

from __future__ import annotations

import math
from collections.abc import Sized

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name


def is_scalar(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is scalar (a single element).

    Scalar represents a length of 1. Primitive types (bool, int, float,
    complex, str, bytes) are always scalar. For sized containers (list,
    tuple, dict, set), checks ``len(x) == 1``.

    Examples
    --------
        >>> is_scalar("a")
        GoalieCheckResult(ok=True)
        >>> is_scalar(None)
        GoalieCheckResult(ok=False, cause="'None' is None.")
        >>> is_scalar(["a", "b"])
        GoalieCheckResult(ok=False, cause="'list' doesn't have a length of 1.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if isinstance(x, (bool, int, float, complex, str, bytes)):
        return _TRUE
    if isinstance(x, Sized):
        if len(x) == 1:
            return _TRUE
        return _false("'%s' doesn't have a length of 1.", _to_name(x))
    return _TRUE


def is_scalar_atomic(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is a scalar atomic value.

    Atomic types in Python: bool, int, float, complex, str, bytes.

    Examples
    --------
        >>> is_scalar_atomic("hello")
        GoalieCheckResult(ok=True)
        >>> is_scalar_atomic([1])
        GoalieCheckResult(ok=False, cause="'list' is not atomic.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    ok = is_scalar(x)
    if not ok:
        return ok
    if not isinstance(x, (bool, int, float, complex, str, bytes)):
        return _false("'%s' is not atomic.", _to_name(x))
    return _TRUE


def is_scalar_bool(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is a scalar boolean.

    Examples
    --------
        >>> is_scalar_bool(True)
        GoalieCheckResult(ok=True)
        >>> is_scalar_bool(1)
        GoalieCheckResult(ok=False, cause="'1' is not bool.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if not isinstance(x, bool):
        return _false("'%s' is not bool.", _to_name(x))
    return _TRUE


def is_scalar_float(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is a scalar float.

    Examples
    --------
        >>> is_scalar_float(1.0)
        GoalieCheckResult(ok=True)
        >>> is_scalar_float(1)
        GoalieCheckResult(ok=False, cause="'1' is not float.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if not isinstance(x, float):
        return _false("'%s' is not float.", _to_name(x))
    return _TRUE


def is_scalar_integer(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is a scalar integer (not bool).

    Examples
    --------
        >>> is_scalar_integer(1)
        GoalieCheckResult(ok=True)
        >>> is_scalar_integer(True)
        GoalieCheckResult(ok=False, cause="'True' is not integer.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if isinstance(x, bool) or not isinstance(x, int):
        return _false("'%s' is not integer.", _to_name(x))
    return _TRUE


def is_scalar_integerish(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is a scalar integer-ish value.

    Returns True for int or float values that are whole numbers (e.g. 1.0).

    Examples
    --------
        >>> is_scalar_integerish(1)
        GoalieCheckResult(ok=True)
        >>> is_scalar_integerish(1.0)
        GoalieCheckResult(ok=True)
        >>> is_scalar_integerish(1.5)
        GoalieCheckResult(ok=False, cause="'1.5' is not integerish.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if isinstance(x, bool):
        return _false("'%s' is not integerish.", _to_name(x))
    if isinstance(x, int):
        return _TRUE
    if isinstance(x, float) and math.isfinite(x) and x == int(x):
        return _TRUE
    return _false("'%s' is not integerish.", _to_name(x))


def is_scalar_list(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is a list of length 1.

    Examples
    --------
        >>> is_scalar_list([1])
        GoalieCheckResult(ok=True)
        >>> is_scalar_list([1, 2])
        GoalieCheckResult(ok=False, cause="'list' doesn't have a length of 1.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if not isinstance(x, list):
        return _false("'%s' is not list.", _to_name(x))
    if len(x) != 1:
        return _false("'%s' doesn't have a length of 1.", _to_name(x))
    return _TRUE


def is_scalar_numeric(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is a scalar numeric (int or float, not bool).

    Examples
    --------
        >>> is_scalar_numeric(1)
        GoalieCheckResult(ok=True)
        >>> is_scalar_numeric(1.5)
        GoalieCheckResult(ok=True)
        >>> is_scalar_numeric(True)
        GoalieCheckResult(ok=False, cause="'True' is not numeric.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return _false("'%s' is not numeric.", _to_name(x))
    return _TRUE


def is_scalar_sequence(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is a sequence (list or tuple) of length 1.

    Examples
    --------
        >>> is_scalar_sequence([1])
        GoalieCheckResult(ok=True)
        >>> is_scalar_sequence((1,))
        GoalieCheckResult(ok=True)
        >>> is_scalar_sequence("a")
        GoalieCheckResult(ok=False, cause="''a'' is not a sequence.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if not isinstance(x, (list, tuple)):
        return _false("'%s' is not a sequence.", _to_name(x))
    if len(x) != 1:
        return _false("'%s' doesn't have a length of 1.", _to_name(x))
    return _TRUE


def is_scalar_str(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is a scalar string.

    Examples
    --------
        >>> is_scalar_str("hello")
        GoalieCheckResult(ok=True)
        >>> is_scalar_str(1)
        GoalieCheckResult(ok=False, cause="'1' is not str.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if not isinstance(x, str):
        return _false("'%s' is not str.", _to_name(x))
    return _TRUE


def is_non_scalar(x: object) -> GoalieCheckResult:
    """Check whether the input is non-scalar (not length 1).

    Examples
    --------
        >>> is_non_scalar([1, 2])
        GoalieCheckResult(ok=True)
        >>> is_non_scalar("a")
        GoalieCheckResult(ok=False, cause="''a'' is scalar (has a length of 1).")
    """
    if is_scalar(x):
        return _false("'%s' is scalar (has a length of 1).", _to_name(x))
    return _TRUE


def is_flag(x: object) -> GoalieCheckResult:
    """Check whether the input contains a boolean flag (True/False).

    ``None`` is not considered a valid flag.

    Examples
    --------
        >>> is_flag(True)
        GoalieCheckResult(ok=True)
        >>> is_flag(False)
        GoalieCheckResult(ok=True)
        >>> is_flag(1)
        GoalieCheckResult(ok=False, cause="'1' is not a boolean flag (True/False).")
    """
    if not isinstance(x, bool):
        return _false("'%s' is not a boolean flag (True/False).", _to_name(x))
    return _TRUE


def is_string(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input contains a non-empty string scalar.

    Examples
    --------
        >>> is_string("hello")
        GoalieCheckResult(ok=True)
        >>> is_string("")
        GoalieCheckResult(ok=False, cause="'''' contains empty string.")
        >>> is_string(1)
        GoalieCheckResult(ok=False, cause="'1' is not str.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    ok = is_scalar(x)
    if not ok:
        return ok
    if not isinstance(x, str):
        return _false("'%s' is not str.", _to_name(x))
    if len(x) == 0:
        return _false("'%s' contains empty string.", _to_name(x))
    return _TRUE


def is_number(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input contains a scalar number.

    Alias for ``is_scalar_numeric``.

    Examples
    --------
        >>> is_number(42)
        GoalieCheckResult(ok=True)
        >>> is_number("42")
        GoalieCheckResult(ok=False, cause="''42'' is not numeric.")
    """
    return is_scalar_numeric(x, none_ok=none_ok)


def is_character(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input contains a non-empty character value.

    Checks for a string or a list/tuple of strings. Must have length,
    cannot contain empty strings.

    Examples
    --------
        >>> is_character("hello")
        GoalieCheckResult(ok=True)
        >>> is_character(["a", "b"])
        GoalieCheckResult(ok=True)
        >>> is_character("")
        GoalieCheckResult(ok=False, cause="'''' has empty string at position 0.")
        >>> is_character([])
        GoalieCheckResult(ok=False, cause="'list' has length 0.")
    """
    if x is None:
        return _TRUE if none_ok else _false("'%s' is None.", _to_name(x))
    if isinstance(x, str):
        return (
            _TRUE
            if len(x) > 0
            else _false(
                "'%s' has empty string at position 0.",
                _to_name(x),
            )
        )
    if not isinstance(x, (list, tuple)):
        return _false("'%s' is not character.", _to_name(x))
    if len(x) == 0:
        return _false("'%s' has length 0.", _to_name(x))
    for i, item in enumerate(x):
        if not isinstance(item, str) or len(item) == 0:
            msg = (
                "'%s' is not character at position %d."
                if not isinstance(item, str)
                else "'%s' has empty string at position %d."
            )
            return _false(msg, _to_name(x), i)
    return _TRUE
