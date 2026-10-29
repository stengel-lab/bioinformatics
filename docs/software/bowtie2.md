# Bowtie2

**Function:** Paired-end alignment. **Evidence:** [CR-S01](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established; do not infer the lab version from the current manual.

Bowtie2 aligns sequencing reads against an indexed reference. The selected CUT&RUN worker maps paired reads to a combined human/yeast index, streams SAM to SAMtools and attaches a read group.

**Installation:** candidate package `bowtie2` in the core environment; index building and alignment require compatible executables and adequate memory/disk. Linux/macOS or WSL2 are the teaching routes. The source index prefix alone does not identify the genome files. See the [official manual](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml).

**Configured minimal usage:** this omits the tutorial's downstream MAPQ filtering and sort.

```bash
mkdir -p align
bowtie2 -p 4 --mm -x refs/combined/index \
  -1 trimmed/control_A_R1.trimmed.fastq.gz -2 trimmed/control_A_R2.trimmed.fastq.gz \
  --no-mixed --no-discordant --rg-id control_A --rg SM:control_A \
  -S align/control_A.sam
```

**Input → output:** indexed FASTA plus paired FASTQ → SAM and alignment statistics on stderr. The source does not explicitly set dovetailing, sensitivity preset, alignment mode or insert-size limits. Those omissions must not be filled in from a different workflow without labeling a change. End-to-end/local and overlapping/containing/dovetailing pairs have distinct meanings, especially for short CUT&RUN inserts. Evaluate reference naming and cross-species mapping before interpreting spike counts.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/02-alignment-and-peaks.md#stage-5-map-paired-reads-and-separate-human-alignments) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
