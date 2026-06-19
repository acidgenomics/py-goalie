"""Numeric comparison check functions.

Converted from R check-vector-isEqual.R.
"""

import functools
from collections.abc import Sequence
from typing import Protocol, cast, runtime_checkable

from goalie._check import _TRUE, GoalieCheckResult, _false
from goalie._vectorize import _check_all

_TOLERANCE = 1.5e-8


@runtime_checkable
class _SupportsComparison(Protocol):
    def __sub__(self, other: object) -> object: ...
    def __abs__(self) -> object: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...


def is_equal_to(
    x: _SupportsComparison,
    y: _SupportsComparison,
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
    diff = abs(cast(float, x - y))
    if diff <= tolerance:
        return _TRUE
    return _false("%g is not equal to %g (abs diff = %g).", x, y, diff)


def is_not_equal_to(
    x: _SupportsComparison,
    y: _SupportsComparison,
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
    diff = abs(cast(float, x - y))
    if diff > tolerance:
        return _TRUE
    return _false("%g is equal to %g.", x, y)


def is_greater_than(x: _SupportsComparison, y: _SupportsComparison) -> GoalieCheckResult:
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
    x: _SupportsComparison,
    y: _SupportsComparison,
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


def is_less_than(x: _SupportsComparison, y: _SupportsComparison) -> GoalieCheckResult:
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
    x: _SupportsComparison,
    y: _SupportsComparison,
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


def all_are_equal_to(
    x: Sequence[_SupportsComparison],
    y: _SupportsComparison,
    tolerance: float = _TOLERANCE,
) -> GoalieCheckResult:
    """Check whether all inputs are equal to y.

    Examples
    --------
        >>> all_are_equal_to([1, 1, 1], 1)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_equal_to, y=y, tolerance=tolerance))


def all_are_not_equal_to(
    x: Sequence[_SupportsComparison],
    y: _SupportsComparison,
    tolerance: float = _TOLERANCE,
) -> GoalieCheckResult:
    """Check whether no inputs are equal to y.

    Examples
    --------
        >>> all_are_not_equal_to([1, 2, 3], 0)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_not_equal_to, y=y, tolerance=tolerance))


def all_are_greater_than(
    x: Sequence[_SupportsComparison],
    y: _SupportsComparison,
) -> GoalieCheckResult:
    """Check whether all inputs are greater than y.

    Examples
    --------
        >>> all_are_greater_than([2, 3, 4], 1)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_greater_than, y=y))


def all_are_greater_than_or_equal_to(
    x: Sequence[_SupportsComparison],
    y: _SupportsComparison,
) -> GoalieCheckResult:
    """Check whether all inputs are greater than or equal to y.

    Examples
    --------
        >>> all_are_greater_than_or_equal_to([1, 2, 3], 1)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_greater_than_or_equal_to, y=y))


def all_are_less_than(
    x: Sequence[_SupportsComparison],
    y: _SupportsComparison,
) -> GoalieCheckResult:
    """Check whether all inputs are less than y.

    Examples
    --------
        >>> all_are_less_than([-1, 0], 1)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_less_than, y=y))


def all_are_less_than_or_equal_to(
    x: Sequence[_SupportsComparison],
    y: _SupportsComparison,
) -> GoalieCheckResult:
    """Check whether all inputs are less than or equal to y.

    Examples
    --------
        >>> all_are_less_than_or_equal_to([1, 2, 3], 3)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_less_than_or_equal_to, y=y))
