# MACS2

**Function:** Enrichment peak calling. **Evidence:** [CR-S01 / CR-S17 / CR-S18](../assays/cut-and-run/sources.md).

**Observed version evidence:** Lab version not established. 2.2.9.1 is an external candidate for investigation, not a discovered version.

MACS2 identifies enriched genomic intervals. The selected CUT&RUN worker uses paired-end fragment mode and narrow peaks without an explicit background BAM. A historical branch requests broad peaks with different thresholds and duplicate handling.

**Installation:** keep a candidate MACS2 environment separate from the core environment while checking Python/NumPy compiled dependencies and architecture. Do not replace it with MACS3 and retain the same method label. The [versioned option validator](https://raw.githubusercontent.com/macs3-project/MACS/v2.2.9.1/MACS2/OptValidator.py) and [calling source](https://raw.githubusercontent.com/macs3-project/MACS/v2.2.9.1/MACS2/callpeak_cmd.py) were consulted for BAMPE, effective-genome and duplicate behavior. The unknown executed lab version remains a gap.

**Configured observed narrow usage:**

```bash
macs2 callpeak -t align/control_A.hg38-only.sorted.bam -f BAMPE \
  -n control_A --outdir peaks/control_A -g hs --qvalue 0.001 --keep-dup auto
```

**Input → output:** paired human BAM → narrowPeak, peak statistics XLS, summits BED and logs. BAMPE uses fragments; it is not an instruction to apply Tn5 shifts. `--keep-dup auto` is a caller policy, not a deduplicated BAM. Review target shape, controls, background and region artifacts. Historical broad output requires compatible downstream imports. Do not interpret absent peaks as proof of absent binding or loosen q-values solely to obtain more peaks.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/02-alignment-and-peaks.md#stage-6-choose-a-peak-model) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
