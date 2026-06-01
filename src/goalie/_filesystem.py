"""Filesystem check functions.

Converted from R check-vector functions:
- check-vector-hasAccess.R
- check-vector-isFile.R
- check-vector-isDirectory.R
- check-vector-isCompressedFile.R
- check-vector-isSymlink.R
- check-vector-isTempFile.R
- check-vector-isGitRepo.R
"""

import functools
import os
import re
import subprocess
import tempfile
from collections.abc import Sequence

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name
from goalie._vectorize import _check_all

_COMPRESS_EXT_PATTERN = (
    r"\.(gz|bz2|xz|zip|7z|lz|lzma|zst|"
    r"tar\.gz|tar\.bz2|tar\.xz|tgz|tbz2|txz)$"
)


def has_access(x: str, access: str = "r") -> GoalieCheckResult:
    """Check file system access rights.

    Args:
        x: File or directory path.
        access: String containing 'r' (read), 'w' (write),
            and/or 'x' (execute).

    Examples
    --------
        >>> import os
        >>> has_access(os.path.expanduser("~"))
        GoalieCheckResult(ok=True)
        >>> has_access("nonexistent_path_xyz")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    mode = os.F_OK
    for ch in access.lower():
        if ch == "r":
            mode |= os.R_OK
        elif ch == "w":
            mode |= os.W_OK
        elif ch == "x":
            mode |= os.X_OK
    if os.access(x, mode):
        return _TRUE
    return _false("'%s' does not have '%s' access.", x, access)


def is_file(x: str) -> GoalieCheckResult:
    """Check whether the input is a file.

    Args:
        x: File path.

    Examples
    --------
        >>> is_file("nonexistent_file.txt")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if os.path.isdir(x):
        return _false("'%s' is a directory, not a file.", x)
    if os.path.isfile(x):
        return _TRUE
    return _false("'%s' is not an existing file.", x)


def is_directory(x: str) -> GoalieCheckResult:
    """Check whether the input is a directory.

    Args:
        x: Directory path.

    Examples
    --------
        >>> import os
        >>> is_directory(os.path.expanduser("~"))
        GoalieCheckResult(ok=True)
        >>> is_directory("nonexistent_dir_xyz")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if os.path.isdir(x):
        return _TRUE
    return _false("'%s' is not an existing directory.", x)


def is_compressed_file(x: str) -> GoalieCheckResult:
    """Check whether the input is a compressed file.

    Checks based on file extension.

    Args:
        x: File path.

    Examples
    --------
        >>> is_compressed_file("sample.fastq")
        GoalieCheckResult(ok=False, cause=...)
    """
    result = is_file(x)
    if not result:
        return result
    if re.search(_COMPRESS_EXT_PATTERN, os.path.basename(x).lower()):
        return _TRUE
    return _false("'%s' does not have a compressed file extension.", x)


def is_symlink(x: str) -> GoalieCheckResult:
    """Check whether the input is a symbolic link.

    Args:
        x: File or directory path.

    Examples
    --------
        >>> is_symlink("nonexistent_link")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if not os.path.lexists(x):
        return _false("'%s' does not exist.", x)
    if os.path.islink(x):
        return _TRUE
    return _false("'%s' is not a symbolic link.", x)


def is_temp_file(x: str) -> GoalieCheckResult:
    """Check whether the input is a temporary file.

    Args:
        x: File path.

    Examples
    --------
        >>> is_temp_file("/home/user/data.csv")
        GoalieCheckResult(ok=False, cause=...)
    """
    result = is_file(x)
    if not result:
        return result
    abspath = os.path.abspath(x)
    tmpdir = os.path.realpath(tempfile.gettempdir())
    if abspath.startswith(tmpdir):
        return _TRUE
    return _false("'%s' is not a temporary file.", x)


def is_git_repo(x: str) -> GoalieCheckResult:
    """Check whether the input is a git repository.

    Args:
        x: Directory path.

    Examples
    --------
        >>> is_git_repo("/tmp")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if not os.path.isdir(x):
        return _false("'%s' is not an existing directory.", x)
    if os.path.isdir(os.path.join(x, ".git")):
        return _TRUE
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=x,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            return _TRUE
    except FileNotFoundError:
        pass
    return _false("'%s' is not a git repository.", x)


def all_are_files(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all inputs are existing files.

    Examples
    --------
        >>> all_are_files([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_file)


def all_are_directories(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all inputs are existing directories.

    Examples
    --------
        >>> all_are_directories([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_directory)


def all_are_compressed_files(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all inputs are compressed files.

    Examples
    --------
        >>> all_are_compressed_files([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_compressed_file)


def all_are_symlinks(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all inputs are symbolic links.

    Examples
    --------
        >>> all_are_symlinks([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_symlink)


def all_are_temp_files(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all inputs are temporary files.

    Examples
    --------
        >>> all_are_temp_files([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_temp_file)


def all_are_git_repos(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all inputs are git repositories.

    Examples
    --------
        >>> all_are_git_repos([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_git_repo)


def all_have_access(x: Sequence[str], access: str = "r") -> GoalieCheckResult:
    """Check whether all inputs have the given access rights.

    Examples
    --------
        >>> all_have_access([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, functools.partial(has_access, access=access))
