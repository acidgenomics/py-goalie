# goalie

Assertive check functions for defensive Python programming.

Every check function returns a `GoalieCheckResult` rather than raising or returning a
bare `bool`: it's truthy/falsy for use in `if`/`assert`, and on failure it carries a
`cause` message describing *why* the check failed, so error messages don't need to be
written by hand at every call site.

## Installation

### uv method

This package is hosted at [python.acidgenomics.com](https://python.acidgenomics.com/).
We recommend using [uv](https://docs.astral.sh/uv/) to install.

```sh
uv pip install \
    --index-url 'https://python.acidgenomics.com/simple/' \
    goalie
```

Or add the index to your project's `pyproject.toml`:

```toml
[[tool.uv.index]]
url = "https://python.acidgenomics.com/simple/"
```

Then install:

```sh
uv add goalie
```

### Conda method

Configure [Conda](https://docs.conda.io/) to use the
[Bioconda](https://bioconda.github.io/) channels.

```sh
# Don't install recipe into base environment.
name='goalie'
conda create --name="$name" "$name"
conda activate "$name"
python -c 'import goalie'
```

## Scalar and vectorized checks

Most checks come in a scalar form (`is_*`, `has_*`, `are_*`) and, where it makes sense
to check a whole collection at once, a vectorized `all_are_*`/`all_have_*` form:

```pycon
>>> from goalie import is_string, is_scalar_integer, all_are_positive
>>> is_string("hello")
GoalieCheckResult(ok=True)
>>> is_scalar_integer(5)
GoalieCheckResult(ok=True)
>>> all_are_positive([1, 2, 3])
GoalieCheckResult(ok=True)
```

A failing check carries a `cause` message instead of just `False`:

```pycon
>>> is_string(5)
GoalieCheckResult(ok=False, cause="'5' is not str.")
```

Categories include comparisons (`is_equal_to`, `is_greater_than`, ...), dimensions
(`has_dims`, `has_rows`, `has_unique_cols`, ...), filesystem (`is_file`, `is_symlink`,
`is_git_repo`, ...), string matching (`is_matching_regex`, `is_matching_fixed`),
numeric ranges (`is_in_range`, `is_percentage`, `is_proportion`, ...), names
(`has_names`, `valid_names`, `has_rownames`, ...), sets (`is_subset`, `are_set_equal`,
...), and type checks (`is_all`, `is_any`, `is_vectorish`).

## System checks

A separate family of checks inspects the runtime environment rather than a value:
`is_linux`/`is_macos`/`is_windows`, `is_docker`, `is_conda_enabled`, `has_internet`,
`has_cpu`/`has_ram`, `is_installed`, `is_system_command`, and `is_package_version`.

```pycon
>>> from goalie import is_installed
>>> is_installed("os")
GoalieCheckResult(ok=True)
```

## Assert and validate

`assert_` raises `GoalieAssertionError` on the first failing check (short-circuit);
`validate` evaluates every check and returns the collected failure causes (or `None`
if all pass), for use in constructors or validators instead of raising immediately:

```pycon
>>> from goalie import assert_, is_string
>>> assert_(is_string(5))
Traceback (most recent call last):
    ...
goalie._engine.GoalieAssertionError: '5' is not str.
```

```pycon
>>> from goalie import validate, is_scalar_integer
>>> validate(is_string(5), is_scalar_integer("x"))
["'5' is not str.", "''x'' is not integer."]
```

## Bioinformatics checks

`has_clusters`, `has_metrics`, and `has_multiple_samples` check AnnData-like objects
(via duck typing, so `anndata`/`scanpy` aren't required unless you use these) for
cluster annotations, QC metrics, and multi-sample structure in `.obs`.

```{toctree}
:maxdepth: 1
:caption: Contents
:hidden:

reference/index
changelog
```
