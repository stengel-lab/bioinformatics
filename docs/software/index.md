# Software reference

The first entries support the [CUT&RUN tutorial draft](../assays/cut-and-run/index.md). Roles and method parameters were reviewed against source evidence; original private scripts are not redistributed. Examples are not analysis-execution-validated.

## CUT&RUN software library

| Function | Tool pages | Role in the reconstructed lesson |
|---|---|---|
| QC | [FastQC](fastqc.md) | Raw and trimmed paired-read reports |
| Preprocessing | [Cutadapt](cutadapt.md) | Adapters, quality and read-length filtering |
| Alignment | [Bowtie2](bowtie2.md), [SAMtools](samtools.md) | Combined-reference mapping, filtering, sorting/indexing and statistics |
| Intervals | [BEDTools](bedtools.md) | Blacklist review, overlap QC and derived region sets |
| Peaks | [MACS2](macs2.md) | Selected narrow and historical broad calling |
| Coverage/QC | [deepTools](deeptools.md) | Coverage, replicate PCA/correlation and region figures |
| Track arithmetic | [WiggleTools](wiggletools.md), [UCSC utilities](ucsc-track-tools.md) | Equal-replicate means and BigWig conversion |
| Statistics | [DiffBind](diffbind.md), [DESeq2](deseq2.md) | Per-replicate counting and modeled binding changes |
| Interpretation | [HOMER](homer.md) | Motif enrichment and genomic annotation |
| Visualization | [IGV](igv.md), [R libraries](r-plotting.md), [Python libraries/helpers](python-figures.md) | Locus inspection and explicitly labeled figures |
| Execution | [Bash, Conda, Slurm and utilities](execution-environments.md) | Environment identity, portability and source operational assumptions |

Cutadapt 5.1/Python 3.11.9 and R 4.4.3/DiffBind 3.16.0 are historical logged versions. Other selected executable/package versions remain unestablished. See the [setup/version table](../assays/cut-and-run/installation.md#known-historical-version-evidence), [methods comparison](../assays/cut-and-run/methods-comparison.md) and [decision log](../assays/cut-and-run/decisions.md).

SEACR and CUT-RUNTools are external/historical alternatives with incomplete execution evidence in the selected lab chain; they are not presented as required installed dependencies. Other assay catalogs will be added after equivalent review.

## Catalog conventions

| Function | Questions an entry must answer |
|---|---|
| Quality control | What measurement is checked, and what constitutes a concern? |
| Preprocessing | What is removed or transformed, and how can that change the signal? |
| Alignment | What reference and mapping assumptions are used? |
| Filtering and intervals | Which reads or regions are retained, and why? |
| Quantification | What unit is counted, and what is the denominator? |
| Peak and motif analysis | What null model, background, and threshold are used? |
| Statistical analysis | What design, normalization, effect, and uncertainty are estimated? |
| Visualization | What transformation, aggregation, or normalization is displayed? |
| Contact analysis | How are valid pairs, bins, normalization, and interactions defined? |
| Runtime and installation | What platform, dependency versions, and resources are required? |

Use one directory per tool when there is enough content for multiple pages. Start a single entry with the [tool template](../contributing/templates/tool.md). Record aliases and alternate implementations explicitly.

Each catalog entry must distinguish an observed invocation, a documented dependency, a historical alternative, and a prose-only mention. Explicit version strings describe the source evidence; they do not establish what is installed on another system.
