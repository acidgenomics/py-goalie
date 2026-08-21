"""String check functions."""

import re

_HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$")


def is_hex_color(x: object) -> bool:
    """Check whether the input is a hexadecimal color code.

    Matches standard 6-digit hex colors with an optional 2-digit alpha
    suffix (e.g. ``#FF0000`` or ``#FF0000FF``).

    Parameters
    ----------
    x : object
        Value to check.

    Returns
    -------
    bool
        ``True`` if ``x`` is a hex color code.

    Examples
    --------
    >>> is_hex_color("#FF0000")
    True
    >>> is_hex_color("#FF0000FF")
    True
    >>> is_hex_color("red")
    False
    """
    return isinstance(x, str) and _HEX_COLOR_PATTERN.match(x) is not None


def is_matching_regex(x: object, pattern: str) -> bool:
    """Check whether the string matches a regex pattern.

    Parameters
    ----------
    x : object
        Value to check.
    pattern : str
        Regular expression pattern.

    Returns
    -------
    bool
        ``True`` if ``x`` is a string and matches ``pattern``.

    Examples
    --------
    >>> is_matching_regex("foobar", "^f")
    True
    >>> is_matching_regex("foobar", "^b")
    False
    """
    return isinstance(x, str) and re.search(pattern, x) is not None
