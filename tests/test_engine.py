"""Tests for goalie._engine."""

import pytest

from goalie._check import _TRUE, GoalieCheckResult
from goalie._engine import GoalieAssertionError, assert_, validate
from goalie._scalar import is_string


class TestAssert:
    def test_pass_single(self):
        assert_(_TRUE)

    def test_pass_multiple(self):
        assert_(_TRUE, _TRUE, _TRUE)

    def test_pass_bool_true(self):
        assert_(True)

    def test_fail_raises(self):
        bad = GoalieCheckResult(ok=False, cause="x is bad.")
        with pytest.raises(GoalieAssertionError, match="x is bad."):
            assert_(bad)

    def test_fail_first_only(self):
        bad1 = GoalieCheckResult(ok=False, cause="first failure.")
        bad2 = GoalieCheckResult(ok=False, cause="second failure.")
        with pytest.raises(GoalieAssertionError, match="first failure."):
            assert_(bad1, bad2)

    def test_fail_bool_false(self):
        with pytest.raises(GoalieAssertionError):
            assert_(False)

    def test_fail_custom_msg(self):
        bad = GoalieCheckResult(ok=False, cause="original cause.")
        with pytest.raises(GoalieAssertionError, match="custom override"):
            assert_(bad, msg="custom override")

    def test_causes_attribute(self):
        bad = GoalieCheckResult(ok=False, cause="some cause.")
        with pytest.raises(GoalieAssertionError) as exc_info:
            assert_(bad)
        assert exc_info.value.causes == ["some cause."]

    def test_is_assertion_error(self):
        with pytest.raises(AssertionError):
            assert_(GoalieCheckResult(ok=False, cause="fail."))

    def test_with_check_fn(self):
        assert_(is_string("hello"))

    def test_with_check_fn_fail(self):
        with pytest.raises(GoalieAssertionError):
            assert_(is_string(123))


class TestValidate:
    def test_pass_returns_none(self):
        assert validate(_TRUE) is None

    def test_pass_multiple(self):
        assert validate(_TRUE, _TRUE) is None

    def test_fail_returns_list(self):
        bad = GoalieCheckResult(ok=False, cause="x is bad.")
        result = validate(bad)
        assert result == ["x is bad."]

    def test_fail_collects_all(self):
        bad1 = GoalieCheckResult(ok=False, cause="first.")
        bad2 = GoalieCheckResult(ok=False, cause="second.")
        result = validate(bad1, bad2)
        assert result == ["first.", "second."]

    def test_mixed_pass_fail(self):
        bad = GoalieCheckResult(ok=False, cause="fail.")
        result = validate(_TRUE, bad, _TRUE)
        assert result == ["fail."]

    def test_bool_false(self):
        result = validate(False)
        assert result == ["Check failed."]

    def test_bool_true(self):
        assert validate(True) is None
