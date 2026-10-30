# References and review boundaries

**Accessed/reviewed: 2026-10-29; scientific review extended 2026-10-30.** This list distinguishes primary methods, a versioned external pipeline, and official software resources. No figure, full source script, private log or result table is redistributed. Links to current manuals describe external interfaces; they do not establish historical installed versions.

## Sources added in scientific review

- [DiffBind 3.16.0 immutable source snapshot](https://github.com/bioc/DiffBind/tree/da0b0442311f6264ac8a14eff80dbf9dcc97f614): DESCRIPTION, API, counting, range conversion, normalization and DESeq2 adapter inspected without executing them. Supports the refined duplicate-policy, defaults, contrast, coordinate and factor-interface explanations. The original package source is not vendored into this repository.
- [The CUT&RUN suspect list of problematic regions of the genome](https://link.springer.com/article/10.1186/s13059-023-03027-3) (Genome Biology, 2023; DOI 10.1186/s13059-023-03027-3): assay-specific artifact-region evidence; a potential comparison to, not an automatic replacement for, the lab mask.
- [Bcor loss perturbs myeloid differentiation and promotes leukaemogenesis](https://www.nature.com/articles/s41467-019-09250-6) (Nature Communications, 2019; DOI 10.1038/s41467-019-09250-6): primary BCOR/Polycomb context distinguishing occupancy and histone-mark questions. Retrieved primary search text supported this context; direct publisher access later encountered an access redirect. It does not validate a specific CUT&RUN caller.
- [DESeq2 vignette](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html), [R prcomp](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/prcomp.html) and [UCSC BED specification](https://genome.ucsc.edu/FAQ/FAQformat.html#format1): model/design, PCA scaling and coordinate contracts.
- [Bash manual](https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin), [Slurm sbatch](https://slurm.schedmd.com/sbatch.html#OPT_dependency), [Conda environment management](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html) and [FAIR principles](https://pmc.ncbi.nlm.nih.gov/articles/PMC4792175/): runtime/provenance references. GNU manual retrieval timed out; shell claims were independently checked using synthetic local Bash examples. No original source worker was executed.

## Primary methods

- Skene PJ, Henikoff S (2017). *An efficient targeted nuclease strategy for high-resolution mapping of DNA binding sites.* eLife 6:e21856. [Article and DOI 10.7554/eLife.21856](https://elifesciences.org/articles/21856). Experimental mechanism and original interpretation of released fragments/calibration.
- Meers MP, Bryson TD, Henikoff JG, Henikoff S (2019). *Improved CUT&RUN chromatin profiling tools.* eLife 8:e46314. [Article and DOI 10.7554/eLife.46314](https://elifesciences.org/articles/46314). Protocol-specific improvements and bacterial carryover calibration; not automatic validation of yeast scaling.
- Meers MP, Tenenbaum D, Henikoff S (2019). *Peak calling by Sparse Enrichment Analysis for CUT&RUN chromatin profiling.* Epigenetics & Chromatin 12:42. [Article and DOI 10.1186/s13072-019-0287-4](https://link.springer.com/article/10.1186/s13072-019-0287-4). Rationale for SEACR as an alternative caller.
- Amemiya HM, Kundaje A, Boyle AP (2019). *The ENCODE Blacklist: Identification of Problematic Regions of the Genome.* Scientific Reports 9:9354. [Article and DOI 10.1038/s41598-019-45839-z](https://www.nature.com/articles/s41598-019-45839-z). Suspect-region filtering rationale.
- Love MI, Huber W, Anders S (2014). *Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2.* Genome Biology 15:550. [Article and DOI 10.1186/s13059-014-0550-8](https://doi.org/10.1186/s13059-014-0550-8). Count-model basis; its application to CUT&RUN requires an appropriate design/counting model.

## Stable external comparator

**nf-core/cutandrun 3.2.2**: [release](https://github.com/nf-core/cutandrun/releases/tag/3.2.2), [overview](https://nf-co.re/cutandrun/3.2.2/), [usage](https://nf-co.re/cutandrun/3.2.2/docs/usage), [parameters](https://nf-co.re/cutandrun/3.2.2/parameters), [outputs](https://nf-co.re/cutandrun/3.2.2/docs/output), [module arguments](https://raw.githubusercontent.com/nf-core/cutandrun/3.2.2/conf/modules.config) and [parameter schema](https://raw.githubusercontent.com/nf-core/cutandrun/3.2.2/nextflow_schema.json). Source was consulted to distinguish host and spike alignment settings. No deployment or execution is implied.

## Official software and setup resources

| Topic | Primary resource | Scope |
|---|---|---|
| FastQC | [Project](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) | Reports and installation |
| Cutadapt | [Guide](https://cutadapt.readthedocs.io/en/stable/guide.html), [5.1 CLI](https://raw.githubusercontent.com/marcelm/cutadapt/v5.1/src/cutadapt/cli.py) | Paired trimming and exact historical `-z` meaning |
| Bowtie2 | [Manual](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml) | Alignment modes and paired geometry |
| SAMtools | [view](https://www.htslib.org/doc/samtools-view.html), [idxstats](https://www.htslib.org/doc/samtools-idxstats.html) | Filtering and mapped-segment count units |
| BEDTools | [intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html) | Interval/BAM overlap semantics |
| MACS2 | [2.2.9.1 option validator](https://raw.githubusercontent.com/macs3-project/MACS/v2.2.9.1/MACS2/OptValidator.py), [paired-end calling source](https://raw.githubusercontent.com/macs3-project/MACS/v2.2.9.1/MACS2/callpeak_cmd.py) | Versioned external semantics; lab version unknown |
| deepTools | [bamCoverage](https://deeptools.readthedocs.io/en/develop/content/tools/bamCoverage.html), [3.5.6 computeMatrix](https://deeptools.readthedocs.io/en/3.5.6/content/tools/computeMatrix.html), [3.5.6 multiBigwigSummary](https://deeptools.readthedocs.io/en/3.5.6/content/tools/multiBigwigSummary.html) | Coverage and signal figures |
| DiffBind | [Manual](https://bioconductor.org/packages/release/bioc/manuals/DiffBind/man/DiffBind.pdf), [vignette](https://bioconductor.org/packages/release/bioc/vignettes/DiffBind/inst/doc/DiffBind.pdf), [Bioconductor 3.20 normalization source](https://raw.githubusercontent.com/bioc/DiffBind/RELEASE_3_20/R/normalize.R) | Counting, contrasts and supported normalization API |
| DESeq2 | [Bioconductor package](https://bioconductor.org/packages/release/bioc/html/DESeq2.html) | Current package documentation; historical dependency unpinned |
| WiggleTools / UCSC | [WiggleTools](https://github.com/Ensembl/WiggleTools), [BigWig documentation](https://genome.ucsc.edu/goldenpath/help/bigWig.html) | Track arithmetic and file conversion |
| HOMER | [Bioconda recipe](https://bioconda.github.io/recipes/homer/README.html), [upstream motif manual](http://homer.ucsd.edu/homer/ngs/peakMotifs.html) | Recipe accessible; upstream manual timed out during review, so invocation claims rely on inspected lab code |
| SEACR | [Maintainer repository](https://github.com/FredHutch/SEACR) | External alternative, not proven execution in selected lab chain |
| IGV | [Desktop documentation](https://igv.org/doc/desktop/) | Reference-matched visual inspection |
| Platforms | [Bioconda](https://bioconda.github.io/), [Bioconductor installation](https://bioconductor.org/install/), [WSL installation](https://learn.microsoft.com/en-us/windows/wsl/install) | Candidate environment guidance, not tested installations |

Further plotting/runtime references are on the individual [software pages](../../software/index.md). The internal [source registry](sources.md) is the primary evidence for observed lab behavior; external recommendations are not evidence that a lab command executed successfully.
