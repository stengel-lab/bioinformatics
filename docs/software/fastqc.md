# FastQC

**Function:** Quality control. **Evidence:** [CR-S01](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established in the selected records.

FastQC summarizes base qualities, read lengths, sequence composition, adapters and related properties for sequencing reads. The CUT&RUN worker runs it on both raw and trimmed mates. Reports support a trimming/library review; a green status is not proof of target enrichment.

**Installation:** candidate package `fastqc` in the core environment; Java/runtime dependencies must be resolved by the package manager or installed according to the [project instructions](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/). Linux/macOS package availability differs; Windows analysis examples use WSL2. Native report viewing is possible in a web browser.

**Configured basic usage:** create the output directory first.

```bash
mkdir -p qc/raw
fastqc --threads 4 --outdir qc/raw reads/control_A_R1.fastq.gz reads/control_A_R2.fastq.gz
```

**Input → output:** FASTQ (compressed accepted) → HTML and ZIP report per file. Keep raw and post-trim reports separately. Inspect pair asymmetry, adapter content and retained read lengths. Enrichment-related sequence bias can trigger flags, while PCR duplication cannot be settled from FastQC's sequence duplication plot alone. Save version and report files with the run record.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/01-design-and-reads.md#stage-3-inspect-raw-reads) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
