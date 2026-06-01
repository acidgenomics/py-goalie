"""Bioinformatics check functions.

Requires the ``[bio]`` optional dependency group (anndata, scanpy).
Functions use duck typing on AnnData-like objects to avoid a hard
import at module load time.
"""

from collections.abc import Sequence

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name


def _is_anndata(x: object) -> bool:
    """Check whether x looks like an AnnData object."""
    return hasattr(x, "obs") and hasattr(x, "var") and hasattr(x, "X")


def has_clusters(x: object) -> GoalieCheckResult:
    """Check whether an AnnData object contains cluster annotations.

    Looks for ``leiden`` or ``louvain`` keys in ``.obs`` columns.

    Parameters
    ----------
    x : object
        AnnData-like object.

    Examples
    --------
        >>> has_clusters("not_anndata")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not _is_anndata(x):
        return _false("'%s' does not appear to be an AnnData object.", _to_name(x))
    obs = x.obs  # type: ignore[union-attr]
    cluster_keys = {"leiden", "louvain"}
    found = [k for k in cluster_keys if k in obs.columns]
    if found:
        return _TRUE
    return _false(
        "'%s' has no cluster annotations (checked: %s).",
        _to_name(x),
        ", ".join(sorted(cluster_keys)),
    )


def has_metrics(
    x: object,
    obs_keys: Sequence[str] | None = None,
) -> GoalieCheckResult:
    """Check whether an AnnData object contains QC metrics in ``.obs``.

    Parameters
    ----------
    x : object
        AnnData-like object.
    obs_keys : Sequence[str] | None
        Keys to check. Defaults to ``["n_genes_by_counts", "total_counts"]``.

    Examples
    --------
        >>> has_metrics("not_anndata")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not _is_anndata(x):
        return _false("'%s' does not appear to be an AnnData object.", _to_name(x))
    if obs_keys is None:
        obs_keys = ["n_genes_by_counts", "total_counts"]
    obs = x.obs  # type: ignore[union-attr]
    missing = [k for k in obs_keys if k not in obs.columns]
    if missing:
        return _false(
            "'%s' is missing QC metrics in .obs: %s.",
            _to_name(x),
            ", ".join(missing),
        )
    return _TRUE


def has_multiple_samples(
    x: object,
    sample_key: str = "sample",
) -> GoalieCheckResult:
    """Check whether an AnnData object contains multiple samples.

    Parameters
    ----------
    x : object
        AnnData-like object.
    sample_key : str
        Column name in ``.obs`` that identifies samples.

    Examples
    --------
        >>> has_multiple_samples("not_anndata")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not _is_anndata(x):
        return _false("'%s' does not appear to be an AnnData object.", _to_name(x))
    obs = x.obs  # type: ignore[union-attr]
    if sample_key not in obs.columns:
        return _false(
            "'%s' has no '%s' column in .obs.",
            _to_name(x),
            sample_key,
        )
    n_samples = obs[sample_key].nunique()
    if n_samples > 1:
        return _TRUE
    return _false(
        "'%s' contains only 1 sample in .obs['%s'].",
        _to_name(x),
        sample_key,
    )
