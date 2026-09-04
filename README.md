# goalie

[![Install with Bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg)](https://bioconda.github.io/recipes/goalie/README.html) ![Lifecycle: experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)

Boolean check functions for defensive Python programming.

## Usage

Every check is a plain function that returns `True` or `False`. Raise at the
call site when a check fails:

```python
from goalie import CheckValueError, is_hex_color

def set_accent(color: str) -> None:
    if not is_hex_color(color):
        raise CheckValueError(color, "a hex color code", name="color")
```

## Installation

### [uv][] method

This is a [Python][] package hosted on [PyPI][] as `acidgenomics-goalie`.
The import name is unchanged: `goalie`.
We recommend using [uv][] to install.

```sh
uv add acidgenomics-goalie
```

Or with [pip][]:

```sh
pip install acidgenomics-goalie
```

### [Conda][] method

Configure [Conda][] to use the [Bioconda][] channels.

```sh
# Don't install recipe into base environment.
name='goalie'
conda create --name="$name" "$name"
conda activate "$name"
python -c 'import goalie'
```

## License

Apache-2.0 — Copyright 2026 Acid Genomics LLC — see [LICENSE](LICENSE).

[bioconda]: https://bioconda.github.io/
[conda]: https://docs.conda.io/
[pip]: https://pip.pypa.io/
[pypi]: https://pypi.org/project/acidgenomics-goalie/
[python]: https://www.python.org/
[uv]: https://docs.astral.sh/uv/
