# Cutadapt

**Function:** Adapter and quality preprocessing. **Evidence:** [CR-S01 / CR-L01](../assays/cut-and-run/sources.md).

**Observed version evidence:** Cutadapt 5.1 and Python 3.11.9 recorded in a historical run; no full lock.

Cutadapt finds adapter sequence and can trim low-quality ends and filter short reads while preserving paired-file relationships. The selected CUT&RUN command supplies paired 3′ adapter sequences and retains reads at least 15 bases long after trimming.

**Installation:** candidate `cutadapt=5.1` in the Python-based core environment. Check Python compatibility and package build on each architecture; the candidate has not been solved or executed here. Use the [official guide](https://cutadapt.readthedocs.io/en/stable/guide.html) for adapter and paired-filter semantics.

**Configured basic usage, observed options with fictional paths:**

```bash
mkdir -p trimmed
cutadapt -j 4 -a AGATCGGAAGAG -A AGATCGGAAGAG -m 15 -q 20 -z \
  -o trimmed/control_A_R1.trimmed.fastq.gz -p trimmed/control_A_R2.trimmed.fastq.gz \
  reads/control_A_R1.fastq.gz reads/control_A_R2.fastq.gz
```

**Input → output:** paired FASTQ → synchronized retained FASTQs and a trimming/filter summary. Record pairs discarded for short length. `-m 15` is a read-length threshold, not an insert-size threshold. In the [5.1 command source](https://raw.githubusercontent.com/marcelm/cutadapt/v5.1/src/cutadapt/cli.py), `-z` means `--zero-cap` for negative qualities; gzip output follows the `.gz` suffix. Confirm the adapter against the actual library preparation before adopting this command.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/01-design-and-reads.md#stage-4-trim-adapters-and-low-quality-ends) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
