"""Goalie: assertive check functions for defensive Python programming."""

from goalie._check import GoalieCheckResult
from goalie._compare import (
    is_equal_to,
    is_greater_than,
    is_greater_than_or_equal_to,
    is_less_than,
    is_less_than_or_equal_to,
    is_not_equal_to,
)
from goalie._dims import (
    has_colnames,
    has_cols,
    has_dimnames,
    has_dims,
    has_nonzero_rows_and_cols,
    has_rows,
    has_unique_cols,
    is_of_dimension,
)
from goalie._duplicates import has_duplicates, has_no_duplicates, is_duplicate
from goalie._filesystem import (
    has_access,
    is_compressed_file,
    is_directory,
    is_file,
    is_git_repo,
    is_symlink,
    is_temp_file,
)
from goalie._hex import is_hex_color
from goalie._length import (
    all_are_atomic,
    are_same_length,
    has_elements,
    has_length,
    n_elements,
)
from goalie._matching import (
    is_matching_fixed,
    is_matching_regex,
    is_not_matching_fixed,
    is_not_matching_regex,
)
from goalie._misc import (
    formal_compress,
    is_alpha,
    is_dark,
    is_header_level,
    is_organism,
)
from goalie._names import (
    has_names,
    has_rownames,
    has_valid_dimnames,
    has_valid_names,
    valid_names,
)
from goalie._range import (
    is_in_closed_range,
    is_in_left_open_range,
    is_in_open_range,
    is_in_range,
    is_in_right_open_range,
    is_negative,
    is_non_negative,
    is_non_positive,
    is_percentage,
    is_positive,
    is_proportion,
)
from goalie._scalar import (
    is_character,
    is_flag,
    is_non_scalar,
    is_number,
    is_scalar,
    is_scalar_atomic,
    is_scalar_bool,
    is_scalar_float,
    is_scalar_integer,
    is_scalar_integerish,
    is_scalar_list,
    is_scalar_numeric,
    is_scalar_sequence,
    is_scalar_str,
    is_string,
)
from goalie._sets import (
    are_disjoint_sets,
    are_intersecting_sets,
    are_set_equal,
    is_subset,
    is_superset,
)
from goalie._type import is_all, is_any, is_vectorish
from goalie._url import is_aws_s3_uri, is_existing_url, is_url

__all__ = [
    "GoalieCheckResult",
    # Compare.
    "is_equal_to",
    "is_greater_than",
    "is_greater_than_or_equal_to",
    "is_less_than",
    "is_less_than_or_equal_to",
    "is_not_equal_to",
    # Dims.
    "has_colnames",
    "has_cols",
    "has_dimnames",
    "has_dims",
    "has_nonzero_rows_and_cols",
    "has_rows",
    "has_unique_cols",
    "is_of_dimension",
    # Duplicates.
    "has_duplicates",
    "has_no_duplicates",
    "is_duplicate",
    # Filesystem.
    "has_access",
    "is_compressed_file",
    "is_directory",
    "is_file",
    "is_git_repo",
    "is_symlink",
    "is_temp_file",
    # Hex.
    "is_hex_color",
    # Length / atomic.
    "all_are_atomic",
    "are_same_length",
    "has_elements",
    "has_length",
    "n_elements",
    # Matching.
    "is_matching_fixed",
    "is_matching_regex",
    "is_not_matching_fixed",
    "is_not_matching_regex",
    # Misc.
    "formal_compress",
    "is_alpha",
    "is_dark",
    "is_header_level",
    "is_organism",
    # Names.
    "has_names",
    "has_rownames",
    "has_valid_dimnames",
    "has_valid_names",
    "valid_names",
    # Range.
    "is_in_closed_range",
    "is_in_left_open_range",
    "is_in_open_range",
    "is_in_range",
    "is_in_right_open_range",
    "is_negative",
    "is_non_negative",
    "is_non_positive",
    "is_percentage",
    "is_positive",
    "is_proportion",
    # Scalar.
    "is_character",
    "is_flag",
    "is_non_scalar",
    "is_number",
    "is_scalar",
    "is_scalar_atomic",
    "is_scalar_bool",
    "is_scalar_float",
    "is_scalar_integer",
    "is_scalar_integerish",
    "is_scalar_list",
    "is_scalar_numeric",
    "is_scalar_sequence",
    "is_scalar_str",
    "is_string",
    # Sets.
    "are_disjoint_sets",
    "are_intersecting_sets",
    "are_set_equal",
    "is_subset",
    "is_superset",
    # Type.
    "is_all",
    "is_any",
    "is_vectorish",
    # URL.
    "is_aws_s3_uri",
    "is_existing_url",
    "is_url",
]
