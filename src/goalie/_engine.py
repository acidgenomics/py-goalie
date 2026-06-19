"""Assert and validate engine for goalie check results."""

from goalie._check import GoalieCheckResult


class GoalieAssertionError(AssertionError):
    """Raised by assert_ when one or more checks fail.

    Parameters
    ----------
    msg : str
        Human-readable failure message.
    causes : list[str]
        Cause strings from each failing check.
    """

    __slots__ = ("causes",)

    def __init__(self, msg: str, causes: list[str]) -> None:
        self.causes = causes
        super().__init__(msg)


def assert_(
    *checks: GoalieCheckResult | bool,
    msg: str | None = None,
) -> None:
    """Assert that all check results are True, raising on first failure.

    Drop-in replacement for ``assert`` statements in defensive code.
    Raises ``GoalieAssertionError`` with the cause message on first failure
    (short-circuit, matching R's ``assert()`` behavior).

    Parameters
    ----------
    *checks : GoalieCheckResult | bool
        One or more goalie check results or plain booleans.
    msg : str | None
        Optional override message. If None, uses the cause from the
        failing check.

    Raises
    ------
    GoalieAssertionError
        If any check fails.

    Examples
    --------
        >>> from goalie._check import _TRUE
        >>> assert_(_TRUE)
        >>> from goalie._scalar import is_string
        >>> assert_(is_string("hello"))
    """
    for check in checks:
        if isinstance(check, GoalieCheckResult):
            if not check:
                cause = check.cause
                raise GoalieAssertionError(
                    msg if msg is not None else cause,
                    causes=[cause],
                )
        elif not check:
            raise GoalieAssertionError(
                msg if msg is not None else "Check failed.",
                causes=["Check failed."],
            )


def validate(
    *checks: GoalieCheckResult | bool,
) -> list[str] | None:
    """Validate check results, returning failure causes instead of raising.

    Evaluates ALL checks (not short-circuit) and returns the collected
    failure cause strings, or ``None`` if all checks pass. Useful in
    ``__post_init__``, ``__init_subclass__``, or dataclass validators.

    Parameters
    ----------
    *checks : GoalieCheckResult | bool
        One or more goalie check results or plain booleans.

    Returns
    -------
    list[str] | None
        List of cause strings for each failed check, or None on success.

    Examples
    --------
        >>> from goalie._check import _TRUE
        >>> validate(_TRUE) is None
        True
        >>> from goalie._scalar import is_string
        >>> validate(is_string(1))
        ["'1' is not str."]
    """
    causes: list[str] = []
    for check in checks:
        if isinstance(check, GoalieCheckResult):
            if not check:
                causes.append(check.cause)
        elif not check:
            causes.append("Check failed.")
    return causes if causes else None
