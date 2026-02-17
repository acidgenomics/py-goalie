"""Core check result infrastructure for goalie."""

from __future__ import annotations


class GoalieCheckResult:
    """Result from a goalie check function.

    Evaluates to True on success, False on failure.
    Failed results carry a ``cause`` message.
    """

    __slots__ = ("_cause", "_ok")

    def __init__(self, *, ok: bool, cause: str = "") -> None:
        self._ok = ok
        self._cause = cause

    def __bool__(self) -> bool:
        return self._ok

    def __repr__(self) -> str:
        if self._ok:
            return "GoalieCheckResult(ok=True)"
        return f"GoalieCheckResult(ok=False, cause={self._cause!r})"

    @property
    def cause(self) -> str:
        """Cause of check failure."""
        return self._cause


_TRUE = GoalieCheckResult(ok=True)
"""Singleton for successful check results."""


def _false(msg: str, *args: object) -> GoalieCheckResult:
    """Create a failed check result with cause message."""
    if args:
        msg = msg % args
    return GoalieCheckResult(ok=False, cause=msg)


def _to_name(x: object) -> str:
    """Get a name representation for use in cause messages."""
    if x is None:
        return "None"
    if isinstance(x, (bool, int, float, str)):
        return repr(x)
    return type(x).__name__
