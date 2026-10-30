# DiffBind

DiffBind imports per-sample peaks/BAMs, defines/counts interval sets and organizes contrast analysis. The selected lab script creates standard and custom spike-normalized branches and uses DESeq2 for the spike branch. Defaults and masks need inspection in the installed release.

## Install

In an R release compatible with your chosen Bioconductor release:

```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager", repos = "https://cloud.r-project.org")
BiocManager::install("DiffBind", ask = FALSE, update = FALSE)
BiocManager::valid()
```

This installs from your selected Bioconductor release; it does **not** reproduce the historical lab environment. For the historical R 4.4 / Bioconductor 3.20 candidate, use the [workflow setup guide](../assays/cut-and-run/installation.md#candidate-environments).

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```r
library(DiffBind)
packageVersion("DiffBind")
sessionInfo()
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
dba(sampleSheet = "samples.csv") → dba.count() → dba.contrast() → dba.analyze() → dba.report()
```

## Common options

| Option / setting | Meaning |
|---|---|
| `sampleSheet` | CSV describing each individual biological replicate and its BAM/peak files. |
| `peakFormat = "narrow"` | Interpret imported peak coordinates as narrowPeak format. |
| `bParallel = FALSE` | Run this counting call without parallel workers. |
| `bRemoveDuplicates = TRUE` | In the final summarizeOverlaps pass, filter duplicate-marked records; does not discover unmarked coordinate duplicates. |
| `bUseSummarizeOverlaps = TRUE` | Use the summarizeOverlaps final-count backend. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```r
library(DiffBind)
db <- dba(sampleSheet = "design/diffbind_samples.csv", peakFormat = "narrow")
db <- dba.count(db, bParallel = FALSE, bRemoveDuplicates = TRUE,
                bUseSummarizeOverlaps = TRUE)
```

## Expected inputs and outputs

sample sheet, peaks, BAM/index → counted object → contrasts/model reports and saved objects. The source leaves consensus/summit/filter settings unspecified. The verified [3.16.0 source](https://github.com/bioc/DiffBind/tree/da0b0442311f6264ac8a14eff80dbf9dcc97f614) defaults to `minOverlap=2`, `summits=200`, `filter=1`; inspect the actual resulting ranges rather than assume original peak widths.

**Duplicate policy correction:** the final summarizeOverlaps count pass filters duplicate-marked records; it does not identify unmarked coordinate duplicates. Default summit estimation also involves a preliminary built-in counting pass, so do not describe every internal pass as identical. The upstream worker has no marking stage. Thus the selected switch is not proof of uniformly deduplicated counts ([counting implementation](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/counts.R)).

The same package snapshot accepts numeric normalization vectors and directly assigns them as DESeq2 size factors in its design-based path. The lab script already matches sample IDs and retrieves normalization diagnostics. Check their actual values/order/positivity, model design and branch-specific masks; `library=FULL` is not an automatic additional depth multiplier on this vector. Follow the [review](../assays/cut-and-run/scientific-review.md) for report sign, full-precision selection, coordinate conversion and the precheck that can suppress all-site CSV output.

## Documentation and lab notes

Installation notes: a compatible R/Bioconductor family with DiffBind, DESeq2, GenomicRanges, GenomicAlignments, SummarizedExperiment, Rsamtools and other resolved dependencies. Candidate setup is centralized below; it is not a verified lock. Review the [official manual](https://bioconductor.org/packages/release/bioc/manuals/DiffBind/man/DiffBind.pdf) and [vignette](https://bioconductor.org/packages/release/bioc/vignettes/DiffBind/inst/doc/DiffBind.pdf), whose current release can differ from the historical source.

**Function:** Peak counting and differential binding. **Evidence:** [CR-S04 / CR-S05 / CR-L02](../assays/cut-and-run/sources.md).

**Observed version evidence:** DiffBind 3.16.0 with R 4.4.3 recorded in a historical run; full dependencies unknown.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/04-differential-and-interpretation.md#stage-12-count-each-replicate-and-specify-contrasts) or [software catalog](index.md).
