"""Goalie: boolean check functions for defensive Python programming."""

from goalie._collection import are_set_equal, has_duplicates, is_subset
from goalie._errors import CheckError, CheckTypeError, CheckValueError
from goalie._filesystem import (
    has_access,
    is_compressed_file,
    is_git_repo,
    is_temp_file,
)
from goalie._string import is_hex_color, is_matching_regex
from goalie._system import (
    has_cpu,
    has_github_pat,
    has_internet,
    has_ram,
    is_conda_enabled,
    is_docker,
    is_installed,
    is_linux,
    is_macos,
    is_package_version,
    is_system_command,
    is_unix,
    is_vscode,
    is_windows,
)
from goalie._url import is_aws_s3_uri, is_existing_aws_s3_uri, is_existing_url, is_url

__all__ = [
    "CheckError",
    "CheckTypeError",
    "CheckValueError",
    "are_set_equal",
    "has_access",
    "has_cpu",
    "has_duplicates",
    "has_github_pat",
    "has_internet",
    "has_ram",
    "is_aws_s3_uri",
    "is_compressed_file",
    "is_conda_enabled",
    "is_docker",
    "is_existing_aws_s3_uri",
    "is_existing_url",
    "is_git_repo",
    "is_hex_color",
    "is_installed",
    "is_linux",
    "is_macos",
    "is_matching_regex",
    "is_package_version",
    "is_subset",
    "is_system_command",
    "is_temp_file",
    "is_unix",
    "is_url",
    "is_vscode",
    "is_windows",
]
