"""Duplicate check functions.

Converted from R check-scalar-hasDuplicates.R.
"""

from collections import Counter

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name


def has_duplicates(x: object) -> GoalieCheckResult:
    """Check whether the input has duplicates.

    Examples
    --------
        >>> has_duplicates(["a", "a"])
        GoalieCheckResult(ok=True)
        >>> has_duplicates(["a", "b"])
        GoalieCheckResult(ok=False, cause="'list' has no duplicates.")
    """
    try:
        seen: set[object] = set()
        for item in x:
            if item in seen:
                return _TRUE
            seen.add(item)
    except TypeError:
        # Unhashable items: fall back to O(n^2) check.
        items = list(x)
        for i, item in enumerate(items):
            if item in items[:i]:
                return _TRUE
    return _false("'%s' has no duplicates.", _to_name(x))


def has_no_duplicates(x: object) -> GoalieCheckResult:
    """Check whether the input has no duplicates.

    Examples
    --------
        >>> has_no_duplicates(["a", "b"])
        GoalieCheckResult(ok=True)
        >>> has_no_duplicates(["a", "a", "b", "b"])
        GoalieCheckResult(ok=False, cause="'list' has duplicates at positions 2, 4.")
    """
    dupe_positions: list[int] = []
    try:
        seen: set[object] = set()
        for i, item in enumerate(x):
            if item in seen:
                dupe_positions.append(i + 1)
            else:
                seen.add(item)
    except TypeError:
        items = list(x)
        for i, item in enumerate(items):
            if item in items[:i]:
                dupe_positions.append(i + 1)
    if dupe_positions:
        positions = ", ".join(str(p) for p in dupe_positions[:10])
        return _false(
            "'%s' has duplicate%s at position%s %s.",
            _to_name(x),
            "" if len(dupe_positions) == 1 else "s",
            "" if len(dupe_positions) == 1 else "s",
            positions,
        )
    return _TRUE


def is_duplicate(x: object) -> list[bool]:
    """Return which elements in the input are duplicated.

    Unlike Python's built-in approach where only subsequent
    occurrences are flagged, this marks ALL occurrences of
    duplicated values as ``True``.

    Converted from R check-vector-isDuplicate.R.

    Args:
        x: Any iterable (e.g. list, tuple).

    Returns
    -------
        List of bools, one per element. ``True`` if the
        element appears more than once.

    Examples
    --------
        >>> is_duplicate(["a", "a", "b", "b", "c", "d"])
        [True, True, True, True, False, False]
        >>> is_duplicate(["a", "b", "c"])
        [False, False, False]
    """
    items = list(x)
    counts = Counter(items)
    return [counts[item] > 1 for item in items]
