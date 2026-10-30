# Installation, environments and reference data

**Status: proposed setup guidance; not installed or executed for analysis in this milestone.** Syntax was checked where possible. The source environment names are labels, not reproducible specifications. No complete historical environment lock was found.

## Choose an execution platform

| Platform | Practical route | Limitations to record |
|---|---|---|
| Linux / Linux HPC | Bash with isolated command-line and R environments; site-approved scheduler or containers | Reference paths, libraries, scratch and resource policy require configuration |
| macOS | Native Conda packages where available for Intel or Apple Silicon; native R for statistics | Historical versions may lack a build for the architecture. GNU shell commands differ; Linux-specific `flock`/`grep -P` in the original wrappers need replacement or Linux execution |
| Windows | Run the analysis commands in a WSL2 Linux distribution or on a remote Linux system | Native PowerShell is not Bash; WSL2 does not supply a Slurm cluster or the source references |

[Bioconda](https://bioconda.github.io/) documents Linux and macOS support. Availability of a particular historical version on a particular architecture still requires checking. The source cluster's storage, module initialization and scheduler settings are deliberately absent from public examples.

### Windows / WSL2

**System setup example — requires administrator rights and may require restart; not performed here.** Follow [Microsoft's WSL installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install).

```powershell
wsl --install -d Ubuntu
wsl --list --verbose
```

Confirm the distribution reports version 2. Launch Ubuntu and run the Bash/Conda examples there. Use a Linux working directory such as `~/cutrun-training`; stage permitted inputs explicitly. Allocate enough WSL memory/disk and record Windows, WSL, distribution and CPU architecture. macOS users can follow the same conceptual steps in a native environment, but must check package builds and shell-tool compatibility.

## Known historical version evidence

| Component | Evidence | What is not established |
|---|---|---|
| Cutadapt 5.1; Python 3.11.9 | Saved run header, CR-L01 | Current installation or full dependency lock |
| R 4.4.3; DiffBind 3.16.0 | Saved run header, CR-L02 | Every R dependency version; identity of all later runs |
| FastQC, Bowtie2, SAMtools, BEDTools, MACS2, deepTools, WiggleTools, HOMER | Invoked by selected source | Exact executed versions were not established from the selected records |
| DESeq2 and figure libraries | Backend/import evidence | Exact versions remain unrecorded |

Documentation examples below do not silently substitute MACS3 for MACS2 or a current DiffBind release for the logged historical release.

The scientific review verified an [immutable upstream snapshot](https://github.com/bioc/DiffBind/tree/da0b0442311f6264ac8a14eff80dbf9dcc97f614) whose DESCRIPTION version is 3.16.0. It supports the documented counting/normalization API interpretation; it does not reconstruct the installed dependency environment or prove the state of a historical fitted model.

## Candidate environments

Install Conda using its official platform instructions linked by [Bioconda](https://bioconda.github.io/). These candidates are **not lockfiles, tested solvers, or verified historical environments**. Use `--dry-run` first; inspect platform builds and then intentionally repeat without that option. Channels are specified per command to avoid modifying global configuration.

```bash
conda create --dry-run --name cutrun-core \
  --override-channels --channel conda-forge --channel bioconda \
  --strict-channel-priority \
  python=3.11 cutadapt=5.1 fastqc bowtie2 samtools bedtools deeptools
```

MACS2 and its compiled NumPy dependencies deserve an isolated solve. This is a proposed candidate release for review, **not the source's proven MACS2 version**:

```bash
conda create --dry-run --name cutrun-macs2 \
  --override-channels --channel conda-forge --channel bioconda \
  --strict-channel-priority python=3.10 'numpy<2' macs2=2.2.9.1
```

For statistical reconstruction, attempt a historically compatible candidate separately. A solver failure requires investigation; removing the pins is a new environment decision.

```bash
conda create --dry-run --name cutrun-r \
  --override-channels --channel conda-forge --channel bioconda \
  --strict-channel-priority \
  r-base=4.4.3 bioconductor-diffbind=3.16.0 \
  r-ggplot2 r-ggrepel r-corrplot r-pheatmap
```

The alternative native R route uses a matching R/Bioconductor pair, not a mixture of releases. Consult [Bioconductor installation](https://bioconductor.org/install/) and the installed package help. The following is a **proposed R 4.4 / Bioconductor 3.20 family setup**, not a guarantee of exactly DiffBind 3.16.0:

```r
install.packages("BiocManager", repos = "https://cloud.r-project.org")
BiocManager::install(version = "3.20", ask = FALSE, update = FALSE)
BiocManager::install(c("DiffBind", "DESeq2"), ask = FALSE, update = FALSE)
install.packages(c("ggplot2", "ggrepel", "corrplot", "pheatmap"),
                 repos = "https://cloud.r-project.org")
BiocManager::valid()
```

Add optional track and figure tools only when their branches are needed:

```bash
conda create --dry-run --name cutrun-figures \
  --override-channels --channel conda-forge --channel bioconda \
  --strict-channel-priority \
  wiggletools ucsc-bedgraphtobigwig homer matplotlib pillow matplotlib-venn
```

HOMER also needs the appropriate genome sequence and annotation resources; installing its executable package is insufficient. Check the [HOMER page](../../software/homer.md) before motif or annotation steps. Do not assume optional figures need pandas, CairoSVG or other packages just because they appeared elsewhere in the lab inventory: the selected motif helpers import Pillow/matplotlib, and the Venn helper optionally imports matplotlib-venn.

### Check identity after an intentional installation

**Configured inspection commands; no analysis is performed.** Activate the appropriate environment for each tool group. These commands were not run against a reconstructed analysis environment here.

```bash
fastqc --version
cutadapt --version
bowtie2 --version
samtools --version
bedtools --version
bamCoverage --version
macs2 --version
macs2 callpeak --help
```

```r
R.version.string
packageVersion("DiffBind")
packageVersion("DESeq2")
sessionInfo()
```

Record executable locations, package build/channel information and environment exports privately. Remove private prefixes before publishing an environment specification. A successful `--version` is weaker evidence than a startup check and a small reviewed input/output run.

## Reference files and indices

Required resources are:

1. Target genome FASTA and assembly identifier, contig lengths, Bowtie2 index and a human-contig BED whitelist.
2. The actual spike species/assembly and an explicit spike-contig list. The source's combined label is human hg38 plus yeast sacCer3; the biological spike protocol must still be confirmed.
3. A target-assembly blacklist and its source/revision/checksum. A BED from another assembly is invalid here.
4. Target-only chromosome sizes for human BigWig means and matching HOMER genome/annotation data.
5. Annotation source/release and coordinate convention for downstream interpretation; a GTF is not directly used by the core alignment/peak commands.

Candidate public providers include the UCSC [hg38 sequence directory](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/) and [sacCer3 sequence directory](https://hgdownload.soe.ucsc.edu/goldenPath/sacCer3/bigZips/). Review the assembly's sequence set, patch/alternate contigs, masking and naming before downloading. Those choices are not established by the historical label alone. Obtain the blacklist from the source associated with the [ENCODE blacklist study](https://www.nature.com/articles/s41598-019-45839-z), record the exact hg38 revision, and match it to the alignment assembly. No reference download or compatibility check was performed here.

**Proposed construction example — requires approved FASTAs; does not reproduce the uninspected historical index automatically.** Prefixing yeast contigs prevents collisions with human names. Inspect existing historical contig headers before deciding whether to rebuild.

```bash
mkdir -p refs/combined
sed 's/^>/>yeast_/' refs/yeast.fa > refs/yeast.prefixed.fa
cat refs/human.fa refs/yeast.prefixed.fa > refs/combined.fa
bowtie2-build --threads 8 refs/combined.fa refs/combined/index
samtools faidx refs/human.fa
samtools faidx refs/yeast.prefixed.fa
awk 'BEGIN{OFS="\t"} {print $1,0,$2}' refs/human.fa.fai \
  > refs/human.contigs.bed
cut -f1,2 refs/human.fa.fai > refs/human.chrom.sizes
cut -f1 refs/yeast.prefixed.fa.fai > refs/spike.contigs.txt
```

The chapter examples use configurable aliases. If using the files just constructed, replace Chapter 1's reference variables as follows; obtain the blacklist separately and set its actual path. This is a **path configuration example**, not a second reference build:

```bash
REF_DIR="$PWD/refs"
BOWTIE2_INDEX="$REF_DIR/combined/index"
HG38_CONTIGS_BED="$REF_DIR/human.contigs.bed"
HUMAN_SIZES="$REF_DIR/human.chrom.sizes"
BLACKLIST="$REF_DIR/hg38.blacklist.bed"
```

Activate each installed environment only for the commands it contains: core for QC/alignment/tracks, MACS2 for peak calling, R for statistics, and figures for optional tools. For example, `conda activate cutrun-core` precedes core commands after an intentional installation. Activate `cutrun-macs2` for `macs2`, then return to core tools for interval filtering. These names are teaching candidates; they do not alter or recreate the private source environment automatically.

On macOS, `sha256sum` may require GNU coreutils; alternatively record equivalent digests with `shasum -a 256`. GNU-specific wrapper options such as `grep -P` and `flock` need Linux or an explicit portable replacement. Work locally with adequate temporary disk and copy permitted outputs deliberately; do not edit raw inputs in a synchronized source archive.

The original coverage worker also invokes **`bc -l` and `xargs`**. Check these utilities separately from the Conda bioinformatics packages; candidate environment lists do not establish their availability. A parent Bash process's error options are not automatically a verified child-worker contract. See [execution dependencies](../../software/execution-environments.md).

Check that the combined reference has no duplicate sequence names, that whitelists do not overlap between species, and that every expected contig has the expected length. Record FASTA, BED, blacklist and annotation checksums and index-build commands. Avoid inferring species from a loose regular expression; [chapter 3](03-normalization-and-qc.md) demonstrates why.

## Tools by tutorial role

| Stage | Linked tool reference |
|---|---|
| QC / trimming | [FastQC](../../software/fastqc.md), [Cutadapt](../../software/cutadapt.md) |
| Alignment / filtering | [Bowtie2](../../software/bowtie2.md), [SAMtools](../../software/samtools.md), [BEDTools](../../software/bedtools.md) |
| Peaks / tracks | [MACS2](../../software/macs2.md), [deepTools](../../software/deeptools.md), [WiggleTools](../../software/wiggletools.md), [UCSC utilities](../../software/ucsc-track-tools.md) |
| Statistics | [DiffBind](../../software/diffbind.md), [DESeq2](../../software/deseq2.md), [R figure libraries](../../software/r-plotting.md) |
| Interpretation | [HOMER](../../software/homer.md), [IGV](../../software/igv.md), [Python figure libraries](../../software/python-figures.md) |
| Execution | [Conda, Bash and Slurm](../../software/execution-environments.md) |

The full workflow has not been installed or executed on Linux, macOS or WSL2 in this milestone. [Validation](validation.md) states the narrower checks actually performed.
