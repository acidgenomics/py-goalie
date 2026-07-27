"""Type check functions.

Converted from R check-scalar-isAll.R, check-scalar-isAny.R,
check-scalar-isVectorish.R.
"""

from collections.abc import Sequence, Set

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name


def is_all(x: object, classes: tuple[type, ...]) -> GoalieCheckResult:
    """Check whether the input belongs to or inherits all of these classes.

    Examples
    --------
        >>> is_all(1, classes=(int, object))
        GoalieCheckResult(ok=True)
        >>> is_all(1, classes=(int, str))
        GoalieCheckResult(ok=False, cause="'1' is not all of: int, str.")
    """
    if not all(isinstance(x, cls) for cls in classes):
        names = ", ".join(cls.__name__ for cls in classes)
        return _false("'%s' is not all of: %s.", _to_name(x), names)
    return _TRUE


def is_any(x: object, classes: tuple[type, ...]) -> GoalieCheckResult:
    """Check whether the object belongs to or inherits any of these classes.

    Examples
    --------
        >>> is_any(1, classes=(int, str))
        GoalieCheckResult(ok=True)
        >>> is_any(1, classes=(str, list))
        GoalieCheckResult(ok=False, cause="'1' is not any of: str, list.")
    """
    if isinstance(x, classes):
        return _TRUE
    names = ", ".join(cls.__name__ for cls in classes)
    return _false("'%s' is not any of: %s.", _to_name(x), names)


def is_vectorish(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the input is vector-like.

    Returns True for list, tuple, set, frozenset, and other non-string,
    non-bytes sequences. Does not consider dicts vector-like.

    Examples
    --------
        >>> is_vectorish([1, 2, 3])
        GoalieCheckResult(ok=True)
        >>> is_vectorish((1, 2))
        GoalieCheckResult(ok=True)
        >>> is_vectorish("hello")
        GoalieCheckResult(ok=False, cause="''hello'' is not a vector.")
    """
    if x is None:
        if none_ok:
            return _TRUE
        return _false("'%s' is None.", _to_name(x))
    if isinstance(x, (list, tuple)):
        return _TRUE
    if isinstance(x, (Set, frozenset)):
        return _TRUE
    if isinstance(x, Sequence) and not isinstance(x, (str, bytes)):
        return _TRUE
    return _false("'%s' is not a vector.", _to_name(x))
