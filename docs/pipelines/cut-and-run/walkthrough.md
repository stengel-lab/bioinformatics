# CUT&RUN: baseline command walkthrough

## Before starting

Have paired FASTQ files, an hg38 Bowtie2 index, and FastQC, Cutadapt, Bowtie2, SAMtools, deepTools, and MACS2 available in the appropriate environments. An [hg38 reference-resource guide](../../setup/references/hg38.md) explains what needs to be documented; the **exact FASTA/index build used by the lab remains to be verified**. Tool installation pages will be added after we agree on their format.

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

**Later variant:** where spike-in calibration is used, the reference, counting method, scaling factors, and statistical normalization should be documented together. No spike-in command is established by these three source files.

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

**Outputs:** MACS2 peak files (including narrowPeak), summits, and logs. The supplied command does **not** specify an explicit control BAM or a broad-peak option. More target-specific peak-calling variants can be introduced later with the bioinformatics lead's approval.

## 6B. DiffBind — compare conditions (to be completed)

**Goal:** Use individual samples' sorted BAMs, MACS2 peak files, replicate assignments, and experimental design to quantify binding changes between conditions.

**Expected inputs:** BAMs, peaks, and a sample sheet specifying conditions/replicates. **Expected outputs:** differential binding results with estimated effects and statistical significance.

**Not yet specified by these source scripts:** the canonical DiffBind commands, consensus peak strategy, counting options, design/contrasts, normalization factors, and export format. We will add the actual commands once the lab bioinformatics lead supplies or approves them. BigWig tracks are **not** the input to DiffBind.

## Source-of-truth boundary

The three supplied source scripts govern steps 1–5 and 6A. Their Slurm array sizes, resource allocations, and file-discovery loops are *execution wrappers*, not intrinsic scientific processing parameters. No uploaded script yet establishes step 6B.

This draft does not reproduce private source paths, assume unknown software versions, or silently combine commands from the previous archived tutorial.
