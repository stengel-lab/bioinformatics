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

`bRemoveDuplicates=TRUE` changes count handling relative to BAMs/tracks that retain duplicates and MACS2's `auto` policy. The source does not explicitly set consensus `minOverlap`, summit recentering, count filters or a batch-aware design. Record the installed defaults and actual counted regions before calling the analysis reproducible. Counting can alter interval widths relative to raw peaks; inspect the returned ranges.

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

The positivity guards are proposed teaching safeguards. **E:** numeric normalization vectors are supported by DiffBind's normalization interface ([manual](https://bioconductor.org/packages/release/bioc/manuals/DiffBind/man/DiffBind.pdf), [release-family source](https://raw.githubusercontent.com/bioc/DiffBind/RELEASE_3_20/R/normalize.R)). This does not prove the source's factor ordering or resulting model denominators. Retrieve and inspect the installed implementation's normalization state and verify with a small designed dataset before relying on biological fold changes.

**Important confound:** the standard branch leaves blacklist behavior at defaults, while the spike branch explicitly disables blacklist and greylist application. Different tested interval universes can produce different results independently of normalization. Compare common regions with consistent approved masks in a future controlled exercise; do not silently change history.

### Reports and sign

**L:** after matching configured contrasts, reporting uses `dba.report(..., th=1, bFlip=NeedsFlip)`. However, an earlier significance-count precheck can skip a contrast with zero default-significant sites. Thus `th=1` does **not** guarantee an all-sites CSV for every contrast. Check statuses including `generated`, `no_differential_sites` and `report_failed` in `contrast_summary.csv`; a missing file does not mean there are no bound regions.

The selected script saves per-branch reports, `dba_analysis.RData`, summary/status files and debug information, plus a combined summary. Typical report fields include coordinates, `Fold`, `FDR`, `Conc` and group concentrations; verify columns in the actual installed version. Do not assume a `baseMean` column exists.

**QC:** compare replicate count distributions, sample relationships, model warnings, normalization factors, tested region totals and the sign of a known contrast. Examine effect sizes alongside FDR; a low FDR is not an effect magnitude. A batch-confounded or underpowered experiment is not rescued by a different plotting threshold. **Output → next:** reports whose direction, tested universe and normalization are explicit.

## Stage 14 — Select regions with safe coordinates

**Purpose:** convert a statistical question into defined intervals for downstream motif/annotation queries. **L, CR-S09/10:** uses FDR < 0.05 and absolute log2-fold threshold 0.5849625 (log2 1.5). One set builder takes only negative significant changes and compares unions/shared intervals across contrasts or timepoints. Those sets are not biological-replicate consensus peaks.

**Coordinate review gate:** source helpers copy `Start`/`End` directly from DiffBind CSV into BED. DiffBind/GRanges ranges are generally one-based closed; BED is zero-based half-open. Confirm the exporter contract. If coordinates are GRanges-style, subtract one from start and retain end. A one-base error can affect sequence extraction and overlap. Source `awk -F,` parsing also does not safely handle quoted CSV fields.

**P — configured, coordinate-explicit R teaching export** (not the existing helper). This presumes the stated column names and GRanges coordinate convention have been verified:

```r
report <- read.csv("reports/treated_vs_control.csv", stringsAsFactors = FALSE)
needed <- c("Chr", "Start", "End", "Fold", "FDR")
stopifnot(all(needed %in% names(report)))
keep <- complete.cases(report[, needed]) & report$FDR < 0.05 &
        abs(report$Fold) > log2(1.5)
selected <- report[keep, ]
stopifnot(all(selected$Start >= 1), all(selected$End >= selected$Start))
bed <- data.frame(chr = selected$Chr, start = selected$Start - 1L,
                  end = selected$End)
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
