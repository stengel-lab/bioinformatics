"""Check documentation mechanics and selected publication boundaries, without analysis."""

from __future__ import annotations

import ast
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE_PATH = "/bioinformatics/"


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.ids.add(attrs["name"])
        key = "href" if tag in {"a", "link"} else "src"
        if tag in {"a", "link", "img", "script", "iframe", "source"} and key in attrs:
            self.links.append(attrs[key])


def main() -> int:
    errors: list[str] = []
    if not (SITE / "index.html").is_file():
        print("Build the documentation first: python -m mkdocs build --strict")
        return 1
    pages = {p.resolve(): Page(p.read_text(encoding="utf-8")) for p in SITE.rglob("*.html")}
    links_checked = 0
    for source, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            if path.startswith("/"):
                if not path.startswith(BASE_PATH):
                    errors.append(f"{source.relative_to(SITE)}: URL outside site base: {href}")
                    continue
                target = SITE / path[len(BASE_PATH):]
            else:
                target = source.parent / path if path else source
            target = target.resolve()
            if target.is_dir():
                target /= "index.html"
            links_checked += 1
            if not target.is_relative_to(SITE.resolve()) or not target.is_file():
                errors.append(f"{source.relative_to(SITE)}: missing internal target: {href}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{source.relative_to(SITE)}: missing fragment: {href}")

    # Include not-yet-staged public files locally; CI sees the checked-out tracked tree.
    raw = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=ROOT
    )
    files = sorted({ROOT / name.decode("utf-8") for name in raw.split(b"\0") if name})
    private_dirs = {".local-audit", "private", "data", "results", ".ssh", ".aws"}
    data_suffixes = {".bam", ".sam", ".cram", ".bai", ".crai", ".bw", ".bigwig", ".fastq", ".fq", ".hic", ".cool", ".mcool", ".bedgraph", ".tdf"}
    # Match indicators without printing matched secrets or private values to CI logs.
    patterns = [
        re.compile(r"[A-Za-z]:[\\/]" + r"Users[\\/](?!PUBLIC_PLACEHOLDER)", re.I),
        re.compile(r"(?<![\w/])/(?:gs/gsfs\d+|home/[a-z][\w.-]+|Users/[a-z][\w.-]+)/"),
        re.compile(r"(?:gh[pousr]_" + r"[A-Za-z0-9]{20,}|github_pat_" + r"[A-Za-z0-9_]{20,})"),
        re.compile(r"AKIA" + r"[A-Z0-9]{16}"),
        re.compile(r"-----BEGIN " + r"(?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
        re.compile(r"https?://[^\s/:]+:[^\s/@]+@"),
    ]
    public_text = []
    for p in files:
        relative = p.relative_to(ROOT)
        if any(part in private_dirs for part in relative.parts):
            errors.append(f"Private directory tracked: {relative}")
        name = p.name.lower()
        if p.suffix.lower() in data_suffixes or name.endswith((".fastq.gz", ".fq.gz", ".pairs.gz", ".pairsam.gz")):
            errors.append(f"Data artifact tracked: {relative}")
        if p.is_file():
            try:
                public_text.append((str(relative), p.read_text(encoding="utf-8")))
            except UnicodeDecodeError:
                # Binary assets need human review; no binary analysis data are allowed above.
                pass
    for p in SITE.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".html", ".json", ".svg", ".py", ".mmd", ".xml"}:
            public_text.append((str(p.relative_to(ROOT)), p.read_text(encoding="utf-8")))
        if p.suffix == ".pyc" or "__pycache__" in p.parts:
            errors.append("Python bytecode in generated website")
    for name, text in public_text:
        if any(pattern.search(text) for pattern in patterns):
            errors.append(f"Publication indicator requires review: {name}")

    bash = shutil.which("bash")
    syntax_checked = 0
    with tempfile.TemporaryDirectory(prefix="docs-syntax-") as folder:
        for p in (ROOT / "docs").rglob("*.md"):
            for n, match in enumerate(re.finditer(r"^```(bash|python)\s*\n(.*?)^```\s*$", p.read_text(encoding="utf-8"), re.M | re.S), 1):
                language, body = match.groups()
                if language == "python":
                    try:
                        ast.parse(body)
                    except SyntaxError:
                        errors.append(f"Python syntax: {p.relative_to(ROOT)} block {n}")
                elif bash:
                    snippet = Path(folder) / "example.sh"
                    snippet.write_text(body, encoding="utf-8", newline="\n")
                    cp = subprocess.run([bash, "-n", snippet.as_posix()], capture_output=True)
                    if cp.returncode:
                        errors.append(f"Bash syntax: {p.relative_to(ROOT)} block {n}")
                else:
                    errors.append("Bash is required for documentation syntax checks")
                syntax_checked += 1
    print(f"Checked {len(pages)} HTML pages, {links_checked} internal references, "
          f"{syntax_checked} Bash/Python blocks and {len(public_text)} public text files.")
    if errors:
        print("\n".join(sorted(set(errors))))
        return 1
    print("Documentation mechanics and publication indicator checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
