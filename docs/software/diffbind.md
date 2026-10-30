# DiffBind

**Function:** Peak counting and differential binding. **Evidence:** [CR-S04 / CR-S05 / CR-L02](../assays/cut-and-run/sources.md).

**Observed version evidence:** DiffBind 3.16.0 with R 4.4.3 recorded in a historical run; full dependencies unknown.

DiffBind imports per-sample peaks/BAMs, defines/counts interval sets and organizes contrast analysis. The selected lab script creates standard and custom spike-normalized branches and uses DESeq2 for the spike branch. Defaults and masks need inspection in the installed release.

**Installation:** a compatible R/Bioconductor family with DiffBind, DESeq2, GenomicRanges, GenomicAlignments, SummarizedExperiment, Rsamtools and other resolved dependencies. Candidate setup is centralized below; it is not a verified lock. Review the [official manual](https://bioconductor.org/packages/release/bioc/manuals/DiffBind/man/DiffBind.pdf) and [vignette](https://bioconductor.org/packages/release/bioc/vignettes/DiffBind/inst/doc/DiffBind.pdf), whose current release can differ from the historical source.

**Configured counting usage** (the CSV needs valid resolved paths):

```r
library(DiffBind)
db <- dba(sampleSheet = "design/diffbind_samples.csv", peakFormat = "narrow")
db <- dba.count(db, bParallel = FALSE, bRemoveDuplicates = TRUE,
                bUseSummarizeOverlaps = TRUE)
```

**Input → output:** sample sheet, peaks, BAM/index → counted object → contrasts/model reports and saved objects. The source leaves consensus/summit/filter settings unspecified. The verified [3.16.0 source](https://github.com/bioc/DiffBind/tree/da0b0442311f6264ac8a14eff80dbf9dcc97f614) defaults to `minOverlap=2`, `summits=200`, `filter=1`; inspect the actual resulting ranges rather than assume original peak widths.

**Duplicate policy correction:** the final summarizeOverlaps count pass filters duplicate-marked records; it does not identify unmarked coordinate duplicates. Default summit estimation also involves a preliminary built-in counting pass, so do not describe every internal pass as identical. The upstream worker has no marking stage. Thus the selected switch is not proof of uniformly deduplicated counts ([counting implementation](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/counts.R)).

The same package snapshot accepts numeric normalization vectors and directly assigns them as DESeq2 size factors in its design-based path. The lab script already matches sample IDs and retrieves normalization diagnostics. Check their actual values/order/positivity, model design and branch-specific masks; `library=FULL` is not an automatic additional depth multiplier on this vector. Follow the [review](../assays/cut-and-run/scientific-review.md) for report sign, full-precision selection, coordinate conversion and the precheck that can suppress all-site CSV output.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/04-differential-and-interpretation.md#stage-12-count-each-replicate-and-specify-contrasts) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
