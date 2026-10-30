# UCSC track utilities

The UCSC `bedGraphToBigWig` utility converts numeric genomic intervals into an indexed, compact browser format. The selected mean-track worker uses it after sorting and restricting intervals to human chromosome names. The tutorial does not imply every UCSC binary is a workflow dependency.

## Install

```bash
conda create --name learn-ucsc-track-tools --override-channels \
  --channel conda-forge --channel bioconda --strict-channel-priority ucsc-bedgraphtobigwig
conda activate learn-ucsc-track-tools
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
command -v bedGraphToBigWig
# Run bedGraphToBigWig without arguments for usage; a nonzero exit is expected.
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
bedGraphToBigWig INPUT.bedGraph CHROM.sizes OUTPUT.bw
```

## Common options

| Option / setting | Meaning |
|---|---|
| `bedGraphToBigWig` | Three positional arguments: sorted bedGraph, chromosome sizes, output BigWig. No normalization is added. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
LC_ALL=C sort -k1,1 -k2,2n tracks/means/control.mean.bedGraph \
  > tracks/means/control.mean.sorted.bedGraph
bedGraphToBigWig tracks/means/control.mean.sorted.bedGraph refs/human.chrom.sizes \
  tracks/means/control.mean.CPM.bw
```

## Expected inputs and outputs

sorted, nonoverlapping zero-based bedGraph plus matching chromosome sizes → BigWig. Wrong assembly names, out-of-bounds intervals or overlap can cause conversion errors. A valid BigWig format does not prove the values have appropriate normalization. Keep units and contributing replicates in a sidecar record and inspect the file in a matching-reference [browser](igv.md).

## Documentation and lab notes

Installation notes: optional candidate package `ucsc-bedgraphtobigwig`, or an appropriate binary from the [UCSC BigWig documentation](https://genome.ucsc.edu/goldenpath/help/bigWig.html). Match OS/architecture; WSL2 uses Linux builds. Retain executable provenance, checksums and usage/license terms as appropriate.

**Function:** Browser track formats. **Evidence:** [CR-S03](../assays/cut-and-run/sources.md).

**Observed version evidence:** Executable versions not established.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/03-normalization-and-qc.md#stage-11-average-approved-tracks-and-view-loci) or [software catalog](index.md).
