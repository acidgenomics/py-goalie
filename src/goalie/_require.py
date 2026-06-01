"""Package namespace requirement utilities."""

import importlib.util
from collections.abc import Sequence


def require_namespaces(packages: Sequence[str]) -> None:
    """Require that Python packages are importable.

    Checks that each package can be found via ``importlib.util.find_spec``.
    Does NOT import or attach the packages. Raises ``ImportError`` listing
    all missing packages if any are not found.

    Parameters
    ----------
    packages : Sequence[str]
        Package names to check.

    Raises
    ------
    ImportError
        If one or more packages are not installed.

    Examples
    --------
        >>> require_namespaces(["os", "sys"])
        >>> require_namespaces(["nonexistent_pkg_xyz"])
        Traceback (most recent call last):
            ...
        ImportError: Package not installed: nonexistent_pkg_xyz.
    """
    missing: list[str] = []
    for pkg in packages:
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
    if missing:
        noun = "Package" if len(missing) == 1 else "Packages"
        names = ", ".join(missing)
        raise ImportError(f"{noun} not installed: {names}.")
