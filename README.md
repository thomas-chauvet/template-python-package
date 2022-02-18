# Template package

Clone this repository and follow the `README.md` to start developing your own python package.

- [Template package](#template-package)
  - [Conda and poetry](#conda-and-poetry)
    - [Prerequisite](#prerequisite)
    - [Install conda environment](#install-conda-environment)
    - [Install poetry](#install-poetry)
    - [Install dependencies with poetry](#install-dependencies-with-poetry)
    - [Add a new python package](#add-a-new-python-package)
    - [Local installation of `package`](#local-installation-of-package)
  - [Static typing checker](#static-typing-checker)
  - [Python formatter](#python-formatter)
  - [Run unit tests (with coverage)](#run-unit-tests-with-coverage)
  - [Version management](#version-management)
  - [Publish to (private) PyPi](#publish-to-private-pypi)
  - [CI pipeline](#ci-pipeline)
    - [Release a new version](#release-a-new-version)
  - [Extra](#extra)
    - [VScode settings](#vscode-settings)

## Conda and poetry

We use advices, from [this blog post](https://ealizadeh.com/blog/guide-to-python-env-pkg-dependency-using-conda-poetry).

In summary, the idea is:
- to use `conda` as environment manager (allow to install different python version),
    - conda `environment.yml` is only used to create the "base" environment with python. Poetry is used to install all dependencies.
- `poetry` as dependency manager:
    - easy way to have dependencies and `dev` dependencies, 
    - multiple tools such as formatter, linting, etc. in the `pyproject.toml`
    - `pyproject.toml` with everything to build the package
    - easy to use,
    - easy to deploy the package on (private) PyPI.

### Prerequisite

Install `conda`:
- on Mac with ARM (M1) processor, install `Miniforge` follow this [doc](https://github.com/conda-forge/miniforge#download).
- on other system you can choose (lighter) [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or (heavier) even [Anaconda](https://docs.anaconda.com/anaconda/install/).

### Install conda environment

```bash
conda env create --file environment.yml
```

Notes: 
- you can rename environment name in `environment.yml` (default: `package`),
- by default, it will install `python 3.10`.

Activate the environment:

```bash
conda activate package
```

### Install poetry

Install `poetry`, follow this [doc](https://python-poetry.org/docs/#installation).

*Note: do not forget to run `source $HOME/.poetry/env` to have poetry in your `PATH`.*

Check it works properly:

```bash
poetry --version
```

### Install dependencies with poetry

```bash
poetry install
```

Default package provided:

- `pytest`: to run tests,
- `pytest-cov`: to get coverage with `pytest`,
- `mypy`: static typing checker,
- `black`: python formatter.

### Add a new python package

```bash
poetry add pandas
```

### Local installation of `package`

```bash
poetry install
```

Here, for instance we implement a `greet` method to greet someone. Once you installed the package locally you can greet someone:

```bash
greet Thomas
```

It will output `Hello Thomas!`.

It works thanks to this part:
```toml
[tool.poetry.scripts]
greet = "package.main:main"
```
in `pyproject.toml`. It tell to run the `run` method in `package.main`.

## Static typing checker

We use [mypy](https://mypy.readthedocs.io/) as static type checker.

```bash
mypy .
```

## Python formatter

We use [`black`](https://black.readthedocs.io/en/stable/) to format python code.

```bash
black .
```

## Run unit tests (with coverage)

```bash
pytest --cov=package tests/
```

## Version management

Versions are managed with git tag based on [this blog post](https://www.nicholasnadeau.com/post/2020/8/one-version-to-rule-them-all-keeping-your-python-package-version-number-in-sync-with-git-and-poetry/). Version in `pyproject.toml` is just a placeholder.

To get the right based on git tag version in `pyproject.toml`:

```bash
poetry version $(git describe --tags --abbrev=0)
```

It allows to automate release based on git tags.

## Publish to (private) PyPi

*Note: this is for example only. It should be automated by CI pipeline.*

On PyPI, simply:

```bash
poetry publish
```

On a private registry:

```bash
poetry config repositories.private http://myprivaterepository:8081/python/
poetry publish -r private
```

## CI pipeline

The CI pipeline is implemented in `.github/workflows/ci-cd.yml`.

It runs following steps:
- Get version based on git tags,
- Install poetry,
- Run black (formatter) checks,
- Static typing checker (mypy),
- Unit tests,
- Packaging (poetry build),
- Artifacts (coverage, wheel and `tar.gz`) upload.

### Release a new version

1) Merge `develop` on `main`,

```bash
git checkout main
git merge develop
```

2) Tag `main` with the version you want,

```bash
git tag -a 1.2.3 -m "New release for v1.2.3"
```

3) Push `main` and `tag`,

```bash
git push origin main --follow-tags
```

4) Rebase `main` on `develop`,

```bash
git checkout develop
git rebase main
```

5) Tag `develop` with the next "dev" version.

```bash
git tag -a 2.0.0.dev -m "Next version v2.0.0"
```

**Do not forget `.dev`.**

*Note: we do not exactly follow [PEP440](https://www.python.org/dev/peps/pep-0440/#public-version-identifiers). It allows to have a simple release process with tagged release and tagged next version.*

1) Push `develop` and `tag`,

```bash
git push origin develop --follow-tags
```

```schema
          1.2.3.dev            2.0.0.dev
develop -----|---------\----------|----------->
            /   *merge* \        / *rebase*
main    ---/-------------|------/------------->              
                       1.2.3
```

## Extra

### VScode settings

We provide a file `.vscode/settings.json` to setup `pytest` in vscode. It allows to run tests directly in vscode with the `testing` module.