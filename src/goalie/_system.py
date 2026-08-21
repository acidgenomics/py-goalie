"""System and environment check functions."""

import importlib.metadata
import importlib.util
import os
import platform
import re
import shutil
import socket
import subprocess


def is_linux() -> bool:
    """Check whether the OS is Linux.

    Returns
    -------
    bool
        ``True`` if running on Linux.

    Examples
    --------
    >>> isinstance(is_linux(), bool)
    True
    """
    return platform.system() == "Linux"


def is_macos() -> bool:
    """Check whether the OS is macOS.

    Returns
    -------
    bool
        ``True`` if running on macOS.

    Examples
    --------
    >>> isinstance(is_macos(), bool)
    True
    """
    return platform.system() == "Darwin"


def is_windows() -> bool:
    """Check whether the OS is Windows.

    Returns
    -------
    bool
        ``True`` if running on Windows.

    Examples
    --------
    >>> isinstance(is_windows(), bool)
    True
    """
    return platform.system() == "Windows"


def is_unix() -> bool:
    """Check whether the OS is Unix-based (Linux or macOS).

    Returns
    -------
    bool
        ``True`` if ``os.name`` is ``"posix"``.

    Examples
    --------
    >>> isinstance(is_unix(), bool)
    True
    """
    return os.name == "posix"


def is_docker() -> bool:
    """Check whether the session is running inside Docker.

    Checks for ``/.dockerenv`` (all platforms) and ``docker`` in
    ``/proc/1/cgroup`` (Linux only).

    Returns
    -------
    bool
        ``True`` if running inside a Docker container.

    Examples
    --------
    >>> isinstance(is_docker(), bool)
    True
    """
    if os.path.isfile("/.dockerenv"):
        return True
    cgroup = "/proc/1/cgroup"
    if os.path.isfile(cgroup):
        try:
            with open(cgroup) as fh:
                return "docker" in fh.read()
        except OSError:
            pass
    return False


def is_conda_enabled() -> bool:
    """Check whether a conda environment is active.

    Returns
    -------
    bool
        ``True`` if ``CONDA_PREFIX`` or ``CONDA_DEFAULT_ENV`` is set.

    Examples
    --------
    >>> isinstance(is_conda_enabled(), bool)
    True
    """
    return bool(os.environ.get("CONDA_PREFIX") or os.environ.get("CONDA_DEFAULT_ENV"))


def has_internet() -> bool:
    """Check whether an internet connection is available.

    Attempts a socket connection to 8.8.8.8 on port 53.

    Returns
    -------
    bool
        ``True`` if the connection succeeds.

    Examples
    --------
    >>> isinstance(has_internet(), bool)
    True
    """
    try:
        with socket.create_connection(("8.8.8.8", 53), timeout=3):
            pass
    except OSError:
        return False
    return True


def has_cpu(n: int) -> bool:
    """Check whether the machine has at least n CPU cores.

    Parameters
    ----------
    n : int
        Minimum number of logical CPU cores required.

    Returns
    -------
    bool
        ``True`` if the machine has at least ``n`` cores.

    Raises
    ------
    RuntimeError
        If the CPU count cannot be determined.

    Examples
    --------
    >>> has_cpu(1)
    True
    """
    count = os.cpu_count()
    if count is None:
        msg = "Could not determine CPU count."
        raise RuntimeError(msg)
    return count >= n


def has_ram(n: float) -> bool:
    """Check whether the machine has at least n GB of RAM.

    Parameters
    ----------
    n : float
        Minimum RAM in gigabytes required.

    Returns
    -------
    bool
        ``True`` if the machine has at least ``n`` GB of RAM.

    Raises
    ------
    RuntimeError
        If the available RAM cannot be determined.

    Examples
    --------
    >>> has_ram(1)
    True
    """
    gb: float | None = None
    system = platform.system()
    if system in ("Linux", "Darwin"):
        try:
            page_size = os.sysconf("SC_PAGE_SIZE")
            page_count = os.sysconf("SC_PHYS_PAGES")
            gb = (page_size * page_count) / (1024**3)
        except (AttributeError, ValueError):
            pass
    if gb is None and system == "Darwin":
        try:
            out = subprocess.check_output(
                ["sysctl", "-n", "hw.memsize"],
                text=True,
                timeout=5,
            )
            gb = int(out.strip()) / (1024**3)
        except (OSError, subprocess.SubprocessError, ValueError):
            pass
    if gb is None:
        msg = "Could not determine available RAM."
        raise RuntimeError(msg)
    return gb >= n


def is_installed(x: object) -> bool:
    """Check whether a Python package is installed (importable).

    Does not import the package; uses ``importlib.util.find_spec``.

    Parameters
    ----------
    x : object
        Package name.

    Returns
    -------
    bool
        ``True`` if the package is importable.

    Examples
    --------
    >>> is_installed("os")
    True
    >>> is_installed("nonexistent_pkg_xyz_abc")
    False
    """
    return isinstance(x, str) and importlib.util.find_spec(x) is not None


def is_system_command(x: object) -> bool:
    """Check whether a system command is available on PATH.

    Parameters
    ----------
    x : object
        Command name (e.g. ``"git"``).

    Returns
    -------
    bool
        ``True`` if the command is found on ``PATH``.

    Examples
    --------
    >>> isinstance(is_system_command("python"), bool)
    True
    >>> is_system_command("nonexistent_cmd_xyz_abc")
    False
    """
    return isinstance(x, str) and shutil.which(x) is not None


def is_vscode() -> bool:
    """Check whether the session is running inside VS Code.

    Returns
    -------
    bool
        ``True`` if the ``TERM_PROGRAM`` environment variable is ``"vscode"``.

    Examples
    --------
    >>> isinstance(is_vscode(), bool)
    True
    """
    return os.environ.get("TERM_PROGRAM") == "vscode"


def has_github_pat() -> bool:
    """Check whether a GitHub PAT is set in the environment.

    Checks ``GITHUB_PAT``, ``GITHUB_TOKEN``, and ``GH_TOKEN``.

    Returns
    -------
    bool
        ``True`` if any of the three environment variables is set.

    Examples
    --------
    >>> isinstance(has_github_pat(), bool)
    True
    """
    return any(os.environ.get(var) for var in ("GITHUB_PAT", "GITHUB_TOKEN", "GH_TOKEN"))


def is_package_version(x: str, version: str, op: str = ">=") -> bool:
    """Check whether an installed package satisfies a version constraint.

    Parameters
    ----------
    x : str
        Package name.
    version : str
        Version string to compare against (e.g. ``"1.2.0"``).
    op : str
        Comparison operator: ``">="``, ``">"``, ``"=="``, ``"!="``, ``"<"``,
        or ``"<="``.

    Returns
    -------
    bool
        ``True`` if the installed version satisfies the constraint.
        ``False`` if the package is not installed.

    Raises
    ------
    ValueError
        If ``op`` is not one of the supported operators.

    Examples
    --------
    >>> isinstance(is_package_version("goalie", "0.0.1"), bool)
    True
    >>> is_package_version("nonexistent_pkg_xyz_abc", "1.0.0")
    False
    """
    op_map = {
        ">=": lambda a, b: a >= b,
        ">": lambda a, b: a > b,
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        "<": lambda a, b: a < b,
        "<=": lambda a, b: a <= b,
    }
    if op not in op_map:
        msg = f"Unsupported operator {op!r}."
        raise ValueError(msg)

    def _parse(v: str) -> tuple[int, ...]:
        # Parse only the numeric part before any alpha/beta/rc suffix.
        m = re.match(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?", v)
        if not m:
            return (0,)
        return tuple(int(g) for g in m.groups() if g is not None)

    try:
        installed_str = importlib.metadata.version(x)
    except importlib.metadata.PackageNotFoundError:
        return False
    return op_map[op](_parse(installed_str), _parse(version))
