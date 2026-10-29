# SAMtools

**Function:** Alignment filtering, sorting and QC. **Evidence:** [CR-S01 / CR-S02](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established in selected evidence.

SAMtools converts and filters alignment records, sorts/indexes BAMs and provides alignment statistics. The CUT&RUN workflow uses `view`, `sort`, `index`, `flagstat` and `idxstats`. Proposed reference preparation additionally uses `faidx`; that is not proof the historical index was built by these instructions.

**Installation:** candidate `samtools` resolves HTSlib and compression/library dependencies in the core environment. On Linux/macOS/WSL2 verify the actual executable and version. Refer to the [view manual](https://www.htslib.org/doc/samtools-view.html) and [idxstats manual](https://www.htslib.org/doc/samtools-idxstats.html).

**Configured usage:** input is SAM; output is MAPQ-filtered sorted BAM and its index.

```bash
set -o pipefail
samtools view -b -q 30 -F 0x4 align/control_A.sam \
  | samtools sort -@ 2 -m 2G -o align/control_A.sorted.bam -
samtools index align/control_A.sorted.bam
samtools flagstat align/control_A.sorted.bam
samtools idxstats align/control_A.sorted.bam
```

`-q 30` filters individual records, and `-F 0x4` excludes unmapped ones. It does not remove duplicates or guarantee both mates remain. `sort -m` is per-thread memory. Coordinate sorting is required for the chosen indexing/region operations. `idxstats` column 3 is mapped read-segments, not complete fragments. A reference-name regex is not a reliable species identifier. `quickcheck` offers basic integrity checks but is weaker than a full alignment/pair audit.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/02-alignment-and-peaks.md#stage-5-map-paired-reads-and-separate-human-alignments) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
