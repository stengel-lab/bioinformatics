# From tutorial draft to a reusable workflow

This milestone adds a manual educational reconstruction. It does not add a production runner, scheduler automation or an nf-core replacement.

## First: make the scientific contract explicit

1. Accept the [source baseline](sources.md) and resolve the high-impact [decisions](decisions.md): species counts/calibration (D07–D09), controls/peaks (D10), consistent masks (D11/D14), pair/duplicate handling (D04/D06), and contrast sign (D15).
2. Obtain exact reference/annotation identities and a full version record. Test installation candidates rather than claiming they reconstruct the old environment.
3. Choose a publishable CUT&RUN dataset with paired FASTQs, target/control metadata and at least biological replication appropriate for the question. A small synthetic input is useful for mechanics, but cannot validate enrichment biology.
4. Agree on QC acceptance and failure criteria by target. Document expected positive/negative loci, fragment distributions, background, replicate concordance and spike sensitivity without selecting criteria after seeing desired results.

## Then execute a bounded teaching exercise

Run each chapter manually, retain commands, checksums, versions, resource measurements and all warnings. Check every expected output against the complete manifest. Use toy tests for coordinate origin, contrast sign, normalization inversion and factor ordering. Compare a deliberately changed option against the unchanged baseline; do not mix several changes into an unexplained new method.

Inspect models on a fixed interval universe, including all requested contrasts and zero-significant statuses. Review selected tracks in a browser with shared scales. Validate motifs with an appropriate background and explain the limitations of nearest-gene annotation. Publish only permitted inputs or accession instructions and sanitized result examples.

## Only after review: choose automation

| Need | Candidate implementation decision | Required evidence before choosing |
|---|---|---|
| Dependency isolation | Versioned containers or platform-specific environment locks | Successful solves/startups and a small input/output run |
| Portable task execution | Adopt/extend nf-core where suitable, or a small reviewed workflow engine design | Which lab choices need preservation, which deviations are accepted, and platform requirements |
| Sample/design validation | Explicit schema with control roles, replicate and batch fields | Reviewed example manifest and invalid-input cases |
| Completion/restart safety | Success-gated dependencies, unique output ownership, input/parameter hashes and atomic outputs | Partial-run and failure recovery exercises; no stale median reuse |
| Scientific provenance | Per-product unit/filter/normalization record and reference hashes | Audit trail from reads to reports and figures |
| Tests | Synthetic checks plus a permitted biological regression dataset | Known-direction effects, interval conversion, scaling and complete-output expectations |

Do not carry over the original supervisor's `afterany`, output-existence completion, shared-file races or destructive set rebuilds by default. A future implementation should preserve accepted scientific choices and make each changed assumption reviewable.

## Suggested first execution lesson

Use one focal target with well-described controls and replicated baseline/treatment libraries. Teach raw/trimmed QC, explicit paired mapping, approved peaks and a normalization comparison before complex time-course sets or footprinting. If calibration details cannot be recovered, keep spike interpretation pending and explain standard normalization's limitations. Complete count-model and contrast-direction review before presenting a differential-binding conclusion.
