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

**Input → output:** sample sheet, peaks, BAM/index → counted object → contrasts/model reports and saved objects. The source does not explicitly set summit recentering, count filters or every consensus default. Duplicate removal here differs from the upstream BAM/coverage policy. Custom numeric normalization is supported, but check order, positivity and retrieved normalization state. Standard default blacklist behavior differs from the spike branch's explicit disabling. Follow the tutorial for report-sign mapping and the significance precheck that can suppress all-site CSV output.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/04-differential-and-interpretation.md#stage-12-count-each-replicate-and-specify-contrasts) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
