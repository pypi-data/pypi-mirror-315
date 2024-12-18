# Developing the Kegstand CLI tool

The Kegstand CLI is published on PyPI as [kegstandcli](https://pypi.org/project/kegstandcli/). It is a Python package that provides a command-line interface for creating and deploying Kegstand services.

## Publish a new package version

To publish a new version of the Kegstand CLI, follow these steps:

1. Update the version number in `pyproject.toml` and commit the change.
2. Publish the new version to PyPI using the following commands:

```shell
> uv build
> uv publish
```
