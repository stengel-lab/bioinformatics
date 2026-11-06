# CUT&RUN: baseline command walkthrough

## Before starting

Have paired FASTQ files, FastQC, Cutadapt, Bowtie2, SAMtools, deepTools, and MACS2 installed, and an hg38 Bowtie2 index available. See [download hg38 and build its Bowtie2 index](../../setup/references/hg38.md) for step-by-step instructions. Tool installation pages will be added separately.

The examples assume a Bash shell and these variables, set once **for each sample**:

```bash
SAMPLE="example_A"
R1="reads/${SAMPLE}_R1_001.fastq.gz"
R2="reads/${SAMPLE}_R2_001.fastq.gz"
SAMPLE_DIR="results/${SAMPLE}"
OUTPUT_PREFIX="${SAMPLE_DIR}/${SAMPLE}"
THREADS=10
GENOME_INDEX="/path/to/hg38/bowtie_hg38"
mkdir -p "$SAMPLE_DIR" "$SAMPLE_DIR/macs2"
```

Replace the example names, paths, and thread count with your own. `GENOME_INDEX` is the Bowtie2 **index prefix**, not a FASTA filename. These snippets document individual operations rather than one independently tested paste-and-run script.

## 1. FastQC — read-quality assessment

**Purpose:** Examine read quality, base content, and possible adapter contamination in the raw R1 and R2 reads.

```bash
fastqc "$R1" "$R2" -o "$SAMPLE_DIR"
```

**Inputs:** two raw FASTQ files. **Outputs:** FastQC HTML and ZIP reports for both mates. Open the HTML reports and inspect per-base quality, sequence lengths, and adapter content. The source script uses FastQC's default analysis settings.

## 2. Cutadapt — adapter trimming

**Purpose:** Remove specified adapter sequences from each mate and discard reads shorter than the minimum retained length.

```bash
cutadapt \
  -a AGATCGGAAGAG \
  -A AGATCGGAAGAG \
  -e 0.10 \
  --minimum-length 15 \
  -o "${OUTPUT_PREFIX}_R1.trimmed.fastq.gz" \
  -p "${OUTPUT_PREFIX}_R2.trimmed.fastq.gz" \
  "$R1" "$R2"
```

| Parameter | Meaning |
| --- | --- |
| `-a` | 3′ adapter sequence for R1 |
| `-A` | 3′ adapter sequence for R2 |
| `-e 0.10` | Maximum adapter matching error rate: 10% |
| `--minimum-length 15` | Minimum retained **read** length of 15 nt |
| `-o`, `-p` | Trimmed output for R1 and R2, respectively |

**Adapter sequences:** The sequences above are from the lab's baseline pipeline. Different library preparation kits or sequencing protocols may require different sequences. Check your library preparation information and FastQC adapter findings, then adjust `-a` and `-A` if needed.

**Outputs:** paired trimmed FASTQs. Review the Cutadapt summary for retained reads and adapter matches before aligning. This baseline does **not** add a `-q` quality-trimming option.

## 3. Bowtie2 — align to hg38

**Purpose:** Align the trimmed paired reads to the human reference genome.

```bash
bowtie2 \
  -p "$THREADS" \
  --mm \
  -x "$GENOME_INDEX" \
  -1 "${OUTPUT_PREFIX}_R1.trimmed.fastq.gz" \
  -2 "${OUTPUT_PREFIX}_R2.trimmed.fastq.gz" \
  -S "${OUTPUT_PREFIX}.hg38.sam"
```

| Parameter | Meaning |
| --- | --- |
| `-p` | Alignment threads; the submitted Slurm script requests 10 |
| `--mm` | Memory-map the Bowtie2 index |
| `-x` | Prefix of the hg38 Bowtie2 index |
| `-1`, `-2` | Paired trimmed FASTQs |
| `-S` | SAM output filename |

**Output:** a SAM file and Bowtie2's alignment summary on standard error. Inspect alignment statistics. The source command does **not** specify a combined human/yeast reference, a custom sensitivity preset, or a MAPQ filter.

## 4. SAMtools — convert, sort, and index

**Purpose:** Convert the SAM alignment to a coordinate-sorted BAM and build an index for genomic access.

```bash
samtools view -@ "$THREADS" -b "${OUTPUT_PREFIX}.hg38.sam" \
  | samtools sort -@ "$THREADS" -o "${OUTPUT_PREFIX}.hg38.sorted.bam"

samtools index "${OUTPUT_PREFIX}.hg38.sorted.bam"
```

| Command/option | Meaning |
| --- | --- |
| `view -b` | Output BAM records |
| `sort` | Sort by genomic coordinate |
| `index` | Create the BAM index (`.bai`) |
| `-@` | Additional worker threads |

**Outputs:** `${OUTPUT_PREFIX}.hg38.sorted.bam` and its index. The source script deletes the intermediate SAM after successful processing. **No explicit MAPQ, duplicate, or mitochondrial filter** appears in these commands.

The sorted BAM is the common input to the remaining analyses. **Step 5 and step 6A do not depend on one another.**

## 5. deepTools — generate BigWig coverage

**Purpose:** Convert the sorted BAM into a genome-browser coverage track, scaled by CPM in this baseline.

```bash
BAM="${OUTPUT_PREFIX}.hg38.sorted.bam"
BW="${OUTPUT_PREFIX}.CPM.bw"

bamCoverage \
  -b "$BAM" \
  -o "$BW" \
  --normalizeUsing CPM \
  --binSize 10 \
  -p 8
```

| Parameter | Meaning |
| --- | --- |
| `-b` | Input BAM |
| `-o` | Output BigWig |
| `--normalizeUsing CPM` | deepTools CPM normalization |
| `--binSize 10` | Genomic bin width of 10 bp |
| `-p 8` | Eight processing threads, matching the BigWig Slurm script |

**Output:** a `.CPM.bw` track for each sample, suitable for genome-browser inspection.

**Later variant:** where spike-in calibration is used, the reference, counting method, scaling factors, and statistical normalization should be documented together.

## 6A. MACS2 — call enriched peaks

**Purpose:** Identify enriched regions from the sorted paired-end BAM.

```bash
BAM="${OUTPUT_PREFIX}.hg38.sorted.bam"
macs2 callpeak \
  -t "$BAM" \
  -f BAMPE \
  -g hs \
  -q 0.001 \
  --keep-dup all \
  --outdir "$SAMPLE_DIR/macs2" \
  -n "$SAMPLE"
```

| Parameter | Meaning |
| --- | --- |
| `-t` | Input sorted BAM |
| `-f BAMPE` | Use paired-end fragments |
| `-g hs` | MACS2 human effective-genome-size shortcut |
| `-q 0.001` | Peak-calling q-value threshold |
| `--keep-dup all` | Retain duplicate reads for peak calling |
| `--outdir` | Destination for peak files |
| `-n` | Prefix for result filenames |

**Outputs:** MACS2 peak files (including narrowPeak), summits, and logs. The supplied command does **not** specify an explicit control BAM or a broad-peak option. More target-specific peak-calling variants can be introduced later.

## 6B. DiffBind — differential binding

**Purpose:** Use the sample sheet, individual BAMs, and MACS2 narrowPeak files to count binding signal and compare experimental conditions.

Prepare a CSV sample sheet containing the experiment's sample IDs, conditions, replicates, and paths to the BAM and peak files. The exact columns and design must match the data being analyzed. Replace `samples.csv` with your own file.

```r
library(DiffBind)

samples <- read.csv("samples.csv", header=TRUE)
names(samples)
samples

tamoxifen <- dba(sampleSheet=samples, peakFormat="narrow")
tamoxifen <- dba.count(tamoxifen, bParallel=FALSE,
                       bRemoveDuplicates=TRUE,
                       bUseSummarizeOverlaps=TRUE)

myDBA <- dba.count(tamoxifen, peaks=NULL, score=DBA_SCORE_READS)
counts <- dba.peakset(myDBA, bRetrieve=TRUE,
                      writeFile="readscores.txt")
head(counts)

normCounts <- dba.peakset(tamoxifen, bRetrieve=TRUE,
                          DataType=DBA_DATA_FRAME)
write.csv(normCounts, "normalized_read_counts_all_samples.csv")

tamoxifen <- dba.normalize(tamoxifen)
norm <- dba.normalize(tamoxifen, bRetrieve=TRUE)
norm

tamoxifen <- dba.contrast(tamoxifen, categories=DBA_CONDITION,
                          minMembers=2)
tamoxifen <- dba.analyze(tamoxifen)

dba.show(tamoxifen, bContrasts=TRUE)
plot(tamoxifen)

tamoxifen.DB <- dba.report(tamoxifen, contrast=1, th=1)
write.csv(tamoxifen.DB, "Differential_analysis_using_diffbind.csv")
```

| Command/setting | Meaning |
| --- | --- |
| `dba(sampleSheet=..., peakFormat="narrow")` | Load sample metadata and MACS2 narrow peaks |
| `dba.count(...)` | Count reads across binding regions using the sample BAMs |
| `bParallel=FALSE` | Disable parallel processing |
| `bRemoveDuplicates=TRUE` | Request duplicate removal during DiffBind counting |
| `bUseSummarizeOverlaps=TRUE` | Use `summarizeOverlaps` for read counting |
| `peaks=NULL, score=DBA_SCORE_READS` | Set the binding matrix to show raw read counts without ordinarily recounting |
| `dba.peakset(..., bRetrieve=TRUE)` | Retrieve/export the binding matrix |
| `dba.normalize()` | Compute normalization using the installed version's defaults |
| `dba.contrast(..., categories=DBA_CONDITION, minMembers=2)` | Define condition-based comparisons requiring at least two samples per group |
| `dba.analyze()` | Fit the selected differential-binding model |
| `dba.report(..., contrast=1, th=1)` | Retrieve the first contrast, without a restrictive FDR cutoff |

**Outputs:** `readscores.txt`, `normalized_read_counts_all_samples.csv`, a contrast plot, and `Differential_analysis_using_diffbind.csv`.

**Notes:** The supplied code exports the file labeled `normalized_read_counts_all_samples.csv` *before* the explicit normalization call. Its values should be checked before treating it as a final normalized-count matrix. The defaults for normalization, region counting, and analysis method depend on the installed DiffBind version and configuration. The input sample sheet and program version were not supplied. For experiments using spike-in normalization, the DiffBind normalization method must be selected consistently with the experimental calibration strategy; the above code does not explicitly configure spike-in factors.

**Source:** Adapted from the lab bioinformatics lead's DiffBind R commands. The private input path was replaced with `samples.csv`, duplicate exploratory retrieval was consolidated, and a missing newline between the plot and report commands was restored. The scientific parameters were not intentionally changed.
