"""Miscellaneous check functions.

Converted from R check-scalar-isAlpha.R, check-scalar-isHeaderLevel.R,
check-scalar-isOrganism.R, check-scalar-isDark.R,
check-scalar-formalCompress.R.
"""

import os
import re

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name


def is_alpha(x: object) -> GoalieCheckResult:
    """Check whether the input contains an alpha level.

    An alpha level must be a float greater than 0 and less than 1
    (exclusive on both ends).

    Examples
    --------
        >>> is_alpha(0.05)
        GoalieCheckResult(ok=True)
        >>> is_alpha(1.0)
        GoalieCheckResult(ok=False, cause="'1.0' is not in open range (0, 1).")
        >>> is_alpha("xxx")
        GoalieCheckResult(ok=False, cause="''xxx'' is not float.")
    """
    if not isinstance(x, float):
        return _false("'%s' is not float.", _to_name(x))
    if not (0.0 < x < 1.0):
        return _false("'%s' is not in open range (0, 1).", _to_name(x))
    return _TRUE


def is_header_level(x: object) -> GoalieCheckResult:
    """Check whether the input contains a Markdown header level (1-7).

    Examples
    --------
        >>> is_header_level(1)
        GoalieCheckResult(ok=True)
        >>> is_header_level(0)
        GoalieCheckResult(ok=False, cause="'0' is not a valid Markdown header level (1-7).")
    """
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return _false("'%s' is not integerish.", _to_name(x))
    if isinstance(x, float):
        if x != int(x):
            return _false("'%s' is not integerish.", _to_name(x))
        x = int(x)
    if x not in range(1, 8):
        return _false(
            "'%s' is not a valid Markdown header level (1-7).",
            _to_name(x),
        )
    return _TRUE


def is_organism(x: object, *, none_ok: bool = False) -> GoalieCheckResult:
    """Check whether the string input is a full Latin organism name.

    The binomial system of naming species uses Latin words. Each name has
    two parts, the genus and the species. For example, *Homo sapiens*.
    Subspecies (trinomial) names are also supported, e.g.
    *Canis lupus familiaris*.

    Examples
    --------
        >>> is_organism("Homo sapiens")
        GoalieCheckResult(ok=True)
        >>> is_organism("Canis lupus familiaris")
        GoalieCheckResult(ok=True)
        >>> is_organism("Human")
        GoalieCheckResult(ok=False, cause="''Human'' is not a valid Latin organism name.")
    """
    if x is None:
        if none_ok:
            return _TRUE
        return _false("'%s' is None.", _to_name(x))
    if not isinstance(x, str):
        return _false("'%s' is not str.", _to_name(x))
    if len(x) == 0:
        return _false("'%s' contains empty string.", _to_name(x))
    pattern = r"^[A-Z][a-z]+\s[a-z]+(\s[a-z]+)?$"
    if not re.match(pattern, x):
        return _false("'%s' is not a valid Latin organism name.", _to_name(x))
    return _TRUE


def is_dark() -> GoalieCheckResult:
    """Check whether dark mode is preferred.

    Checks for ``GOALIE_DARK`` environment variable or
    ``acid.dark`` style setting.

    Examples
    --------
        >>> is_dark()
        GoalieCheckResult(ok=False, cause='Dark mode is not enabled.')
    """
    dark_env = os.environ.get("GOALIE_DARK", "").lower()
    if dark_env in ("1", "true", "yes"):
        return _TRUE
    return _false("Dark mode is not enabled.")


def formal_compress(compress: object) -> GoalieCheckResult:
    """Check the compress formal argument.

    Valid values are Python compression format strings (``bz2``,
    ``gzip``, ``lzma``, ``xz``, ``zstd``) or a boolean flag.

    Examples
    --------
        >>> formal_compress("gzip")
        GoalieCheckResult(ok=True)
        >>> formal_compress(True)
        GoalieCheckResult(ok=True)
        >>> formal_compress("xxx")
        GoalieCheckResult(ok=False, cause="''xxx'' is not a valid compression format.")
    """
    if isinstance(compress, bool):
        return _TRUE
    if isinstance(compress, str):
        valid = {"bz2", "gzip", "lzma", "xz", "zstd"}
        if compress in valid:
            return _TRUE
        return _false(
            "'%s' is not a valid compression format.",
            _to_name(compress),
        )
    return _false(
        "'%s' is not a valid compression argument (str or bool).",
        _to_name(compress),
    )
