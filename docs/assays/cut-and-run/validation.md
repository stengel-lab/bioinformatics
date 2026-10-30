# Validation record

**Scientific review: 2026-10-30; prior milestone checked 2026-10-29.** These checks do not establish an accepted analysis protocol.

## Scientific review checks — 2026-10-30

The current strict build and local link/syntax checks are rerun after all edits. The reviewed text-table counting example has **7 passing synthetic unittest methods**, covering host/spike identity, malformed/incomplete dictionaries, zero counts, CLI behavior, byte hashes and input preservation. No original processing script is imported or executed by those tests.

Additional synthetic checks execute the **public proposed CSV→BED example** with both GRanges-style and explicit data-frame column names, including the one-base interval `1–1` → BED `0–1`. Literal arithmetic checks verify reciprocal factors, unchanged relative ratios under common median scaling, and a rounding example near the selection threshold. No DiffBind/DESeq2 model is fitted.

Minimal Bash examples demonstrate the post-increment exit status, lack of guaranteed child error options, masked producer failure and masked `local` assignment. Corrected minimal examples propagate failure as intended. This tests shell semantics, not original cluster jobs. R fixture tests use an isolated C locale; parser R 4.3.1 is not the historical analysis environment.

Source checks compare the 344-file inventory and 28 selected source/log hashes against the prior snapshot, plus all 18 additionally inspected saved logs against this review's read-only records. The private diagnostics retain exact paths, commands, reference searches, external-source hashes and full results. Public text and code are screened for sensitive paths/credentials before commit.

To reproduce the public build and counter tests from the repository root, activate the [documentation preview environment](../../getting-started/preview.md), then run:

```bash
python -m mkdocs build --strict
python -m unittest discover -s tests -p 'test_cutrun_reference_counting.py' -v
```

The [reference audit](reference-audit.md) states exactly what the counting example validates and what reference/calibration evidence remains absent. The [review summary](scientific-review.md) separates immediate documentation corrections from proposed source changes.

| Current check | Result / boundary |
|---|---|
| Strict MkDocs build | Passed; missing section anchors fail strict builds |
| Internal targets/assets/fragments | 4,056 generated references checked; no missing targets or anchors |
| Syntax | 51 fenced blocks parsed: 40 Bash, 9 R, 1 Python, 1 PowerShell; helper/test code also passes interpreter checks |
| Counter tests | 7 passing synthetic unittest methods; no BAM/reference access |
| Export/math fixtures | Both CSV schemas export expected BED boundaries; literal rounding and scale-ratio checks pass |
| Shell fixtures | Failure masking and safe alternatives reproduced with minimal synthetic commands |
| Decisions | Exactly D01–D20, each with all 7 required review fields |
| Diagram | Updated Mermaid/SVG separates CPM from calibration and connects approved counts to the spike model; rendered preview visually reviewed |
| Source integrity | 344 inventory files, 28 selected source/log records and 18 additional saved-log records unchanged under the stated checks; counts overlap |
| Publication assets | Public code/text and generated HTML/search/download assets screened; Python bytecode/cache artifacts excluded from the website |

## Prior milestone record — 2026-10-29

| Check | Result and scope |
|---|---|
| MkDocs strict build | Passed with MkDocs 1.6.1 / Material 9.8.0; missing section anchors are configured as warnings and fail strict builds |
| Internal links and assets | All 3,777 generated link/asset references checked, including target files and HTML fragments; no missing targets/anchors |
| Example syntax | 48 blocks parsed: 37 Bash, 9 R, 1 Python and 1 PowerShell; no syntax failures |
| Parser environment | Git Bash `bash -n`; R 4.3.1 `parse()` only; Python AST; PowerShell language parser. These are syntax parsers, not the reconstructed analysis environment |
| Workflow diagram | Mermaid rendered to standalone SVG and visually inspected through a PNG preview; XML valid, no scripts or external asset links in the SVG |
| Species-count toy example | Historical regex returns 175 when only 50 synthetic mapped segments are spike; proposed exact-membership example returns 50 |
| Shell exit-status toy example | Post-increment from zero under `set -e` exits 1; assignment-based increment proceeds. Only minimal synthetic shell code was run |
| Source preservation | Content hashes, sizes and modification times unchanged for 344 inventoried CUT&RUN files; all 28 selected source/log hashes also match their review records |
| Publication review | Reviewed newly written prose, generic commands, source IDs and diagram; path/credential-pattern screen found no flagged private paths, hosts or credential patterns. No original scripts, datasets or logs are tracked |

The private review record retains exact commands, source hashes and full diagnostics without publishing source locations or private contents. Link checks cover local website targets; external links were consulted during methodological review but not exhaustively monitored for future availability. Pattern screening supplements manual review and is not proof that arbitrary future content is safe.

## Checks deliberately outside this milestone

- No original lab worker, supervisor, analysis script or scheduler job was executed.
- No FASTQ/BAM/peak processing, normalization, count model, motif enrichment or biological figure was run on lab data.
- Candidate Linux/macOS/WSL2 environments were not installed or solver-verified; software/version availability remains to be checked.
- No genome-reference download, index construction or historical-reference equivalence check was performed.
- No fitted contrast/model, historical factor application, historical coordinate export or biological QC threshold was execution-validated. Only the stated synthetic export/arithmetic checks were executed.
- HOMER's upstream manual was unavailable during review; source invocations were inspected, not runtime-verified.

Saved version headers establish that certain historical software was reported in a log, not that all processing stages succeeded. A website build, link check or syntax parse cannot resolve the [scientific decisions](decisions.md).
