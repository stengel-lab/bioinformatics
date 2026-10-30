# DESeq2

DESeq2 models replicate count variation with negative-binomial methods and supports condition-effect testing. It is a backend in the selected DiffBind analysis, not a replacement for experimental design or an analysis of averaged tracks. The [original paper](https://doi.org/10.1186/s13059-014-0550-8) describes its model and estimation; [Bioconductor](https://bioconductor.org/packages/release/bioc/html/DESeq2.html) provides package documentation.

## Install

In an R release compatible with your chosen Bioconductor release:

```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager", repos = "https://cloud.r-project.org")
BiocManager::install("DESeq2", ask = FALSE, update = FALSE)
BiocManager::valid()
```

This installs from your selected Bioconductor release; it does **not** reproduce the historical lab environment. For the historical R 4.4 / Bioconductor 3.20 candidate, use the [workflow setup guide](../assays/cut-and-run/installation.md#candidate-environments).

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```r
library(DESeq2)
packageVersion("DESeq2")
sessionInfo()
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
DiffBind: dba.analyze(reviewed_object, method = DBA_DESEQ2)
```

## Common options

| Option / setting | Meaning |
|---|---|
| `categories = DBA_CONDITION` | Construct contrasts from reviewed condition metadata. |
| `minMembers = 2` | Require at least two members per contrasted group; not a power guarantee. |
| `method = DBA_DESEQ2` | Select the DESeq2 backend within DiffBind. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```r
db_model <- dba.contrast(db, categories = DBA_CONDITION, minMembers = 2)
db_model <- dba.analyze(db_model, method = DBA_DESEQ2)
```

## Expected inputs and outputs

integer counts, design and normalization state → estimated effects, statistical evidence and adjusted significance in reports. This excerpt does not reproduce the custom spike branch or guarantee a batch-aware design. Check sample order, effective factors, model warnings, tested regions and contrast direction. A global biological change can violate simple library-depth assumptions; a flawed spike denominator can also mislead. FDR is neither a probability of causal regulation nor an effect size.

## Documentation and lab notes

Installation notes: resolve through the reviewed R/Bioconductor family with DiffBind. Do not install an arbitrary current DESeq2 into the historical environment without recording the changed dependency. Bioconductor packages may require compilers/system libraries when binary packages are unavailable.

**Function:** Count-based statistical modeling. **Evidence:** [CR-S05 / CR-L03](../assays/cut-and-run/sources.md).

**Observed version evidence:** Backend use confirmed; DESeq2 version not established.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/04-differential-and-interpretation.md#stage-13-compare-standard-and-spike-normalized-models) or [software catalog](index.md).
