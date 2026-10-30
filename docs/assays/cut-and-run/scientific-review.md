# CUT&RUN scientific review summary

**Reviewed 2026-10-30, starting from `82bd4ec`.** All [20 decisions](decisions.md) now record source behavior, rationale, classification, external evidence, recommended default, immediate action and conditional historical impact. The original lab source files remain unchanged. No biological processing was executed.

## Confirmed bugs and recommended fixes

| Finding | Evidence / recommended remedy | Historical conclusion |
|---|---|---|
| Nonspecific spike-name expression | CR-S01/02 can count human `chrX`/`chrM` as yeast. Use exact roles from the actual reference, validate the complete name/length dictionary and keep mapped-segment units explicit. A synthetic-tested [teaching example](reference-audit.md) is supplied | Matching defect confirmed; actual reference susceptibility and source-to-count-table provenance remain unverified |
| Post-increment under `set -e` | CR-S02:219–227 can exit 1 on its first successful track check. Future source fix: assignment-based increment plus explicit completion validation | Valid files can coexist with a failed job status; no historical file is automatically invalid |
| Error handling is not explicitly established in child Bash workers | CR-S02:213–214 starts new shells; parent error options are not automatically guaranteed there. A successful log-filter command can hide a failed producer, and `local value=$(...)` can mask substitution status. Future remedy: explicit child options and checked assignments/pipelines | Synthetic shell behavior confirmed; actual cluster environment/output impact not reconstructed |
| Empty filtered-peak contract disagrees across stages | CR-S01 can use raw peaks when filtering leaves none, while CR-S06 requests the filtered file. Future remedy: explicit empty-set status and a single reviewed file contract | Defect conditional on that path; no historical empty-set exposure established |
| GRanges-derived CSV is copied directly into BED | CR-S05 defaults to GRanges output; CR-S09/10 do not convert its one-based start. Use format-aware export or start−1/end unchanged after verifying provenance | Boundary-conversion defect for this contract; no specific historical BED/motif effect measured |
| Cache/output existence is not content identity | Cached median/table and existing tracks can represent different cohorts or rules. Future remedy: complete manifest, parameter/reference/input hashes, consistent cohort records and atomic outputs | Risk confirmed in code design; no stale historical artifact is asserted |

These remedies are documented and tested at the stated synthetic boundaries. The private processing workers were not patched or executed. A changed common median alone is not the same as a sample-specific scaling error; see the [algebra and downstream trace](reference-audit.md#a-common-median-is-not-a-sample-dependent-error).

## Scientific choices requiring lab approval

| Decision | Recommended starting default, with limits |
|---|---|
| Calibration biology / reference | Recover the actual reference dictionary and spike protocol before quantitative spike claims; exact-role counting fixes name classification, not experimental calibration |
| Duplicate handling | Preserve source BAMs and describe each product's actual policy. Assess complexity and duplicate flags before selecting removal/retention. No single policy is imposed |
| Focal transcription-factor peaks | Retain the narrow lab baseline for reconstruction; evaluate target-appropriate controls and reproducible focal enrichment before approving another threshold/caller |
| BCOR-associated occupancy | Begin with the narrow baseline **when enrichment is focal**, then compare domain-aware alternatives if profiles support broader association. BCOR is a PRC1.1-associated corepressor, not a histone modification; its label alone does not justify broad calling |
| Broad histone modifications | Evaluate broad/domain calling and domain-preserving count intervals for demonstrably broad signals such as H3K27me3. Some histone signals are focal, so “histone” is not a sufficient selection rule |
| Negative controls | Use compatible IgG/no-primary or specificity controls where scientifically appropriate; target-loss/orthogonal validation can strengthen specificity assessment. An untreated target-IP is a biological baseline, not an IgG background. Poor/very shallow controls also need review |
| Reproducibility | Seek support across independent biological replicates before high-confidence peak claims; predefine target-specific interval overlap and retain exploratory sets separately. Binned signal correlation and cross-contrast intersections do not establish peak reproducibility |
| Masks / count model | Compare normalization branches on a common approved interval universe and inspect actual counted widths, design, sample order and factors. Broad peaks plus default summit recentering do not imply domain-wide counting |

[BCOR-associated chromatin work](https://www.nature.com/articles/s41467-019-09250-6) supports separating occupancy questions from broad histone-mark measurements; it does not validate a caller for this lab's experiments. The [SEACR study](https://link.springer.com/article/10.1186/s13072-019-0287-4) offers an alternative for sparse enrichment. The [CUT&RUN suspect-list study](https://link.springer.com/article/10.1186/s13059-023-03027-3) motivates reviewing assay-associated problematic regions alongside an assembly-matched ENCODE blacklist. A suspect-list exclusion should be assessed and recorded; it is not automatically equivalent to the lab's existing mask. External pipelines and papers are comparators, not approval of a new method.

## Historical results potentially requiring re-evaluation

No specific historical biological result was proven incorrect. Saved logs establish use of a narrow MACS2 option pattern and use of spike factors in recorded R runs. They do not establish the historical index dictionary or prove that the bad regex generated the R inputs. A script snapshot without a run hash is insufficient attribution.

Use a targeted review rather than rerunning everything:

1. Identify the exact run, script revision, reference dictionary, calibration protocol, cohort and table/count inputs for a candidate result. Preserve existing outputs.
2. If matching host contigs and regex-generated counts are confirmed, reassess spike-scaled tracks and the spike-normalized model, then their derived means/heatmaps/selected-region analyses. CPM tracks and selected MACS2 peak calls do not directly consume this factor.
3. If duplicate removal was intended, check original duplicate flags and the actual count path. Unmarked repeated-coordinate reads were not deduplicated merely by the selected DiffBind switch.
4. Compare tested ranges/masks, sample design and complete contrast statuses. Inspect whether 401 bp default windows were appropriate, particularly for broad domains.
5. Verify CSV coordinate origin and statistical precision before revisiting downstream BED overlaps, motifs and annotations. Regenerate only the affected descendants after approval.

The private review map records exact source/log locations and line-level evidence; no private counts, sample identities or result tables are published here.

## Documentation corrections made

- **Duplicate removal claim corrected:** the final summarizeOverlaps pass filters duplicate-marked records; it does not discover fresh unmarked coordinate duplicates. Default summit estimation also uses a preliminary built-in pass, so no uniformly deduplicated count process is established.
- **Normalization API uncertainty narrowed:** the verified 3.16.0 source accepts numeric vectors and assigns them directly as DESeq2 size factors in the design-based path. `S/median(S)` has the intended denominator direction. `library=FULL` is not an automatic extra depth multiplier there. This is static API verification, not model execution.
- **Sample ordering and diagnostics recognized:** the lab script already matches count IDs to sample order and exports retrieved normalization diagnostics; these checks are not newly invented remedies.
- **Implicit counting defaults explained:** `minOverlap=2`, `summits=200` and `filter=1` are version-specific defaults, not explicit lab selections. The resulting count universe needs inspection.
- **Contrast direction clarified:** the mapper's flip logic is consistent with positive numerator enrichment; no static sign bug was found. Biological contrast intent still requires review.
- **Coordinate/schema and report precision clarified:** GRanges CSV uses `seqnames/start/end`; explicit data-frame output can use `Chr/Start/End`. A full-precision export is proposed for threshold selection; the observed report command is retained unchanged in the reconstruction.
- Algorithm explanations were added for QC, trimming, alignment, peaks, scaling, replicate summaries, overlap counting and statistical inference. Observed commands and proposed alternatives remain labeled separately.

## Remaining unresolved questions

The highest-priority missing evidence is the historical reference/build manifest and the experimental spike protocol. The lab must also decide target-specific peak/control and duplicate policies, mitochondrial handling, reproducibility criteria, model design and common masks. Historical source attribution, input-table freshness, realized count widths and environment locks remain incomplete. All 20 entries have a scoped recommendation; numerical thresholds or scientific choices without adequate evidence remain explicitly open.

See [validation](validation.md) for the checks actually performed. This review ends at documentation, reference-aware text-table validation and synthetic tests. It does not begin another assay-processing or automation milestone.
