"""Dimension check functions.

Converted from R check-scalar-hasDims.R, check-scalar-hasDimnames.R,
check-scalar-hasNonzeroRowsAndCols.R, check-scalar-hasUniqueCols.R,
check-scalar-isOfDimension.R.
"""

from __future__ import annotations

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name


def has_dims(x: object, n: tuple[int, ...] | None = None) -> GoalieCheckResult:
    """Check whether the input has dimensions.

    Works with numpy arrays, pandas DataFrames, and any object with
    a ``shape`` attribute.

    Examples
    --------
        >>> has_dims([[1, 2], [3, 4]])
        GoalieCheckResult(ok=False, cause="'list' has no dimensions.")
    """
    shape = _get_shape(x)
    if shape is None:
        return _false("'%s' has no dimensions.", _to_name(x))
    if n is not None and tuple(shape) != tuple(n):
        return _false(
            "Dimension mismatch for '%s': expected %s; actual %s.",
            _to_name(x),
            str(n),
            str(tuple(shape)),
        )
    return _TRUE


def has_rows(x: object, n: int | None = None) -> GoalieCheckResult:
    """Check whether the input has rows.

    Examples
    --------
        >>> has_rows({"shape": (3, 2)})
        GoalieCheckResult(ok=False, cause="'dict' has no row count.")
    """
    nr = _get_nrow(x)
    if nr is None:
        return _false("'%s' has no row count.", _to_name(x))
    if n is not None:
        if nr != n:
            return _false(
                "Row number mismatch for '%s': expected %d; actual %d.",
                _to_name(x),
                n,
                nr,
            )
    elif nr == 0:
        return _false("The number of rows in '%s' is zero.", _to_name(x))
    return _TRUE


def has_cols(x: object, n: int | None = None) -> GoalieCheckResult:
    """Check whether the input has columns.

    Examples
    --------
        >>> has_cols({"shape": (3, 2)})
        GoalieCheckResult(ok=False, cause="'dict' has no column count.")
    """
    nc = _get_ncol(x)
    if nc is None:
        return _false("'%s' has no column count.", _to_name(x))
    if n is not None:
        if nc != n:
            return _false(
                "Column number mismatch for '%s': expected %d; actual %d.",
                _to_name(x),
                n,
                nc,
            )
    elif nc == 0:
        return _false("The number of columns in '%s' is zero.", _to_name(x))
    return _TRUE


def has_dimnames(x: object) -> GoalieCheckResult:
    """Check whether the input has dimension names.

    For pandas DataFrames, checks that both index and columns are
    non-empty and contain non-empty strings.

    Examples
    --------
        >>> has_dimnames([1, 2])
        GoalieCheckResult(ok=False, cause="'list' has no dimension names.")
    """
    index = getattr(x, "index", None)
    columns = getattr(x, "columns", None)
    if callable(index):
        index = None
    if callable(columns):
        columns = None
    if index is None and columns is None:
        # Try for named dict-like structures.
        if isinstance(x, dict) and len(x) > 0:
            return _TRUE
        return _false("'%s' has no dimension names.", _to_name(x))
    has_idx = index is not None and len(index) > 0
    has_col = columns is not None and len(columns) > 0
    if not has_idx and not has_col:
        return _false(
            "The dimension names of '%s' are all empty.",
            _to_name(x),
        )
    return _TRUE


def has_colnames(x: object) -> GoalieCheckResult:
    """Check whether the input has column names.

    Examples
    --------
        >>> has_colnames([1, 2])
        GoalieCheckResult(ok=False, cause="'list' has no column names.")
    """
    columns = getattr(x, "columns", None)
    if columns is None:
        if isinstance(x, dict) and len(x) > 0:
            return _TRUE
        return _false("'%s' has no column names.", _to_name(x))
    try:
        cols = list(columns)
    except Exception:
        return _false("'columns' on '%s' failed.", _to_name(x))
    if len(cols) == 0:
        return _false("The column names of '%s' are empty.", _to_name(x))
    return _TRUE


def has_nonzero_rows_and_cols(x: object) -> GoalieCheckResult:
    """Check whether the input contains non-zero rows and columns.

    Checks that no row or column sums to zero. Works with numpy arrays
    and any 2D array-like with ``sum`` method or that supports indexing.

    Examples
    --------
        >>> has_nonzero_rows_and_cols([[1, 2], [3, 4]])
        GoalieCheckResult(ok=False, cause="'list' is not a 2D array.")
    """
    shape = _get_shape(x)
    if shape is None or len(shape) != 2:
        return _false("'%s' is not a 2D array.", _to_name(x))
    nrow, ncol = shape
    if nrow == 0 or ncol == 0:
        dim = "rows" if nrow == 0 else "columns"
        return _false("The number of %s in '%s' is zero.", dim, _to_name(x))
    # Check for zero rows and cols using duck typing.
    try:
        # Works for numpy arrays and similar.
        for i in range(nrow):
            row_sum = sum(x[i])
            if row_sum == 0:
                return _false(
                    "'%s' has a zero row at position %d.",
                    _to_name(x),
                    i + 1,
                )
        for j in range(ncol):
            col_sum = sum(x[i][j] for i in range(nrow))
            if col_sum == 0:
                return _false(
                    "'%s' has a zero column at position %d.",
                    _to_name(x),
                    j + 1,
                )
    except TypeError, IndexError, KeyError:
        return _false(
            "'%s' does not support row/column sum checks.",
            _to_name(x),
        )
    return _TRUE


def has_unique_cols(x: object) -> GoalieCheckResult:
    """Check whether the input has columns with unique values.

    Checks a 2D array for duplicated columns.

    Examples
    --------
        >>> has_unique_cols([[1, 1], [2, 2]])
        GoalieCheckResult(ok=False, cause="'list' is not a 2D array.")
    """
    shape = _get_shape(x)
    if shape is None or len(shape) != 2:
        return _false("'%s' is not a 2D array.", _to_name(x))
    _nrow, ncol = shape
    if ncol < 2:
        return _false("'%s' doesn't have >= 2 columns.", _to_name(x))
    try:
        cols: list[tuple[object, ...]] = []
        for j in range(ncol):
            col = tuple(x[i][j] for i in range(shape[0]))
            cols.append(col)
        seen: set[tuple[object, ...]] = set()
        dupes: list[int] = []
        for j, col in enumerate(cols):
            if col in seen:
                dupes.append(j + 1)
            else:
                seen.add(col)
        if dupes:
            positions = ", ".join(str(d) for d in dupes[:10])
            return _false(
                "'%s' has duplicated columns at: %s.",
                _to_name(x),
                positions,
            )
    except TypeError, IndexError, KeyError:
        return _false(
            "'%s' does not support column comparison.",
            _to_name(x),
        )
    return _TRUE


def is_of_dimension(x: object, n: tuple[int, ...] | None) -> GoalieCheckResult:
    """Check whether the input contains specific dimensions.

    Examples
    --------
        >>> is_of_dimension({"shape": (2, 2)}, n=None)
        GoalieCheckResult(ok=False, cause="'dict' has no dimensions.")
    """
    shape = _get_shape(x)
    if n is None:
        if shape is not None:
            return _false(
                "'%s' has dimensions %s, not None.",
                _to_name(x),
                str(tuple(shape)),
            )
        return _TRUE
    if shape is None:
        return _false("'%s' has no dimensions.", _to_name(x))
    shape_tuple = tuple(shape)
    n_tuple = tuple(n)
    mismatches = [
        i + 1
        for i, (s, expected) in enumerate(
            zip(shape_tuple, n_tuple, strict=False),
        )
        if s != expected
    ]
    if len(shape_tuple) != len(n_tuple) or mismatches:
        positions = ", ".join(str(m) for m in mismatches) if mismatches else "all"
        return _false(
            "Dimension%s %s of '%s' %s incorrect.",
            "" if len(mismatches) == 1 else "s",
            positions,
            _to_name(x),
            "is" if len(mismatches) == 1 else "are",
        )
    return _TRUE


def _get_shape(x: object) -> tuple[int, ...] | None:
    """Get shape from an object, if available."""
    shape = getattr(x, "shape", None)
    if shape is not None:
        try:
            return tuple(int(s) for s in shape)
        except TypeError, ValueError:
            return None
    return None


def _get_nrow(x: object) -> int | None:
    """Get number of rows from an object."""
    shape = _get_shape(x)
    if shape is not None and len(shape) >= 1:
        return shape[0]
    return None


def _get_ncol(x: object) -> int | None:
    """Get number of columns from an object."""
    shape = _get_shape(x)
    if shape is not None and len(shape) >= 2:
        return shape[1]
    return None
