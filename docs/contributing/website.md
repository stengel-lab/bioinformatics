# Website publishing

The [public documentation](https://stengel-lab.github.io/bioinformatics/) is built with MkDocs Material from Markdown on `main`. The [workflow](https://github.com/stengel-lab/bioinformatics/blob/main/.github/workflows/docs.yml) also checks pull requests before they merge.

## Before merging documentation

From an environment containing `requirements-docs.txt`:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m mkdocs build --strict
python scripts/check_docs.py
```

The checker verifies generated internal links/assets/fragments, parses Bash and Python examples without executing analysis, and screens public files for selected private-path, credential and data patterns. It is a guardrail, not a substitute for reading the proposed changes. External sites can block automated requests; check official-documentation links when editing them.

Keep `.local-audit/`, source archives, sequencing data, unpublished results and real sample metadata out of commits and deployment artifacts. Only generated `site/` contents are uploaded; neither the local inventory nor the repository root is a Pages artifact.

## Deployment

A push to `main` builds, checks and uploads the site, then deploys through the `github-pages` environment. Pull requests only build/check; they cannot deploy. Actions are pinned to full commit hashes. Repository contents are read-only during builds; only the deployment job receives `pages: write` and `id-token: write`.

Deployment uses GitHub's built-in `GITHUB_TOKEN` and short-lived OIDC identity, following [GitHub's Pages workflow guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use). No personal access token is needed in repository secrets. Repository Pages must be enabled with **GitHub Actions** as its source, and the `github-pages` environment should allow deployment from `main` only.

## If publishing fails

Open the [Actions runs](https://github.com/stengel-lab/bioinformatics/actions), inspect the failing job, and correct the source through a PR. Build failures do not deploy a new artifact. For a deployment-only failure, check Pages settings, environment branch restrictions and job permissions before rerunning the workflow. After deployment, verify the live home page, tool navigation, search results and CUT&RUN walkthrough on desktop and mobile.

The website build and synthetic tests validate documentation mechanics. They do not execute or scientifically validate the biological workflow. See the [CUT&RUN validation record](../assays/cut-and-run/validation.md).
