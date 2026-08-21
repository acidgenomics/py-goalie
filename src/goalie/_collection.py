"""Collection check functions."""

from collections.abc import Hashable, Iterable


def has_duplicates(x: Iterable[Hashable]) -> bool:
    """Check whether the input has duplicate elements.

    Parameters
    ----------
    x : iterable of hashable
        Values to check.

    Returns
    -------
    bool
        ``True`` if any element appears more than once.

    Examples
    --------
    >>> has_duplicates(["a", "a"])
    True
    >>> has_duplicates(["a", "b"])
    False
    """
    seen: set[Hashable] = set()
    for item in x:
        if item in seen:
            return True
        seen.add(item)
    return False


def is_subset(x: Iterable[Hashable], y: Iterable[Hashable]) -> bool:
    """Check whether x is a subset of y.

    Parameters
    ----------
    x : iterable of hashable
        Candidate subset.
    y : iterable of hashable
        Candidate superset.

    Returns
    -------
    bool
        ``True`` if every element of ``x`` is in ``y``.

    Examples
    --------
    >>> is_subset(["a"], ["a", "b"])
    True
    >>> is_subset(["c"], ["a", "b"])
    False
    """
    return set(x) <= set(y)


def are_set_equal(x: Iterable[Hashable], y: Iterable[Hashable]) -> bool:
    """Check whether x and y contain the same elements, ignoring order.

    Parameters
    ----------
    x : iterable of hashable
        First collection to compare.
    y : iterable of hashable
        Second collection to compare.

    Returns
    -------
    bool
        ``True`` if ``x`` and ``y`` have the same set of elements.

    Examples
    --------
    >>> are_set_equal(["a", "b"], ["b", "a"])
    True
    >>> are_set_equal(["a", "b"], ["b", "c"])
    False
    >>> are_set_equal([1, 2, 2], [2, 1])
    True
    """
    return set(x) == set(y)
