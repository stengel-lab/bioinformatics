# HOMER

**Function:** Motif enrichment and genomic annotation. **Evidence:** [CR-S10 / CR-S11 / CR-S12](../assays/cut-and-run/sources.md).

**Observed version evidence:** Version not established; hg38 resource release also unknown.

HOMER's `findMotifsGenome.pl` searches sequences in selected regions for motif enrichment; `annotatePeaks.pl` assigns genomic context. The selected workers use 200 bp motif windows, motif length 8, and supplied interval widths for annotation. Enrichment and nearest-gene labels support hypotheses rather than proving occupancy or gene regulation.

**Installation:** optional candidate `homer` plus compatible Perl/runtime and separately configured genome/annotation resources. A package install alone does not establish that hg38 sequences are available. The [Bioconda recipe](https://bioconda.github.io/recipes/homer/README.html) was accessible; the [upstream motif manual](http://homer.ucsd.edu/homer/ngs/peakMotifs.html) timed out during review. Exact runtime behavior must be checked with the installed version before execution.

**Configured source-derived usage:**

```bash
mkdir -p motifs/preparsed annotations
findMotifsGenome.pl regions/differential.bed hg38 motifs/differential \
  -size 200 -len 8 -preparsedDir motifs/preparsed
annotatePeaks.pl regions/differential.bed hg38 -size given \
  -annStats annotations/differential.stats.tsv > annotations/differential.annotated.tsv
```

**Input → output:** coordinate-safe BED and matching genome resources → motif tables/HTML and annotation/statistics tables. Source scripts do not specify custom background matching. Review sequence validity, region/window geometry, GC/length background and selection direction. The upstream source's CSV-to-BED conversion needs review before use. Empty or broad interval sets require separate decisions; do not call a zero-sequence run successful enrichment analysis.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/04-differential-and-interpretation.md#stage-15-motifs-and-genomic-annotation) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
