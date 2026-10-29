# Scientific decisions and uncertainty log

**Status: open review log, 2026-10-29.** No entry below is a completed scientific validation. **L/E/P/U** have the meanings defined in the [tutorial overview](index.md). Source IDs refer to the [registry](sources.md). Maintainers should record reviewer, evidence and date when resolving an entry.

## D01 — Select the reconstruction baseline

**L:** supervisor and monitor select the same core workers, and the R wrapper selects the full standard/spike analysis (CR-S04/07/08). **U:** no signed authoritative-version record. **P:** retain this call-graph baseline and ask the workflow maintainer to accept or revise it; modification dates alone are insufficient.

## D02 — Sample completeness and design

**L:** source names infer conditions/replicates; coverage discovers completed BAM subsets (CR-S02/06). **U:** whether all intended replicates and correct controls reach every stage. **P:** explicit manifest, preflight all samples, distinguish biological baseline, IgG and calibrator; model donor/batch where appropriate. Resolution requires a reviewed design and complete expected-output checklist.

## D03 — Adapter and short-read policy

**L:** paired adapter `AGATCGGAAGAG`, `-m 15 -q 20 -z`; logged Cutadapt 5.1 (CR-S01/L01). **E:** `-z` means zero-cap in that release. **U:** chemistry-specific correctness. **P:** confirm facility specification, compare trimming yield and fragment classes; avoid a blanket short-fragment exclusion.

## D04 — Paired-end alignment and MAPQ

**L:** no-mixed/no-discordant and MAPQ ≥30; no explicit dovetail/sensitivity/insert bounds or complete-pair enforcement. **E:** nf-core 3.2.2 explicitly differs ([comparison](methods-comparison.md)). **U:** retained pair completeness and lost short inserts. **P:** versioned pair policy and synthetic/real fragment audit before changing flags.

## D05 — Reference and mitochondrial identity

**L:** hg38–sacCer3 label and BED human extraction; no explicit mito exclusion. **U:** exact FASTAs, contig whitelist, blacklist revision and annotation release. **P:** checksummed reference manifest, unique species names and explicit chrM policy for counts, tracks and peaks.

## D06 — Duplicates across products

**L:** tracks/BAMs retain duplicates, selected MACS2 uses `auto`, historical broad uses `all`, DiffBind removes duplicates at count time. **U:** technical versus biological duplication and effects on global comparisons. **P:** review library complexity and antibody target; state the unit/policy separately for each artifact rather than calling the workflow uniformly deduplicated.

## D07 — Calibration protocol

**L:** code expects yeast-associated counts; experimental addition/recovery details are absent. **U:** deliberate spike material, dose, stage of addition, cell-number and recovery assumptions. **P:** obtain protocol evidence before accepting quantitative global occupancy claims. Bacterial carryover recommendations do not automatically apply to yeast.

## D08 — Species counts, cohort and scale factors

**L:** loose regex can match human chrX/chrM; column 3 of idxstats counts mapped segments; cached median/subset discovery can change or stale the cohort (CR-S01/02). **Confirmed code defect:** species expression is not specific. **P:** exact species membership, complete-cohort recomputation, positive-factor checks, and fragment-unit review. **U:** effect on any actual dataset remains unassessed. See the [synthetic demonstration](03-normalization-and-qc.md#confirmed-defect-in-the-observed-expression).

## D09 — Coverage representation

**L:** spike BigWigs from combined BAM, CPM from human BAM, 10 bp bins, no explicit extension. **U:** intended coverage unit and artifact/mito contributions. **P:** compare a human-only spike track and explicit fragment extension with the historical result; record changed inputs/options and units.

## D10 — Peak model and background

**L:** narrow MACS2 BAMPE q 0.001 without control; historical broad q 0.05/broad cutoff 0.1 and alternative dual calling. **U:** target-specific choice and suitable IgG usage. **P:** review focal versus domain-like enrichment, controls, duplicate choice and candidate SEACR outputs using an agreed evaluation set. Broad outputs need compatible downstream import.

## D11 — Blacklist and empty filtered peaks

**L:** selected peak-only filtering is optional and falls back to raw if empty; alternative worker filters alignments; statistical branches differ in mask settings. **U:** consistent tested universe. **P:** require assembly-matched masks, record removed intervals and stop for review on empty filtered results. No automatic raw fallback in a future implementation.

## D12 — QC units and acceptance criteria

**L:** selected FRiP is any-overlap read-segment FRiP; no validated universal cutoff. **U:** target-specific background/enrichment criteria. **P:** record exact numerator/denominator, complete pairs and fragment distributions; review controls and known loci. Do not compare to fragment FRiP thresholds without harmonization.

## D13 — Replicate reproducibility and averages

**L:** historical bin PCA/correlation, equal all-replicate mean in selected average worker, possible unequal nested historical means; shared contrast sets are not replicate consensus. **U:** accepted support/overlap criterion and exclusion policy. **P:** assess individual replicates, define reproducible regions by target, and retain group membership/weights. Means are visualization summaries only.

## D14 — DiffBind defaults, factors and design

**L:** duplicate-removing summarizeOverlaps count path, unspecified count defaults; custom numeric `S/median(S)` normalization; standard default masks versus spike masks disabled. **E:** numeric vector interface is supported. **U:** actual counted intervals, applied normalization denominators and design adequacy. **P:** capture installed defaults, retrieve normalization state, fix a common interval universe for comparison, and test factor/sample ordering and global changes in a designed toy dataset.

## D15 — Contrast orientation and missing reports

**L:** configured numerator/denominator matched with `bFlip`; zero default-significant sites can skip even `th=1` output. **U:** accepted positive/negative biological meaning. **P:** known-direction toy test, explicit contrast table and status per expected contrast; a missing CSV must not imply no binding.

## D16 — Coordinates, set definitions and motifs

**L:** source copies DiffBind Start/End directly to BED, merges cross-contrast sets, motif windows 200 bp/length 8, no explicit custom background. **U:** coordinate export contract, valid motif background and target-specific window. **P:** test one-base conversion, robust CSV parsing, preserve original interval IDs and assess matched background; distinguish annotation from causal gene assignment.

## D17 — Figures and provenance

**L:** common pre-branch PCA, two MA coordinate modes, rank fallback for missing abundance and center heatmaps with missing-as-zero. **U:** how existing figures were labeled and interpreted. **P:** expose actual matrix/units/coordinates in captions, reject rank-as-abundance labeling, use fixed regions/shared scales, retain replicate views. Figure-library versions and annotation resources remain unrecorded.

## D18 — Scheduler, restarts and exit status

**L:** `afterany`, existence-based skipping, coverage subset discovery, cached median, and a post-increment under `set -e` (CR-S01/02/07/08). **U:** which failed/partial executions were later resumed; no private-run outcome is inferred. **P:** future success-based dependencies, content-aware completion records and safe arithmetic. A per-job `/tmp` lock does not serialize different jobs writing common tables. Do not run original automation to resolve this documentation question.

## D19 — Version and installation reproducibility

**L:** explicit logged Cutadapt/Python and R/DiffBind versions, otherwise environment labels. **U:** full executed dependencies, platform availability and package solver compatibility. **P:** test candidate environments on approved Linux/macOS/WSL2 systems and export reviewed locks; never infer versions from current documentation.

## D20 — Publication and execution readiness

**L:** private sources remain private; public text uses generic examples and source IDs. **U:** owner scientific acceptance and a permitted teaching dataset. **P:** independent scientific review, rights/license decision, security review of future artifacts, then bounded execution before automation. Current checks cover documentation and syntax only ([validation](validation.md)).
