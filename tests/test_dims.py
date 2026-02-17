"""Tests for goalie._dims module."""

import goalie


class TestHasDims:
    """Tests for `has_dims`."""

    def test_no_shape(self) -> None:
        """Object without shape attribute returns False."""
        assert not goalie.has_dims([1, 2])

    def test_dict_fails(self) -> None:
        """Dict without shape attribute returns False."""
        assert not goalie.has_dims({"a": 1})


class TestHasRows:
    """Tests for `has_rows`."""

    def test_no_shape(self) -> None:
        """Object without shape attribute returns False."""
        assert not goalie.has_rows([1, 2])


class TestHasCols:
    """Tests for `has_cols`."""

    def test_no_shape(self) -> None:
        """Object without shape attribute returns False."""
        assert not goalie.has_cols([1, 2])


class TestHasDimnames:
    """Tests for `has_dimnames`."""

    def test_no_attrs(self) -> None:
        """Object without dimension names returns False."""
        assert not goalie.has_dimnames([1, 2])


class TestHasColnames:
    """Tests for `has_colnames`."""

    def test_no_columns(self) -> None:
        """Object without columns attribute returns False."""
        assert not goalie.has_colnames([1, 2])


class TestHasNonzeroRowsAndCols:
    """Tests for `has_nonzero_rows_and_cols`."""

    def test_no_shape(self) -> None:
        """Object without shape attribute returns False."""
        assert not goalie.has_nonzero_rows_and_cols([1, 2])


class TestHasUniqueCols:
    """Tests for `has_unique_cols`."""

    def test_no_shape(self) -> None:
        """Object without shape attribute returns False."""
        assert not goalie.has_unique_cols([1, 2])


class TestIsOfDimension:
    """Tests for `is_of_dimension`."""

    def test_no_shape(self) -> None:
        """Object without shape attribute returns False."""
        assert not goalie.is_of_dimension([1, 2], n=(2,))
