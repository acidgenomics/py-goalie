"""System and environment check functions.

Converted from R system-check-scalar-* and system-check-vector-* functions.
"""

import importlib.metadata
import importlib.util
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
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


def is_rstudio() -> GoalieCheckResult:
    """Check whether the session is running inside RStudio.

    Checks for the ``RSTUDIO_USER_IDENTITY`` environment variable.

    Examples
    --------
        >>> result = is_rstudio()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    if os.environ.get("RSTUDIO_USER_IDENTITY"):
        return _TRUE
    return _false("Session is not running inside RStudio.")


def is_vscode() -> GoalieCheckResult:
    """Check whether the session is running inside VS Code.

    Checks for the ``VSCODE_INIT_R`` or ``TERM_PROGRAM`` environment variable.

    Examples
    --------
        >>> result = is_vscode()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    if os.environ.get("VSCODE_INIT_R") or os.environ.get("TERM_PROGRAM") == "vscode":
        return _TRUE
    return _false("Session is not running inside VS Code.")


def is_devel() -> GoalieCheckResult:
    """Check whether the Python build is a development/pre-release version.

    Returns True for alpha (a), beta (b), release candidate (rc), or
    development (dev) builds.

    Examples
    --------
        >>> result = is_devel()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    vi = sys.version_info
    if vi.releaselevel != "final" or "dev" in sys.version.lower():
        return _TRUE
    return _false(
        "Python version '%s' is not a development build.", sys.version.split()[0]
    )


def has_github_pat() -> GoalieCheckResult:
    """Check whether a GitHub PAT is set in the environment.

    Checks for the ``GITHUB_PAT``, ``GITHUB_TOKEN``, or
    ``GH_TOKEN`` environment variables.

    Examples
    --------
        >>> result = has_github_pat()
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    for var in ("GITHUB_PAT", "GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(var):
            return _TRUE
    return _false(
        "No GitHub PAT found (checked GITHUB_PAT, GITHUB_TOKEN, GH_TOKEN)."
    )


def is_package_version(
    x: str,
    version: str,
    op: str = ">=",
) -> GoalieCheckResult:
    """Check whether an installed package satisfies a version constraint.

    Parameters
    ----------
    x : str
        Package name.
    version : str
        Version string to compare against (e.g. ``"1.2.0"``).
    op : str
        Comparison operator: ``">="``, ``">"``, ``"=="``, ``"!="``,
        ``"<"``, ``"<="``. Default ``">="``.

    Examples
    --------
        >>> result = is_package_version("pip", "1.0.0")
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    from importlib.metadata import PackageNotFoundError, version as _meta_version  # noqa: I001,PLC0415

    def _parse(v: str) -> tuple[int, ...]:
        # Parse only the numeric part before any alpha/beta/rc suffix.
        m = re.match(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?", v)
        if not m:
            return (0,)
        return tuple(int(g) for g in m.groups() if g is not None)

    op_map = {
        ">=": lambda a, b: a >= b,
        ">": lambda a, b: a > b,
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        "<": lambda a, b: a < b,
        "<=": lambda a, b: a <= b,
    }
    if op not in op_map:
        return _false("Unsupported operator '%s'.", op)
    try:
        installed_str = _meta_version(x)
    except PackageNotFoundError:
        return _false("Package '%s' is not installed.", x)
    installed = _parse(installed_str)
    required = _parse(version)
    if op_map[op](installed, required):
        return _TRUE
    return _false(
        "Package '%s' version %s does not satisfy %s %s.",
        x,
        installed_str,
        op,
        version,
    )
