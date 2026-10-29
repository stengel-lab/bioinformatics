# deepTools

**Function:** Coverage, replicate QC and region figures. **Evidence:** [CR-S02 / CR-S15 / CR-S16](../assays/cut-and-run/sources.md).

**Observed version evidence:** Lab version not established; versioned 3.5.6 manuals are external references.

deepTools creates BigWig coverage (`bamCoverage`), binned signal matrices (`multiBigwigSummary`), sample PCA/correlation, and region-centered matrices/heatmaps/profiles (`computeMatrix`, `plotHeatmap`, `plotProfile`). Coverage and replicate figures are distinct from statistical differential-binding counts.

**Installation:** candidate `deeptools` in the Python core environment; compiled scientific and BigWig dependencies must resolve for the platform. Linux/macOS or WSL2 are proposed routes, not verified installations. Official references: [bamCoverage](https://deeptools.readthedocs.io/en/develop/content/tools/bamCoverage.html), [multiBigwigSummary](https://deeptools.readthedocs.io/en/3.5.6/content/tools/multiBigwigSummary.html), [computeMatrix](https://deeptools.readthedocs.io/en/3.5.6/content/tools/computeMatrix.html).

**Configured human CPM usage:**

```bash
mkdir -p tracks/cpm
bamCoverage -b align/control_A.hg38-only.sorted.bam \
  -o tracks/cpm/control_A.CPM.bw --normalizeUsing CPM --binSize 10 \
  --effectiveGenomeSize 2913022398 --numberOfProcessors 4
```

**Input → output:** sorted/indexed BAM → BigWig; matched BigWigs/regions → matrices, tables and figures. Source spike coverage instead uses the combined BAM and `None` plus an external multiplier. No explicit `--extendReads` is set. Giving an effective genome size does not change CPM into RPGC. Historical heatmaps use region centers, ±2 kb and missing-as-zero; those are scientific display assumptions. Keep units, contigs, region sets, scales and replicate labels explicit.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/03-normalization-and-qc.md#stage-9-make-coverage-tracks-with-an-explicit-denominator) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
