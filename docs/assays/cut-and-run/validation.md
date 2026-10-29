# Validation record

**Review date: 2026-10-29.** This milestone reconstructs source behavior and builds educational documentation. It does not establish an accepted analysis protocol.

## Documentation and source checks

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
- No reference download, index construction or historical-reference equivalence check was performed.
- No statistical contrast sign, factor application, reference coordinate export or biological QC threshold was execution-validated.
- HOMER's upstream manual was unavailable during review; source invocations were inspected, not runtime-verified.

Saved version headers establish that certain historical software was reported in a log, not that all processing stages succeeded. A website build, link check or syntax parse cannot resolve the [scientific decisions](decisions.md).
