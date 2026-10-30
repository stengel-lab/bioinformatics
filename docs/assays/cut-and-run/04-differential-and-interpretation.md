# 4. Differential binding and biological interpretation

Previous: [normalization and QC](03-normalization-and-qc.md) · [Workflow overview](index.md)

**Status:** source reconstruction and review-gated teaching examples. No statistical model, enrichment analysis or figure based on real data was run. Source **CR-S05** is the selected analysis; the separate standard-only **CR-S21** is not an automatic fallback.

## Stage 12 — Count each replicate and specify contrasts

### Scientific purpose

Differential binding compares counts from independent biological samples over a defined interval universe. It estimates a condition effect and uncertainty, conditional on counting, normalization and model design. Averaged tracks cannot supply replicate-level dispersion. [DiffBind](../../software/diffbind.md) organizes peaks/BAM counts and delegates modeling; [DESeq2](../../software/deseq2.md) supplies the selected negative-binomial analysis branch.

**Inputs/environment:** individual human BAMs/indexes, actual approved peak paths, a reviewed sample sheet and contrast specification; R, DiffBind, its Bioconductor dependencies and plotting packages. Historical logs record R 4.4.3 and DiffBind 3.16.0, not DESeq2's version (**CR-L02**). Counting source settings disable parallel counting even though the wrapper requests 16 CPUs/64 GB/24 h.

### Build metadata deliberately

**Configured teaching schema:** save a CSV such as the following as `design/diffbind_samples.csv`, after replacing the fictional inputs. Paths here are project-root-relative, whereas the lab generator writes resolved project paths. The selected R script changes its working directory into an output subdirectory, so relative paths require resolution before that change. Do not copy this CSV into the unchanged private worker and assume path semantics agree.

```csv
SampleID,Tissue,Factor,Condition,Replicate,bamReads,Peaks,PeakCaller
control_A,teaching,target_X,control,1,align/control_A.hg38-only.sorted.bam,peaks/control_A/control_A_peaks.blacklist_filtered.narrowPeak,narrow
control_B,teaching,target_X,control,2,align/control_B.hg38-only.sorted.bam,peaks/control_B/control_B_peaks.blacklist_filtered.narrowPeak,narrow
treated_A,teaching,target_X,treated,1,align/treated_A.hg38-only.sorted.bam,peaks/treated_A/treated_A_peaks.blacklist_filtered.narrowPeak,narrow
treated_B,teaching,target_X,treated,2,align/treated_B.hg38-only.sorted.bam,peaks/treated_B/treated_B_peaks.blacklist_filtered.narrowPeak,narrow
```

The actual filtered files must exist and contain the intended intervals. Name inference in **CR-S06** can confuse background-control labels with biological baseline labels. Batch/donor labels in a CSV are not sufficient unless the statistical design uses them.

The selected custom contrast configuration uses columns:

```csv
ContrastName,Numerator,Denominator
treated_vs_control,treated,control
```

This is an input to the custom source's orientation logic, not a universal `dba.contrast()` argument format. **L:** it matches configured labels to `Group`/`Group2`, detects reversed orientation, and passes `bFlip` to reporting. **U:** verify with a known toy increase that positive `Fold` means the intended numerator is enriched before interpreting positive/negative biology.

### Reconstruct the counting stage

**Configured R teaching excerpt**, run from a project root with the illustrated CSV. It demonstrates the observed counting options without reproducing the entire private script:

```r
library(DiffBind)
samples <- read.csv("design/diffbind_samples.csv", stringsAsFactors = FALSE)
samples$bamReads <- normalizePath(samples$bamReads, mustWork = TRUE)
samples$Peaks <- normalizePath(samples$Peaks, mustWork = TRUE)
db <- dba(sampleSheet = samples, peakFormat = "narrow")
db <- dba.count(db, bParallel = FALSE, bRemoveDuplicates = TRUE,
                bUseSummarizeOverlaps = TRUE)
db_reads <- dba.count(db, peaks = NULL, score = DBA_SCORE_READS)
```

**Duplicate correction:** in the final summarizeOverlaps counting pass, DiffBind 3.16.0 implements `bRemoveDuplicates=TRUE` by excluding duplicate-flagged records. That pass does not discover unmarked coordinate duplicates. Default summit estimation also uses a preliminary built-in counting pass, so internal stages should not be described as uniformly identical. The fresh FASTQ→BAM worker has no duplicate-marking step, and the switch alone does not establish uniformly deduplicated counts. Inspect actual BAM flags and returned ranges before attributing a difference to duplicate removal ([versioned counting code](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/counts.R)).

**How overlap counting works:** a consensus interval universe is formed, then eligible alignments/pairs are assigned under the overlap algorithm. The selected path uses summarizeOverlaps with pair detection and its configured handling of unmatched/ambiguous records; this is not simply summing coverage bins. Lost mates and overlapping features can change eligibility. Counting BAMs preserves biological samples; pooling them first would remove replicate-level variation.

The source leaves important counting defaults unspecified. The verified [3.16.0 API](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/man/dba.count.Rd) supplies `minOverlap=2`, `summits=200`, `filter=1`. The first refers to support across input peaksets; the second can recenter intervals into **401 bp** windows (200 bp each side plus center), rather than retaining original widths. These are installed defaults, not explicit lab selections. Inspect the final ranges, filter state and design. For broad biology, fixed summit windows may answer a different question from domain-wide counting.

**Outputs:** counted DiffBind object, read-score export and a common pre-branch count table. **L:** the source exports `normalized_read_counts_all_samples.csv` before standard/spike model branching. Its filename does not establish that it contains spike-normalized counts. Preserve the normalization state and sample order rather than infer them from names.

**QC/troubleshooting:** inspect ranges, counts, zero-count sites, duplicate treatment, BAM header/sample identity and overlap between input peaks and counted regions. Missing peaks or file paths can silently change what is represented if helper-generated assumptions are accepted. Save `sessionInfo()`, package versions, full warnings and the counted object. **Output → next:** a fixed count object and reviewed contrasts, before applying model-specific normalization.

## Stage 13 — Compare standard and spike-normalized models

### Observed standard branch

**L, CR-S05:** copies the counted object, calls `dba.contrast(..., categories=DBA_CONDITION, minMembers=2)`, then `dba.analyze()` using installed defaults. Saved logs show DESeq2 and blacklist application. The source does not explicitly equalize all default filters with the spike branch.

**Configured excerpt:**

```r
db_standard <- dba.contrast(db, categories = DBA_CONDITION, minMembers = 2)
db_standard <- dba.analyze(db_standard)
```

This is not a reviewed batch/donor model. Inspect the actual contrast table and design. Standard library-size normalization carries assumptions about stable abundance structure; a plausible global occupancy change is a reason to assess calibration, not proof that calibration is valid.

**How the statistical model works:** DESeq2 models each interval's replicate counts with a negative-binomial distribution, allowing variance above a Poisson model. The expected count combines a sample size factor and an interval abundance whose condition effects are represented by a design matrix. Dispersion estimation uses information across intervals; a condition test asks whether the relevant effect is distinguishable from zero. Multiple-testing adjustment applies over the tested universe. This is why design, masks and normalization matter independently. A model cannot separate perfectly confounded condition and batch labels. See the [DESeq2 vignette](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html).

### Observed spike branch and its review gate

The source matches `spike_counts.tsv` to DiffBind sample IDs and forms `S_i / median(S)`. It checks IDs/numeric conversion and missing matches, but calibration and strict positivity still need scientific and implementation review. A zero denominator/factor is not acceptable for a logarithmic count model.

**Review-gated R excerpt:** `spike_counts_in_db_order` must be a verified, positive numeric vector in exactly the counted object's sample order. This variable is deliberately not fabricated from a real dataset here.

```r
stopifnot(is.numeric(spike_counts_in_db_order),
          all(is.finite(spike_counts_in_db_order)),
          all(spike_counts_in_db_order > 0))
size_factors <- spike_counts_in_db_order / median(spike_counts_in_db_order)
db_spike <- dba.normalize(db, method = DBA_DESEQ2, normalize = size_factors,
                          library = DBA_LIBSIZE_FULL, background = FALSE)
db_spike <- dba.contrast(db_spike, categories = DBA_CONDITION, minMembers = 2)
db_spike <- dba.analyze(db_spike, method = DBA_DESEQ2,
                       bGreylist = FALSE, bBlacklist = FALSE)
```

The positivity guards are proposed teaching safeguards. **E — now verified against package version 3.16.0:** the [normalization interface](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/normalize.R) accepts a numeric vector, and its [DESeq2 adapter](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/analyze_deseq2.R#L188-L196) directly assigns the supplied values as size factors in the design-based path. `library=DBA_LIBSIZE_FULL` does not automatically multiply that vector by library depth there. The intended denominator direction `S/median(S)` is therefore consistent with this API; do not invert it as a presumed bug fix.

**L:** the source already matches spike IDs to the counted sample IDs and retrieves normalization state at CR-S05:538–542, writing `debug_spike_normalize_retrieve.csv` and a text record. Review those records and the realized model/sample order; do not describe retrieval or ID matching as absent. Also check positivity/finiteness and state after contrast setup/analysis. Static source verification is narrower than executing and scientifically validating the fitted model.

**Important confound:** the standard branch leaves blacklist behavior at defaults, while the spike branch explicitly disables blacklist and greylist application. Different tested interval universes can produce different results independently of normalization. Compare common regions with consistent approved masks in a future controlled exercise; do not silently change history.

### Reports and sign

**L:** after matching configured contrasts, reporting uses `dba.report(..., th=1, bFlip=NeedsFlip)`. However, an earlier significance-count precheck can skip a contrast with zero default-significant sites. Thus `th=1` does **not** guarantee an all-sites CSV for every contrast. Check statuses including `generated`, `no_differential_sites` and `report_failed` in `contrast_summary.csv`; a missing file does not mean there are no bound regions.

The [3.16.0 report contract](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/man/dba.report.Rd) defines positive Fold as greater binding in group 1; `bFlip` swaps the groups. The source flips when group 1 is the configured denominator, so its static logic is consistent with positive **numerator** enrichment. No sign bug was found. Confirm the intended comparison with metadata and a known-direction toy model before biological interpretation.

The selected script saves per-branch reports, `dba_analysis.RData`, summary/status files and debug information, plus a combined summary. GRanges-to-CSV output can use `seqnames/start/end/width/strand`; explicit data-frame output can use `Chr/Start/End`. Statistics include `Fold`, `FDR`, `Conc` and group concentrations. Verify the actual schema; do not assume a `baseMean` column exists.

**Precision decision:** source `dba.report()` leaves the 3.16.0 default `precision=2:3` in place. Thresholding exported rounded Fold/FDR values can change membership near a cutoff. **P:** for a future selection/export, request `precision=0` to retain full precision and keep rounded display tables separately. This changes reporting precision, not the peak caller or hypothesis test; the observed report invocation above remains the reconstruction.

**QC:** compare replicate count distributions, sample relationships, model warnings, normalization factors, tested region totals and the sign of a known contrast. Examine effect sizes alongside FDR; a low FDR is not an effect magnitude. A batch-confounded or underpowered experiment is not rescued by a different plotting threshold. **Output → next:** reports whose direction, tested universe and normalization are explicit.

## Stage 14 — Select regions with safe coordinates

**Purpose:** convert a statistical question into defined intervals for downstream motif/annotation queries. **L, CR-S09/10:** uses FDR < 0.05 and absolute log2-fold threshold 0.5849625 (log2 1.5). One set builder takes only negative significant changes and compares unions/shared intervals across contrasts or timepoints. Those sets are not biological-replicate consensus peaks.

**Coordinate contract:** source helpers copy `Start`/`End` or `start/end` directly from DiffBind CSV into BED. Verified DiffBind 3.16.0 defaults to a GRanges result; its CSV coordinates are one-based closed. BED is zero-based half-open, so a direct copy violates the boundary contract: convert start to start−1 and retain end. Verify the producer for each historical CSV before changing it; column capitalization alone does not prove coordinate origin. A one-base defect can affect sequence extraction and overlap without changing the upstream statistical model. Source `awk -F,` parsing also does not safely handle quoted CSV fields.

**P — configured, coordinate-explicit R teaching export** (not the existing helper). This presumes the stated column names and GRanges coordinate convention have been verified:

```r
report <- read.csv("reports/treated_vs_control.csv", stringsAsFactors = FALSE)
if (all(c("seqnames", "start", "end") %in% names(report))) {
  coords <- report[, c("seqnames", "start", "end")]
} else if (all(c("Chr", "Start", "End") %in% names(report))) {
  coords <- report[, c("Chr", "Start", "End")]
} else {
  stop("Unrecognized coordinate schema: inspect the producer")
}
names(coords) <- c("chr", "start", "end")
stopifnot(all(c("Fold", "FDR") %in% names(report)))
valid <- complete.cases(coords) & is.finite(report$Fold) & is.finite(report$FDR)
keep <- valid & report$FDR < 0.05 & abs(report$Fold) >= log2(1.5)
selected <- coords[keep, ]
stopifnot(all(is.finite(selected$start)), all(is.finite(selected$end)),
          all(selected$start >= 1), all(selected$end >= selected$start),
          all(selected$start == floor(selected$start)),
          all(selected$end == floor(selected$end)))
bed <- data.frame(chr = selected$chr, start = selected$start - 1L,
                  end = selected$end)
dir.create("regions", showWarnings = FALSE)
write.table(bed, "regions/differential.bed", sep = "\t", quote = FALSE,
            row.names = FALSE, col.names = FALSE)
```

Keep positive and negative changes separate when they answer different biological questions. Sort before interval merging. A merge/union changes boundaries and can combine multiple peaks; record this when selecting motif windows. Source set building includes a destructive output-directory rebuild; do not launch it without a separate reviewed execution plan. This tutorial does not reproduce that operation.

**QC/outputs:** BED files, original report row IDs, selection predicate, direction, count of retained regions, coordinate convention and conversion test. Use a known one-base toy locus to check overlap and sequence extraction. Empty sets are valid outcomes; do not force enrichment analysis. **Output → next:** coordinate-safe, explicitly selected region sets.

## Stage 15 — Motifs and genomic annotation

### Motif enrichment

**Scientific purpose:** ask whether sequences in selected regions contain motifs more often than an appropriate background. Enrichment suggests a sequence association; it does not prove direct binding by the motif's named factor.

**Inputs/environment:** approved BED intervals, genome resources matching the alignment assembly, [HOMER](../../software/homer.md); source requests 8 CPUs/32 GB/24 h. **L, CR-S10/11:**

```bash
mkdir -p motifs/preparsed
findMotifsGenome.pl regions/differential.bed hg38 motifs/differential \
  -size 200 -len 8 -preparsedDir motifs/preparsed
```

The source requests a 200 bp analysis window and 8-base motif search length. These choices may suit focal sites differently from broad domains. It does not specify a custom matched background with `-bg`. **P:** review GC/length/accessible-region matching, target class, window placement and multiple-testing interpretation before selecting background parameters. Do not assume an entire broad domain is analyzed just because its BED interval is wide.

**How enrichment works:** observed motif occurrences in foreground sequences are compared with a background sequence distribution. Foreground selection, window size, GC/repeat composition and background definition can create or remove apparent enrichment. A factor-associated motif may belong to a partner or another protein with a similar sequence preference. In a BCOR-associated occupancy experiment, motif enrichment is particularly a hypothesis about recruitment/partners, not evidence of a BCOR DNA-binding motif. Keep motif association separate from target specificity and functional regulation.

**Outputs/QC:** HOMER enrichment tables, HTML, known/de novo motifs and sequence/background summaries as provided by the installed release. Check number of valid sequences, reference consistency, background composition, low-complexity artifacts and whether results persist across reasonable window/background choices. HOMER's upstream web manual was unavailable during this review; the source invocation is confirmed, runtime/version-specific output behavior remains untested.

### Genomic annotation

**L, CR-S12:**

```bash
mkdir -p annotations
annotatePeaks.pl regions/differential.bed hg38 -size given \
  -annStats annotations/differential.stats.tsv \
  > annotations/differential.annotated.tsv
```

`-size given` requests the supplied intervals. Save the HOMER genome/annotation resource version. **Outputs:** annotated interval table and annotation statistics, followed by custom R summary bar plots. **QC:** inspect chromosome and gene identifiers, promoter definition, ambiguous/overlapping gene assignments and annotation category denominators. A nearest-gene label is a hypothesis, not an experimentally established enhancer–gene connection. **Output → next:** explicitly qualified sequence and genomic context, not automatic causal interpretation.

## Stage 16 — Figures that preserve the measurement

### Sample PCA and MA plots

**L, CR-S05:** a shared pre-branch matrix is transformed with `log2(x+1)`, zero-variance rows removed, and `prcomp(t(...), scale=TRUE)` used for sample PCA. Unit-variance feature scaling weights regions differently from an unscaled or variance-stabilized PCA. Because the matrix is exported before branch normalization, do not label this “spike-normalized PCA” solely from its location. The historical BigWig PCA in Chapter 3 measures something different again.

**L, CR-S13/14:** the separate MA helper supports two coordinate modes:

| Mode | x and y coordinates | Review requirement |
|---|---|---|
| `fold_baseMean` | Reported `Fold` versus `baseMean`, otherwise `2^Conc`, then a geometric concentration fallback | Label the abundance source; its final rank fallback is not measured abundance |
| `conc_derived` | `M = Conc_left − Conc_right`; `A = 2^((Conc_left + Conc_right)/2)` | Concentration-derived M need not equal model-reported Fold |

Both modes color by reported Fold/FDR with defaults FDR 0.05 and absolute log2-fold 0.584963. Model-based effects, concentration differences and their shrinkage/normalization can differ. Inspect the selected mode and sign before interpreting points. [R plotting libraries](../../software/r-plotting.md) and [Python figure helpers](../../software/python-figures.md) support rendering; figure composition is not another statistical test.

### Region heatmaps and profiles

**Historical reconstruction, CR-S16:** center-aligned ±2 kb windows, 10 bp bins, and missing values replaced by zero. The following assumes `regions/reviewed_peaks.bed` is an approved fixed region set and `tracks/means/treated.mean.CPM.bw` was created as in Chapter 3. The processor count is reduced for the teaching example.

```bash
mkdir -p figures
computeMatrix reference-point --referencePoint center -b 2000 -a 2000 \
  -R regions/reviewed_peaks.bed \
  -S tracks/means/control.mean.CPM.bw tracks/means/treated.mean.CPM.bw \
  --binSize 10 --missingDataAsZero -p 4 -o figures/region_matrix.gz
plotHeatmap -m figures/region_matrix.gz -out figures/region_heatmap.pdf \
  --colorMap RdYlBu_r --sortRegions descend --dpi 300
plotProfile -m figures/region_matrix.gz -out figures/region_profile.pdf
```

**Scientific interpretation:** interval centers are not automatically binding summits or transcription start sites. Missing reference coverage is not necessarily biological zero; `--missingDataAsZero` is an explicit assumption. Use the same regions, row order and meaningful shared color ranges for condition comparisons, and inspect individual replicates alongside means. Do not hide stderr as some historical plotting wrappers do.

**Outputs/QC:** matrix, heatmap, profile, MA plots and PCA with sample identities/normalization/units in captions. Confirm region counts, selected order and axis labels. Browser views should use a matching genome and comparable y-axis ranges. **Final output:** a figure-supported interpretation that distinguishes occupancy evidence, statistical uncertainty, motif association and gene-assignment hypotheses. Review the [open decisions](decisions.md) before treating this draft as an accepted analysis protocol.
