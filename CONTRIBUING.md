# Contributing pictokit

Thank you for considering contributing to this project!

## Prerequisites

This project was initially designed to use **Poetry** and **Python 3.11**, but it should work with other Python versions as well. In the future, we will add proper validation for multiple Python versions.

Clone the repository and install dependencies with:

```bash
git clone https://github.com/fabrik5k/pictokit.git
cd pictokit
poetry install
```

## Language and Style

- **Language:** All code, documentation, and comments must be in **English**.  
- **Linting:** Use [ruff](https://github.com/astral-sh/ruff) for linting and formatting.  
- **Docstrings:** Follow Google-style docstrings for functions and classes.  

## Commits and Versioning

- Use [Conventional Commits](https://www.conventionalcommits.org/).  
- **Only the maintainer** is allowed to bump the version. Contributions that change the version will not be accepted. If needed, the maintainer will update the version to the current release.  
- **Changelog policy:** after every 3 new transformations are implemented, the version will be bumped, e.g., from `0.0.3` to `0.1.0`.  

## Tests and Lint

We use [taskipy](https://github.com/taskipy/taskipy) tasks defined in `pyproject.toml`.  

To execute tasks:

```bash
# Run lint
task lint

# Auto-format
task format

# Run the application
task run

# Run tests (includes lint pre-check)
task test

# Serve coverage report locally
task htmlcov
```

## Pull Requests

- Open small and focused PRs.  
- Always update the **CHANGELOG** if the modification is relevant.  
- Describe the motivation and how to test the change.  

## Branching and Release

- The main development branch is `main` (or `master`).  
- Release flow: create a tag `vX.Y.Z`, CI will publish to PyPI.  
- If necessary, use hotfix/feature branches for parallel development.  
