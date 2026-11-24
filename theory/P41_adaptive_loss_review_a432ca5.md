# Final exact-version audit — P41 loss/oracle clarification

Reviewer p41_adaptive. Author revision
`a432ca5287093ab08f8d8e54b0f19fec4d071b2c`.

**Primary verdict: proved as written**, within the source/loss/encoding,
sampling-stage and fixed-or-guaranteed-cost hypotheses explicitly stated.
No ideal-lossless, universal-encoding, whole-hybrid or measured-Lucy claim
is supported by this verdict.

## Audited artifacts

1. `theory/P41_obstruction_loss_entropy.md`, SHA256
   `7343c32e97d8bd3c46698b95b2c857e70905e6b57121e724446f9bbe570ced8f`.
2. `theory/P41_obstruction_loss_cost_certificate.md`, SHA256
   `539d960b0e131ecc823db545eca87b048ceb802b33c9290fdd3eb4b28485f418`.

The initial reconstruction was committed at fd479d8 before author b760636
was read. Its exact-version audit is preserved separately in
P41_adaptive_loss_review_b760636.md; that earlier verdict is not overwritten.

## Correction check

The b760636->a432ca5 diff in the entropy proof only changes the two flagged
issues. It treats eta=0 by a=0 before introducing logs and otherwise states
0<eta<1/alpha. It defines cC,cQ as fixed primitive costs and explicitly allows
deterministic upper classical/lower optical bounds, while rejecting average
timings alone as a finite-floor guarantee. The companion cost certificate
also makes the fixed/bounded-cost interpretation explicit.

These corrections close the stated review restriction without changing any
numeric result or mathematical nondegenerate implication. The main derivation,
constant, index, endpoint-quarter and alpha2 checks in the initial audit remain
valid for this exact source version.

## Companion rational certificate, additionally reconstructed

The companion file's exact finite comparison is

    nC[-log(1-p0)] >= nQ[-log(1-a)],

and its rational sufficient condition, for0<=a<1, is

    nC p0(1-a) >= nQ a.

Since p0<=-log(1-p0) and -log(1-a)<=a/(1-a), multiplying the latter
condition by1/(1-a) gives the required chain. Its direction is correct.
The asymptotic rate criterion cC/cQ<=[-log(1-p0)]/[-log(1-a)] follows on
dividing the large-budget counts; it is explicitly not substituted for
finite floor counts. a=0 is treated directly; a=1 supplies no nontrivial
certificate of this kind. Complement symmetry makes0<p0<1 for k>=2.

## Scope that remains load-bearing

The theorem is uniform over graphs, graph-informed optical preparations and
adaptive choices, because >=k true detections from one fresh attempt is a
necessary success event at every history. It is deliberately an oracle upper
bound on the optical stage, while the uniform classical sampler requires no
oracle during execution. A conditional fixed/common frontend is separated;
its discoveries cannot be added to the stage event and then bounded by the
same survival formula.

Independent uniform loss is essential; a mere mean transmission does not
control a correlated survival tail. Emission attempts are not nonempty-event
provider shots. Recycling, photon memory, correction, or classical completion
from fewer than k photons changes the premise. New encodings and unbounded
source overhead are not ruled out. Actual apparatus/cost calibration has not
been established by this proof review.

No new numerical experiment was run or needed for the analytic correction.
This audit does not freshly validate the author's finite probe or source
novelty report. Earlier captures remain tied to their recorded source revisions.
The present verdict pins only the two theory hashes above. Shared project
context and the supplied claim card are disclosed; the reviewer did not
author these proofs or their numerical experiment. No QPU call was made.
