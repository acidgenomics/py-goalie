"""Filesystem check functions."""

import os
import re
import subprocess
import tempfile

_COMPRESS_EXT_PATTERN = re.compile(
    r"\.(gz|bz2|xz|zip|7z|lz|lzma|zst|tar\.gz|tar\.bz2|tar\.xz|tgz|tbz2|txz)$"
)


def has_access(x: str | os.PathLike[str], access: str = "r") -> bool:
    """Check filesystem access rights.

    Parameters
    ----------
    x : str or os.PathLike
        Path to check.
    access : str
        Access rights to check, as a string of ``r``/``w``/``x``.

    Returns
    -------
    bool
        ``True`` if ``x`` has the requested access rights.

    Examples
    --------
    >>> import os
    >>> has_access(os.path.expanduser("~"))
    True
    >>> has_access("nonexistent_path_xyz")
    False
    """
    mode = os.F_OK
    for ch in access.lower():
        if ch == "r":
            mode |= os.R_OK
        elif ch == "w":
            mode |= os.W_OK
        elif ch == "x":
            mode |= os.X_OK
    return os.access(x, mode)


def is_compressed_file(x: str | os.PathLike[str]) -> bool:
    """Check whether the input is a compressed file.

    Checks based on file extension.

    Parameters
    ----------
    x : str or os.PathLike
        File path.

    Returns
    -------
    bool
        ``True`` if ``x`` is an existing file with a compressed extension.

    Examples
    --------
    >>> is_compressed_file("sample.fastq")
    False
    """
    if not os.path.isfile(x):
        return False
    return _COMPRESS_EXT_PATTERN.search(os.path.basename(x).lower()) is not None


def is_temp_file(x: str | os.PathLike[str]) -> bool:
    """Check whether the input is a file inside the system temp directory.

    Parameters
    ----------
    x : str or os.PathLike
        File path.

    Returns
    -------
    bool
        ``True`` if ``x`` is an existing file under the temp directory.

    Examples
    --------
    >>> is_temp_file("/home/user/data.csv")
    False
    """
    if not os.path.isfile(x):
        return False
    abspath = os.path.realpath(x)
    tmpdir = os.path.realpath(tempfile.gettempdir())
    return abspath.startswith(tmpdir)


def is_git_repo(x: str | os.PathLike[str]) -> bool:
    """Check whether the input is a git repository.

    Parameters
    ----------
    x : str or os.PathLike
        Directory path.

    Returns
    -------
    bool
        ``True`` if ``x`` is a directory tracked by git.

    Examples
    --------
    >>> is_git_repo("/tmp")
    False
    """
    if not os.path.isdir(x):
        return False
    if os.path.isdir(os.path.join(x, ".git")):
        return True
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=x,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return False
    return result.returncode == 0
