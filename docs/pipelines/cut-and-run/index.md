# CUT&RUN

CUT&RUN (Cleavage Under Targets and Release Using Nuclease) is a sequencing method for profiling DNA associated with a targeted protein or chromatin feature. This guide follows the **Stengel Lab baseline commands** supplied by the lab bioinformatics lead.

**[Open the step-by-step walkthrough](walkthrough.md)**

## Inputs and outputs

- **Input:** paired-end FASTQ files (R1 and R2) for each sample, an hg38 Bowtie2 index, and a configured analysis environment.
- **Core output:** one coordinate-sorted, indexed BAM per sample.
- **Coverage output:** a CPM-normalized BigWig track from each BAM.
- **Peak output:** MACS2 narrow peak calls from each BAM.
- **Planned downstream endpoint:** DiffBind analysis using the individual BAMs, peak calls, and experimental design. The lab-authoritative DiffBind commands have **not yet been supplied**.

## Processing map

```text
Paired FASTQs (R1, R2)
    │
    ▼
1. FastQC                  — raw-read QC
    │
    ▼
2. Cutadapt                — adapter trimming
    │
    ▼
3. Bowtie2                 — hg38 alignment (SAM)
    │
    ▼
4. SAMtools                — sorted, indexed BAM
    │
    ├──► 5. deepTools/bamCoverage — CPM BigWig
    │
    └──► 6A. MACS2              — peak calls
              │
              └──► 6B. DiffBind — differential binding (implementation pending)
                        ▲
                        └── individual BAMs + sample design
```

**Numbering note:** Step 5 is part of the standard workflow, but its BigWig **is not an input** to MACS2 or DiffBind. Both coverage and peak calling branch from the BAM produced in step 4.

## Baseline and variants

The current baseline uses **hg38 only** for alignment, **CPM** for BigWig normalization, and **paired-end narrow peaks** with MACS2. Different experiments may require spike-in normalization, alternative peak models, or different DiffBind normalization. Those variations will be added only when their processing commands and choices have been reviewed. Normalization for tracks and statistical models must be conceptually consistent, while allowing the tools to use different units or models.

This is a **working educational draft** based on supplied scripts, not a newly execution-validated pipeline. It describes the baseline processing operations, not the Slurm job-array wrapper. The commands and original source evidence are summarized in the [walkthrough](walkthrough.md).