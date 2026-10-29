# 3. Normalization, coverage and replicate QC

Previous: [alignment and peaks](02-alignment-and-peaks.md) · Next: [differential binding](04-differential-and-interpretation.md)

**Review gate:** do not treat the historical spike-normalized outputs as quantitatively validated. The selected species-count expression and the identity of the calibration material require resolution first. This chapter reconstructs behavior and separates proposed corrections.

## Stage 8 — Audit spike counts before scaling

### Scientific purpose and assumptions

Sequencing more deeply increases read counts without necessarily increasing biological occupancy. Exogenous calibration can help measure global changes that a constant-total library assumption might hide, but only if spike input and recovery have a suitable relationship to the target material. Record when and how much spike was added, whether equal cell numbers were used, and whether the spike itself responds to the experimental treatment. Deliberate yeast calibration and incidental bacterial DNA are not interchangeable protocols ([original method](https://elifesciences.org/articles/21856), [improved CUT&RUN tools](https://elifesciences.org/articles/46314)).

**Inputs/tools:** indexed combined BAM, exact target/spike contig manifests, SAMtools `idxstats`, awk. **L, CR-S01/02:** sum column 3 from `idxstats` over a name regex. That column counts **mapped read-segments**, not paired fragments ([SAMtools manual](https://www.htslib.org/doc/samtools-idxstats.html)). Multiple/supplementary alignments and mate retention need separate review.

### Confirmed defect in the observed expression

The source regex begins `^(chrI|chrII|...|chrX|...|chrM|yeast_|sacCer)`. Human `chrX` and `chrM` satisfy it; lack of an end anchor also permits additional prefix matches. This is a code-level finding, not a claim about the magnitude of error in any unpublished dataset.

**Copy-ready synthetic demonstration — no real data:**

```bash
printf 'chrX\t1000\t100\t0\nchrM\t1000\t25\t0\nyeast_chrI\t1000\t50\t0\n' \
  | awk '$1 ~ /^(chrI|chrII|chrIII|chrIV|chrV|chrVI|chrVII|chrVIII|chrIX|chrX|chrXI|chrXII|chrXIII|chrXIV|chrXV|chrXVI|chrM|yeast_|sacCer)/ {s+=$3} END {print s+0}'
```

Expected output is `175`; true spike-only mapped segments in this toy example are `50`. Merely prefixing yeast names does not fix the expression if human `chrX` still matches.

**P — configured alternative, not the historical implementation:** after manually verifying that `spike.contigs.txt` lists only exact spike names present in this reference, use exact membership. This example deliberately retains the source's mapped-segment unit; it does not solve fragment counting or protocol validation.

```bash
samtools idxstats "$COMBINED_BAM" > "qc/${SAMPLE}.idxstats.tsv"
awk 'NR==FNR {spike[$1]=1; next} ($1 in spike) {s+=$3} END {print s+0}' \
  "$REF_DIR/spike.contigs.txt" "qc/${SAMPLE}.idxstats.tsv" \
  > "qc/${SAMPLE}.spike_mapped_segments.txt"
```

**Outputs/QC:** per-sample count, contig-level table, manifest hash, counting rule and reference hash. Review zero/very low spike counts, host/spike ambiguity, extreme scale factors, and variation among replicates. A finite positive count alone does not establish suitable calibration. Recompute all counts consistently if the rule changes; do not mix old regex counts with new exact-contig counts.

**Troubleshooting:** names alone cannot recover species identity from a reference with colliding contigs. Rebuild a uniquely named index or select another reviewed mapping strategy. **Output → next:** an approved, complete cohort count table; otherwise keep spike-based interpretation pending.

## Stage 9 — Make coverage tracks with an explicit denominator

### What the selected worker does

**L, CR-S02:** discovers samples for which both combined and human BAMs exist. It creates `spike_counts.tsv` and caches a `spike_median.txt` if the latter does not exist. Subsequent runs can reuse an old median while calculating fresh per-BAM denominators. A partial discovered cohort changes the median; existence is not evidence of sample completeness.

For approved counts \(S_i\), it uses:

```text
M = median of the selected cohort's spike mapped-segment counts
k_i = M / S_i                 (coverage multiplier)
d_i = S_i / M                 (intended count-model size factor)
```

The multiplier and size factor are reciprocals for a reason: a track is multiplied, while a count-model normalization denominator divides counts. For synthetic `S = 50, 100, 200`, `M = 100`, the coverage factors are `2, 1, 0.5` and the denominators are `0.5, 1, 2`. This algebra does not prove that DiffBind applied the factors as intended.

**Inputs/tools:** combined and human BAMs/indexes; reviewed cohort and scale factor; [deepTools](../../software/deeptools.md). Source version is not established. The following is a **review-gated reconstruction**, using `SCALE_FACTOR=2` only as a fictional numerical illustration. Replace it with the reviewed cohort calculation; never leave the toy value for a real sample.

```bash
SCALE_FACTOR=2
bamCoverage -b "$COMBINED_BAM" -o "tracks/spike/${SAMPLE}.spikeNorm.bw" \
  --normalizeUsing None --scaleFactor "$SCALE_FACTOR" --binSize 10 \
  --effectiveGenomeSize 2913022398 --numberOfProcessors 4
bamCoverage -b "$HUMAN_BAM" -o "tracks/cpm/${SAMPLE}.CPM.bw" \
  --normalizeUsing CPM --binSize 10 \
  --effectiveGenomeSize 2913022398 --numberOfProcessors 4
```

| Choice | Meaning and limitation |
|---|---|
| `--binSize 10` | Resolution of the output coverage bins; affects file size and smoothing |
| `None` plus `--scaleFactor` | External multiplicative scaling, not CPM or RPGC |
| `CPM` | Library-depth scaling of the human BAM; may conceal a global target-associated change |
| `--effectiveGenomeSize 2913022398` | Observed argument; supplying it does not turn `None`/CPM into RPGC normalization |
| Combined BAM for spike track | Individual spike-scaled BigWigs may contain yeast contigs; this is the actual selected input |
| No `--extendReads` | Do not describe these tracks as validated full-fragment occupancy coverage; compare extension semantics with the installed deepTools version |

The source does not add duplicate, MAPQ, blacklist or mitochondrial filters at this stage. The earlier BAM choices therefore determine what contributes. See the [bamCoverage manual](https://deeptools.readthedocs.io/en/develop/content/tools/bamCoverage.html). **P:** using the human BAM with the same approved spike factor would produce human-only spike tracks; record this as a changed input, not a correction already present in the source.

**Outputs:** per-sample spike-scaled and CPM BigWigs. Tutorial paths `tracks/spike` and `tracks/cpm` replace the original worker's directory names only. **QC:** inspect contigs/lengths, nonempty signal, common browser y-axis ranges and extreme factors. Verify normalized values at a synthetic or known reference interval in a future execution exercise. No signal can indicate reference mismatch, failed scaling, empty input or a true lack of enrichment.

**Operational problem:** `set -e` with `SUCCESS_COUNT=0; ((SUCCESS_COUNT++))` can terminate the worker on the first successful output check, because arithmetic evaluates the old zero value and returns status 1. File presence may thus coexist with a failed scheduler job. Fixing the private worker is outside this milestone; a future implementation should use a safe increment and explicit completion checks. Review [D18](decisions.md#d18-scheduler-restarts-and-exit-status).

**Output → next:** retain each replicate's tracks separately, with units and normalization recorded. Do not average yet.

## Stage 10 — Assess replicates and reproducible regions

### Signal concordance

**Scientific purpose:** determine whether independently prepared biological replicates support similar signal structure. Global bin correlations are affected by background, sequencing depth, region choice and extreme loci. They do not prove reproducible peaks or remove batch effects.

**Inputs/tools:** individual, consistently normalized BigWigs; deepTools. **Historical reconstruction, CR-S15:** 10 kb genomic bins followed by PCA and Spearman correlation.

```bash
multiBigwigSummary bins \
  -b tracks/cpm/control_A.CPM.bw tracks/cpm/control_B.CPM.bw \
     tracks/cpm/treated_A.CPM.bw tracks/cpm/treated_B.CPM.bw \
  --labels control_A control_B treated_A treated_B \
  --binSize 10000 --numberOfProcessors 4 -o qc/replicate_bins.npz
plotPCA -in qc/replicate_bins.npz -o qc/track_PCA.pdf \
  --outFileNameData qc/track_PCA_coordinates.tsv
plotCorrelation -in qc/replicate_bins.npz --corMethod spearman \
  --whatToPlot heatmap -o qc/track_correlation.pdf \
  --outFileCorMatrix qc/track_correlation.tsv
```

The source requests 16 processors here; four is an explicit teaching resource adjustment. Keep sample order/labels consistent and use human-only matched contigs for cross-sample comparison. **Outputs:** bin matrix, coordinates, correlation matrix and plots. Investigate outliers with raw QC and metadata; do not drop a replicate solely because it opposes an expected biological story.

### Peak reproducibility is a separate question

**U:** the selected chain does not establish a validated biological-replicate consensus/IDR procedure. Downstream “shared” peaksets in **CR-S09** intersect significant **contrasts/timepoints**, not independently called replicate peaks. They cannot substitute for replicate reproducibility.

**P:** predefine a target-appropriate rule using replicate overlap, signal support and controls. A union retains any replicate's regions; an intersection can miss genuine weak peaks and narrow shifted summits; a reproducibility model such as IDR needs its own suitability review. nf-core's `replicate_threshold=1` default is not a requirement for agreement by two replicates. Record overlap geometry and the number of required replicates explicitly.

**Output → next:** a replicate review record and a justified analysis universe. DiffBind counts must still use the individual BAMs. No exclusion or reproducibility cutoff is validated by this documentation draft.

## Stage 11 — Average approved tracks and view loci

**Purpose:** produce readable condition summaries after checking individual replicates. Averaging loses replicate variation and cannot increase the number of independent observations.

**Inputs/tools:** same-normalization replicate BigWigs, human chromosome sizes, [WiggleTools](../../software/wiggletools.md), [UCSC utilities](../../software/ucsc-track-tools.md), [IGV](../../software/igv.md). **L, CR-S03:** groups replicate names matching `^(.+)_([A-Za-z]+)$`, requires at least two tracks, and computes an equal-weight arithmetic mean. Review membership manually; naming is not design metadata.

**Configured reconstruction for two fictional replicates:**

```bash
mkdir -p tracks/means
wiggletools write_bg tracks/means/control.raw.bedGraph mean \
  tracks/cpm/control_A.CPM.bw tracks/cpm/control_B.CPM.bw
awk 'NR==FNR {human[$1]=1; next} ($1 in human)' \
  "$HUMAN_SIZES" tracks/means/control.raw.bedGraph \
  | LC_ALL=C sort -k1,1 -k2,2n > tracks/means/control.mean.bedGraph
bedGraphToBigWig tracks/means/control.mean.bedGraph "$HUMAN_SIZES" \
  tracks/means/control.mean.CPM.bw
```

The human-contig step also removes yeast from means of combined-reference spike tracks. Check how missing intervals/contigs are handled before comparing means. A historical worker nested pairwise BigWig means; with three replicates this can yield weights ¼, ¼, ½ rather than equal thirds. Use explicit all-replicate means when reconstructing the selected averaging worker.

**QC/outputs:** sorted bedGraph and BigWig, grouping manifest, expected number of tracks and comparable units. Converter failures often indicate unsorted/overlapping intervals or chromosome-size mismatch. Keep intermediate bedGraph until inspected. In IGV load the matching genome, individual replicates, mean tracks and approved peaks; apply common scales and inspect background as well as positive loci. CPM and spike-scaled tracks need clear separate labels.

**Output → next:** visualization summaries only. Continue to [per-replicate count modeling](04-differential-and-interpretation.md), which does not consume these averages.
