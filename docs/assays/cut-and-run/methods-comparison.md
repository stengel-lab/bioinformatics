# Lab methods compared with established approaches

**Scientific review updated: 2026-10-30.** External comparator: stable **nf-core/cutandrun 3.2.2**, not its development branch. Consult the [release](https://github.com/nf-core/cutandrun/releases/tag/3.2.2), [usage](https://nf-co.re/cutandrun/3.2.2/docs/usage), [parameters](https://nf-co.re/cutandrun/3.2.2/parameters) and versioned implementation links below. No nf-core analysis was run. Defaults are comparison points, not universal scientific requirements.

**L** = observed lab code; **E** = external documented method; **P** = proposed change; **U** = unresolved. Lab evidence resolves through the [source registry](sources.md); all proposals require review rather than silently replacing the reconstruction.

## Preprocessing and alignment

| Topic | L — selected lab practice | E — comparator | P / U — decision to review |
|---|---|---|---|
| Trimming | Direct Cutadapt, paired adapters `AGATCGGAAGAG`, `-m 15 -q 20 -z` (CR-S01) | nf-core wraps trimming with Trim Galore; the [module configuration](https://raw.githubusercontent.com/nf-core/cutandrun/3.2.2/conf/modules.config) identifies the wrapper | P: compare retained reads and fragment sizes on the same library. U: actual adapter chemistry; `-m` is read length, not fragment length |
| Short fragments | No explicit fragment-size class selection | [Original CUT&RUN](https://elifesciences.org/articles/21856) motivates inspecting fragment classes | P: report short/nucleosomal distributions by target; do not discard short fragments using an imported assay rule |
| Host/spike mapping | Combined hg38–sacCer3 reference | nf-core [usage](https://nf-co.re/cutandrun/3.2.2/docs/usage) supports separate target and spike references | U: historical reference identity, naming, cross-mapping and spike material; strategies have different denominators |
| Target paired-end settings | `--no-mixed --no-discordant`; other geometry/presets not explicit | [3.2.2 modules](https://raw.githubusercontent.com/nf-core/cutandrun/3.2.2/conf/modules.config) use `--end-to-end --very-sensitive --no-mixed --no-discordant --phred33 --minins 10 --maxins 700 --dovetail` by default; local mode is configurable | P: evaluate short-insert alignment retention and multimapping under an explicitly versioned policy |
| Spike alignment geometry | Same combined alignment for both species | nf-core spike alignment uses `--no-overlap --no-dovetail` with its insert limits, unlike the host alignment | P: do not assume identical geometry is appropriate for calibrator and target; compare species counts under a defined protocol |
| MAPQ | Per-alignment threshold 30 | nf-core [parameter schema](https://raw.githubusercontent.com/nf-core/cutandrun/3.2.2/nextflow_schema.json) defines default 20 | U: sensitivity/specificity tradeoff and complete-mate retention. Neither number alone guarantees unique species assignment |
| Mitochondria | No explicit mitochondrial exclusion; human BED may include chrM | nf-core has configurable mitochondrial removal | P: quantify mitochondrial fraction and state whether it contributes to each denominator |

Bowtie2 paired-end terminology is defined by its [official manual](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml). The lab version is unknown, so unspecified defaults cannot be reconstructed from a current manual alone. CUT&RUN uses targeted nuclease cleavage; CUT&Tag uses tagmentation. Do not transfer cleavage-site shifts, duplication assumptions or fragment interpretation between them without evidence.

## Duplicates, controls and normalization

| Topic | L — selected lab practice | E — comparator | P / U — decision to review |
|---|---|---|---|
| Duplicates | BAMs/tracks retain records; MACS2 `auto`; DiffBind requests removal but its final summarizeOverlaps pass filters duplicate flags, with no upstream marking step established | nf-core [usage](https://nf-co.re/cutandrun/3.2.2/docs/usage) defaults to deduplicating controls, with optional target deduplication | U: distinguish technical amplification from genuine repeated cleavage; inspect flags and complexity. P: document final count policy and preliminary summit pass separately |
| Calibration biology | Combined reference suggests yeast use; full spike protocol absent | [Meers et al.](https://elifesciences.org/articles/46314) discuss bacterial carryover calibration in a defined protocol | U: deliberate yeast versus carryover, amount/addition stage and equal-cell assumptions; one protocol does not validate another |
| Spike identity/counts | Prefix regex may include human chrX/chrM; idxstats sums mapped segments | nf-core supports a distinct spike reference | P: exact contig manifest or separately validated mapping; reconcile segments versus fragments before using scale factors |
| Coverage denominator | `median(S)/S_i`; CPM also produced | nf-core schema exposes normalization modes and spike constant 10,000 | U: cohort/cache consistency and whether a common multiplicative scale is the only difference; compare counts and filters first |
| Coverage geometry | No explicit extension; spike track from combined BAM, CPM from human BAM | nf-core schema defaults `extend_fragments=true` | P: evaluate fragment extension and human-only spike tracks as documented changes |
| Background control | Selected MACS2 has no `-c` | nf-core defaults `use_control=true` and supports IgG background use | U: available control quality and compatibility; baseline target-IP samples are not IgG controls |

The normalization and coverage defaults above come from the [versioned schema](https://raw.githubusercontent.com/nf-core/cutandrun/3.2.2/nextflow_schema.json). A different common spike constant changes displayed units; different spike assignment, pair filters or cohort selection can change relative scaling. Do not claim equivalence from the formulas alone.

## Peaks, reproducibility and inference

| Topic | L — selected lab practice | E — comparator | P / U — decision to review |
|---|---|---|---|
| Peak caller | MACS2 narrow BAMPE, q 0.001, `keep-dup auto`; historical broad branch differs | nf-core [parameters](https://nf-co.re/cutandrun/3.2.2/parameters) default SEACR; optional MACS2 q 0.01, narrow/broad selection | U: choose focal/domain model and control strategy by target, with the [SEACR method](https://link.springer.com/article/10.1186/s13072-019-0287-4) as a candidate |
| Blacklist | Peak-only subtraction; empty filtered set can fall back to raw | nf-core [outputs](https://nf-co.re/cutandrun/3.2.2/docs/output) expose filtering and peak/QC products | P: consistent assembly-specific mask, explicit empty-set status, inspect suspect regions with the [blacklist rationale](https://www.nature.com/articles/s41598-019-45839-z) |
| FRiP | BAM record overlap / BAM record total, any overlap | nf-core [parameters](https://nf-co.re/cutandrun/3.2.2/parameters) define fragment overlap threshold 0.2 | P: compare only after harmonizing units and numerator/denominator rules |
| Signal concordance | Historical binned BigWig PCA and Spearman correlation | nf-core [output documentation](https://nf-co.re/cutandrun/3.2.2/docs/output) includes replicate/QC reports | P: inspect individual replicates before averaging; broad genomic correlation is not peak reproducibility |
| Reproducible peaks | No demonstrated accepted biological-replicate consensus/IDR stage in selected chain | nf-core provides consensus/reproducibility products; `replicate_threshold=1` is its default | U: predefine replicate support and overlap rule. A one-replicate threshold is not proof of agreement |
| Differential binding | Custom DiffBind standard/spike branches and contrast mapping | [DiffBind](https://bioconductor.org/packages/release/bioc/vignettes/DiffBind/inst/doc/DiffBind.pdf) supports count/model workflows | U: tested universe, custom normalization, design and sign. nf-core peak consensus does not validate this separate inferential model |
| Downstream sets | Negative-change sets shared across contrasts; direct coordinate copying | BED and GRanges use different coordinate conventions | P: validated coordinate export; do not describe cross-contrast intersections as replicate consensus |

## What comparison can establish

This review establishes source-level differences and documented alternatives. It does not establish which approach performs better for these experiments. The next useful comparison is a small approved dataset with fixed reference identities, explicit controls and a prereviewed target-specific evaluation plan. Change one major assumption at a time; retain both outputs and the reason for choosing between them. See the [decision log](decisions.md) and [validation scope](validation.md).
