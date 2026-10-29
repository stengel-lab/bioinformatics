# R plotting and numerical libraries

**Function:** Statistical figure support. **Evidence:** [CR-S05 / CR-S12 / CR-S14](../assays/cut-and-run/sources.md).

**Observed version evidence:** R 4.4.3 logged; individual plotting/numerical package versions not established.

The custom R code uses plotting libraries to render PCA, correlations, heatmaps, MA plots and annotation summaries. Plotting transformations and labels can change interpretation even when the underlying statistical test is unchanged.

| Library | Observed role | Primary reference |
|---|---|---|
| ggplot2 | Scatter/MA/PCA and summary plots | [Project](https://ggplot2.tidyverse.org/) |
| ggrepel | Repelled labels on plots | [Project](https://ggrepel.slowkow.com/) |
| corrplot | Correlation display | [Maintainer documentation](https://taiyun.github.io/corrplot/) |
| pheatmap | Matrix heatmaps | [CRAN](https://cran.r-project.org/web/packages/pheatmap/index.html) |
| stats / grid | PCA, transformations and layout; distributed with R | [R manuals](https://cran.r-project.org/manuals.html) |
| `rowVars` provider | Variance filtering called without an explicit namespace | U: verify the attached/exported provider in the installed session; do not infer an independently versioned package from the function name alone |

**Installation:** CRAN plotting packages plus the compatible statistical environment. Candidate install commands and version recording are centralized in the setup guide. Base R `stats`/`grid` need no separate CRAN installation. An attached dependency can accidentally provide a function; record `find("rowVars")` and qualify it in a future reviewed implementation.

**Configured basic usage with synthetic data only:**

```r
library(ggplot2)
library(ggrepel)
toy <- data.frame(abundance = c(10, 100, 1000),
                  log2_fold = c(-1, 0, 1), label = c("a", "b", "c"))
p <- ggplot(toy, aes(abundance, log2_fold, label = label)) +
     geom_point() + geom_text_repel() + scale_x_log10()
print(p)
```

**Input → output:** tables/matrices with defined units → figure objects/files. This synthetic plot is not a recreation of lab results. Source PCA uses a common pre-branch matrix, log2(x+1) and unit-variance scaling. MA modes may use different abundance coordinates and report Fold versus concentration-derived M. Review captions, sign, shared scales and missing-as-zero assumptions; never label a rank fallback as measured abundance.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/04-differential-and-interpretation.md#stage-16-figures-that-preserve-the-measurement) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
