# UCSC track utilities

**Function:** Browser track formats. **Evidence:** [CR-S03](../assays/cut-and-run/sources.md).

**Observed version evidence:** Executable versions not established.

The UCSC `bedGraphToBigWig` utility converts numeric genomic intervals into an indexed, compact browser format. The selected mean-track worker uses it after sorting and restricting intervals to human chromosome names. The tutorial does not imply every UCSC binary is a workflow dependency.

**Installation:** optional candidate package `ucsc-bedgraphtobigwig`, or an appropriate binary from the [UCSC BigWig documentation](https://genome.ucsc.edu/goldenpath/help/bigWig.html). Match OS/architecture; WSL2 uses Linux builds. Retain executable provenance, checksums and usage/license terms as appropriate.

**Configured usage:**

```bash
LC_ALL=C sort -k1,1 -k2,2n tracks/means/control.mean.bedGraph \
  > tracks/means/control.mean.sorted.bedGraph
bedGraphToBigWig tracks/means/control.mean.sorted.bedGraph refs/human.chrom.sizes \
  tracks/means/control.mean.CPM.bw
```

**Input → output:** sorted, nonoverlapping zero-based bedGraph plus matching chromosome sizes → BigWig. Wrong assembly names, out-of-bounds intervals or overlap can cause conversion errors. A valid BigWig format does not prove the values have appropriate normalization. Keep units and contributing replicates in a sidecar record and inspect the file in a matching-reference [browser](igv.md).

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/03-normalization-and-qc.md#stage-11-average-approved-tracks-and-view-loci) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
