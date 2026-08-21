# goalie

Boolean check functions for defensive Python programming.

Every check function returns a plain `bool`. Raise at the call site when a check
fails, using one of the bundled error classes or a builtin exception:

```pycon
>>> from goalie import CheckValueError, is_hex_color
>>> color = "red"
>>> if not is_hex_color(color):
...     raise CheckValueError(color, "a hex color code", name="color")
Traceback (most recent call last):
    ...
goalie._errors.CheckValueError: color must be a hex color code, got 'red'.
```

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

## Errors

`CheckError` is the base class; `CheckTypeError` also subclasses `TypeError` and
`CheckValueError` also subclasses `ValueError`, so existing `except TypeError`/
`except ValueError` blocks catch them without changes.

## Collection and string checks

`has_duplicates`, `is_subset`, and `are_set_equal` operate on any iterable of
hashable values. `is_hex_color` and `is_matching_regex` check strings.

```pycon
>>> from goalie import has_duplicates, is_subset
>>> has_duplicates(["a", "a", "b"])
True
>>> is_subset({1, 2}, {1, 2, 3})
True
```

## Filesystem and URL checks

`has_access`, `is_compressed_file`, `is_git_repo`, and `is_temp_file` check paths.
`is_url`, `is_existing_url`, `is_aws_s3_uri`, and `is_existing_aws_s3_uri` check
URLs and S3 URIs; the `is_existing_*` pair make a network call.

## System checks

A separate family of checks inspects the runtime environment rather than a value:
`is_linux`/`is_macos`/`is_windows`/`is_unix`, `is_docker`, `is_conda_enabled`,
`is_vscode`, `has_internet`, `has_cpu`/`has_ram`, `has_github_pat`, `is_installed`,
`is_system_command`, and `is_package_version`.

```pycon
>>> from goalie import is_installed
>>> is_installed("os")
True
```

`has_cpu` and `has_ram` raise `RuntimeError` if the machine's core count or RAM
cannot be determined; a failed measurement isn't the same as a "no" answer.
`is_existing_aws_s3_uri` raises `RuntimeError` under the same reasoning when
neither `boto3` nor the `aws` CLI is available to make the check.

```{toctree}
:maxdepth: 1
:caption: Contents
:hidden:

reference/index
changelog
```
