# 2. Alignment, filtering and peak calling

Previous: [reads and QC](01-design-and-reads.md) · Next: [normalization and replicate QC](03-normalization-and-qc.md)

**Status:** configured reconstructions, not an executed or validated analysis. Define the Chapter 1 variables and prepare the [references](installation.md#reference-files-and-indices). **L** below refers to **CR-S01** unless another source is named.

## Stage 5 — Map paired reads and separate human alignments

### Why align to a combined reference?

Mapping against human plus yeast allows the selected workflow to retain target-genome alignments and estimate exogenous alignment abundance from one BAM. This strategy depends on disjoint, known contig names and on how conserved or ambiguous sequences map. A read assigned MAPQ 30 against a combined reference is not automatically a species-specific fragment. The [nf-core comparison](methods-comparison.md) describes its separate-index approach.

**Inputs/tools:** trimmed paired FASTQ, the combined Bowtie2 index, human-contig BED; [Bowtie2](../../software/bowtie2.md), [SAMtools](../../software/samtools.md). Versions of these two programs are not established in the selected evidence. The source requests 16 CPUs, 64 GB and 24 hours; these are not measured requirements.

**How alignment works:** Bowtie2 uses an indexed reference to find candidate matches for read segments, then evaluates extended alignments with mismatches/gaps and paired-end geometry. Pairing supplies information beyond either mate alone. Conserved human/yeast sequence can create competing placements in the combined index. MAPQ reflects uncertainty under that search/scoring model; filtering on it selects records but does not repair a wrong reference or recover a lost mate. The actual index construction remains [unrecovered](reference-audit.md#what-reference-construction-can-be-recovered).

**What sorting/indexing accomplish:** coordinate sorting orders existing alignment records; indexing builds a lookup for reference regions. Neither operation improves the alignment or proves species identity. Check the BAM header/dictionary and the complete contig manifest before interpreting indexed counts.

### Observed alignment and MAPQ filtering

**Configured reconstruction:**

```bash
set -o pipefail
bowtie2 -p "$THREADS" --mm -x "$BOWTIE2_INDEX" \
  -1 "$TRIM_R1" -2 "$TRIM_R2" \
  --no-mixed --no-discordant \
  --rg-id "$SAMPLE" --rg "SM:$SAMPLE" \
  2> "qc/${SAMPLE}.bowtie2.log" \
  | samtools view -b -q 30 -F 0x4 -@ "$((THREADS/2))" - \
  | samtools sort -@ "$((THREADS/2))" -m 2G -o "$COMBINED_BAM" -
samtools index -@ "$THREADS" "$COMBINED_BAM"
samtools flagstat "$COMBINED_BAM" > "qc/${SAMPLE}.flagstat.txt"
```

`pipefail` and a named alignment log are teaching safeguards. Paths are aliases. The alignment/filter/sort options reproduce the selected command.

| Parameter | Meaning |
|---|---|
| `-1`, `-2` | Paired trimmed read files |
| `--mm` | Memory-mapped index access; filesystem behavior needs local assessment |
| `--no-mixed --no-discordant` | Suppress unpaired fallback and discordant pair alignment; this does not define every desired post-alignment record filter |
| `--rg-id`, `SM` | Read-group identity and sample tag; preserve sample identity for downstream tools |
| `view -q 30` | Retain alignments with mapping quality at least 30 |
| `-F 0x4` | Exclude records flagged unmapped |
| `sort -m 2G` | Approximate memory per sorting thread, not total job memory |

**Important omissions:** the source does not explicitly set `--very-sensitive`, `--dovetail`, local/end-to-end mode, minimum/maximum insert size, or `-f 2`. It does not explicitly remove secondary, supplementary, duplicate or mitochondrial records. Do not silently add these and call the result the same workflow. Bowtie2 defaults depend on the installed version; review the [official paired-end definitions](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml).

Per-alignment MAPQ filtering can retain only one mate of a pair. A proper-pair flag alone does not establish that both records remain in a filtered BAM. **P:** measure complete retained pairs and decide a fragment-aware filtering policy before calling fragment-based statistics validated. Bowtie2's restriction on dovetailing also matters for very short inserts; changing it requires a documented comparison.

**Intermediate/output:** coordinate-sorted, indexed **combined** BAM. The original directory called `spikein_outputs` contains human plus yeast alignments; it is not a spike-only BAM. No raw unsorted BAM is retained by this streamed version; some earlier workers did retain one.

### Human-only extraction

**Configured reconstruction:**

```bash
samtools view -b -@ "$THREADS" -L "$HG38_CONTIGS_BED" "$COMBINED_BAM" \
  | samtools sort -@ "$((THREADS/2))" -m 2G -o "$HUMAN_BAM" -
samtools index -@ "$THREADS" "$HUMAN_BAM"
samtools quickcheck -v "$COMBINED_BAM" "$HUMAN_BAM"
samtools idxstats "$COMBINED_BAM" > "qc/${SAMPLE}.idxstats.tsv"
```

`-L` keeps alignments overlapping intervals in the supplied BED. A whole-contig BED implements human-contig selection only if its contents are correct. The actual reference BED has not been publication-reviewed or supplied. Human `chrM` may be included; “human-only” does not mean “nuclear-only.”

**QC:** inspect headers/contig lengths, mapping summary, mapped pairs, MAPQ distribution, human/yeast assignments, mitochondrial fraction and fragment-size distributions. Compare samples before normalizing. `quickcheck` checks basic file integrity; it does not scan every alignment or establish proper pairing. Retain a separate metric for duplicate-marked alignments if duplicates are assessed; the source does not perform a validated mark-duplicates stage.

**Troubleshooting:** missing contigs indicate mismatched assembly/naming or an incorrect whitelist. Very low mapping can reflect adapters, species, reference or library failure. CPU oversubscription is possible because Bowtie2 and both SAMtools processes run concurrently. Inspect peak memory and temporary disk before scaling up. **Output → next:** indexed human BAM for peaks and DiffBind; combined BAM for the currently observed spike count/track branch.

## Stage 6 — Choose a peak model

### Scientific purpose

Peak calling asks where enrichment is distinguishable from a caller's background model. A peak list is an interval selection, not a table of biological replicate measurements. Transcription-factor binding is often focal, while some chromatin marks form broader domains; target biology and controls must drive the choice. Neither target class guarantees one peak shape.

**How the model works:** MACS compares fragment pileup with an estimated background using a Poisson enrichment model and corrects significance across tested positions/regions. With a suitable control, background can reflect experimental biases; without `-c`, a background is still estimated from the treatment/reference assumptions rather than measured in an independent negative-control library. A small q-value cannot distinguish an antibody-specific biological signal from every systematic artifact. Exact background calculation is version-dependent; the [MACS2 implementation](https://github.com/macs3-project/MACS/blob/v2.2.9.1/MACS2/callpeak_cmd.py) is an external reference, not an established lab version.

**Inputs/tools:** human BAM; [MACS2](../../software/macs2.md). Version is unspecified in the selected sources. Historical scripts show alternatives but do not identify a universally approved caller. The selected command has **no `-c` background-control BAM**.

**Configured narrow-peak reconstruction, CR-S01 lines 228–235:**

```bash
macs2 callpeak -t "$HUMAN_BAM" -f BAMPE -n "$SAMPLE" \
  --outdir "peaks/$SAMPLE" --keep-dup auto -g hs --qvalue 0.001
```

| Option | Interpretation |
|---|---|
| `-f BAMPE` | Use paired-end fragments from BAM; verify valid retained pairs |
| `--keep-dup auto` | MACS2's automatic duplicate policy, not identical to keeping all duplicates or removing them from the BAM |
| `-g hs` | MACS2 human effective-genome preset; upstream MACS2 2.2.9.1 uses 2.7 × 10⁹, not the coverage worker's 2,913,022,398 |
| `--qvalue 0.001` | Observed stringent q-value cutoff; not a universal CUT&RUN quality criterion |
| No `--broad`, no `-c` | Narrow calling without an explicit experimental background library |

**Outputs:** `${SAMPLE}_peaks.narrowPeak`, `${SAMPLE}_peaks.xls`, `${SAMPLE}_summits.bed` plus logs. Keep the complete caller log. NarrowPeak is BED-like and zero-based, with extra score/statistic columns; the summit offset has its own meaning. Do not treat every column as a count.

### Optional target-dependent alternatives

**Historical lab branch, CR-S17; review before use:**

```bash
macs2 callpeak -t "$HUMAN_BAM" -f BAMPE -n "${SAMPLE}_broad" \
  --outdir "peaks/${SAMPLE}_broad" -g hs \
  --broad -q 0.05 --broad-cutoff 0.1 --keep-dup all -B --SPMR
```

This changes peak shape, thresholds, duplicate policy and output tracks simultaneously. BroadPeak/gappedPeak output requires broad-aware import and plotting; the selected DiffBind helper assumes narrow peaks. Do not just toggle `--broad` while leaving downstream parsing unchanged. MACS pileup tracks requested by `-B --SPMR` are different products from deepTools coverage.

**Narrow versus broad:** narrow calling emphasizes local enriched cores and summits. Broad mode uses stronger enrichment to seed regions and a more permissive threshold to connect surrounding enrichment, producing domain-like intervals. `--broad-cutoff 0.1` governs that weaker enrichment threshold; it is not a fold-change cutoff. Domain coverage and a focal summit are different biological questions.

| Target/question | Recommended comparison starting point | What requires approval |
|---|---|---|
| Focal sequence-specific transcription factor | Observed narrow baseline plus controls and replicate support | Caller, threshold, fragment class and reproducible-peak rule |
| BCOR-associated chromatin occupancy | Narrow baseline if profiles are focal; compare a domain-aware view if the signal is broad | Antibody specificity, target-loss/background controls, region width and interpretation of associated rather than direct sequence-specific binding |
| Broad histone modification such as H3K27me3 | Broad/domain candidate and count intervals that preserve the biological domain question | Caller/background, boundaries, duplicate policy and whether fixed summit windows are appropriate |

BCOR-associated occupancy is not interchangeable with H2AK119ub/H3K27me3 signal. [Primary BCOR/Polycomb work](https://www.nature.com/articles/s41467-019-09250-6) motivates separating these measurements; it does not establish a universally correct peak shape. Histone marks can also be focal. These are comparison defaults, not substitutions for the actual narrow lab command.

**Negative controls and reproducibility:** a compatible IgG/no-primary library helps assess nonspecific recovery; a target-loss or orthogonal experiment can help assess specificity when available. Controls must be suitable for the assay and adequately sampled; an untreated target-IP is not background. Compare independently called biological replicates, widths and local enrichment before merging/averaging. A stringent q-value without a control is a methodological choice requiring evidence, not a syntax error; neither controls nor q-values alone establish reproducible binding.

**E:** [SEACR](https://github.com/FredHutch/SEACR) was developed for sparse CUT&RUN signal, and nf-core 3.2.2 defaults to SEACR with control-aware options. **L/U:** a footprint wrapper looks up SEACR, but complete SEACR execution is not established in the selected lab chain. A caller/control comparison is a proposed study, not an already validated replacement. Earlier `--shift -100 --extsize 200` flags must not be copied as an ATAC-style CUT&RUN correction; MACS2 BAMPE handling changes how shift/model options apply ([versioned source](https://raw.githubusercontent.com/macs3-project/MACS/v2.2.9.1/MACS2/OptValidator.py)).

**QC/troubleshooting:** inspect enrichment at known positive and negative regions, target-appropriate peak widths, peak totals, background-control signal and replicate overlap. An empty list may indicate low enrichment, an unsuitable model or a stringent cutoff. Do not lower thresholds until a biologically attractive answer appears. **Output → next:** retain raw peak lists and the explicit caller decision.

## Stage 7 — Review suspect regions and calculate enrichment QC

**Purpose:** remove recurrent technical artifacts from peak interpretation and quantify how much mapped signal overlaps peaks. A blacklist is assembly-specific; it does not replace biological negative controls. See the [ENCODE blacklist study](https://www.nature.com/articles/s41598-019-45839-z).

**Inputs/tools:** raw narrowPeak, reviewed hg38 blacklist, human BAM, [BEDTools](../../software/bedtools.md), SAMtools. **L:** selected filtering affects **peak intervals only**, not BAMs or coverage. It is conditional on the blacklist and BEDTools being available.

**Configured reconstruction with an explicit review gate:**

```bash
RAW_PEAKS="peaks/$SAMPLE/${SAMPLE}_peaks.narrowPeak"
FILTERED_PEAKS="peaks/$SAMPLE/${SAMPLE}_peaks.blacklist_filtered.narrowPeak"
bedtools intersect -v -a "$RAW_PEAKS" -b "$BLACKLIST" > "$FILTERED_PEAKS"
bedtools intersect -u -a "$RAW_PEAKS" -b "$BLACKLIST" \
  > "peaks/$SAMPLE/${SAMPLE}_peaks.blacklist_removed.narrowPeak"
```

`-v` retains intervals with no overlap; `-u` reports each overlapping A interval once. Whole peaks are excluded on any overlap. **U:** the source falls back to raw peaks if the filtered list is empty; the sample-sheet generator still predicts filtered paths. Existing empty files can also satisfy skip logic. **P:** stop and review an empty filtered list; do not silently reintroduce excluded regions. Set the following variable only after approving the actual file:

An interval overlap is a coordinate comparison, not a test that a signal is artifactual. The mask must be justified separately. The [CUT&RUN suspect-list study](https://link.springer.com/article/10.1186/s13059-023-03027-3) provides an assay-specific artifact resource that differs from an ENCODE blacklist. Filtering alignments before a caller can change its background/scaling; filtering peaks afterward only removes selected intervals. Review that distinction before changing the lab's peak-only approach.

```bash
PEAKS_FOR_QC="$FILTERED_PEAKS"
```

### Observed FRiP unit

The source intersects human BAM alignments with peaks and divides mapped alignment-record counts. This is **read-segment/alignment FRiP**, not a proven paired-fragment FRiP. The peak set is called from the same data, so the metric also depends on caller choice and thresholds.

**Configured example with a proposed zero-denominator guard:**

```bash
TOTAL=$(samtools view -c "$HUMAN_BAM")
IN_PEAKS=$(bedtools intersect -u -ubam -a "$HUMAN_BAM" -b "$PEAKS_FOR_QC" \
  | samtools view -c -)
awk -v n="$IN_PEAKS" -v d="$TOTAL" \
  'BEGIN {if(d==0){print "undefined: zero alignments"; exit 1} print n/d}'
```

**QC:** record numerator, denominator, unit, filtering and peak-set identity. Do not compare directly to nf-core's fragment/overlap-based FRiP without reconciling definitions. The source has no universal FRiP acceptance threshold; set target-specific review criteria using controls and replication. Low FRiP can reflect poor enrichment or a mismatched peak model. Blacklist-free peaks do not make an unfiltered browser track artifact-free.

**Output → next:** approved peak files for DiffBind and human BAMs for counts/CPM. The combined BAM remains the source of the [spike-count audit](03-normalization-and-qc.md#stage-8-audit-spike-counts-before-scaling).
