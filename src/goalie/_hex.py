"""Hex color check functions.

Converted from R check-vector-isHexColor.R.
"""

from __future__ import annotations

import re

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name


def is_hex_color(x: str) -> GoalieCheckResult:
    """Check whether the input is a hexadecimal color code.

    Matches standard 6-digit hex colors with optional 2-digit
    alpha suffix (e.g. ``#FF0000`` or ``#FF0000FF``).

    Args:
        x: Input string.

    Examples
    --------
        >>> is_hex_color("#FF0000")
        GoalieCheckResult(ok=True)
        >>> is_hex_color("#FF0000FF")
        GoalieCheckResult(ok=True)
        >>> is_hex_color("red")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if re.match(
        r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$",
        x,
    ):
        return _TRUE
    return _false("'%s' is not a hex color code.", x)
