"""Name check functions.

Converted from R check-scalar-hasNames.R, check-scalar-hasValidNames.R,
check-scalar-validNames.R, check-scalar-hasRownames.R.
"""

import keyword

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name
from goalie._duplicates import has_no_duplicates


def has_names(x: object) -> GoalieCheckResult:
    """Check whether the input has names.

    For dicts, checks for non-empty keys. For objects with a ``columns``
    attribute (e.g. pandas DataFrames), checks column names.

    Examples
    --------
        >>> has_names({"a": 1, "b": 2})
        GoalieCheckResult(ok=True)
        >>> has_names([1, 2])
        GoalieCheckResult(ok=False, cause="'list' does not have names.")
    """
    if isinstance(x, dict):
        return (
            _TRUE
            if len(x) > 0
            else _false(
                "The names of '%s' are empty.",
                _to_name(x),
            )
        )
    # Support pandas-like objects with .columns.
    columns = getattr(x, "columns", None)
    if columns is not None:
        try:
            cols = list(columns)
        except Exception:
            return _false("'columns' on '%s' failed.", _to_name(x))
        if len(cols) == 0:
            return _false("The names of '%s' are empty.", _to_name(x))
        return _TRUE
    # Support objects with .__dict__ keys or named tuples.
    if hasattr(x, "_fields") and len(x._fields) > 0:
        return _TRUE
    return _false("'%s' does not have names.", _to_name(x))


def has_valid_names(x: object) -> GoalieCheckResult:
    """Check whether the input has syntactically valid names.

    For dicts, checks that all keys are valid Python identifiers.
    For objects with ``columns``, checks column names.

    Examples
    --------
        >>> has_valid_names({"a": 1, "b": 2})
        GoalieCheckResult(ok=True)
        >>> has_valid_names({"1bad": 1})
        GoalieCheckResult(ok=False, cause="'dict' has invalid names: [0] 1bad.")
    """
    ok = has_names(x)
    if not ok:
        return ok
    names = _get_names(x)
    if names is None:
        return _false("'%s' doesn't have names.", _to_name(x))
    return valid_names(names)


def has_valid_dimnames(x: object) -> GoalieCheckResult:
    """Check whether the input has valid dimension names.

    Works with objects that have ``index`` and ``columns`` attributes
    (e.g. pandas DataFrames).

    Examples
    --------
        >>> has_valid_dimnames({"a": 1})
        GoalieCheckResult(ok=True)
    """
    # Check row names (index).
    index = getattr(x, "index", None)
    if index is not None:
        try:
            row_names = [str(n) for n in index]
        except Exception:
            return _false("'index' on '%s' failed.", _to_name(x))
        if len(row_names) > 0 and not all(isinstance(n, int) for n in index):
            ok = valid_names(row_names)
            if not ok:
                return ok
    # Check column names.
    columns = getattr(x, "columns", None)
    if columns is not None:
        try:
            col_names = [str(c) for c in columns]
        except Exception:
            return _false("'columns' on '%s' failed.", _to_name(x))
        if len(col_names) > 0:
            ok = valid_names(col_names)
            if not ok:
                return ok
    return _TRUE


def valid_names(x: object) -> GoalieCheckResult:
    """Check whether the values are valid Python identifiers.

    Checks that all strings are valid Python identifiers that are not
    keywords. No duplicates allowed.

    Examples
    --------
        >>> valid_names(["sample_1", "sample_2"])
        GoalieCheckResult(ok=True)
        >>> valid_names(["1bad", "good"])
        GoalieCheckResult(ok=False, cause="'list' has invalid names: [0] 1bad.")
    """
    if not isinstance(x, (list, tuple)):
        return _false("'%s' is not a list or tuple.", _to_name(x))
    if len(x) == 0:
        return _false("'%s' is empty.", _to_name(x))
    # Check for non-string entries.
    for i, name in enumerate(x):
        if not isinstance(name, str):
            return _false("'%s' has non-string at position %d.", _to_name(x), i)
    ok = has_no_duplicates(x)
    if not ok:
        return ok
    invalid: list[str] = []
    for i, name in enumerate(x):
        if not name.isidentifier() or keyword.iskeyword(name):
            invalid.append(f"[{i}] {name}")
    if invalid:
        info = ", ".join(invalid[:10])
        return _false("'%s' has invalid names: %s.", _to_name(x), info)
    return _TRUE


def has_rownames(x: object) -> GoalieCheckResult:
    """Check whether the input has row names.

    For pandas DataFrames, checks whether the index contains
    meaningful (non-default integer) row names.

    Examples
    --------
        >>> has_rownames({"a": 1})
        GoalieCheckResult(ok=False, cause="'dict' does not have row names.")
    """
    index = getattr(x, "index", None)
    if index is None:
        return _false("'%s' does not have row names.", _to_name(x))
    try:
        idx_list = list(index)
    except Exception:
        return _false("'index' on '%s' failed.", _to_name(x))
    if len(idx_list) == 0:
        return _false("'%s' has empty row names.", _to_name(x))
    # Check for default integer index (0, 1, 2, ...).
    if idx_list == list(range(len(idx_list))):
        return _false("'%s' has default integer row names.", _to_name(x))
    return _TRUE


def _get_names(x: object) -> list[str] | None:
    """Get names from an object."""
    if isinstance(x, dict):
        return [str(k) for k in x]
    columns = getattr(x, "columns", None)
    if columns is not None:
        try:
            return [str(c) for c in columns]
        except Exception:
            return None
    if hasattr(x, "_fields"):
        return list(x._fields)
    return None
