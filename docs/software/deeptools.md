# deepTools

deepTools creates BigWig coverage (`bamCoverage`), binned signal matrices (`multiBigwigSummary`), sample PCA/correlation, and region-centered matrices/heatmaps/profiles (`computeMatrix`, `plotHeatmap`, `plotProfile`). Coverage and replicate figures are distinct from statistical differential-binding counts.

## Install

```bash
conda create --name learn-deeptools --override-channels \
  --channel conda-forge --channel bioconda --strict-channel-priority deeptools
conda activate learn-deeptools
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
bamCoverage --version
computeMatrix --version
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
bamCoverage -b INPUT.bam -o OUTPUT.bw [options]
```

## Common options

| Option / setting | Meaning |
|---|---|
| `-b / -o` | Input BAM / output BigWig for bamCoverage. |
| `--normalizeUsing CPM` | Scale by library depth; not spike calibration. |
| `--binSize 10` | 10-base coverage bins. |
| `--numberOfProcessors 4` | Worker count. |
| `--effectiveGenomeSize` | Required for some normalization modes; does not change CPM to RPGC. |
| `--scaleFactor` | External multiplier, only after its denominator is approved. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
mkdir -p tracks/cpm
bamCoverage -b align/control_A.hg38-only.sorted.bam \
  -o tracks/cpm/control_A.CPM.bw --normalizeUsing CPM --binSize 10 \
  --effectiveGenomeSize 2913022398 --numberOfProcessors 4
```

## Expected inputs and outputs

sorted/indexed BAM → BigWig; matched BigWigs/regions → matrices, tables and figures. Source spike coverage instead uses the combined BAM and `None` plus an external multiplier. No explicit `--extendReads` is set. Giving an effective genome size does not change CPM into RPGC. Historical heatmaps use region centers, ±2 kb and missing-as-zero; those are scientific display assumptions. Keep units, contigs, region sets, scales and replicate labels explicit.

## Documentation and lab notes

Installation notes: candidate `deeptools` in the Python core environment; compiled scientific and BigWig dependencies must resolve for the platform. Linux/macOS or WSL2 are proposed routes, not verified installations. Official references: [bamCoverage](https://deeptools.readthedocs.io/en/develop/content/tools/bamCoverage.html), [multiBigwigSummary](https://deeptools.readthedocs.io/en/3.5.6/content/tools/multiBigwigSummary.html), [computeMatrix](https://deeptools.readthedocs.io/en/3.5.6/content/tools/computeMatrix.html).

**Function:** Coverage, replicate QC and region figures. **Evidence:** [CR-S02 / CR-S15 / CR-S16](../assays/cut-and-run/sources.md).

**Observed version evidence:** Lab version not established; versioned 3.5.6 manuals are external references.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/03-normalization-and-qc.md#stage-9-make-coverage-tracks-with-an-explicit-denominator) or [software catalog](index.md).
