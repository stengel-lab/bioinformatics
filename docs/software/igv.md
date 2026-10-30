# Integrative Genomics Viewer (IGV)

IGV displays alignments, coverage and annotation at genomic loci. Use it to inspect whether numerical summaries reflect plausible local signal, artifacts or reference mismatches. It is not a peak caller or differential-binding model.

## Install

Download the desktop installer for your operating system from the [official IGV site](https://igv.org/doc/desktop/). Install its recommended runtime, launch IGV, and choose your genome.

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

Open **Help → About** and record the version. Load a permitted test BigWig with the matching genome, navigate to a known covered interval, and confirm the track renders.

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
Choose genome → load individual tracks and peaks → inspect loci and common scales
```

## Common options

| Option / setting | Meaning |
|---|---|
| `Genome selection` | Use the assembly matching the alignments and tracks. |
| `Data range` | Use a common y-axis for tracks whose amplitudes are compared. |
| `Autoscale` | Independent autoscaling can hide amplitude differences; inspect the scale labels. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

**Basic use (GUI):** select the exact genome assembly, load indexed human BAMs and the CPM or approved spike BigWigs, then load approved BED/peak intervals. Add biological replicates before condition means. Set comparable y-axis ranges for tracks being compared, and retain a separate label for each normalization mode.

## Expected inputs and outputs

BAM/BAI, BigWig and intervals → interactive views and optional snapshots. Check chromosome naming/lengths, positive/negative regions, background and excluded suspect regions. Combined-reference spike tracks can contain contigs not in the human genome view. An attractive snapshot at one locus is not a genome-wide reproducibility result. Publish snapshots only from permitted data with nonsensitive labels and documented scales.

## Documentation and lab notes

Installation notes: install a platform-appropriate desktop release using the [official documentation](https://igv.org/doc/desktop/). Native Windows/macOS/Linux viewing can accompany analysis run in WSL2 or on HPC. Runtime requirements depend on the release; follow its packaged Java instructions rather than assuming the source cluster provides them.

**Function:** Interactive genomic visualization. **Evidence:** [CR-S02 / CR-S03 produce browser-ready tracks; viewing is an educational follow-up.](../assays/cut-and-run/sources.md).

**Observed version evidence:** No IGV version established for this selected processing chain.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/03-normalization-and-qc.md#stage-11-average-approved-tracks-and-view-loci) or [software catalog](index.md).
