# Scientific decisions and uncertainty log

**Scientific review: 2026-10-30; baseline `82bd4ec`.** This expands the original 20 entries. Source IDs and line ranges resolve through the [registry](sources.md) and private provenance map. Read the [concise review summary](scientific-review.md) first, or the [reference/count audit](reference-audit.md) for the normalization trace.

**Classification** separates demonstrable defects, methodological choices and missing information; an entry may contain more than one. **Recommended default** is scoped to reconstruction, validation or a proposed comparison. It is not a silently applied change to the lab workflow. External methods supply evidence, not automatic authority. **Historical impact** is conditional unless a complete run-to-input-to-output chain was established. No historical biological result was proven wrong in this review.

The reviewed upstream DiffBind snapshot has DESCRIPTION version **3.16.0**, matching the recorded package version; its [immutable commit](https://github.com/bioc/DiffBind/tree/da0b0442311f6264ac8a14eff80dbf9dcc97f614) supports API-level conclusions. The installed dependency state and realized historical objects still require separate verification.

## D01 — Select the reconstruction baseline

**Classification:** Missing authority/run provenance; choosing a baseline is a documentation choice.

**Observed lab behavior:** CR-S07:64–82 and CR-S08:881–988 select CR-S01, CR-S02 and CR-S04; CR-S04:89 selects CR-S05. Downstream figure workers are separate entry points. Filename dates do not establish that a particular script revision ran.

**Why it matters:** A correct description of an unused revision cannot establish the method behind an older figure. Source intent, recorded invocation, completed output and scientific acceptance are different evidence levels.

**Established methods / references:** The versioned [nf-core release](https://github.com/nf-core/cutandrun/releases/tag/3.2.2) illustrates an identifiable implementation, not authority to replace lab choices.

**Recommended default:** Use the call-graph baseline for teaching; label alternatives explicitly. Require an immutable script/environment/reference record when attributing a historical run.

**Immediate correction versus lab review:** Correct the evidence labels now. Lab maintainer acceptance of an authoritative method and attribution of old runs remain open.

**Potential historical impact:** No result is invalidated by a documentation-baseline choice. Re-evaluation is warranted only after connecting an affected implementation to the specific result.


## D02 — Sample completeness and design

**Classification:** Method/design choice plus missing metadata; silent subset acceptance is a reliability defect.

**Observed lab behavior:** CR-S02:58–76 accepts samples with two existing BAMs, not necessarily the entire sample list. CR-S06 infers metadata from names. CR-S05:193–196 normalizes hyphens to underscores and later matches IDs; it rejects duplicate normalized spike-table IDs but does not establish a complete experimental design.

**Why it matters:** Missing or misclassified replicates alter precision, contrast eligibility and cohort composition. A biological baseline target-IP, IgG background and calibration material have different roles. Name normalization can collapse distinct identifiers.

**Established methods / references:** The [DESeq2 design guidance](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html) requires a model that represents the experiment; design rank and confounding matter.

**Recommended default:** Use an explicit manifest with unique IDs, antibody, condition, biological replicate, batch/donor and control roles. Require a one-to-one match to expected samples before accepting a cohort.

**Immediate correction versus lab review:** Explain the missing checks now; lab review must establish intended samples, exclusions and design. No automatic replicate removal or new model was applied.

**Potential historical impact:** Potentially all affected count contrasts and condition means if libraries were omitted, mislabeled or confounded. No such sample error was confirmed in this review.


## D03 — Adapter and short-read policy

**Classification:** Method choice; adapter chemistry is missing information. Misdescribing `-z` would be a documentation error.

**Observed lab behavior:** CR-S01:44–50,158–180 uses paired AGATCGGAAGAG adapters, minimum read length 15, quality threshold 20 and `-z`. CR-L01 records Cutadapt 5.1/Python 3.11.9.

**Why it matters:** Short CUT&RUN inserts can cause adapter read-through. Excess trimming loses biological sequence; insufficient trimming harms alignment. Minimum retained read length is not minimum paired-fragment length.

**Established methods / references:** The [Cutadapt guide](https://cutadapt.readthedocs.io/en/stable/guide.html) describes paired filtering. The [5.1 CLI](https://raw.githubusercontent.com/marcelm/cutadapt/v5.1/src/cutadapt/cli.py) defines `-z` as zero-cap; output gzip follows the filename suffix.

**Recommended default:** Retain the observed command as the reconstruction default; verify library adapters and review retained read/fragment distributions before changing it. Do not apply a blanket short-fragment exclusion.

**Immediate correction versus lab review:** Clarify algorithm/flags now. Library chemistry, loss tolerances and alternative adapter rules require protocol evidence.

**Potential historical impact:** A different trimming rule can propagate to mapping, peaks and counts. No library-specific adapter mismatch or historical trimming damage was established.


## D04 — Paired-end alignment and MAPQ

**Classification:** Method choice with incomplete version/default information; per-record filtering is not itself a bug.

**Observed lab behavior:** CR-S01:193–204 maps with no-mixed/no-discordant, then filters each alignment at MAPQ ≥30 and excludes unmapped records. Sensitivity, local/end-to-end mode, insert bounds and dovetailing are not explicitly configured. There is no complete-mate post-filter check.

**Why it matters:** MAPQ describes alignment ambiguity under the aligner model, not a literal probability of species identity. One mate can fail MAPQ while the other survives. Short-insert geometry affects valid CUT&RUN fragment retention.

**Established methods / references:** The [Bowtie2 manual](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml) defines pair geometry. The [nf-core configuration](https://raw.githubusercontent.com/nf-core/cutandrun/3.2.2/conf/modules.config) makes different host/spike choices; this is a comparator, not a mandatory replacement.

**Recommended default:** Keep MAPQ 30 and observed geometry in the baseline. Record aligner version and assess complete pairs/short inserts before approving any changed flags.

**Immediate correction versus lab review:** Improve the explanation immediately. Pair eligibility, dovetail policy and MAPQ alternatives require a target/reference comparison approved by the lab.

**Potential historical impact:** Potential changes to short-fragment sensitivity, species assignment, paired counting and FRiP. No measured loss rate or historical misalignment is claimed.


## D05 — Reference and mitochondrial identity

**Classification:** Missing reference construction/assets; mitochondrial inclusion is a scientific choice.

**Observed lab behavior:** CR-S01 names an hg38–sacCer3 index and human BED. No build command, index files or matching reference manifest was recovered in the reviewed corpus. The available genes BED is not evidence of the actual human-contig whitelist. No explicit mitochondrial removal is present.

**Why it matters:** Assembly names alone do not specify alternate contigs, naming, masking or sequence identity. Host/yeast collisions can make species assignment ambiguous. Mitochondrial signal can alter library denominators without measuring nuclear occupancy.

**Established methods / references:** [Bowtie2 inspection](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#the-bowtie2-inspect-index-inspector) exposes index names; [SAMtools idxstats](https://www.htslib.org/doc/samtools-idxstats.html) exposes contig lengths and counts. Neither assigns species biologically.

**Recommended default:** Require a checksummed reference manifest and exact contig-role map; retain baseline mitochondrial behavior while reporting the fraction and evaluating a nuclear-only sensitivity view. No universal mito cutoff is supported here.

**Immediate correction versus lab review:** State the missing construction evidence now. The lab/reference custodian must supply the actual FASTAs/index dictionary/whitelist and choose mitochondrial policy.

**Potential historical impact:** Reference mismatch could affect every coordinate-based artifact; name-dependent spike contamination is conditional on the actual dictionary. It has not been verified against historical index files.


## D06 — Duplicates across products

**Classification:** Scientific choice plus a confirmed documentation overstatement about count deduplication; absent marking is missing evidence, not proof that removal is the desired method.

**Observed lab behavior:** CR-S01 has no mark/remove-duplicates stage; BAMs and CR-S02 tracks retain records. MACS2 uses `auto`; CR-S17 broad calling uses `all`. CR-S05:178 sets `bRemoveDuplicates=TRUE` with summarizeOverlaps. In DiffBind 3.16.0 the final overlap-count pass excludes duplicate-flagged records rather than discovering unmarked coordinate duplicates; default summit estimation also uses a preliminary built-in pass.

**Why it matters:** Repeated fragments may reflect PCR amplification or genuine concentrated cleavage. A duplicate flag, coordinate duplication, molecular duplication and library complexity are distinct. If freshly mapped BAMs are unmarked, the DiffBind switch alone does not make counts deduplicated.

**Established methods / references:** DiffBind’s [3.16.0 counting implementation](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/counts.R#L645-L679) uses a ScanBam duplicate flag. [nf-core usage](https://nf-co.re/cutandrun/3.2.2/docs/usage) demonstrates a different control/target policy.

**Recommended default:** Document each product separately and preserve original BAMs. Assess flagged versus repeated-coordinate fragments and library complexity before choosing retention/removal; do not prescribe one universal policy.

**Immediate correction versus lab review:** Correct “DiffBind removes duplicates” to the qualified final-pass flag policy now; do not claim every internal pass is identical. Lab approval is needed for a marking strategy and whether target/control products should exclude duplicates.

**Potential historical impact:** Potential effect on peaks and counts if an intended deduplication step was absent, or on comparisons of products with different policies. Historical flags/complexity were not measured.


## D07 — Calibration protocol

**Classification:** Missing experimental information; choice of calibrator and interpretation is methodological.

**Observed lab behavior:** CR-S01/02/05 expect yeast-associated counts, but the source does not establish spike amount, addition stage, cell equivalence or species identity. A reference label is not a protocol record.

**Why it matters:** Calibration only corrects variation introduced after the material enters the measurement chain, subject to matched recovery assumptions. DNA added after digestion cannot automatically calibrate upstream cleavage/cell-input variation.

**Established methods / references:** [Skene and Henikoff](https://elifesciences.org/articles/21856) and [Meers et al.](https://elifesciences.org/articles/46314) describe protocol-specific calibration approaches. Bacterial carryover and deliberate yeast additions are not interchangeable.

**Recommended default:** Keep spike-based global occupancy claims pending until the calibration protocol is recovered. Standard-depth tracks may be shown with the explicit limitation that global changes can be obscured.

**Immediate correction versus lab review:** Teach the assumptions immediately. Wet-lab review must establish material, amount, timing, antibody relationship and cell-input rationale before accepting calibration.

**Potential historical impact:** Potentially all quantitative spike-scaled comparisons, even with perfectly counted species. No historical calibration failure has been demonstrated.


## D08 — Species counts, cohort and scale factors

**Classification:** Confirmed nonspecific-regex defect under matching host names; cache/cohort omissions are reliability defects; actual reference and historical exposure remain unconfirmed.

**Observed lab behavior:** CR-S01:301–303 sums idxstats column 3 using a regex also matching host chrX/chrM. CR-S02:94–125 can cache counts/median, while 154–169 recounts for track factors. CR-S05:466–550 reads that table, matches sample order and passes S/median(S) to normalization.

**Why it matters:** Sample-dependent host contamination changes relative factors. A shared positive median alone changes the common scale, not within-cohort ratios; mixing old/new tracks or stale per-sample counts is more serious. Counts are mapped segments, not fragments.

**Established methods / references:** [idxstats semantics](https://www.htslib.org/doc/samtools-idxstats.html) and [DiffBind normalization](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/normalize.R) support explicit units and factor inspection. See the [reference audit](reference-audit.md).

**Recommended default:** Count by exact, complete reference roles and verify lengths; reject unclassified/missing/duplicate contigs. Recompute a complete cohort consistently and reject nonpositive/nonfinite factors before modeling. The teaching counter does not establish calibration validity.

**Immediate correction versus lab review:** Correct documentation and provide a synthetic-tested reference-aware example now. Applying revised counts to lab results requires the actual reference and run attribution, then lab review.

**Potential historical impact:** Selected code routes these counts into spike BigWigs and the spike model; it does not directly rescale CPM tracks or MACS2 peaks. Saved R logs prove factor use, not regex derivation. No historical contamination is confirmed.


## D09 — Coverage representation

**Classification:** Method/visualization choice, not a demonstrated caller or normalization bug.

**Observed lab behavior:** CR-S02 uses 10 bp bins, combined BAM for spike-scaled coverage, human BAM for CPM, no explicit extension, duplicate/mito/blacklist options at this stage. The effective-genome argument does not change None/CPM into RPGC.

**Why it matters:** Read-covered bases, extended paired fragments and fragment centers measure different geometries. CPM constrains depth; external scaling is a multiplication. Host and yeast contigs in one BigWig complicate browser compatibility.

**Established methods / references:** The [bamCoverage manual](https://deeptools.readthedocs.io/en/develop/content/tools/bamCoverage.html) distinguishes extension and normalization modes. The [nf-core schema](https://raw.githubusercontent.com/nf-core/cutandrun/3.2.2/nextflow_schema.json) exposes a different extension default.

**Recommended default:** Preserve/label baseline tracks and units. For a proposed nuclear occupancy display, compare an explicitly human-only, reviewed fragment-coverage track with the original; do not silently replace it.

**Immediate correction versus lab review:** Explain geometry now. Choosing extension, nuclear contigs and final displayed normalization requires lab agreement on the measurement.

**Potential historical impact:** May affect visual peak shape, heatmaps, profile amplitude and track correlations. It does not by itself change BAM counts in a separately run DiffBind model.


## D10 — Peak model and background

**Classification:** Scientific choice; narrow q 0.001 without a control is supported syntax, not automatically a bug.

**Observed lab behavior:** CR-S01:228–235 uses MACS2 BAMPE narrow, `keep-dup auto`, q 0.001, no `-c`. CR-S17 broad uses q 0.05, broad cutoff 0.1, keep all duplicates; CR-S18 is another target-aware alternative. A saved command log confirms the narrow/no-control option pattern, not every later stage.

**Why it matters:** Narrow calling finds focal enrichment; broad calling joins enriched cores through weaker regions. Statistical stringency cannot replace antibody specificity, appropriate background controls or reproducibility. BCOR occupancy is not equivalent to a broad histone modification.

**Established methods / references:** [MACS2 calling source](https://github.com/macs3-project/MACS/blob/v2.2.9.1/MACS2/callpeak_cmd.py), the [SEACR method](https://link.springer.com/article/10.1186/s13072-019-0287-4), and [BCOR/PRC1.1 primary work](https://www.nature.com/articles/s41467-019-09250-6) motivate target-dependent evaluation, not a universal caller.

**Recommended default:** Retain narrow q 0.001 as the lab reconstruction. For focal TF/BCOR-associated enrichment, begin the comparison with narrow calling; for demonstrably broad histone domains, evaluate a broad/domain method. Use appropriate negative controls and independent replicate support; no universal new q-value is approved.

**Immediate correction versus lab review:** Add model/target/control teaching now. Lab approval is needed for target-specific caller, cutoff, control pairing and broad-aware count intervals.

**Potential historical impact:** Can change region discovery, FRiP, consensus/count universe and downstream motifs. Lack of `-c` alone does not establish false peaks or invalidate historical results.


## D11 — Blacklist and empty filtered peaks

**Classification:** Mask selection is methodological; the empty-filtered producer/consumer disagreement is a demonstrable conditional contract defect.

**Observed lab behavior:** CR-S01:244–279 filters peaks only if resources exist and falls back to raw peaks when the filtered set is empty. CR-S06 predicts the filtered filename. CR-S05 standard uses default analysis masks; spike explicitly disables them. These are different filtering levels.

**Why it matters:** Artifact regions can dominate enrichment, tracks or contrasts. Raw fallback can reintroduce every rejected region, while a downstream reader receives an empty filtered file. A successful file-existence check does not resolve that disagreement.

**Established methods / references:** The [ENCODE blacklist paper](https://www.nature.com/articles/s41598-019-45839-z) explains recurrent artifacts. CUT&RUN-specific suspect-region work is discussed in the [review summary](scientific-review.md#scientific-choices-requiring-lab-approval).

**Recommended default:** Require an assembly-matched mask and an explicit empty-set status; never automatically label raw fallback as blacklist-filtered. Compare normalization branches on a common approved interval universe.

**Immediate correction versus lab review:** Explain/fix tutorial contracts now; source remediation is proposed only. The exact mask, suspect-list handling and consistent model filtering require lab approval.

**Potential historical impact:** Potentially affected peaks, FRiP and differential regions if fallback/mask differences occurred. Region removal lists and corresponding historical outputs were not available to establish individual effects.


## D12 — QC units and acceptance criteria

**Classification:** Metric definition and acceptance criteria are choices; a zero-denominator case is an arithmetic failure mode.

**Observed lab behavior:** CR-S01:282–290 counts any-overlap human BAM records in peaks divided by total human BAM records, without a source zero guard. It is not a complete-pair fragment FRiP. The selected peaks derive from the same sample.

**Why it matters:** FRiP changes with caller, region width, filtering and numerator/denominator unit. Broad regions often capture more reads without implying a better experiment. A zero library makes the ratio undefined.

**Established methods / references:** [BEDTools intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html) defines record overlap; [nf-core outputs](https://nf-co.re/cutandrun/3.2.2/docs/output) describe a different fragment metric.

**Recommended default:** Keep the label “alignment/read-segment FRiP,” retain numerator and denominator and reject division by zero. Review target-specific enrichment jointly with controls, fragment distribution and replication; no universal FRiP cutoff is justified.

**Immediate correction versus lab review:** Correct units and show the zero guard now. Lab review must set any acceptance threshold and decide whether to add a fragment-based metric.

**Potential historical impact:** Could change QC rankings or exclusion decisions when metrics were mislabeled/compared across definitions. No historical sample should be rejected from this documentation alone.


## D13 — Replicate reproducibility and averages

**Classification:** Scientific consensus rule plus missing review evidence; unequal nested means are an aggregation issue if equal weights were intended.

**Observed lab behavior:** CR-S03 means all matched tracks equally; CR-S16 can nest pairwise means. CR-S15 uses binned track PCA/correlation. CR-S09 shares contrasts, not biological replicates. DiffBind 3.16.0 implicitly requires peaks in two input peaksets when `minOverlap` is not set; that is not necessarily within-condition replicate support.

**Why it matters:** High global correlations can be driven by background; pooling loses biological variation. Reproducibility of interval discovery is distinct from modeled count differences. With three tracks, nested means can weight 1/4,1/4,1/2.

**Established methods / references:** [WiggleTools](https://github.com/Ensembl/WiggleTools) documents arithmetic, and [DiffBind counting defaults](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/man/dba.count.Rd) define the input-peakset criterion. A pipeline consensus default is not scientific acceptance.

**Recommended default:** Review individual replicates; use an explicit equal-weight mean for display. For high-confidence peak claims with ≥2 biological replicates, seek support in ≥2 within a condition, with target-appropriate overlap. Keep exploratory unions separate; do not silently apply a new count-universe filter.

**Immediate correction versus lab review:** Explain defaults/weighting now. The lab must approve overlap geometry, replicate exclusions and whether IDR or another concordance rule suits the target.

**Potential historical impact:** Potential differences in historical mean plots and region sets; equal-weight intent or a particular affected figure has not been established. No replicate is automatically excluded.


## D14 — DiffBind defaults, factors and design

**Classification:** Mostly methodological choices and missing realized state; numeric-factor support and inverse direction are not bugs.

**Observed lab behavior:** CR-S05:174–191 uses narrow import and summarizeOverlaps counting. In verified 3.16.0 source the unmodified defaults include `minOverlap=2`, `summits=200`, `filter=1`. CR-S05:510–550 matches sample IDs, supplies S/median(S), retrieves normalization diagnostics, and disables masks only in the spike branch.

**Why it matters:** Default recentering can produce 401 bp counted windows rather than original broad/narrow widths. Overlap counting/pair eligibility changes measurements. Conditions/categories do not prove that batch, donor or target confounding is modeled.

**Established methods / references:** Verified [3.16.0 API](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/DBA.R), [normalization source](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/normalize.R), and [DESeq2 adapter](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/analyze_deseq2.R) show numeric factors passed directly to DESeq2 size factors in the design-based path; `library=FULL` does not automatically multiply them by library depth.

**Recommended default:** Preserve the accepted API direction S/median(S); reject invalid factors. Capture actual design, sample order, counted ranges, defaults and pre/post-analysis normalization. Use a common approved universe when comparing normalization branches.

**Immediate correction versus lab review:** Correct API/default explanations now. Do not “fix” the numeric interface or invert the vector. Lab approval remains necessary for design, interval widths, count filters and masks; fitting/biological validation was not performed.

**Potential historical impact:** Wrong counts/calibration/masks/design could change inference; the mere use of a numeric vector or `FULL` is not evidence of a historical error. An implicit 401 bp universe needs review before interpreting domain-wide changes.


## D15 — Contrast orientation and missing reports

**Classification:** Orientation is statically consistent with the API; report suppression is a reporting choice that conflicts with an all-sites expectation.

**Observed lab behavior:** CR-S05:286–325 flips when Group is denominator and Group2 is numerator. Report `bFlip` is then used at 368. Lines 362–365 skip CSV when the default-significant count is zero despite a subsequent `th=1` request.

**Why it matters:** A reversed effect sign reverses gain/loss conclusions. Absence of a CSV is not absence of binding, nor a statement that no regions were eligible for testing.

**Established methods / references:** The [3.16.0 report contract](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/man/dba.report.Rd) defines positive Fold as greater group-1 binding and `bFlip` as swapping groups. The source mapper is consistent with positive configured-numerator enrichment.

**Recommended default:** State positive = numerator-enriched; require explicit numerator/denominator and a known-direction toy verification before interpreting a new model. For a future all-sites export, emit every analyzed contrast with status, including zero-significant cases.

**Immediate correction versus lab review:** Correct the explanation now: no static sign bug was found. Lab review confirms intended biological comparison; source export behavior needs an explicit report contract before change.

**Potential historical impact:** Misinterpreted sign or skipped CSV could mislead downstream selection. No actual reversed contrast or missing-result conclusion was established.


## D16 — Coordinates, set definitions and motifs

**Classification:** Confirmed boundary-conversion defect for GRanges-derived CSV; set definitions/motif background are scientific choices. Rounded-report thresholding is another export concern.

**Observed lab behavior:** CR-S05 exports `dba.report()` objects without explicit DataType/precision. DiffBind 3.16.0 defaults to GRanges and report precision 2:3. CR-S09/10 copy Start/End or start/end directly into BED without origin conversion. CR-S09 selects negative changes with FDR<0.05 and |Fold|≥log2(1.5); motif helpers have their own strict thresholds/windows.

**Why it matters:** GRanges is one-based closed; BED is zero-based half-open. Direct copying shortens/shifts the represented interval by one base. Thresholding rounded Fold/FDR can change boundary membership. Cross-contrast intersections are not replicate consensus, and motif background affects enrichment.

**Established methods / references:** The [UCSC BED contract](https://genome.ucsc.edu/FAQ/FAQformat.html#format1), [DiffBind range conversion](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/utils.R) and [report API](https://github.com/bioc/DiffBind/blob/da0b0442311f6264ac8a14eff80dbf9dcc97f614/R/DBA.R) establish these contracts.

**Recommended default:** Export a known GRanges object with a format-aware exporter, or explicitly use BED start=GRanges start−1 and unchanged end. Retain full-precision statistics for selection, robust CSV parsing and original IDs. Keep motif window/background decisions target-specific.

**Immediate correction versus lab review:** Correct tutorial export/schema handling now. Historical correction requires verifying each CSV producer/coordinate convention; motif background, gene assignment and set question require lab review.

**Potential historical impact:** Potentially BED overlaps, one-base boundaries, selected motif sequences and threshold-edge region membership. Peak coordinates/statistical model results upstream of export are not automatically invalidated. No specific historical motif result was tested.


## D17 — Figures and provenance

**Classification:** Display/transform choices; abundance rank fallback is a semantic error if labeled measured abundance. Historical figure labels are missing evidence.

**Observed lab behavior:** CR-S05 exports a common pre-branch matrix for log2(x+1), variance filtering and scaled PCA. CR-S13/14 have reported-Fold and concentration-derived MA modes; the abundance helper can fall back to row rank. CR-S16 uses centers and missing-as-zero.

**Why it matters:** Scaling features changes their contribution to PCA. Concentration-derived M need not equal a shrunken model effect. Missing coverage is not automatically zero and a region center is not necessarily a binding summit.

**Established methods / references:** [R prcomp](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/prcomp.html) documents scaling; [deepTools computeMatrix](https://deeptools.readthedocs.io/en/3.5.6/content/tools/computeMatrix.html) documents region geometry/missing handling.

**Recommended default:** Label actual matrix, transformation, units and scale in every caption; never label common pre-branch PCA as spike-specific or rank as abundance. Use fixed regions/comparable scales and show replicates alongside means.

**Immediate correction versus lab review:** Correct educational labeling now. Alternative variance stabilization, window anchoring and figure selection require a declared purpose and review.

**Potential historical impact:** May change the interpretation of clustering, abundance trends and heatmap differences. No historical figure was shown to have incorrect labels or biological conclusions.


## D18 — Scheduler, restarts and exit status

**Classification:** Confirmed shell/control-flow defects plus cache/completion design weaknesses; not evidence that all produced files are wrong.

**Observed lab behavior:** CR-S07 uses `afterany`; CR-S01/02 skip existing files. CR-S02:39 uses a job-specific lock; 94–125 caches cohort statistics; 213–214 launches exported functions in new Bash children without explicitly enabling parent error options; 219–227 post-increments zero under `set -e`.

**Why it matters:** Post-increment returns failure on the first success. Child Bash may mask a failed producer behind successful sed; `local x=$(command)` can mask substitution status too. Distinct job locks do not serialize common outputs, and partial/stale files can satisfy existence gates.

**Established methods / references:** [Bash error-option semantics](https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin) and [Slurm dependencies](https://slurm.schedmd.com/sbatch.html#OPT_dependency) describe behavior; source-specific consequences were checked with synthetic shell examples only.

**Recommended default:** For future execution: explicit child error checks/options, assignment-safe counters, complete expected manifests, success-gated dependencies, content/parameter identities, one output owner and atomic publication. Keep per-run cohort/count/median identities together.

**Immediate correction versus lab review:** Document remedies and synthetic demonstrations now. Do not patch/run the private supervisor here. Lab/HPC review must approve any operational replacement before execution.

**Potential historical impact:** Potential false failures, masked failures, partial cohorts or mixed-version artifacts. Existing valid tracks may survive a status failure; only output-by-output provenance can determine historical rework.


## D19 — Version and installation reproducibility

**Classification:** Missing environment locks; candidate setup is not verified installation.

**Observed lab behavior:** CR-L01/L02 record Cutadapt/Python and R/DiffBind versions. The reviewed upstream DiffBind commit da0b044 identifies package version 3.16.0. Other executed dependencies remain unknown. CR-S02 also requires bc, flock, xargs and GNU grep behavior, not merely bioinformatics packages.

**Why it matters:** A Conda name, current tool manual or compatible parser does not reconstruct an executed environment. Compiled packages, architecture and defaults can alter behavior or prevent startup.

**Established methods / references:** [Bioconductor installation](https://bioconductor.org/install/) specifies compatible release families; [Conda environment management](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html) supports explicit dependency recording.

**Recommended default:** Keep known historical pins and unknowns separate; mark candidate solves/install commands unverified. Capture full runtime versions, reference hashes, command parameters and platform-specific locks after an intentional installation.

**Immediate correction versus lab review:** Correct dependency/default documentation now. Installation solves and Linux/macOS/WSL2 execution remain a later, bounded validation task.

**Potential historical impact:** Unknown versions weaken reproduction but do not themselves prove historical results incorrect. Compare artifacts only after establishing the relevant environment differences.


## D20 — Publication and execution readiness

**Classification:** Publication/validation governance and missing acceptance evidence, not a biological algorithm defect.

**Observed lab behavior:** Public text uses generic examples and opaque source IDs; full paths/logs/provenance remain ignored locally. This review adds a text-table teaching counter with synthetic tests, not an automated assay workflow.

**Why it matters:** Reproducibility requires enough safe method detail while respecting data rights and confidentiality. A docs build or synthetic test validates only its stated contract, not enrichment biology.

**Established methods / references:** The [FAIR principles](https://pmc.ncbi.nlm.nih.gov/articles/PMC4792175/) encourage reusable metadata/provenance; they do not require making private results public.

**Recommended default:** Publish only reviewed methods and permitted teaching artifacts; maintain separate documentation, execution and scientific acceptance records. Continue manual educational validation before any automation milestone.

**Immediate correction versus lab review:** Finish safe documentation and tests now. Dataset rights, scientific acceptance and deployment remain explicit future decisions; no push or public PR is authorized here.

**Potential historical impact:** No historical result change follows from publication review. Execution readiness remains unestablished for all assay stages despite the narrower passing checks.
