"""Set comparison functions.

Converted from R check-scalar-sets.R.
"""

from collections.abc import Iterable
from typing import cast

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name
from goalie._length import has_length


def _to_set(obj: object, label: str) -> "set | GoalieCheckResult":
    """Convert obj to a set, returning a failed result if not iterable."""
    if isinstance(obj, set):
        return obj
    try:
        return set(cast("Iterable[object]", obj))
    except TypeError:
        return _false("'%s' is not iterable.", label)


def is_subset(x: object, y: object) -> GoalieCheckResult:
    """Check whether x is a subset of y.

    Examples
    --------
        >>> is_subset(["a"], ["a", "b"])
        GoalieCheckResult(ok=True)
        >>> is_subset(["c"], ["a", "b"])
        GoalieCheckResult(ok=False, cause="'list' has elements not in 'list': c.")
    """
    ok = has_length(x)
    if not ok:
        return ok
    x_set = _to_set(x, _to_name(x))
    if isinstance(x_set, GoalieCheckResult):
        return x_set
    y_set = _to_set(y, _to_name(y))
    if isinstance(y_set, GoalieCheckResult):
        return y_set
    if not x_set.issubset(y_set):
        diff = x_set - y_set
        diff_str = ", ".join(str(d) for d in sorted(diff, key=str)[:10])
        return _false(
            "'%s' has elements not in '%s': %s.",
            _to_name(x),
            _to_name(y),
            diff_str,
        )
    return _TRUE


def is_superset(x: object, y: object) -> GoalieCheckResult:
    """Check whether x is a superset of y.

    Examples
    --------
        >>> is_superset(["a", "b", "c"], ["a", "b"])
        GoalieCheckResult(ok=True)
        >>> is_superset(["a"], ["a", "b"])
        GoalieCheckResult(ok=False, cause="'list' has elements not in 'list': b.")
    """
    return is_subset(x=y, y=x)


def are_disjoint_sets(x: object, y: object) -> GoalieCheckResult:
    """Check whether x and y are disjoint sets (no common elements).

    Examples
    --------
        >>> are_disjoint_sets(["a", "b"], ["c", "d"])
        GoalieCheckResult(ok=True)
        >>> are_disjoint_sets(["a", "b"], ["b", "a"])
        GoalieCheckResult(ok=False, cause="'list' and 'list' have common elements: a, b.")
    """
    ok = has_length(x)
    if not ok:
        return ok
    x_set = _to_set(x, _to_name(x))
    if isinstance(x_set, GoalieCheckResult):
        return x_set
    y_set = _to_set(y, _to_name(y))
    if isinstance(y_set, GoalieCheckResult):
        return y_set
    common = x_set & y_set
    if common:
        common_str = ", ".join(str(c) for c in sorted(common, key=str)[:10])
        return _false(
            "'%s' and '%s' have common elements: %s.",
            _to_name(x),
            _to_name(y),
            common_str,
        )
    return _TRUE


def are_intersecting_sets(x: object, y: object) -> GoalieCheckResult:
    """Check whether x and y have at least one common element.

    Examples
    --------
        >>> are_intersecting_sets(["a", "b"], ["b", "c"])
        GoalieCheckResult(ok=True)
        >>> are_intersecting_sets(["a", "b"], ["c", "d"])
        GoalieCheckResult(ok=False, cause="'list' and 'list' have 0 common elements.")
    """
    ok = has_length(x)
    if not ok:
        return ok
    x_set = _to_set(x, _to_name(x))
    if isinstance(x_set, GoalieCheckResult):
        return x_set
    y_set = _to_set(y, _to_name(y))
    if isinstance(y_set, GoalieCheckResult):
        return y_set
    if not x_set & y_set:
        return _false(
            "'%s' and '%s' have 0 common elements.",
            _to_name(x),
            _to_name(y),
        )
    return _TRUE


def are_set_equal(x: object, y: object) -> GoalieCheckResult:
    """Check whether x and y are set-equal (same elements, ignoring order).

    Examples
    --------
        >>> are_set_equal(["a", "b"], ["b", "a"])
        GoalieCheckResult(ok=True)
        >>> are_set_equal(["a", "b"], ["b", "c"])
        GoalieCheckResult(ok=False, cause="'list' has elements not in 'list': a.")
    """
    ok = has_length(x)
    if not ok:
        return ok
    x_uniq = _to_set(x, _to_name(x))
    if isinstance(x_uniq, GoalieCheckResult):
        return x_uniq
    y_uniq = _to_set(y, _to_name(y))
    if isinstance(y_uniq, GoalieCheckResult):
        return y_uniq
    if len(x_uniq) != len(y_uniq):
        return _false(
            "'%s' and '%s' have different numbers of elements (%d versus %d).",
            _to_name(x),
            _to_name(y),
            len(x_uniq),
            len(y_uniq),
        )
    ok = is_subset(x, y)
    return ok if not ok else is_subset(y, x)
