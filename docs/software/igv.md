# Integrative Genomics Viewer (IGV)

**Function:** Interactive genomic visualization. **Evidence:** [CR-S02 / CR-S03 produce browser-ready tracks; viewing is an educational follow-up.](../assays/cut-and-run/sources.md).

**Observed version evidence:** No IGV version established for this selected processing chain.

IGV displays alignments, coverage and annotation at genomic loci. Use it to inspect whether numerical summaries reflect plausible local signal, artifacts or reference mismatches. It is not a peak caller or differential-binding model.

**Installation:** install a platform-appropriate desktop release using the [official documentation](https://igv.org/doc/desktop/). Native Windows/macOS/Linux viewing can accompany analysis run in WSL2 or on HPC. Runtime requirements depend on the release; follow its packaged Java instructions rather than assuming the source cluster provides them.

**Basic use (GUI):** select the exact genome assembly, load indexed human BAMs and the CPM or approved spike BigWigs, then load approved BED/peak intervals. Add biological replicates before condition means. Set comparable y-axis ranges for tracks being compared, and retain a separate label for each normalization mode.

**Input → output:** BAM/BAI, BigWig and intervals → interactive views and optional snapshots. Check chromosome naming/lengths, positive/negative regions, background and excluded suspect regions. Combined-reference spike tracks can contain contigs not in the human genome view. An attractive snapshot at one locus is not a genome-wide reproducibility result. Publish snapshots only from permitted data with nonsensitive labels and documented scales.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/03-normalization-and-qc.md#stage-11-average-approved-tracks-and-view-loci) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
