# Preview the documentation

Use Python 3.11 or newer and Git. Run the following commands from a local clone of this repository. The environment is for documentation only.

## Windows PowerShell

```powershell
py -3 -m venv .venv-docs
.\.venv-docs\Scripts\python.exe -m pip install -r requirements-docs.txt
.\.venv-docs\Scripts\python.exe -m mkdocs serve --dev-addr 127.0.0.1:8000
```

## macOS or Linux

```bash
python3 -m venv .venv-docs
.venv-docs/bin/python -m pip install -r requirements-docs.txt
.venv-docs/bin/python -m mkdocs serve --dev-addr 127.0.0.1:8000
```

Open the local address printed by MkDocs. To build without serving, replace the final `serve` command with `build --strict`. Generated pages go into ignored `site/`.

`requirements-docs.txt` pins the two direct dependencies used for the initial preview; it does not pin every transitive dependency. Record the resolved package versions for a reproducible preview. Review version updates deliberately. Keep analysis environments separate from this environment.

## Website framework decision

The site uses [MkDocs configuration](https://www.mkdocs.org/user-guide/configuration/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/getting-started/). Material announces end of life on May 5, 2027 and identifies Zensical as its successor. v0.1 retains the current renderer; reassess it before support ends. Markdown sources keep that transition manageable. [GitHub Actions publishes the site](../contributing/website.md) after checks pass on `main`.
