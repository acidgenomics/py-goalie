"""String matching check functions.

Converted from R check-vector-isMatching.R.
"""

import functools
import re
from collections.abc import Sequence

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name
from goalie._vectorize import _check_all


def is_matching_regex(
    x: str,
    pattern: str,
) -> GoalieCheckResult:
    """Check whether the string matches a regex pattern.

    Args:
        x: Input string.
        pattern: Regular expression pattern.

    Examples
    --------
        >>> is_matching_regex("foobar", "^f")
        GoalieCheckResult(ok=True)
        >>> is_matching_regex("foobar", "^b")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if re.search(pattern, x):
        return _TRUE
    return _false("'%s' doesn't match pattern '%s'.", x, pattern)


def is_matching_fixed(
    x: str,
    pattern: str,
) -> GoalieCheckResult:
    """Check whether the string contains a fixed (literal) pattern.

    Args:
        x: Input string.
        pattern: Fixed string to search for.

    Examples
    --------
        >>> is_matching_fixed("foobar", "bar")
        GoalieCheckResult(ok=True)
        >>> is_matching_fixed("foobar", "baz")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if pattern in x:
        return _TRUE
    return _false("'%s' doesn't contain '%s'.", x, pattern)


def is_not_matching_regex(
    x: str,
    pattern: str,
) -> GoalieCheckResult:
    """Check whether the string does NOT match a regex pattern.

    Args:
        x: Input string.
        pattern: Regular expression pattern.

    Examples
    --------
        >>> is_not_matching_regex("foobar", "^b")
        GoalieCheckResult(ok=True)
        >>> is_not_matching_regex("foobar", "^f")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if not re.search(pattern, x):
        return _TRUE
    return _false("'%s' matches pattern '%s'.", x, pattern)


def is_not_matching_fixed(
    x: str,
    pattern: str,
) -> GoalieCheckResult:
    """Check whether the string does NOT contain a fixed (literal) pattern.

    Args:
        x: Input string.
        pattern: Fixed string to search for.

    Examples
    --------
        >>> is_not_matching_fixed("foo", "bar")
        GoalieCheckResult(ok=True)
        >>> is_not_matching_fixed("foobar", "bar")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if pattern not in x:
        return _TRUE
    return _false("'%s' contains '%s'.", x, pattern)


def all_are_matching_regex(
    x: Sequence[str],
    pattern: str,
) -> GoalieCheckResult:
    """Check whether all inputs match a regex pattern.

    Examples
    --------
        >>> all_are_matching_regex(["foo", "foobar"], "^foo")
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_matching_regex, pattern=pattern))


def all_are_matching_fixed(
    x: Sequence[str],
    pattern: str,
) -> GoalieCheckResult:
    """Check whether all inputs contain a fixed pattern.

    Examples
    --------
        >>> all_are_matching_fixed(["foobar", "foo"], "foo")
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_matching_fixed, pattern=pattern))


def all_are_not_matching_regex(
    x: Sequence[str],
    pattern: str,
) -> GoalieCheckResult:
    """Check whether no inputs match a regex pattern.

    Examples
    --------
        >>> all_are_not_matching_regex(["bar", "baz"], "^foo")
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_not_matching_regex, pattern=pattern))


def all_are_not_matching_fixed(
    x: Sequence[str],
    pattern: str,
) -> GoalieCheckResult:
    """Check whether no inputs contain a fixed pattern.

    Examples
    --------
        >>> all_are_not_matching_fixed(["bar", "baz"], "foo")
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, functools.partial(is_not_matching_fixed, pattern=pattern))
