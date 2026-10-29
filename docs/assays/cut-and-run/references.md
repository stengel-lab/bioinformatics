# References and review boundaries

**Accessed/reviewed: 2026-10-29.** This list distinguishes primary methods, a versioned external pipeline, and official software resources. No figure, full source script, private log or result table is redistributed. Links to current manuals describe external interfaces; they do not establish historical installed versions.

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
