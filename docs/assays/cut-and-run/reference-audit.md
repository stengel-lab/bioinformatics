# Reference-aware spike counting and downstream trace

**Scientific review, 2026-10-30.** Read [D05–D09](decisions.md#d05-reference-and-mitochondrial-identity) and the [source registry](sources.md). This page distinguishes a proven matching defect from unverified historical exposure. The new counter is an educational text-table example, not an alignment or normalization pipeline.

## What reference construction can be recovered?

The selected worker points Bowtie2 at a combined index labeled `hg38-sacCer3`; it does not build the index. A content search of reviewed scripts/documents and archived text evidence found no `bowtie2-build` recipe or `bowtie2-inspect` record. Matching genome FASTAs, index binaries, a reference checksum manifest and the actual human-contig whitelist were not located in the supplied source corpus. The [proposed construction example](installation.md#reference-files-and-indices) is therefore **not** a recovered historical recipe.

This prevents confirmation of the exact FASTA release, chromosome names, lengths, masking, alternate sequences and species partition. No remote reference directory or cluster was accessed. A `hg38-sacCer3` filename is evidence of intent, not sequence identity.

When the actual reference becomes available, a read-only audit should collect the following. These are **configured inspection commands, not executed here**, using a new metadata directory outside the original source archive:

```bash
mkdir -p metadata
bowtie2-inspect -s "$BOWTIE2_INDEX" > metadata/index-summary.txt
bowtie2-inspect -n "$BOWTIE2_INDEX" > metadata/index-contig-names.txt
samtools view -H "$COMBINED_BAM" > metadata/alignment-header.sam
samtools idxstats "$COMBINED_BAM" > metadata/combined.idxstats.tsv
```

Check the index sequence dictionary against BAM `@SQ` names/lengths, then against a manifest derived from the **actual input species FASTAs and build record**. Compare sequence digests where available, and record hashes of the index files, FASTAs, whitelist and manifest. Name/length agreement is necessary but cannot prove identical sequence. A stale BAM index also needs independent identity/integrity review. See the [Bowtie2 inspection manual](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#the-bowtie2-inspect-index-inspector) and [idxstats contract](https://www.htslib.org/doc/samtools-idxstats.html).

If host and spike contigs have colliding names, a post hoc regex cannot repair the species assignment. Recover the build provenance and resolve reference identity before counting; uniquely prefixing a future rebuild is a proposed change requiring comparison with the old mapping.

## Confirmed matching behavior versus actual exposure

CR-S01:301–303 and CR-S02:32,107–108,154–155 use the same prefix expression. Its alternatives include `chrX`, `chrM`, `yeast_` and `sacCer`, with no final boundary. The following classifications are mathematical properties of that expression:

| Dictionary name | Hypothetical role | Old expression matches? |
|---|---|---|
| `chrX` | human | Yes — false spike assignment |
| `chrM` | human | Yes — false spike assignment |
| `chrX_hg38` | human | Yes — the prefix still matches |
| `hg38_chrX` | human | No |
| `yeast_chrI` | yeast | Yes |
| `Scer_chrI` | yeast | No — an unrecognized naming scheme |

Thus the species rule is not reference-aware. Whether **the historical BAM actually contains host names that match** is still unconfirmed. Prefixing yeast alone would not protect an unprefixed human `chrX`. Adding an end anchor to `chrX`/`chrM` alone would not resolve their species ambiguity either.

## Exactly where the count propagates

| Consumer | Selected source behavior | What a bad count can change |
|---|---|---|
| Per-sample count | CR-S01:301–303 writes `_spike_count.txt` from mapped segments matching the regex | Stored calibration count |
| Shared table/median | CR-S02:94–125 reads per-sample counts if present, otherwise recounts; creates `spike_counts.tsv`/`spike_median.txt` only when the median file is absent | Cached per-sample counts, median/cohort provenance |
| Spike BigWig | CR-S02:151–179 skips an existing track; otherwise **freshly recounts** and multiplies coverage by cached median / fresh count | Sample-specific spike-scaled track amplitude |
| CPM BigWig | CR-S02:184–195 uses human BAM and CPM, without the spike table | No direct spike-factor rescaling; operational/sample-selection failures can still affect whether it is produced |
| Narrow MACS2 peaks | CR-S01 calls peaks before writing the spike count; no spike factor is passed | No direct change to the original selected peak calls |
| Standard DiffBind | CR-S05:445–463 analyzes the counted object before the spike branch | No direct use of the spike factor in this model; an upstream interruption can prevent later outputs |
| Spike DiffBind | CR-S05:466–550 reads the **table**, matches IDs, forms count/median, retrieves factors, then analyzes | Model size factors and resulting normalized counts/effects/inference, conditional on the actual contaminated input |
| Downstream summaries | Track means, spike-based heatmaps or spike-model region/motif selection inherit their parent artifact | Derived figures/regions can require review even when raw alignments/peaks do not |

Two paths can disagree: track generation can use a fresh denominator while DiffBind consumes an older table; reused tracks can also retain older factors. A corrected per-sample file alone does not update every dependent artifact.

**Historical evidence boundary:** 18 saved `.out`/`.err` logs were inspected read-only. They include a narrow MACS2 invocation matching the documented option pattern and R runs that logged spike-table consumption/factors. They do **not** include a completed spike-count phase, coverage-worker trace, or reference sequence dictionary. Consequently, the available logs establish downstream factor use but not that those factors were generated by this regex against a susceptible reference. No particular historical normalization result is declared affected.

## A common median is not a sample-dependent error

For one cohort, let `S_i` be its accepted spike count and `M` a common positive median:

```text
coverage multiplier k_i = M / S_i
model size factor   d_i = S_i / M
k_i / k_j = S_j / S_i
d_i / d_j = S_i / S_j
```

Changing only a common `M` changes the common scale, not these relative ratios. It is therefore incorrect to claim that a different median alone necessarily reverses within-cohort relative normalization. Mixed cached/new medians across artifacts, stale per-sample denominators, or counts `S_i + host_i` can change relative comparisons. Common rescaling can still alter displayed units and some downstream summaries; inspect model state before claiming statistical equivalence.

## Proposed exact-role counting example

The [downloadable Python example](examples/count_reference_segments.py) reads a reviewed manifest and an already exported idxstats table. It never opens BAMs, launches tools, changes reference names, chooses a calibration protocol or computes model factors.

Manifest columns are exactly `contig`, `length`, `role`, TAB-separated. Every reference contig must appear exactly once with its actual length and one of `target`, `spike`, `exclude`. Both target and spike roles must exist. Roles come from source FASTA provenance; **the program cannot verify a biologically incorrect manifest**. Mitochondrial/spike-organelle inclusion is an explicit manifest decision, not a prefix heuristic.

**Copy-ready synthetic demonstration**, from the repository root; all names, lengths and counts are fictional:

```bash
mkdir -p review-demo
printf 'contig\tlength\trole\nchrX\t1000\ttarget\nchrM\t1000\ttarget\nyeast_chrI\t1000\tspike\n' \
  > review-demo/reference-roles.tsv
printf 'chrX\t1000\t100\t0\nchrM\t1000\t25\t0\nyeast_chrI\t1000\t50\t0\n*\t0\t0\t3\n' \
  > review-demo/combined.idxstats.tsv
python docs/assays/cut-and-run/examples/count_reference_segments.py \
  --manifest review-demo/reference-roles.tsv --idxstats review-demo/combined.idxstats.tsv
```

Expected JSON has target mapped segments **125**, spike mapped segments **50**, excluded mapped segments **0**, and unmapped segments **3**, plus input hashes. The old regex would sum **175** as spike. The example requires the complete reference dictionary and idxstats `*` summary row; it rejects unknown/missing/duplicate contigs, length disagreement, invalid roles, malformed tables and negative/noninteger counts. It accepts and explicitly flags a zero spike count for diagnosis; a normalization consumer must reject zero/nonfinite factors. A positive count is not a “calibration validated” flag.

**Unit remains mapped read-segments.** Alignments to multiple places or retained supplementary records may be counted more than once; fragments are not silently substituted. Changing to complete-fragment counting needs a separate pair/MAPQ/secondary/duplicate policy and comparison. Reconcile this unit with the BAM filters and experimental protocol before interpreting scale factors.

Seven synthetic test methods cover reference classification, malformed/incomplete inputs, zero counts, exact input hashes, CLI failure behavior and input preservation. These tests validate a text-table contract only. They do not verify the historical reference, BAM correctness or biological calibration. No real sample counts were processed by this example during review.
