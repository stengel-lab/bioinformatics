# SAMtools

SAMtools converts and filters alignment records, sorts/indexes BAMs and provides alignment statistics. The CUT&RUN workflow uses `view`, `sort`, `index`, `flagstat` and `idxstats`. Proposed reference preparation additionally uses `faidx`; that is not proof the historical index was built by these instructions.

## Install

```bash
conda create --name learn-samtools --override-channels \
  --channel conda-forge --channel bioconda --strict-channel-priority samtools
conda activate learn-samtools
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
samtools --version
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
samtools <view|sort|index|flagstat|idxstats> [options] INPUT
```

## Common options

| Option / setting | Meaning |
|---|---|
| `view -b` | Write BAM instead of SAM. |
| `view -q 30` | Keep alignment records with MAPQ at least 30. |
| `view -F 0x4` | Exclude unmapped records. |
| `view -L` | Select records overlapping BED intervals, used for human-contig selection. |
| `sort -@ / -m` | Additional threads / approximate memory per thread. |
| `sort -o` | Coordinate-sorted BAM output. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
set -o pipefail
samtools view -b -q 30 -F 0x4 align/control_A.sam \
  | samtools sort -@ 2 -m 2G -o align/control_A.sorted.bam -
samtools index align/control_A.sorted.bam
samtools flagstat align/control_A.sorted.bam
samtools idxstats align/control_A.sorted.bam
```

## Expected inputs and outputs

SAM input → coordinate-sorted BAM, index, flag statistics and mapped-segment tables.

`-q 30` filters individual records, and `-F 0x4` excludes unmapped ones. It does not remove duplicates or guarantee both mates remain. `sort -m` is per-thread memory. Coordinate sorting is required for the chosen indexing/region operations. `idxstats` column 3 is mapped read-segments, not complete fragments. A reference-name regex is not a reliable species identifier. `quickcheck` offers basic integrity checks but is weaker than a full alignment/pair audit.

## Documentation and lab notes

Installation notes: candidate `samtools` resolves HTSlib and compression/library dependencies in the core environment. On Linux/macOS/WSL2 verify the actual executable and version. Refer to the [view manual](https://www.htslib.org/doc/samtools-view.html) and [idxstats manual](https://www.htslib.org/doc/samtools-idxstats.html).

**Function:** Alignment filtering, sorting and QC. **Evidence:** [CR-S01 / CR-S02](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established in selected evidence.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/02-alignment-and-peaks.md#stage-5-map-paired-reads-and-separate-human-alignments) or [software catalog](index.md).
