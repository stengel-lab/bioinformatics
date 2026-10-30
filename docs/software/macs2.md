# MACS2

MACS2 identifies enriched genomic intervals. The selected CUT&RUN worker uses paired-end fragment mode and narrow peaks without an explicit background BAM. A historical branch requests broad peaks with different thresholds and duplicate handling.

## Install

```bash
conda create --name learn-macs2 --override-channels \
  --channel conda-forge --channel bioconda --strict-channel-priority \
  python=3.10 'numpy<2' macs2=2.2.9.1
conda activate learn-macs2
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
macs2 --version
macs2 callpeak --help
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
macs2 callpeak -t INPUT.bam -f BAMPE [options]
```

## Common options

| Option / setting | Meaning |
|---|---|
| `-t` | Treatment alignment input. |
| `-f BAMPE` | Use observed paired-end fragments. |
| `-g hs` | Human effective-genome-size shortcut. |
| `--qvalue 0.001` | Observed significance threshold; not a replicate-reproducibility criterion. |
| `--keep-dup auto` | Caller-specific duplicate policy; does not rewrite/deduplicate the BAM. |
| `-n / --outdir` | Output prefix / directory. |
| `-c / --broad` | Optional control input / broad model; neither is enabled in this selected narrow example. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
macs2 callpeak -t align/control_A.hg38-only.sorted.bam -f BAMPE \
  -n control_A --outdir peaks/control_A -g hs --qvalue 0.001 --keep-dup auto
```

## Expected inputs and outputs

paired human BAM → narrowPeak, peak statistics XLS, summits BED and logs. BAMPE uses fragments; it is not an instruction to apply Tn5 shifts. `--keep-dup auto` is a caller policy, not a deduplicated BAM. Review target shape, controls, background and region artifacts. Historical broad output requires compatible downstream imports. Do not interpret absent peaks as proof of absent binding or loosen q-values solely to obtain more peaks.

## Documentation and lab notes

Installation notes: keep a candidate MACS2 environment separate from the core environment while checking Python/NumPy compiled dependencies and architecture. Do not replace it with MACS3 and retain the same method label. The [versioned option validator](https://raw.githubusercontent.com/macs3-project/MACS/v2.2.9.1/MACS2/OptValidator.py) and [calling source](https://raw.githubusercontent.com/macs3-project/MACS/v2.2.9.1/MACS2/callpeak_cmd.py) were consulted for BAMPE, effective-genome and duplicate behavior. The unknown executed lab version remains a gap.

**Function:** Enrichment peak calling. **Evidence:** [CR-S01 / CR-S17 / CR-S18](../assays/cut-and-run/sources.md).

**Observed version evidence:** Lab version not established. 2.2.9.1 is an external candidate for investigation, not a discovered version.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/02-alignment-and-peaks.md#stage-6-choose-a-peak-model) or [software catalog](index.md).
