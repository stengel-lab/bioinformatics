# Stengel Lab Bioinformatics

**[Read the documentation →](https://stengel-lab.github.io/bioinformatics/)**

A centralized collection of educational bioinformatics resources, software documentation, and standardized processing workflows for the Stengel Lab and collaborators.

- [Home](docs/index.md)
- [Pipelines](docs/pipelines/index.md)
- [Tools](docs/tools/index.md)
- [Setup](docs/setup/index.md)

## Status

The documentation source contains four section landing pages. Individual tutorials, tool references, and platform guides will be developed incrementally. The previous documentation is preserved in the [`v0.1-archive` tag](https://github.com/stengel-lab/bioinformatics/tree/v0.1-archive) and Git history.

## Documentation development

Markdown website content lives in `docs/`. Reserve `workflows/` for future executable processing pipelines; it is not created yet. See [contribution conventions](CONTRIBUTING.md).

With Python 3.11 or newer in an isolated environment, install the documentation dependencies and preview or check the site:

```sh
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

```sh
python -m mkdocs build --strict
python scripts/check_docs.py
```

GitHub Actions checks pull requests and deploys only from `main`, using the built-in Actions token. Only generated `site/` content is uploaded. Private audit records, source archives, sequencing data, unpublished results, credentials, and institutional configuration must stay outside tracked content.

The repository has no license file. Maintainers must select terms before representing its contents as licensed for reuse.
