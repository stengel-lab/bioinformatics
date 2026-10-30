# 1. Design, inputs and read QC

[Workflow overview](index.md) · Next: [alignment and peaks](02-alignment-and-peaks.md)

**Status:** manual teaching draft; no dataset processing was run. Commands labeled **configured example** require the [installation and reference preparation](installation.md). Source IDs resolve through the [registry](sources.md).

## Stage 1 — Define the biological comparison

### Why this comes first

CUT&RUN enriches DNA released by antibody-directed nuclease cleavage. A peak supports enrichment near a target-associated region; it does not directly measure transcription or prove that the nearest gene is regulated. Fragment length, antibody specificity, digestion, cell recovery and sequencing depth all affect the measurement. The [original method](https://elifesciences.org/articles/21856) provides the experimental rationale.

Separate three meanings of “control”:

| Control | Question answered | Consequence for analysis |
|---|---|---|
| Baseline biological condition, assayed with the same target antibody | What changes after treatment? | Defines a differential-binding contrast |
| IgG or another experimental background control | What enrichment may arise without target-specific binding? | Can inform background assessment and a supported control-aware peak caller |
| Known exogenous calibration material | How does recovery compare across samples? | Can supply a normalization denominator if addition and recovery assumptions hold |

An IgG library is not automatically a baseline target-IP replicate. A spike-in library is not an IgG control. **L:** selected MACS2 calling does not pass a control BAM, and the statistical helper infers some design information from names (**CR-S01, CR-S06**). **P:** enter and review the design explicitly rather than accepting name-based inference.

### Inputs and planning artifact

Create an approved sample sheet containing sample ID, target antibody, biological condition, biological replicate, batch/donor, paired FASTQ paths, and the relationship to any background control. Record the spike species, amount, addition stage and whether it is a deliberate spike or reagent carryover. Keep real metadata outside this public repository.

Fictional design only:

| Sample | Target | Condition | Biological replicate |
|---|---|---|---|
| control_A | target_X | control | 1 |
| control_B | target_X | control | 2 |
| treated_A | target_X | treated | 1 |
| treated_B | target_X | treated | 2 |

Two replicates satisfy the selected `minMembers=2` contrast setting; this is not evidence of adequate power. Paired donors, batches and interactions require a reviewed model. Comparisons across different antibodies do not have the same interpretation as a within-antibody condition contrast.

**QC and troubleshooting:** check for confounding before sequencing analysis. A condition sequenced only in one batch cannot be separated from that batch by adding a label to a plot. Decide whether the target is expected to produce focal peaks, broad domains, or both; retain that decision for Stage 6. **Output → next:** a reviewed design, explicit control roles, and an expected sample list.

## Stage 2 — Identify files and references

**Purpose:** preserve the link between a sequenced library, its paired reads and the reference coordinates used downstream. The selected source expects one merged R1/R2 pair per sample; lane merging and demultiplexing are not implemented in that worker. Do not concatenate unrelated libraries merely to satisfy its filename pattern.

**Required inputs/tools:** gzipped paired FASTQ, a checksum manifest, design metadata, Bash and [execution environments](../../software/execution-environments.md). Source naming is `${sample}_R1.fastq.gz` and `${sample}_R2.fastq.gz` (**CR-S01**). Check mate read counts/order and read identifiers; gzip integrity alone does not establish pairing.

**Copy-ready scaffold**, from a new teaching directory:

```bash
mkdir -p reads qc/raw qc/trimmed trimmed align peaks tracks/spike tracks/cpm
```

**Configured example: variables used through Chapters 1–3.** Paths are teaching aliases, not original institutional locations. Each shell session needs its variables defined. Replace the reference directory with your prepared, reviewed files.

```bash
SAMPLE=control_A
THREADS=8
REF_DIR="$HOME/references/cutrun-teaching"
BOWTIE2_INDEX="$REF_DIR/hg38-sacCer3"
HG38_CONTIGS_BED="$REF_DIR/hg38.contigs.bed"
BLACKLIST="$REF_DIR/hg38.blacklist.bed"
HUMAN_SIZES="$REF_DIR/hg38.chrom.sizes"
COMBINED_BAM="align/${SAMPLE}.hg38-sacCer3.sorted.bam"
HUMAN_BAM="align/${SAMPLE}.hg38-only.sorted.bam"
R1="reads/${SAMPLE}_R1.fastq.gz"
R2="reads/${SAMPLE}_R2.fastq.gz"
TRIM_R1="trimmed/${SAMPLE}_R1.trimmed.fastq.gz"
TRIM_R2="trimmed/${SAMPLE}_R2.trimmed.fastq.gz"
gzip -t "$R1" "$R2"
sha256sum "$R1" "$R2" > "qc/${SAMPLE}.input.sha256"
```

The source labels its combined reference `hg38-sacCer3`; that label does not identify the exact FASTA release, contig naming or index checksum. Review [reference requirements](installation.md#reference-files-and-indices) before aligning. Human `chrX`/`chrM` and yeast Roman-numeral contigs make species identity especially important.

**QC/troubleshooting:** stop on missing, truncated or mismatched mates. Obtain the sequencing facility's adapter/library specification; it is not inferred from an assay name. The source does not establish a validated UMI extraction or lane-merging procedure. **Output → next:** intact paired FASTQs and a traceable reference manifest.

## Stage 3 — Inspect raw reads

**Scientific purpose:** detect adapter read-through, base-quality loss, unexpected read composition and library anomalies before applying transformations. Short released fragments can cause paired reads to sequence through the insert into adapters. Enrichment assays can have nonrandom sequence composition; a warning is a prompt for investigation rather than an automatic sample rejection.

**Input/tool:** original R1/R2; [FastQC](../../software/fastqc.md). **L, CR-S01** runs FastQC before and after trimming. Its version is not established by the reviewed evidence.

**How the computation works:** FastQC summarizes properties such as quality by read position and repeated sequence content over the input reads. Phred quality expresses an estimated base-call error probability (`Q = -10 log10(p)`): Q20 corresponds to an estimated 1% error probability, not a rule that an entire read is bad. Looking at distributions by position helps distinguish a consistent low-quality tail from a few poor bases. The [FastQC project](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) describes its reports; quality flags do not test antibody specificity.

**Configured example:**

```bash
fastqc --threads "$THREADS" --outdir qc/raw "$R1" "$R2"
```

**Parameters:** threads control concurrent work; output directory separates raw from trimmed reports. **Outputs:** one HTML report and ZIP archive per input read file. Save both, with tool version and command record.

**QC:** inspect adapter content, per-base quality, read length, overrepresented sequences and duplication. Compare R1 with R2 and samples within a library-preparation batch. FastQC duplication is not a direct estimate of PCR duplicates after genomic mapping. Do not prescribe a universal pass/fail threshold from these sources.

**Problems:** persistent adapter signal may indicate the wrong adapter sequence; skewed composition can reflect biology or contamination. Check the library specification and sequence examples before changing parameters. **Output → next:** a raw QC record and a justified adapter-trimming choice.

## Stage 4 — Trim adapters and low-quality ends

**Scientific purpose:** remove nonbiological adapter sequence so short inserts can map correctly. Avoid discarding informative short CUT&RUN fragments by importing an unrelated ATAC-seq or ChIP-seq length rule. Read length after trimming and paired-end insert/fragment length are different quantities.

**Inputs/tools:** paired raw FASTQ; [Cutadapt](../../software/cutadapt.md). **L, CR-S01 lines 44–50 and CR-L01:** Cutadapt 5.1 with Python 3.11.9 was recorded in a historical run; the environment is not locked.

**How the computation works:** adapter matching is error-tolerant sequence matching, allowing a read-through adapter to be recognized even with sequencing errors. Quality trimming selects low-quality ends rather than deleting every base whose quality is below 20. Length filtering is applied to the resulting reads, and paired filtering decides whether the pair survives. These operations can change which fragments are observable, so compare both retained yield and the length distribution rather than optimizing a single QC flag. Exact matching defaults belong to the installed version, not just the abbreviated adapter string.

**Configured reconstruction:**

```bash
cutadapt -j "$THREADS" \
  -a AGATCGGAAGAG -A AGATCGGAAGAG \
  -m 15 -q 20 -z \
  -o "$TRIM_R1" -p "$TRIM_R2" "$R1" "$R2" \
  > "qc/${SAMPLE}.cutadapt.log" 2>&1
fastqc --threads "$THREADS" --outdir qc/trimmed "$TRIM_R1" "$TRIM_R2"
```

| Option | Meaning and scientific consequence |
|---|---|
| `-a`, `-A` | Same observed 3′ adapter sequence for R1 and R2; verify it matches the actual library |
| `-m 15` | Minimum retained **read** length, not minimum genomic fragment length; paired filtering can discard the pair if one mate is too short |
| `-q 20` | Quality trimming threshold; compare retained length and yield before increasing it |
| `-z` | In Cutadapt 5.1, `--zero-cap`: change negative quality values to zero. It does **not** request gzip output |
| `-o`, `-p` | Paired outputs; `.gz` filename suffix selects compressed output |
| `-j` | CPU threads; use a value consistent with your allocation |

The `-z` interpretation is verified against the [version 5.1 CLI source](https://raw.githubusercontent.com/marcelm/cutadapt/v5.1/src/cutadapt/cli.py); the [guide](https://cutadapt.readthedocs.io/en/stable/guide.html) explains paired filtering and adapters. These flags are retained to reconstruct the lab command, not endorsed for every library.

**Outputs:** two paired trimmed FASTQs, the trimming report, and post-trimming FastQC reports. **QC:** record input pairs, pairs retained, adapter matches, too-short pairs and length distributions. Examine whether trimming disproportionately removes a particular condition or short-fragment population. Verify that mates remain synchronized.

**Troubleshooting:** excessive loss may reflect incorrect adapters or poor input quality. Remaining adapter signal can reflect an insufficient adapter match or library-specific sequence. Change one reviewed choice at a time and retain the original reports. Do not turn a QC concern into an unexplained parameter change.

**Output → next:** use the trimmed pair in [combined-reference alignment](02-alignment-and-peaks.md). Raw FASTQs and pre-trim reports remain the provenance baseline; trimming does not overwrite them.
