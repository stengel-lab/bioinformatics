# WiggleTools

**Function:** Track arithmetic. **Evidence:** [CR-S03](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established in selected evidence.

WiggleTools performs arithmetic on genomic signal tracks. The selected averaging worker uses one mean operation over all matched replicates, producing an intermediate bedGraph before human-contig selection and UCSC conversion. A mean is a display summary, not an independent sample.

**Installation:** optional candidate package `wiggletools`; check native dependencies/build availability. The [maintainer repository](https://github.com/Ensembl/WiggleTools) describes operations and build dependencies. The source activates an environment named `genomics`, which is not an exported specification.

**Configured usage:**

```bash
mkdir -p tracks/means
wiggletools write_bg tracks/means/control.raw.bedGraph mean \
  tracks/cpm/control_A.CPM.bw tracks/cpm/control_B.CPM.bw
```

**Input → output:** replicate BigWigs in the same units → arithmetic-mean bedGraph. Sort/filter/convert with [UCSC utilities](ucsc-track-tools.md) as in the tutorial. Review missing interval behavior and exact group membership. Sequentially averaging a prior mean with a third replicate need not give equal thirds; the selected all-replicate operation avoids that historical weighting ambiguity. Preserve individual tracks for QC.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/03-normalization-and-qc.md#stage-11-average-approved-tracks-and-view-loci) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
