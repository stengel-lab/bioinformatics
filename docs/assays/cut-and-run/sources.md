# Source workflow and provenance

**Evidence reviewed:** 2026-10-29. The local inventory from milestone `4027d17` was revisited against the original files. The exact private map records full paths, SHA256 hashes, line ranges and inspection notes. Public IDs below expose only reviewed method descriptions and generic filenames. Original source scripts and logs are not redistributed.

**Scientific review extension, 2026-10-30:** source hashes were rechecked; reference-build searches and 18 saved-log inspections are recorded privately. The [review](scientific-review.md) distinguishes source-level dependencies from historical exposure. Saved logs demonstrate a MACS2 option pattern and use of spike factors, but supply neither a reference dictionary nor a completed upstream count/coverage trace. The exact upstream [DiffBind 3.16.0 commit](https://github.com/bioc/DiffBind/tree/da0b0442311f6264ac8a14eff80dbf9dcc97f614) was inspected as external API evidence, not substituted for the executed lab environment.

## Why this is the selected baseline

The current supervisor (**CR-S07**, lines 64–82) and monitor (**CR-S08**, lines 881–988) both select `cutrun_fastq2bam_oai.sbatch`, `cutrun_bam2bw_oai.sbatch`, and `diffbind.sbatch`. The latter selects `diffbind_analysis.R` (**CR-S04**, line 89). That call relationship is stronger evidence of intended use than a directory named “newest.” It establishes a reconstruction baseline, not a declaration that the implementation is authoritative or scientifically accepted.

The averaging, MA, peakset, motif and annotation workers are separate downstream entry points; they are not all automatically launched by that three-stage supervisor. Heatmaps and per-sample track concordance are reconstructed from explicitly identified historical workers. A later plot revision does not supersede an earlier alignment algorithm.

## Source registry

| ID | Reviewed source | Relevant lines | Role |
|---|---|---|---|
| CR-S01 | `cutrun_fastq2bam_oai.sbatch` | 44–50, 147–204, 207–306 | QC, Cutadapt, Bowtie2/SAMtools, human selection, MACS2, peak blacklist, FRiP and spike count |
| CR-S02 | `cutrun_bam2bw_oai.sbatch` | 31–35, 58–125, 145–230 | Cohort discovery, cached median and spike/CPM BigWigs |
| CR-S03 | `cutrun_bw_avg.sbatch` | 44–85, 144–187 | Replicate-name grouping, arithmetic means and human-contig filtering |
| CR-S04 | `diffbind.sbatch` | 13–27, 84–106 | R/DiffBind probes and selected R analysis |
| CR-S05 | `diffbind_analysis.R` | 17–32, 150–191, 270–581, 591–643, 1112–1123 | Environment/imports, counting, configured contrast direction, standard/spike models and shared PCA |
| CR-S06 | `diffbind_input_file_gen.py` | 23–105, 282–517 | Naming-based sample/design inference and blacklist-filtered peak paths |
| CR-S07 / CR-S08 | `cutrun_supervisor.sbatch` / `monitor_cutrun.sh` | 64–82 / 881–988 | Selected workers and scheduler behavior |
| CR-S09 | `build_condition_peaksets.sh` | 19–20, 56, 70–171, 203–261 | Differential-contrast unions/shared sets, including destructive rebuild behavior |
| CR-S10 / CR-S11 | `cutrun_motif_worker.sbatch` / `cutrun_peakset_motif_worker.sbatch` | 16–21, 88–157 / 69–84 | Contrast-derived or named-region HOMER analyses |
| CR-S12 | `cutrun_peakset_annotate_worker.sbatch` | 69–104 | HOMER annotation and R bar plots |
| CR-S13 / CR-S14 | `cutrun_ma_plots.sbatch` / `make_cutrun_ma_plots.R` | 90–114 / 71–104, 227–251 | Two MA coordinate modes and significance coloring |
| CR-S15 / CR-S16 | Historical `pca_bw_bedgraph.sbatch` / `heatmaps_cutrun.sbatch` | 143–161 / 218–265, 318–350 | Track concordance, legacy averaging, heatmaps and profiles |
| CR-S17 / CR-S18 | Historical broad worker / alternate target-aware worker | 216–231 / 97–111, 171–194, 328–432 | Broad peaks, dual calling and alignment-level blacklist alternative |
| CR-S19 / CR-S20 | Earlier combined-reference worker / earlier narrow worker | 143–207 / 177–246 | Trimming, raw BAM intermediate and peak-parameter history |
| CR-S21 | `diffbind_analysis_no-spike-in.R` | 149–280 | Separate standard-only analysis; not selected by current wrapper |
| CR-S22 | `crtools_bulk.sbatch` | 17–68 | External CUT-RUNTools footprint wrapper; internal workflow absent |
| CR-S23 / CR-S24 | Custom motif-table / Venn figure helpers | imports and entry points | Python figure composition; no new inferential method |
| CR-S25 | `validate_cutrun_outputs.py` | 1–310 | Output checks; insufficient by themselves for biological validation |
| CR-L01 | Saved read-processing log | 18–20 | Cutadapt 5.1, Python 3.11.9; includes the observed `-z` invocation |
| CR-L02 | Saved statistical-analysis log | 3–6 | R 4.4.3 and DiffBind 3.16.0 |
| CR-L03 | Saved statistical stderr | 83–99 | Standard-path blacklist/default-normalization messages and warnings |

IDs identify private source records, not downloadable scripts. Access to the private map is required to audit the complete originals. All command fragments in this tutorial were reconstructed with generic paths and fictional labels. No source log values, result counts, sample identities or institutional configuration are included.

## File contracts and teaching aliases

The source organizes outputs under each sample and contains system-specific reference locations. The lesson uses shorter generic directories. These translations change paths, not scientific parameters; actual scripts are not supplied by the tutorial.

| Observed generic source pattern | Teaching alias / role |
|---|---|
| `${sample}_R1.fastq.gz`, `${sample}_R2.fastq.gz` in project root | `reads/` holds the original paired inputs |
| `${sample}/spikein_outputs/${sample}.hg38-sacCer3.sorted.bam` | `align/${sample}.hg38-sacCer3.sorted.bam`; **combined**, not spike-only |
| `${sample}/hg38-only/${sample}.hg38-only.sorted.bam` | `align/${sample}.hg38-only.sorted.bam`; selection depends on the BED |
| `${sample}/macs2/${sample}_peaks.narrowPeak` | `peaks/${sample}/${sample}_peaks.narrowPeak` |
| `${sample}/macs2/${sample}_peaks.blacklist_filtered.narrowPeak` | `peaks/${sample}/${sample}_peaks.blacklist_filtered.narrowPeak` |
| Per-sample spike/CPM BigWigs in separate normalization directories | `tracks/spike/` and `tracks/cpm/` |
| Project `spike_counts.tsv` / `spike_median.txt` | Private calibration table/cache; review cohort, count rule and freshness before use |
| `diffbind_input.csv` and selected `diffbind_analysis.R` in project root | Chapter 4 demonstrates a reviewed CSV schema in `design/` and annotated R excerpts; these do not automatically configure the unchanged private script |

The statistical wrapper invokes `Rscript diffbind_analysis.R`. The script changes into its output directory and expects source-specific inputs/helper conventions; running that entry point requires a separately reviewed private execution setup. The lesson's `reports/`, `regions/` and `figures/` paths are teaching output aliases, not proof of identical source naming. No entire source script is required or distributed for the chapter explanations.

## Version reconciliation

| Implementation | Observed difference | Tutorial treatment |
|---|---|---|
| Selected core vs earlier narrow worker | Stream directly into a coordinate-sorted BAM instead of retaining a raw BAM; selected worker also filters peak intervals against a blacklist | Main lesson follows the selected core; output aliases are explained explicitly |
| Earlier combined-reference worker | Empty custom Cutadapt option array; peak command includes `--keep-dup all --nomodel --shift -100 --extsize 200` | Historical option set, not added to the selected command. Paired-end MACS semantics must be checked before interpreting shift/extension flags |
| Broad worker | `BAMPE --broad -q 0.05 --broad-cutoff 0.1 --keep-dup all -B --SPMR` | Optional target-dependent branch, not a universal replacement |
| Alternate target-aware worker | Removes blacklist-overlapping alignments, varies target-specific peak flags, and includes dual narrow/broad calling | Distinct implementation; its BAMs, FRiP and denominators are not interchangeable with peak-only filtering |
| Selected vs separate non-spike R file | Selected R code recomputes counts, exports standard/spike subdirectories and maps configured contrasts; separate standard-only file can reuse prior top-level outputs | Main lesson documents both selected branches. No silent fallback to the standard-only file |
| Current MA wrapper vs older embedded plotting | Separate normalization-mode directories and `Fold/baseMean` versus `Conc_*` coordinates | Label coordinate definitions; colors still use reported `Fold` and FDR |
| Current vs historical averaging | WiggleTools mean of all matched replicates versus older pairwise means in a historical plotting worker | Prefer the observed all-replicate mean for reconstruction; verify equal weights if comparing historical figures |

“Historical” here describes source context; it does not prove abandonment. There is no maintainer-signed version-selection or scientific acceptance record.

## Computational requests in the sources

| Worker | Requested CPUs | Requested memory | Requested wall time |
|---|---:|---:|---|
| FASTQ → BAM/peaks | 16 | 64 GB | 24 h |
| BAM → spike/CPM tracks | 8 | 64 GB | 24 h |
| Replicate mean | 2 | 8 GB | 2 h |
| DiffBind | 16 | 64 GB | 24 h |
| Motif worker | 8 | 32 GB | 24 h |
| Annotation worker | 4 | 64 GB | 8 h |
| MA plotting | 4 | 16 GB | 8 h |

These are scheduler requests, not measured minima or runtime benchmarks. The alignment pipeline overlaps Bowtie2, SAMtools conversion and sorting; thread totals and per-thread sort memory need a resource review. DiffBind counting explicitly disables parallel counting despite the CPU request. Local machines require separate resource measurements.

The supervisor uses **`afterany`**, which permits downstream jobs after an upstream failure. The coverage worker then discovers completed subsets. This is observed behavior, not a success guarantee. Require a complete expected sample list and inspect scheduler exits, output validity and QC before advancing. [Decision log](decisions.md) entries D02, D08 and D18 explain the consequences.
