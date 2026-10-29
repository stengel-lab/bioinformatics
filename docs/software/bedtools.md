# BEDTools

**Function:** Genomic interval operations. **Evidence:** [CR-S01 / CR-S09](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established in selected evidence.

BEDTools compares genomic intervals and alignment overlaps. The selected CUT&RUN worker removes whole narrowPeak intervals overlapping a blacklist and counts BAM records overlapping peaks; downstream helpers merge and intersect derived peak sets.

**Installation:** candidate `bedtools` in the core environment on Linux/macOS or WSL2. Confirm compatible assembly/contig naming and coordinate conventions before use. Official semantics: [intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html) and [merge](https://bedtools.readthedocs.io/en/latest/content/tools/merge.html).

**Configured usage:**

```bash
bedtools intersect -v -a peaks/control_A_peaks.narrowPeak -b refs/hg38.blacklist.bed \
  > peaks/control_A.filtered.narrowPeak
LC_ALL=C sort -k1,1 -k2,2n regions/differential.bed \
  | bedtools merge -i - > regions/differential.merged.bed
```

**Input → output:** BED-like intervals → retained/merged intervals; BAM overlap can emit BAM or BED depending on options. `-v` emits nonoverlapping A records; `-u` emits each overlapping A record once. Peak-only filtering does not clean the BAM or tracks. Merge changes boundaries and discards per-peak metadata unless explicitly aggregated. Source differential CSV→BED conversion needs a one-based/zero-based review. An empty blacklist-filtered output should trigger review, not automatic fallback to unfiltered peaks.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/02-alignment-and-peaks.md#stage-7-review-suspect-regions-and-calculate-enrichment-qc) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
