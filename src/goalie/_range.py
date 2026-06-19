"""Numeric range check functions.

Converted from R check-vector-isInRange.R.
"""

import functools
import math
from collections.abc import Sequence

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name
from goalie._vectorize import _check_all


def is_in_range(
    x: object,
    lower: float = -math.inf,
    upper: float = math.inf,
    closed: tuple[bool, bool] = (True, True),
) -> GoalieCheckResult:
    """Check whether the input is in range.

    Args:
        x: Numeric value.
        lower: Lower bound.
        upper: Upper bound.
        closed: Tuple of bools indicating if lower and upper
            bounds are inclusive.

    Examples
    --------
        >>> is_in_range(0.5, lower=0, upper=1)
        GoalieCheckResult(ok=True)
        >>> is_in_range(2, lower=0, upper=1)
        GoalieCheckResult(ok=False, cause=...)
    """
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return _false("'%s' is not numeric.", _to_name(x))
    too_low = (x < lower) if closed[0] else (x <= lower)
    too_high = (x > upper) if closed[1] else (x >= upper)
    if too_low:
        return _false("%g is too low (lower bound: %g).", x, lower)
    if too_high:
        return _false("%g is too high (upper bound: %g).", x, upper)
    return _TRUE


def is_in_closed_range(
    x: object,
    lower: float = -math.inf,
    upper: float = math.inf,
) -> GoalieCheckResult:
    """Check whether the input is in closed range [lower, upper].

    Examples
    --------
        >>> is_in_closed_range(1, lower=0, upper=1)
        GoalieCheckResult(ok=True)
    """
    return is_in_range(x, lower, upper, closed=(True, True))


def is_in_open_range(
    x: object,
    lower: float = -math.inf,
    upper: float = math.inf,
) -> GoalieCheckResult:
    """Check whether the input is in open range (lower, upper).

    Examples
    --------
        >>> is_in_open_range(0.5, lower=0, upper=1)
        GoalieCheckResult(ok=True)
        >>> is_in_open_range(1, lower=0, upper=1)
        GoalieCheckResult(ok=False, cause=...)
    """
    return is_in_range(x, lower, upper, closed=(False, False))


def is_in_left_open_range(
    x: object,
    lower: float = -math.inf,
    upper: float = math.inf,
) -> GoalieCheckResult:
    """Check whether the input is in left-open range (lower, upper].

    Examples
    --------
        >>> is_in_left_open_range(1, lower=0, upper=1)
        GoalieCheckResult(ok=True)
        >>> is_in_left_open_range(0, lower=0, upper=1)
        GoalieCheckResult(ok=False, cause=...)
    """
    return is_in_range(x, lower, upper, closed=(False, True))


def is_in_right_open_range(
    x: object,
    lower: float = -math.inf,
    upper: float = math.inf,
) -> GoalieCheckResult:
    """Check whether the input is in right-open range [lower, upper).

    Examples
    --------
        >>> is_in_right_open_range(0, lower=0, upper=1)
        GoalieCheckResult(ok=True)
        >>> is_in_right_open_range(1, lower=0, upper=1)
        GoalieCheckResult(ok=False, cause=...)
    """
    return is_in_range(x, lower, upper, closed=(True, False))


def is_negative(x: object) -> GoalieCheckResult:
    """Check whether the input is negative (< 0).

    Examples
    --------
        >>> is_negative(-1)
        GoalieCheckResult(ok=True)
        >>> is_negative(0)
        GoalieCheckResult(ok=False, cause=...)
    """
    return is_in_range(x, lower=-math.inf, upper=0, closed=(True, False))


def is_positive(x: object) -> GoalieCheckResult:
    """Check whether the input is positive (> 0).

    Examples
    --------
        >>> is_positive(1)
        GoalieCheckResult(ok=True)
        >>> is_positive(0)
        GoalieCheckResult(ok=False, cause=...)
    """
    return is_in_range(x, lower=0, upper=math.inf, closed=(False, True))


def is_non_negative(x: object) -> GoalieCheckResult:
    """Check whether the input is non-negative (>= 0).

    Examples
    --------
        >>> is_non_negative(0)
        GoalieCheckResult(ok=True)
        >>> is_non_negative(-1)
        GoalieCheckResult(ok=False, cause=...)
    """
    return is_in_range(x, lower=0, upper=math.inf, closed=(True, True))


def is_non_positive(x: object) -> GoalieCheckResult:
    """Check whether the input is non-positive (<= 0).

    Examples
    --------
        >>> is_non_positive(0)
        GoalieCheckResult(ok=True)
        >>> is_non_positive(1)
        GoalieCheckResult(ok=False, cause=...)
    """
    return is_in_range(x, lower=-math.inf, upper=0, closed=(True, True))


def is_percentage(x: object) -> GoalieCheckResult:
    """Check whether the input is a percentage (0 to 100).

    Examples
    --------
        >>> is_percentage(50)
        GoalieCheckResult(ok=True)
        >>> is_percentage(110)
        GoalieCheckResult(ok=False, cause=...)
    """
    return is_in_range(x, lower=0, upper=100, closed=(True, True))


def is_proportion(x: object) -> GoalieCheckResult:
    """Check whether the input is a proportion (0 to 1).

    Examples
    --------
        >>> is_proportion(0.5)
        GoalieCheckResult(ok=True)
        >>> is_proportion(1.1)
        GoalieCheckResult(ok=False, cause=...)
    """
    return is_in_range(x, lower=0, upper=1, closed=(True, True))


def all_are_in_range(
    x: Sequence[object],
    lower: float = -math.inf,
    upper: float = math.inf,
    closed: tuple[bool, bool] = (True, True),
) -> GoalieCheckResult:
    """Check whether all inputs are within the given range.

    Examples
    --------
        >>> all_are_in_range([0.1, 0.5, 0.9], lower=0, upper=1)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_in_range, lower=lower, upper=upper, closed=closed))


def all_are_in_closed_range(
    x: Sequence[object],
    lower: float = -math.inf,
    upper: float = math.inf,
) -> GoalieCheckResult:
    """Check whether all inputs are in closed range [lower, upper].

    Examples
    --------
        >>> all_are_in_closed_range([0, 0.5, 1], lower=0, upper=1)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_in_closed_range, lower=lower, upper=upper))


def all_are_in_open_range(
    x: Sequence[object],
    lower: float = -math.inf,
    upper: float = math.inf,
) -> GoalieCheckResult:
    """Check whether all inputs are in open range (lower, upper).

    Examples
    --------
        >>> all_are_in_open_range([0.1, 0.5, 0.9], lower=0, upper=1)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_in_open_range, lower=lower, upper=upper))


def all_are_in_left_open_range(
    x: Sequence[object],
    lower: float = -math.inf,
    upper: float = math.inf,
) -> GoalieCheckResult:
    """Check whether all inputs are in left-open range (lower, upper].

    Examples
    --------
        >>> all_are_in_left_open_range([0.1, 0.5, 1], lower=0, upper=1)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_in_left_open_range, lower=lower, upper=upper))


def all_are_in_right_open_range(
    x: Sequence[object],
    lower: float = -math.inf,
    upper: float = math.inf,
) -> GoalieCheckResult:
    """Check whether all inputs are in right-open range [lower, upper).

    Examples
    --------
        >>> all_are_in_right_open_range([0, 0.5, 0.9], lower=0, upper=1)
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_in_right_open_range, lower=lower, upper=upper))


def all_are_negative(x: Sequence[object]) -> GoalieCheckResult:
    """Check whether all inputs are negative.

    Examples
    --------
        >>> all_are_negative([-1, -2, -3])
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, is_negative)


def all_are_positive(x: Sequence[object]) -> GoalieCheckResult:
    """Check whether all inputs are positive.

    Examples
    --------
        >>> all_are_positive([1, 2, 3])
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, is_positive)


def all_are_non_negative(x: Sequence[object]) -> GoalieCheckResult:
    """Check whether all inputs are non-negative.

    Examples
    --------
        >>> all_are_non_negative([0, 1, 2])
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, is_non_negative)


def all_are_non_positive(x: Sequence[object]) -> GoalieCheckResult:
    """Check whether all inputs are non-positive.

    Examples
    --------
        >>> all_are_non_positive([-1, 0])
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, is_non_positive)


def all_are_percentage(x: Sequence[object]) -> GoalieCheckResult:
    """Check whether all inputs are percentages (0-100).

    Examples
    --------
        >>> all_are_percentage([0, 50, 100])
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, is_percentage)


def all_are_proportion(x: Sequence[object]) -> GoalieCheckResult:
    """Check whether all inputs are proportions (0-1).

    Examples
    --------
        >>> all_are_proportion([0.0, 0.5, 1.0])
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, is_proportion)
