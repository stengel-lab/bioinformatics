# Contributing

Use a focused feature branch and submit original Markdown documentation in small, reviewable changes. Begin with a scientific question and the reader's prerequisites.

1. Select the [tool](docs/contributing/templates/tool.md) or [tutorial](docs/contributing/templates/tutorial.md) template.
2. Explain the scientific rationale, inputs, outputs, parameters, and interpretation limits.
3. Cite primary documentation for software behavior. Record an explicit version only when supported by evidence.
4. Use public or synthetic inputs with a documented origin. Replace private paths and metadata with descriptive placeholders.
5. Apply the [publication review](docs/contributing/publication.md) and [provenance conventions](docs/contributing/provenance.md).
6. Preview with `python -m mkdocs build --strict` in the documentation environment. This checks documentation construction; it does not validate analysis commands.
7. Request scientific and software review. Keep execution status and scientific review status separate.

Do not copy historical lab scripts into this repository without permission and content review. Do not infer that a script is authoritative from its name, modification date, or version suffix. Avoid including environment exports containing private prefixes or machine state.

New automation and production pipelines require a separate design milestone after the educational material and source inventory have been reviewed.
