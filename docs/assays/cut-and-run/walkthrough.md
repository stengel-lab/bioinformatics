# CUT&RUN: step by step

Follow paired-end reads through QC, alignment, peaks and coverage, then compare biological replicates and interpret binding changes.

**Educational draft:** fictional names, configured inputs, and a manual sequence. The complete analysis and installation candidates have not been executed or validated as a teaching protocol. No data or automated pipeline is distributed.

## Before you begin

Install the [workflow tools](installation.md#candidate-environments) on Linux, macOS or Windows/WSL2. Prepare paired FASTQs, a reviewed sample/replicate design, a combined human/yeast Bowtie2 index, a whole-human-contig BED and an assembly-matched blacklist. See [reference preparation](installation.md#reference-files-and-indices).

Establish the antibody target, negative-control role and biological comparison first. A baseline target-antibody sample and an IgG background control serve different purposes. See [design details](01-design-and-reads.md#stage-1-define-the-biological-comparison).

```text
Paired FASTQ → FastQC → Cutadapt → FastQC
  → Bowtie2 (combined reference) → SAMtools (MAPQ, sort, index)
  → human BAM
      ├─ MACS2 → blacklist-filtered peaks
      ├─ deepTools → per-replicate CPM tracks → replicate QC → IGV
      └─ individual BAMs + peaks + design → DiffBind/DESeq2 → interpretation
Optional after review: verified spike counts → calibrated tracks / count model
```

[Full workflow diagram](assets/workflow.svg)

## 1. Set up one sample

Work in a new analysis directory with permitted input reads. Repeat the per-sample steps for every biological replicate. These paths match the [proposed reference example](installation.md#reference-files-and-indices); substitute your approved resources. Define variables in the same Bash session.

```bash
mkdir -p reads qc/raw qc/trimmed trimmed align peaks tracks/cpm
SAMPLE=control_A
THREADS=4
REF_DIR="$PWD/refs"
BOWTIE2_INDEX="$REF_DIR/combined/index"
HG38_CONTIGS_BED="$REF_DIR/human.contigs.bed"
BLACKLIST="$REF_DIR/hg38.blacklist.bed"
R1="reads/${SAMPLE}_R1.fastq.gz"
R2="reads/${SAMPLE}_R2.fastq.gz"
TRIM_R1="trimmed/${SAMPLE}_R1.trimmed.fastq.gz"
TRIM_R2="trimmed/${SAMPLE}_R2.trimmed.fastq.gz"
COMBINED_BAM="align/${SAMPLE}.hg38-sacCer3.sorted.bam"
HUMAN_BAM="align/${SAMPLE}.hg38-only.sorted.bam"
```

**Check:** R1/R2 must belong to the same library, include all intended lanes, and have matching read names/order. Gzip integrity alone does not establish pairing. Record versions, sample membership and reference identities privately. Four threads are a teaching adjustment, not a measured resource prescription; concurrent programs and sorting need additional memory and temporary disk.

## 2. Inspect raw reads

[FastQC](../../software/fastqc.md) summarizes quality, lengths, adapters and sequence composition before trimming.

```bash
fastqc --threads "$THREADS" --outdir qc/raw "$R1" "$R2"
```

**Output/check:** HTML and ZIP per mate. Open the reports and inspect adapter read-through, low-quality ends, unexpected lengths and mate asymmetry. Enrichment-related sequence bias can trigger warnings; review what a flag means rather than requiring every module to be green. FastQC does not measure target enrichment.

## 3. Trim adapters and inspect retained reads

Short CUT&RUN inserts can cause sequencing into adapters. [Cutadapt](../../software/cutadapt.md) removes adapters and low-quality ends while preserving paired-file synchronization.

```bash
cutadapt -j "$THREADS" -a AGATCGGAAGAG -A AGATCGGAAGAG -m 15 -q 20 -z \
  -o "$TRIM_R1" -p "$TRIM_R2" "$R1" "$R2" \
  > "qc/${SAMPLE}.cutadapt.log"
fastqc --threads "$THREADS" --outdir qc/trimmed "$TRIM_R1" "$TRIM_R2"
```

**Parameters:** `-a`/`-A` specify R1/R2 3′ adapters; confirm them against the library preparation. `-m 15` sets a trimmed read-length threshold, not a fragment-length cutoff. `-q 20` trims low-quality ends. In observed Cutadapt 5.1, `-z` zero-caps negative qualities; the `.gz` filenames request compression.

**Output/check:** paired trimmed FASTQs, log and new FastQC reports. Compare adapter content, retained pairs and length distributions with the raw reports. Excessive loss can indicate incorrect adapters or poor quality. Very short reads can map ambiguously. Trimmed reads feed alignment. [More explanation](01-design-and-reads.md#stage-4-trim-adapters-and-low-quality-ends).

## 4. Align, filter, sort and index

[Bowtie2](../../software/bowtie2.md) finds read placements in the combined reference. [SAMtools](../../software/samtools.md) filters alignment records and creates indexed, coordinate-sorted BAMs.

```bash
set -o pipefail
bowtie2 -p "$THREADS" --mm -x "$BOWTIE2_INDEX" \
  -1 "$TRIM_R1" -2 "$TRIM_R2" --no-mixed --no-discordant \
  --rg-id "$SAMPLE" --rg "SM:$SAMPLE" \
  2> "qc/${SAMPLE}.bowtie2.log" \
  | samtools view -b -q 30 -F 0x4 -@ 2 - \
  | samtools sort -@ 2 -m 2G -o "$COMBINED_BAM" -
samtools index "$COMBINED_BAM"
samtools flagstat "$COMBINED_BAM" > "qc/${SAMPLE}.flagstat.txt"
samtools view -b -L "$HG38_CONTIGS_BED" "$COMBINED_BAM" \
  | samtools sort -@ 2 -m 2G -o "$HUMAN_BAM" -
samtools index "$HUMAN_BAM"
samtools quickcheck -v "$COMBINED_BAM" "$HUMAN_BAM"
```

**Parameters:** `--no-mixed --no-discordant` suppress unpaired fallback and discordant alignments. `--mm` memory-maps the index. `-q 30` applies a per-record MAPQ threshold; `-F 0x4` excludes unmapped records. `-L` selects records overlapping the human BED. Sorting `-m 2G` is per-thread memory; several processes run concurrently.

**Output/check:** combined and human BAMs, indexes and mapping logs. Inspect mapping rates, reference names/lengths, retained pairs and mitochondrial fraction. Per-record filtering can leave one mate behind. Human-only does not necessarily mean nuclear-only. `quickcheck` is a basic integrity check, not a complete pair audit.

The observed method adds no explicit duplicate marking/removal, mitochondrial exclusion, dovetail option or sensitivity preset. [Alignment details](02-alignment-and-peaks.md#stage-5-map-paired-reads-and-separate-human-alignments) explain these choices. `pipefail` and named logs are teaching safeguards. Inspect failures before continuing; the snippets do not implement restart management.

## 5. Call peaks

[MACS2](../../software/macs2.md) identifies enriched intervals relative to its background model. The selected lab command uses paired-end fragments and narrow peaks:

```bash
macs2 callpeak -t "$HUMAN_BAM" -f BAMPE -n "$SAMPLE" \
  --outdir "peaks/$SAMPLE" -g hs --qvalue 0.001 --keep-dup auto
```

`BAMPE` uses observed paired-end fragments; `-g hs` is the human effective-genome shortcut; `--qvalue 0.001` sets the significance cutoff. `--keep-dup auto` is MACS2's internal duplicate policy and does not rewrite the BAM.

**Output/check:** narrowPeak intervals, summit BED, statistics and logs. Inspect peak numbers, widths, positive/negative loci and background. This observed command has **no explicit `-c` control BAM**. Its q-value does not establish antibody specificity or replicate reproducibility. Focal transcription-factor or BCOR-associated occupancy and broad histone domains may need different models. Review [controls and narrow/broad alternatives](02-alignment-and-peaks.md#stage-6-choose-a-peak-model) before changing the command.

## 6. Review blacklist overlap

[BEDTools](../../software/bedtools.md) compares peaks with assembly-matched artifact intervals.

```bash
RAW_PEAKS="peaks/$SAMPLE/${SAMPLE}_peaks.narrowPeak"
FILTERED_PEAKS="peaks/$SAMPLE/${SAMPLE}_peaks.blacklist_filtered.narrowPeak"
bedtools intersect -v -a "$RAW_PEAKS" -b "$BLACKLIST" > "$FILTERED_PEAKS"
bedtools intersect -u -a "$RAW_PEAKS" -b "$BLACKLIST" \
  > "peaks/$SAMPLE/${SAMPLE}_peaks.blacklist_removed.narrowPeak"
wc -l "$RAW_PEAKS" "$FILTERED_PEAKS"
```

`-v` retains whole peaks with no overlap; `-u` records each removed peak once. Review removed counts and intervals. Stop on an unexpectedly empty result instead of silently reusing raw peaks; this review gate differs from the source fallback.

**Output:** retained and removed peak lists. This filters peaks only, leaving the original BAM/track signal intact. See [blacklist and FRiP details](02-alignment-and-peaks.md#stage-7-review-suspect-regions-and-calculate-enrichment-qc) for enrichment QC and mask limitations.

## 7. Make per-replicate coverage tracks

[deepTools](../../software/deeptools.md) converts alignments into BigWig tracks. The human CPM branch gives a library-depth-scaled view:

```bash
bamCoverage -b "$HUMAN_BAM" -o "tracks/cpm/${SAMPLE}.CPM.bw" \
  --normalizeUsing CPM --binSize 10 \
  --effectiveGenomeSize 2913022398 --numberOfProcessors "$THREADS"
```

**Output/check:** one CPM BigWig per replicate, using 10-base bins. The effective-genome argument does not turn CPM into RPGC. No explicit read extension or additional duplicate/mitochondrial filters are added here. CPM can conceal global occupancy changes; it is not a universal normalization solution.

**Optional spike branch — review required:** the historical species-count regex can count human `chrX`/`chrM` as yeast. Do not use those counts as a calibration denominator. Establish the exact reference dictionary and spike protocol first, then use [reference-aware counting](reference-audit.md#proposed-exact-role-counting-example). The [normalization chapter](03-normalization-and-qc.md) retains the observed formulas and downstream trace. Historical result impact is not established. This gate applies to both spike-scaled tracks and spike-normalized differential binding.

## 8. Compare replicates and view loci

Repeat steps 1–7 for all samples. With four fictional tracks available:

```bash
multiBigwigSummary bins \
  -b tracks/cpm/control_A.CPM.bw tracks/cpm/control_B.CPM.bw \
     tracks/cpm/treated_A.CPM.bw tracks/cpm/treated_B.CPM.bw \
  --labels control_A control_B treated_A treated_B \
  --binSize 10000 --numberOfProcessors 4 -o qc/replicate_bins.npz
plotPCA -in qc/replicate_bins.npz -o qc/track_PCA.pdf
plotCorrelation -in qc/replicate_bins.npz --corMethod spearman \
  --whatToPlot heatmap -o qc/track_correlation.pdf
```

**Output/check:** signal matrix, PCA and Spearman-correlation heatmap. Investigate outliers with QC, design and controls. Genome-wide correlation can reflect shared background; peak reproducibility needs a separate target-appropriate assessment. Do not exclude a replicate solely because it contradicts an expected result.

In [IGV](../../software/igv.md), select the matching assembly, load individual tracks and peaks, and inspect positive and negative loci with common y-axis ranges. Optionally average approved tracks with [WiggleTools](../../software/wiggletools.md) and convert with [UCSC utilities](../../software/ucsc-track-tools.md); see the [averaging lesson](03-normalization-and-qc.md#stage-11-average-approved-tracks-and-view-loci). Preserve individual tracks.

## 9. Count binding and test biological contrasts

[DiffBind](../../software/diffbind.md) counts individual BAMs over a shared region universe; [DESeq2](../../software/deseq2.md) can model variation between biological conditions. **Averaged tracks are not statistical replicates.**

Prepare `design/diffbind_samples.csv` with `SampleID`, `Condition`, `Replicate`, `bamReads`, `Peaks` and `PeakCaller` (`narrow` for these narrowPeak files). Use approved per-sample peak files and real BAM paths. Review the full [sample-sheet and model example](04-differential-and-interpretation.md#stage-12-count-each-replicate-and-specify-contrasts) before using this standard-branch excerpt:

```r
library(DiffBind)
db <- dba(sampleSheet = "design/diffbind_samples.csv", peakFormat = "narrow")
db <- dba.count(db, bParallel = FALSE, bRemoveDuplicates = TRUE,
                bUseSummarizeOverlaps = TRUE)
db <- dba.contrast(db, categories = DBA_CONDITION, minMembers = 2)
db <- dba.analyze(db, method = DBA_DESEQ2)
```

This does not implement the custom spike branch or a batch-aware model. In logged DiffBind 3.16.0, the final duplicate switch filters duplicate-marked records; upstream code does not mark duplicates. Summit/consensus defaults also change the counted regions. Review the [DiffBind settings](../../software/diffbind.md), design, normalization and contrast direction.

**Output/check:** counted/model objects and contrast reports, exported in the detailed lesson. Review effect size, FDR, replicate support and warnings. Paired donors/batches need suitable design factors. Convert one-based R ranges to zero-based BED before interval analysis.

## 10. Interpret and present

Use [HOMER](../../software/homer.md) for motifs and genomic annotation; [deepTools](../../software/deeptools.md) for region-centered heatmaps/profiles; and [R](../../software/r-plotting.md) or [Python figure libraries](../../software/python-figures.md) for figures. Follow [interpretation commands and checks](04-differential-and-interpretation.md#stage-15-motifs-and-genomic-annotation).

Keep units, assembly, region selection, contrast direction and replicate identities in captions. Nearest-gene annotation does not prove regulation; motif enrichment does not establish direct factor binding.

## Read more

[Detailed lessons and diagram](index.md) · [Method comparison](methods-comparison.md) · [Scientific review](scientific-review.md) · [References](references.md)
