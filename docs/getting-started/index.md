# Getting started

## Look up a tool

Open the [software library](../software/index.md), choose a program, and follow **Install → Verify installation → Basic syntax → Workflow example**. Use the search box to find a command or parameter directly.

## Follow an analysis

1. Start with the [CUT&RUN walkthrough](../assays/cut-and-run/index.md).
2. Prepare a Linux, macOS or Windows/WSL2 [environment](../installation/index.md).
3. Review the required reads, sample design and [reference files](../assays/cut-and-run/installation.md#reference-files-and-indices).
4. Work through one sample's QC, trimming, alignment, peaks and coverage. Inspect each output before continuing.
5. Compare biological replicates before differential binding or condition summaries.

The command examples use fictional names and require your own permitted inputs and reviewed references. They are manual teaching examples, not a single script to paste and run. The CUT&RUN lesson remains a draft awaiting end-to-end execution validation.

## Read command examples

`reads/control_A_R1.fastq.gz` is an example path, not a downloadable file. Variables such as `$SAMPLE` must be defined in the same Bash session. Lines ending in `\` continue on the next line. Do not paste Bash commands into PowerShell; on Windows use WSL2 or a remote Linux shell.

If file formats are unfamiliar, read [FASTQ, BAM, BED and coordinates](../concepts/file-formats.md). For errors, start with [troubleshooting](../troubleshooting/index.md). Contributors can [preview the website locally](preview.md).
