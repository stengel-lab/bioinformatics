# DESeq2

**Function:** Count-based statistical modeling. **Evidence:** [CR-S05 / CR-L03](../assays/cut-and-run/sources.md).

**Observed version evidence:** Backend use confirmed; DESeq2 version not established.

DESeq2 models replicate count variation with negative-binomial methods and supports condition-effect testing. It is a backend in the selected DiffBind analysis, not a replacement for experimental design or an analysis of averaged tracks. The [original paper](https://doi.org/10.1186/s13059-014-0550-8) describes its model and estimation; [Bioconductor](https://bioconductor.org/packages/release/bioc/html/DESeq2.html) provides package documentation.

**Installation:** resolve through the reviewed R/Bioconductor family with DiffBind. Do not install an arbitrary current DESeq2 into the historical environment without recording the changed dependency. Bioconductor packages may require compilers/system libraries when binary packages are unavailable.

**Configured role-specific usage through DiffBind:** assumes a reviewed counted `db` object and contrasts appropriate to the experiment.

```r
db_model <- dba.contrast(db, categories = DBA_CONDITION, minMembers = 2)
db_model <- dba.analyze(db_model, method = DBA_DESEQ2)
```

**Input → output:** integer counts, design and normalization state → estimated effects, statistical evidence and adjusted significance in reports. This excerpt does not reproduce the custom spike branch or guarantee a batch-aware design. Check sample order, effective factors, model warnings, tested regions and contrast direction. A global biological change can violate simple library-depth assumptions; a flawed spike denominator can also mislead. FDR is neither a probability of causal regulation nor an effect size.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/04-differential-and-interpretation.md#stage-13-compare-standard-and-spike-normalized-models) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
