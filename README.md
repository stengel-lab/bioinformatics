# Stengel Lab Bioinformatics

**[Read the documentation →](https://stengel-lab.github.io/bioinformatics/)**

A documentation-first bioinformatics resource for the Stengel Lab at Albert Einstein College of Medicine. v0.1 includes a searchable software library, a step-by-step CUT&RUN teaching draft, and installation help for Linux, macOS, Windows/WSL2 and HPC.

- [Software library](docs/software/index.md): installation, verification, syntax, common options and examples.
- [CUT&RUN walkthrough](docs/assays/cut-and-run/index.md): paired reads through QC, trimming, alignment, peaks, coverage and downstream interpretation.
- [Getting started](docs/getting-started/index.md) and [installation](docs/installation/index.md).
- [Other assays](docs/assays/index.md): outlines, not yet developed.
- [Contributing](CONTRIBUTING.md) and [local preview](docs/getting-started/preview.md).

## Status

CUT&RUN is an educational draft; commands and installation candidates are not end-to-end analysis validated. Detailed methodological review is available as secondary reference. No production pipeline or sequencing dataset is distributed.

## Documentation development

Markdown sources live in `docs/`; `mkdocs.yml` defines navigation and search. GitHub Actions builds and checks pull requests, then deploys GitHub Pages from `main` using the built-in Actions token. See [website publishing](docs/contributing/website.md).

Private inventories, original scripts with unclear publication rights, unpublished findings, sample metadata, credentials and institutional configuration are excluded from Git and from the site. See the [publication boundary](docs/contributing/publication.md).

The repository has no license file. Maintainers must select terms before representing its contents as licensed for reuse.
