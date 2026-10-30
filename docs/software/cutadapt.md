# Cutadapt

Cutadapt finds adapter sequence and can trim low-quality ends and filter short reads while preserving paired-file relationships. The selected CUT&RUN command supplies paired 3′ adapter sequences and retains reads at least 15 bases long after trimming.

## Install

```bash
conda create --name learn-cutadapt --override-channels \
  --channel conda-forge --channel bioconda --strict-channel-priority cutadapt=5.1
conda activate learn-cutadapt
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
cutadapt --version
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
cutadapt [options] -o out_R1.fastq.gz -p out_R2.fastq.gz in_R1.fastq.gz in_R2.fastq.gz
```

## Common options

| Option / setting | Meaning |
|---|---|
| `-j` | Worker cores. |
| `-a / -A` | 3-prime adapter for R1 / R2. |
| `-m 15` | Discard pairs according to the paired-filter rule when a trimmed read is too short; not a fragment-length cutoff. |
| `-q 20` | Trim low-quality ends using a Phred-quality threshold of 20. |
| `-z` | Zero-cap negative qualities in version 5.1; gzip output is selected by the .gz filename. |
| `-o / -p` | Output R1 / R2; keep mate files synchronized. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
mkdir -p trimmed
cutadapt -j 4 -a AGATCGGAAGAG -A AGATCGGAAGAG -m 15 -q 20 -z \
  -o trimmed/control_A_R1.trimmed.fastq.gz -p trimmed/control_A_R2.trimmed.fastq.gz \
  reads/control_A_R1.fastq.gz reads/control_A_R2.fastq.gz
```

## Expected inputs and outputs

paired FASTQ → synchronized retained FASTQs and a trimming/filter summary. Record pairs discarded for short length. `-m 15` is a read-length threshold, not an insert-size threshold. In the [5.1 command source](https://raw.githubusercontent.com/marcelm/cutadapt/v5.1/src/cutadapt/cli.py), `-z` means `--zero-cap` for negative qualities; gzip output follows the `.gz` suffix. Confirm the adapter against the actual library preparation before adopting this command.

## Documentation and lab notes

Installation notes: candidate `cutadapt=5.1` in the Python-based core environment. Check Python compatibility and package build on each architecture; the candidate has not been solved or executed here. Use the [official guide](https://cutadapt.readthedocs.io/en/stable/guide.html) for adapter and paired-filter semantics.

**Function:** Adapter and quality preprocessing. **Evidence:** [CR-S01 / CR-L01](../assays/cut-and-run/sources.md).

**Observed version evidence:** Cutadapt 5.1 and Python 3.11.9 recorded in a historical run; no full lock.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/01-design-and-reads.md#stage-4-trim-adapters-and-low-quality-ends) or [software catalog](index.md).
