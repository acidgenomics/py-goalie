"""Numeric comparison check functions.

Converted from R check-vector-isEqual.R.
"""

from __future__ import annotations

from goalie._check import _TRUE, GoalieCheckResult, _false

_TOLERANCE = 1.5e-8


def is_equal_to(
    x: object,
    y: object,
    tolerance: float = _TOLERANCE,
) -> GoalieCheckResult:
    """Check whether x is equal to y (within tolerance).

    Args:
        x: Numeric value.
        y: Numeric value to compare against.
        tolerance: Tolerance for floating-point comparison.

    Examples
    --------
        >>> is_equal_to(1, 1.0)
        GoalieCheckResult(ok=True)
        >>> is_equal_to(1, 2)
        GoalieCheckResult(ok=False, cause=...)
    """
    diff = abs(x - y)
    if diff <= tolerance:
        return _TRUE
    return _false("%g is not equal to %g (abs diff = %g).", x, y, diff)


def is_not_equal_to(
    x: object,
    y: object,
    tolerance: float = _TOLERANCE,
) -> GoalieCheckResult:
    """Check whether x is not equal to y.

    Args:
        x: Numeric value.
        y: Numeric value to compare against.
        tolerance: Tolerance for floating-point comparison.

    Examples
    --------
        >>> is_not_equal_to(2, 1)
        GoalieCheckResult(ok=True)
    """
    diff = abs(x - y)
    if diff > tolerance:
        return _TRUE
    return _false("%g is equal to %g.", x, y)


def is_greater_than(x: object, y: object) -> GoalieCheckResult:
    """Check whether x is greater than y.

    Examples
    --------
        >>> is_greater_than(2, 1)
        GoalieCheckResult(ok=True)
        >>> is_greater_than(1, 2)
        GoalieCheckResult(ok=False, cause=...)
    """
    if x > y:
        return _TRUE
    return _false("%g is not greater than %g.", x, y)


def is_greater_than_or_equal_to(
    x: object,
    y: object,
) -> GoalieCheckResult:
    """Check whether x is greater than or equal to y.

    Examples
    --------
        >>> is_greater_than_or_equal_to(1, 1)
        GoalieCheckResult(ok=True)
    """
    if x >= y:
        return _TRUE
    return _false("%g is not greater than or equal to %g.", x, y)


def is_less_than(x: object, y: object) -> GoalieCheckResult:
    """Check whether x is less than y.

    Examples
    --------
        >>> is_less_than(-1, 0)
        GoalieCheckResult(ok=True)
    """
    if x < y:
        return _TRUE
    return _false("%g is not less than %g.", x, y)


def is_less_than_or_equal_to(
    x: object,
    y: object,
) -> GoalieCheckResult:
    """Check whether x is less than or equal to y.

    Examples
    --------
        >>> is_less_than_or_equal_to(1, 3)
        GoalieCheckResult(ok=True)
    """
    if x <= y:
        return _TRUE
    return _false("%g is not less than or equal to %g.", x, y)
