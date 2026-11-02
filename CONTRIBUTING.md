# Contributing

Submit focused changes on a feature branch and open a pull request for review.

- **Pipelines:** use `docs/pipelines/<assay>/index.md` for a short overview and `walkthrough.md` for one continuous processing lesson. Add pages only when necessary.
- **Tools:** use one standalone page per program or package under `docs/tools/`, shared by multiple pipelines. Develop installation, usage, parameters, and examples together.
- **Setup:** keep operating-system, environment, dependency, and reference-data guidance under `docs/setup/`; link to it from walkthroughs.
- **Executable workflows:** reserve the root `workflows/` directory for future processing code. Keep `docs/` dedicated to website content.
- **Navigation:** retain Home, Pipelines, Tools, and Setup as the four primary sections. Add guides when they contain useful material; avoid empty hierarchies and placeholder directories.

Use original explanations, primary references, and permitted public or synthetic examples. Review paths, metadata, credentials, and publication rights before committing. Keep private audits, laboratory source archives, unpublished results, and real sample metadata out of Git.

Run `python -m mkdocs build --strict` and `python scripts/check_docs.py` before submitting. See [README](README.md) for preview commands. Do not merge or publish without review.
