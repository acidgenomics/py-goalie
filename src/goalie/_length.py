"""Length and element check functions.

Converted from R check-scalar-hasLength.R, check-scalar-hasElements.R,
check-scalar-areSameLength.R, check-scalar-allAreAtomic.R.
"""

from collections.abc import Sized
from typing import cast

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name


def has_length(x: object, n: int | None = None) -> GoalieCheckResult:
    """Check whether the input has a non-zero or defined length.

    Examples
    --------
        >>> has_length([1, 2, 3])
        GoalieCheckResult(ok=True)
        >>> has_length([])
        GoalieCheckResult(ok=False, cause="'list' has length 0.")
        >>> has_length("ab", n=2)
        GoalieCheckResult(ok=True)
    """
    try:
        length = len(cast("Sized", x))
    except TypeError:
        return _false("'%s' has no length.", _to_name(x))
    if n is None:
        if length == 0:
            return _false("'%s' has length 0.", _to_name(x))
        return _TRUE
    if length != n:
        return _false("'%s' doesn't have a length of %d.", _to_name(x), n)
    return _TRUE


def has_elements(x: object, n: int | None = None) -> GoalieCheckResult:
    """Check whether the input has elements.

    Examples
    --------
        >>> has_elements("hello")
        GoalieCheckResult(ok=True)
        >>> has_elements("hello", n=5)
        GoalieCheckResult(ok=True)
        >>> has_elements([])
        GoalieCheckResult(ok=False, cause="'list' has 0 elements.")
    """
    n_x = n_elements(x)
    if n is None:
        if n_x == 0:
            return _false("'%s' has 0 elements.", _to_name(x))
        return _TRUE
    if n_x != n:
        return _false(
            "'%s' has %d element%s, not %d.",
            _to_name(x),
            n_x,
            "" if n_x == 1 else "s",
            n,
        )
    return _TRUE


def n_elements(x: object) -> int:
    """Return the number of elements in an object.

    For nested structures, recursively counts leaf elements.

    Examples
    --------
        >>> n_elements([1, 2, 3])
        3
        >>> n_elements({"a": [1, 2], "b": [3]})
        3
    """
    if isinstance(x, dict):
        return sum(n_elements(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        total = 0
        for item in x:
            if isinstance(item, (list, tuple, dict)):
                total += n_elements(item)
            else:
                total += 1
        return total
    if isinstance(x, Sized) and not isinstance(x, (str, bytes)):
        return len(x)
    return 1


def are_same_length(x: object, y: object) -> GoalieCheckResult:
    """Check whether the inputs have the same length.

    Examples
    --------
        >>> are_same_length([1, 2], [3, 4])
        GoalieCheckResult(ok=True)
        >>> are_same_length([1], [2, 3])
        GoalieCheckResult(ok=False, cause="'list' doesn't have the same length as 'list'.")
    """
    ok = has_length(x)
    if not ok:
        return ok
    ok = has_length(y)
    if not ok:
        return ok
    if len(cast("Sized", x)) != len(cast("Sized", y)):
        return _false(
            "'%s' doesn't have the same length as '%s'.",
            _to_name(x),
            _to_name(y),
        )
    return _TRUE


def all_are_atomic(x: object) -> GoalieCheckResult:
    """Check whether the input contains elements that are all atomic.

    Atomic types: bool, int, float, complex, str, bytes.

    Examples
    --------
        >>> all_are_atomic({"a": "foo", "b": "bar"})
        GoalieCheckResult(ok=True)
        >>> all_are_atomic({"a": "x", "b": []})
        GoalieCheckResult(ok=False, cause="Not all elements in 'dict' are atomic.")
    """
    ok = has_length(x)
    if not ok:
        return ok
    atomic_types = (bool, int, float, complex, str, bytes, type(None))
    if isinstance(x, dict):
        items = x.values()
    elif isinstance(x, (list, tuple, set, frozenset)):
        items = x
    else:
        return _false("'%s' is not iterable.", _to_name(x))
    if not all(isinstance(item, atomic_types) for item in items):
        return _false("Not all elements in '%s' are atomic.", _to_name(x))
    return _TRUE
