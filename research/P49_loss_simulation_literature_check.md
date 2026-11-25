# P49: two 2026 loss-simulation preprints, bounded literature check

Checked 2026-11-25 using mathbox:literature-check. Question: do these
statements give a TV-accurate polynomial classical replacement for P49's
graph-dependent spectral circuits? **Direct application: inapplicable.**
Both versions and theorem statements were authenticated/extracted from
primary arXiv full HTML, not merely abstracts. Neither complete proof has
been independently audited here; “the preprint states” below is deliberate.
TV means half the L1 distance. No P49 code, graph, raw, acceptance gate,
article or hardware decision is changed.

## Go–Jeong: source summary (under180 words)

Byeongseon Go and Hyunseok Jeong,
[Polynomial-Time Classical Simulation of BosonSampling under Any Constant-Fraction Photon Loss](https://arxiv.org/html/2610.27065v1),
arXiv:2610.27065v1 (19 October 2026).
The preprint states: CF N-photon input, M modes, uniformly chosen n survivors.
Theorem2 (§IV.1,17–18) assumes 1<=n<N and M>=C0 n²N. Its collision-collapsed
sampler has TV<=epsilon for >=1-delta of Haar U and arithmetic cost
MnN³ epsilon^-2 delta^-1 2^{O(d)}, where
(n/N)^{d+1}/(1-n/N)<=epsilon²delta/C, or d=n. Corollary4 (§IX,94–95)
restores full Fock outputs with additional M>=CB n²/(epsilon delta).
Theorem3/Corollary5 (§X) cover fixed independent transmission eta in(0,1),
still dilute; Corollary5 assumes M>=C0 N³. Remark1 adds full-output collision
suppression M=Omega(E[S_eta²]/(epsilon delta)). Polynomial exponents can
depend on fixed survival/transmission and need not stay bounded as it
approaches1. The extracted cost is arithmetic operations; bit complexity
was not checked.

## Lim: source summary (under180 words)

Youngrong Lim,
[Boson sampling is fragile to loss](https://arxiv.org/html/2611.01434v1),
arXiv:2611.01434v1 (1 November 2026).
The preprint states: Theorem1 (§IV.1,3–4), with Problem1, covers CF n-photon
inputs plus arbitrary vacuum, every M>=n, independent uniform transmission
0<eta<1 fixed with size, and the FULL Fock law including all survivor
sectors/collisions. It gives E_Haar TV(P_U,Q_U)<=epsilon, 0<epsilon<=1/2,
and worst-case arithmetic cost poly_eta(M,n,1/epsilon). Degrees/constants
depend on eta; D.4 requires
L+1>=log[256/((1-eta)epsilon²)]/(-log eta), so this is not uniform near eta1.
AppendixD.4 states polynomial bit precision suffices. AppendixA.2 converts
mean error to high probability over the initial Haar circuit; it does not
identify exceptional U. AppendixF.1 requires separate correlation-tail and
estimator-variance bounds for a specified structured U. Gaussian-input
extensions are outside this check.

## Translation and application to P49

Their M equals P49's vertex/output-mode count, while input photon count
is P49's K. Go–Jeong's n denotes survivors; Lim's n denotes INPUT photons.
The distinct-single-photon input assumption DOES match P49 when R is part
of the network; intermediate HOM bunching is not a source mismatch.
Thus P49's M=2K is dense, not Go–Jeong's cubic-mode fixed-survival regime.
Lim removes that density obstruction, so it must not be described as
requiring negligible collisions. Current P49 is ideal eta1, excluded from
both fixed-nonzero-loss conclusions. The arithmetic polynomial at fixed eta
is not a uniform polynomial as eta tends to1 with size. Lim averages the
distance at each fixed U, not merely the distance of two Haar-averaged laws.

There is a more fundamental ensemble mismatch even for a FUTURE eta<1.
P49 uses real marked-graph eigenvectors E and a fixed finite rotation grid
V=ER. P=VV*=EE^T remains real. A nontrivial rank-K occupied projector of a
complex Haar unitary is generically not real: the real-projector condition
is a Haar-null algebraic constraint. The blind Fourier frame with finitely
many carried row orders is likewise not a Haar draw. Random graph labels,
marks or arbitrary VACUUM-column completion supply no missing Haar guarantee.
This is an application-obstruction argument, not a proof these circuits
are hard or loss-robust. Separate structured-circuit error bounds would be
needed; these statements do not provide them.

If a full-law TV bound for the ACTUAL fixed circuit were established,
applying the SAME randomized PIT/decoder to target and replacement could
not increase TV. A collision-collapsed guarantee alone cannot reconstruct
P49's resolved collisions. Neither fact removes the ensemble/loss mismatch,
and independently changing the replacement's PIT is not that same channel.
No sampling or optimization advantage, or impossibility thereof, follows.

## Verification limits and provenance

Read: arXiv version histories; Go–Jeong §§III–IV,IX–X and cited theorem/
corollary statements and adjacent proof outlines; Lim §§II,IV,V and
AppendicesA,D.1/D.4,F.1. Only Fock implications were checked. Source status:
the preprints present proofs; full technical proof validation, implementation
and finite-device runtime assessment were NOT performed. Overlap label:
partial/adjacent results only for the P49 application, not a novelty search.

Exact-ID local-cache lookups returned no active cache; the legacy local
references search found no matching retained source. No PDF/cache was
created, so no local retained hash is claimed. Versioned primary HTML URLs
above and arXiv histories identify the inspected sources. Browser/text and
read-only metadata/cache queries only: no scientific numerical computation,
simulation, QPU, credential access or manuscript edit occurred. This one
new note is written in the isolated replication branch.
