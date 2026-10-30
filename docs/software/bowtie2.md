# Bowtie2

Bowtie2 aligns sequencing reads against an indexed reference. The selected CUT&RUN worker maps paired reads to a combined human/yeast index, streams SAM to SAMtools and attaches a read group.

## Install

```bash
conda create --name learn-bowtie2 --override-channels \
  --channel conda-forge --channel bioconda --strict-channel-priority bowtie2
conda activate learn-bowtie2
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
bowtie2 --version
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
bowtie2 -x INDEX -1 READ1 -2 READ2 [options] -S OUTPUT.sam
```

## Common options

| Option / setting | Meaning |
|---|---|
| `-x` | Index prefix, without a .bt2 suffix. |
| `-1 / -2` | Paired FASTQ inputs. |
| `-p 4` | Alignment threads. |
| `--mm` | Memory-map the reference index. |
| `--no-mixed / --no-discordant` | Suppress single-mate fallback and discordant-pair alignments. |
| `--rg-id / --rg SM:` | Read-group identifier and sample name. |
| `-S` | SAM output; omit when streaming SAM to stdout. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
mkdir -p align
bowtie2 -p 4 --mm -x refs/combined/index \
  -1 trimmed/control_A_R1.trimmed.fastq.gz -2 trimmed/control_A_R2.trimmed.fastq.gz \
  --no-mixed --no-discordant --rg-id control_A --rg SM:control_A \
  -S align/control_A.sam
```

## Expected inputs and outputs

indexed FASTA plus paired FASTQ → SAM and alignment statistics on stderr. The source does not explicitly set dovetailing, sensitivity preset, alignment mode or insert-size limits. Those omissions must not be filled in from a different workflow without labeling a change. End-to-end/local and overlapping/containing/dovetailing pairs have distinct meanings, especially for short CUT&RUN inserts. Evaluate reference naming and cross-species mapping before interpreting spike counts.

## Documentation and lab notes

Installation notes: candidate package `bowtie2` in the core environment; index building and alignment require compatible executables and adequate memory/disk. Linux/macOS or WSL2 are the teaching routes. The source index prefix alone does not identify the genome files. See the [official manual](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml).

**Function:** Paired-end alignment. **Evidence:** [CR-S01](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established; do not infer the lab version from the current manual.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/02-alignment-and-peaks.md#stage-5-map-paired-reads-and-separate-human-alignments) or [software catalog](index.md).
