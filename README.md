# goalie

[![Install with Bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg)](https://bioconda.github.io/recipes/goalie/README.html) ![Lifecycle: experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)

Assertive check functions for defensive Python programming.

## Installation

### [uv][] method

This is a [Python][] package hosted at [python.acidgenomics.com][].
We recommend using [uv][] to install.

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
[python]: https://www.python.org/
[python.acidgenomics.com]: https://python.acidgenomics.com
[uv]: https://docs.astral.sh/uv/
