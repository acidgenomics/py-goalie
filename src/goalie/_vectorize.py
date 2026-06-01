"""Vectorized batch check utilities."""

from collections.abc import Callable, Sequence

from goalie._check import _TRUE, GoalieCheckResult, _false


def _check_all(
    x: Sequence[object],
    check_fn: Callable[..., GoalieCheckResult],
    *,
    fn_name: str = "",
) -> GoalieCheckResult:
    """Apply a check function to each element, returning a scalar result.

    Returns ``_TRUE`` if all elements pass. On the first failure,
    returns a failed result with the cause annotated with position.

    Parameters
    ----------
    x : Sequence[object]
        Items to check.
    check_fn : Callable[[object], GoalieCheckResult]
        Single-argument check function.
    fn_name : str
        Optional name of the calling function for cause messages.

    Examples
    --------
        >>> from goalie._filesystem import is_file
        >>> _check_all([], is_file)
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    try:
        items = list(x)
    except TypeError:
        return _false("Input is not iterable.")
    if not items:
        return _false("Input has no elements.")
    for i, item in enumerate(items):
        result = check_fn(item)
        if not result:
            prefix = f"{fn_name}: " if fn_name else ""
            return _false("%sElement %d failed: %s", prefix, i + 1, result.cause)
    return _TRUE
