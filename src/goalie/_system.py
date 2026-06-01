"""System and environment check functions.

Converted from R system-check-scalar-* and system-check-vector-* functions.
"""

import importlib.util
import os
import platform
import shutil
import socket
import subprocess
from collections.abc import Sequence

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name
from goalie._vectorize import _check_all


def is_linux() -> GoalieCheckResult:
    """Check whether the OS is Linux.

    Examples
    --------
        >>> result = is_linux()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    if platform.system() == "Linux":
        return _TRUE
    return _false("OS is not Linux (actual: %s).", platform.system())


def is_macos() -> GoalieCheckResult:
    """Check whether the OS is macOS.

    Examples
    --------
        >>> result = is_macos()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    if platform.system() == "Darwin":
        return _TRUE
    return _false("OS is not macOS (actual: %s).", platform.system())


def is_windows() -> GoalieCheckResult:
    """Check whether the OS is Windows.

    Examples
    --------
        >>> result = is_windows()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    if platform.system() == "Windows":
        return _TRUE
    return _false("OS is not Windows (actual: %s).", platform.system())


def is_unix() -> GoalieCheckResult:
    """Check whether the OS is Unix-based (Linux or macOS).

    Examples
    --------
        >>> result = is_unix()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    if os.name == "posix":
        return _TRUE
    return _false("OS is not Unix-based (os.name: %s).", os.name)


def is_docker() -> GoalieCheckResult:
    """Check whether the session is running inside Docker.

    Checks for the presence of ``/.dockerenv`` (all platforms) and
    ``docker`` in ``/proc/1/cgroup`` (Linux only).

    Examples
    --------
        >>> result = is_docker()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    if os.path.isfile("/.dockerenv"):
        return _TRUE
    cgroup = "/proc/1/cgroup"
    if os.path.isfile(cgroup):
        try:
            with open(cgroup) as fh:
                if "docker" in fh.read():
                    return _TRUE
        except OSError:
            pass
    return _false("Session is not running inside Docker.")


def is_conda_enabled() -> GoalieCheckResult:
    """Check whether a conda environment is active.

    Examples
    --------
        >>> result = is_conda_enabled()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    if os.environ.get("CONDA_PREFIX") or os.environ.get("CONDA_DEFAULT_ENV"):
        return _TRUE
    return _false("No active conda environment detected.")


def has_internet() -> GoalieCheckResult:
    """Check whether an internet connection is available.

    Attempts a socket connection to dns.google (8.8.8.8) on port 53.

    Examples
    --------
        >>> result = has_internet()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    try:
        sock = socket.create_connection(("8.8.8.8", 53), timeout=3)
        sock.close()
        return _TRUE
    except OSError:
        pass
    return _false("No internet connection detected.")


def has_cpu(n: int) -> GoalieCheckResult:
    """Check whether the machine has at least n CPU cores.

    Parameters
    ----------
    n : int
        Minimum number of logical CPU cores required.

    Examples
    --------
        >>> has_cpu(1)
        GoalieCheckResult(ok=True)
    """
    count = os.cpu_count()
    if count is None:
        return _false("Could not determine CPU count.")
    if count >= n:
        return _TRUE
    return _false("Machine has %d CPU core%s; %d required.", count, "" if count == 1 else "s", n)


def has_ram(n: int) -> GoalieCheckResult:
    """Check whether the machine has at least n GB of RAM.

    Parameters
    ----------
    n : int
        Minimum RAM in gigabytes required.

    Examples
    --------
        >>> has_ram(1)
        GoalieCheckResult(ok=True)
    """
    gb: float | None = None
    sys = platform.system()
    if sys in ("Linux", "Darwin"):
        try:
            page_size = os.sysconf("SC_PAGE_SIZE")
            page_count = os.sysconf("SC_PHYS_PAGES")
            gb = (page_size * page_count) / (1024**3)
        except (AttributeError, ValueError):
            pass
    if gb is None and sys == "Darwin":
        try:
            out = subprocess.check_output(
                ["sysctl", "-n", "hw.memsize"],
                text=True,
                timeout=5,
            )
            gb = int(out.strip()) / (1024**3)
        except Exception:
            pass
    if gb is None:
        return _false("Could not determine available RAM.")
    if gb >= n:
        return _TRUE
    return _false("Machine has %.1f GB RAM; %d GB required.", gb, n)


def is_installed(x: str) -> GoalieCheckResult:
    """Check whether a Python package is installed (importable).

    Does not import the package; uses ``importlib.util.find_spec``.

    Parameters
    ----------
    x : str
        Package name.

    Examples
    --------
        >>> is_installed("os")
        GoalieCheckResult(ok=True)
        >>> is_installed("nonexistent_pkg_xyz_abc")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if importlib.util.find_spec(x) is not None:
        return _TRUE
    return _false("Package '%s' is not installed.", x)


def all_are_installed(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all packages are installed.

    Examples
    --------
        >>> all_are_installed(["os", "sys"])
        GoalieCheckResult(ok=True)
    """
    return _check_all(x, is_installed)


def is_system_command(x: str) -> GoalieCheckResult:
    """Check whether a system command is available on PATH.

    Parameters
    ----------
    x : str
        Command name (e.g. ``"git"``).

    Examples
    --------
        >>> is_system_command("python")
        GoalieCheckResult(ok=True)
        >>> is_system_command("nonexistent_cmd_xyz_abc")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if shutil.which(x) is not None:
        return _TRUE
    return _false("System command '%s' is not available on PATH.", x)


def all_are_system_commands(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all system commands are available on PATH.

    Examples
    --------
        >>> all_are_system_commands([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_system_command)
