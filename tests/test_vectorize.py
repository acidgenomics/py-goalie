"""Tests for goalie._vectorize and all_are_* wrappers."""

from goalie._compare import (
    all_are_equal_to,
    all_are_greater_than,
    all_are_greater_than_or_equal_to,
    all_are_less_than,
    all_are_less_than_or_equal_to,
    all_are_not_equal_to,
)
from goalie._filesystem import (
    all_are_directories,
    all_are_files,
    all_have_access,
)
from goalie._hex import all_are_hex_colors
from goalie._matching import (
    all_are_matching_fixed,
    all_are_matching_regex,
    all_are_not_matching_fixed,
    all_are_not_matching_regex,
)
from goalie._range import (
    all_are_in_closed_range,
    all_are_in_open_range,
    all_are_in_range,
    all_are_negative,
    all_are_non_negative,
    all_are_non_positive,
    all_are_percentage,
    all_are_positive,
    all_are_proportion,
)
from goalie._scalar import all_are_integerish
from goalie._url import all_are_aws_s3_uris, all_are_urls
from goalie._vectorize import _check_all


class TestCheckAll:
    def test_empty_fails(self):
        from goalie._scalar import is_string

        result = _check_all([], is_string)
        assert not bool(result)
        assert "no elements" in result.cause

    def test_all_pass(self):
        from goalie._scalar import is_string

        result = _check_all(["a", "b", "c"], is_string)
        assert bool(result)

    def test_first_fails(self):
        from goalie._scalar import is_string

        result = _check_all([1, "b", "c"], is_string)
        assert not bool(result)
        assert "Element 1" in result.cause

    def test_middle_fails(self):
        from goalie._scalar import is_string

        result = _check_all(["a", 2, "c"], is_string)
        assert not bool(result)
        assert "Element 2" in result.cause

    def test_non_iterable_fails(self):
        from goalie._scalar import is_string

        result = _check_all(42, is_string)
        assert not bool(result)


class TestAllAreHexColors:
    def test_pass(self):
        assert bool(all_are_hex_colors(["#FF0000", "#00FF00", "#0000FF"]))

    def test_fail(self):
        assert not bool(all_are_hex_colors(["#FF0000", "red"]))

    def test_empty(self):
        assert not bool(all_are_hex_colors([]))


class TestAllAreUrls:
    def test_pass(self):
        assert bool(all_are_urls(["https://example.com", "http://foo.bar"]))

    def test_fail(self):
        assert not bool(all_are_urls(["https://example.com", "not-a-url"]))

    def test_empty(self):
        assert not bool(all_are_urls([]))


class TestAllAreAwsS3Uris:
    def test_pass(self):
        assert bool(all_are_aws_s3_uris(["s3://bucket/key", "s3://other/path"]))

    def test_fail(self):
        assert not bool(all_are_aws_s3_uris(["s3://bucket/key", "https://example.com"]))


class TestAllAreCompare:
    def test_all_are_equal_to(self):
        assert bool(all_are_equal_to([1, 1, 1], 1))
        assert not bool(all_are_equal_to([1, 2, 1], 1))

    def test_all_are_not_equal_to(self):
        assert bool(all_are_not_equal_to([1, 2, 3], 0))
        assert not bool(all_are_not_equal_to([1, 0, 3], 0))

    def test_all_are_greater_than(self):
        assert bool(all_are_greater_than([2, 3, 4], 1))
        assert not bool(all_are_greater_than([2, 1, 4], 1))

    def test_all_are_greater_than_or_equal_to(self):
        assert bool(all_are_greater_than_or_equal_to([1, 2, 3], 1))
        assert not bool(all_are_greater_than_or_equal_to([1, 0, 3], 1))

    def test_all_are_less_than(self):
        assert bool(all_are_less_than([-1, 0], 1))
        assert not bool(all_are_less_than([-1, 1], 1))

    def test_all_are_less_than_or_equal_to(self):
        assert bool(all_are_less_than_or_equal_to([1, 2, 3], 3))
        assert not bool(all_are_less_than_or_equal_to([1, 2, 4], 3))


class TestAllAreRange:
    def test_all_are_in_range(self):
        assert bool(all_are_in_range([0.1, 0.5, 0.9], lower=0, upper=1))
        assert not bool(all_are_in_range([0.1, 1.1], lower=0, upper=1))

    def test_all_are_in_closed_range(self):
        assert bool(all_are_in_closed_range([0, 0.5, 1], lower=0, upper=1))
        assert not bool(all_are_in_closed_range([0, 1.1], lower=0, upper=1))

    def test_all_are_in_open_range(self):
        assert bool(all_are_in_open_range([0.1, 0.5, 0.9], lower=0, upper=1))
        assert not bool(all_are_in_open_range([0.0, 0.5], lower=0, upper=1))

    def test_all_are_negative(self):
        assert bool(all_are_negative([-1, -2, -3]))
        assert not bool(all_are_negative([-1, 0]))

    def test_all_are_positive(self):
        assert bool(all_are_positive([1, 2, 3]))
        assert not bool(all_are_positive([1, 0]))

    def test_all_are_non_negative(self):
        assert bool(all_are_non_negative([0, 1, 2]))
        assert not bool(all_are_non_negative([0, -1]))

    def test_all_are_non_positive(self):
        assert bool(all_are_non_positive([-1, 0]))
        assert not bool(all_are_non_positive([0, 1]))

    def test_all_are_percentage(self):
        assert bool(all_are_percentage([0, 50, 100]))
        assert not bool(all_are_percentage([0, 101]))

    def test_all_are_proportion(self):
        assert bool(all_are_proportion([0.0, 0.5, 1.0]))
        assert not bool(all_are_proportion([0.0, 1.1]))


class TestAllAreMatching:
    def test_all_are_matching_regex(self):
        assert bool(all_are_matching_regex(["foo", "foobar"], "^foo"))
        assert not bool(all_are_matching_regex(["foo", "bar"], "^foo"))

    def test_all_are_matching_fixed(self):
        assert bool(all_are_matching_fixed(["foobar", "foo"], "foo"))
        assert not bool(all_are_matching_fixed(["foo", "bar"], "foo"))

    def test_all_are_not_matching_regex(self):
        assert bool(all_are_not_matching_regex(["bar", "baz"], "^foo"))
        assert not bool(all_are_not_matching_regex(["foo", "bar"], "^foo"))

    def test_all_are_not_matching_fixed(self):
        assert bool(all_are_not_matching_fixed(["bar", "baz"], "foo"))
        assert not bool(all_are_not_matching_fixed(["foobar", "baz"], "foo"))


class TestAllAreIntegerish:
    def test_pass(self):
        assert bool(all_are_integerish([1, 2.0, 3]))

    def test_fail(self):
        assert not bool(all_are_integerish([1, 1.5]))

    def test_empty(self):
        assert not bool(all_are_integerish([]))


class TestAllAreFilesystem:
    def test_all_are_files_empty(self):
        assert not bool(all_are_files([]))

    def test_all_are_directories_home(self):
        import os

        assert bool(all_are_directories([os.path.expanduser("~")]))

    def test_all_are_directories_empty(self):
        assert not bool(all_are_directories([]))

    def test_all_have_access_home(self):
        import os

        assert bool(all_have_access([os.path.expanduser("~")]))
