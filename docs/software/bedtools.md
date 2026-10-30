# BEDTools

BEDTools compares genomic intervals and alignment overlaps. The selected CUT&RUN worker removes whole narrowPeak intervals overlapping a blacklist and counts BAM records overlapping peaks; downstream helpers merge and intersect derived peak sets.

## Install

```bash
conda create --name learn-bedtools --override-channels \
  --channel conda-forge --channel bioconda --strict-channel-priority bedtools
conda activate learn-bedtools
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
bedtools --version
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
bedtools <intersect|merge> [options]
```

## Common options

| Option / setting | Meaning |
|---|---|
| `intersect -a / -b` | Primary intervals / intervals used for comparison. |
| `intersect -v` | Keep A intervals with no overlap in B. |
| `intersect -u` | Report each overlapping A interval once. |
| `intersect -ubam` | Write uncompressed BAM for a downstream pipe. |
| `merge -i -` | Read sorted intervals from stdin and merge overlapping or book-ended intervals. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
bedtools intersect -v -a peaks/control_A_peaks.narrowPeak -b refs/hg38.blacklist.bed \
  > peaks/control_A.filtered.narrowPeak
LC_ALL=C sort -k1,1 -k2,2n regions/differential.bed \
  | bedtools merge -i - > regions/differential.merged.bed
```

## Expected inputs and outputs

BED-like intervals → retained/merged intervals; BAM overlap can emit BAM or BED depending on options. `-v` emits nonoverlapping A records; `-u` emits each overlapping A record once. Peak-only filtering does not clean the BAM or tracks. Merge changes boundaries and discards per-peak metadata unless explicitly aggregated. Source differential CSV→BED conversion needs a one-based/zero-based review. An empty blacklist-filtered output should trigger review, not automatic fallback to unfiltered peaks.

## Documentation and lab notes

Installation notes: candidate `bedtools` in the core environment on Linux/macOS or WSL2. Confirm compatible assembly/contig naming and coordinate conventions before use. Official semantics: [intersect](https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html) and [merge](https://bedtools.readthedocs.io/en/latest/content/tools/merge.html).

**Function:** Genomic interval operations. **Evidence:** [CR-S01 / CR-S09](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established in selected evidence.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/02-alignment-and-peaks.md#stage-7-review-suspect-regions-and-calculate-enrichment-qc) or [software catalog](index.md).
