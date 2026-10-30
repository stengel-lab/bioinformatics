# WiggleTools

WiggleTools performs arithmetic on genomic signal tracks. The selected averaging worker uses one mean operation over all matched replicates, producing an intermediate bedGraph before human-contig selection and UCSC conversion. A mean is a display summary, not an independent sample.

## Install

```bash
conda create --name learn-wiggletools --override-channels \
  --channel conda-forge --channel bioconda --strict-channel-priority wiggletools
conda activate learn-wiggletools
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
command -v wiggletools
# Run wiggletools without arguments to inspect its usage; it may exit nonzero.
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
wiggletools write_bg OUTPUT.bedGraph mean INPUT1.bw INPUT2.bw ...
```

## Common options

| Option / setting | Meaning |
|---|---|
| `write_bg` | Write a bedGraph result. |
| `mean` | Arithmetic mean over all following input tracks; include all intended replicates in one operation. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
mkdir -p tracks/means
wiggletools write_bg tracks/means/control.raw.bedGraph mean \
  tracks/cpm/control_A.CPM.bw tracks/cpm/control_B.CPM.bw
```

## Expected inputs and outputs

replicate BigWigs in the same units → arithmetic-mean bedGraph. Sort/filter/convert with [UCSC utilities](ucsc-track-tools.md) as in the tutorial. Review missing interval behavior and exact group membership. Sequentially averaging a prior mean with a third replicate need not give equal thirds; the selected all-replicate operation avoids that historical weighting ambiguity. Preserve individual tracks for QC.

## Documentation and lab notes

Installation notes: optional candidate package `wiggletools`; check native dependencies/build availability. The [maintainer repository](https://github.com/Ensembl/WiggleTools) describes operations and build dependencies. The source activates an environment named `genomics`, which is not an exported specification.

**Function:** Track arithmetic. **Evidence:** [CR-S03](../assays/cut-and-run/sources.md).

**Observed version evidence:** Not established in selected evidence.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/03-normalization-and-qc.md#stage-11-average-approved-tracks-and-view-loci) or [software catalog](index.md).
