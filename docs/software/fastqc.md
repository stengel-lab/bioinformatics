# FastQC

FastQC summarizes base qualities, read lengths, sequence composition, adapters and related properties for sequencing reads. The CUT&RUN worker runs it on both raw and trimmed mates. Reports support a trimming/library review; a green status is not proof of target enrichment.

## Install

```bash
conda create --name learn-fastqc --override-channels \
  --channel conda-forge --channel bioconda --strict-channel-priority fastqc
conda activate learn-fastqc
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
fastqc --version
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
fastqc [options] reads.fastq.gz ...
```

## Common options

| Option / setting | Meaning |
|---|---|
| `--threads` | Number of files processed concurrently; each needs memory. |
| `--outdir` | Existing directory for HTML and ZIP reports. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
mkdir -p qc/raw
fastqc --threads 4 --outdir qc/raw reads/control_A_R1.fastq.gz reads/control_A_R2.fastq.gz
```

## Expected inputs and outputs

FASTQ (compressed accepted) → HTML and ZIP report per file. Keep raw and post-trim reports separately. Inspect pair asymmetry, adapter content and retained read lengths. Enrichment-related sequence bias can trigger flags, while PCR duplication cannot be settled from FastQC's sequence duplication plot alone. Save version and report files with the run record.

## Documentation and lab notes

Installation notes: candidate package `fastqc` in the core environment; Java/runtime dependencies must be resolved by the package manager or installed according to the [project instructions](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/). Linux/macOS package availability differs; Windows analysis examples use WSL2. Native report viewing is possible in a web browser.

**Function:** Quality control. **Evidence:** [CR-S01](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established in the selected records.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/01-design-and-reads.md#stage-3-inspect-raw-reads) or [software catalog](index.md).
