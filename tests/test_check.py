"""Tests for goalie._check module."""

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name


class TestGoalieCheckResult:
    """Tests for GoalieCheckResult."""

    def test_true_result(self) -> None:
        """True result is truthy with empty cause."""
        result = GoalieCheckResult(ok=True)
        assert result
        assert result.cause == ""

    def test_false_result(self) -> None:
        """False result is falsy with cause message."""
        result = GoalieCheckResult(ok=False, cause="test cause")
        assert not result
        assert result.cause == "test cause"

    def test_repr_true(self) -> None:
        """Repr of true result shows ok=True."""
        assert repr(_TRUE) == "GoalieCheckResult(ok=True)"

    def test_repr_false(self) -> None:
        """Repr of false result includes cause message."""
        result = _false("bad input")
        assert "bad input" in repr(result)


class TestToName:
    """Tests for _to_name."""

    def test_none(self) -> None:
        """None renders as 'None'."""
        assert _to_name(None) == "None"

    def test_int(self) -> None:
        """Integer renders as its string representation."""
        assert _to_name(42) == "42"

    def test_str(self) -> None:
        """String renders with surrounding quotes."""
        assert _to_name("hello") == "'hello'"

    def test_list(self) -> None:
        """List renders as type name 'list'."""
        assert _to_name([1, 2]) == "list"

    def test_dict(self) -> None:
        """Dict renders as type name 'dict'."""
        assert _to_name({"a": 1}) == "dict"
