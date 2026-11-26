# P85: prior nonnegative-GBS claims and their precise scope

ROOT read the complete261-line report, independently checked the thermal
counterexample and Schur-complement identity, and verified the actual2020
PDF's sign argument as well as its HTML. The broad nonnegative-GBS classical
simulation idea predates this project. P78/P80 retain their exact internal
proofs and limits; this check supplies no novelty clearance.

Evidence: `research/P85_PRIMARY_NONNEGATIVE_GBS_COMPARISON.md`, original
2c45237f902e6ad4b5f52eb447ac9309044f2c3e, SHA256
02150f2d1bbbbe62ebb912f68351f0c3aae934d132cd18c9b8b4b2472586d925.
It is an addendum to the preserved three-source P78 record. ROOT supplied
the identifiers and candidate counterexample; the agent reconstructed
the algebra. This is not blind discovery or an external referee report.

The two authenticated primary publications are
[Quesada–Arrazola, arXiv1908.08068v3](https://arxiv.org/abs/1908.08068v3)
(revision16-Nov-2020, Phys.Rev.Research2,023005) and
[Uvarov–Vinichenko, arXiv2312.10143v2](https://arxiv.org/abs/2312.10143v2)
(revision6-Mar-2024). The first proposes an approximate nonnegative-GBS
sampler based on sequential hafnian estimates. The second examines
variance limitations of determinant estimators. Their existence and
scope do not automatically discharge P80's full TV/random-bit contract.
No first general dequantization claim is justified by our new derivation.

The earlier paper's pure B maps EXACTLY to project Z, with doubled
A=diag(Z,Z), K=XA and Q=(I-K)^(-1). It is the same complete raw PNR law,
not merely a fixed-CF conditional distribution. No notation change removes
that overlap. Its broad efficient-approximation statement is already prior;
our loop/mean-photon/finite-bit refinements still have unresolved priority.

## Internal algebra checks and their limits

The report's physical thermal counterexample disproves the GENERAL
implication that entrywise nonnegative Gaussian covariance has an
entrywise nonnegative hafnian kernel. Its exact3x3 occupation matrix has
leading minors1,16/25,171/500; H=I+N has det1653/250 and inverse entry
H^(-1)_13=40/1653. The doubled thermal covariance is physical and
nonnegative, while A_(1,6)=-40/1653. ROOT independently verified this
cofactor and the uncertainty blocks diag(N+I,N).

ROOT also read the actual v3 PDF, printedpages6–7, AppendixA(A1)–(A16).
The inverse-sign inference occurs between(A3) and(A4), so it is not merely
an unconfirmed HTML equation-rendering issue. This refutes that particular
general inference, not the whole article or its special pure targets.

For the pure nonnegative class, direct block elimination correctly gives

    I-Q_RR^(-1)=K_RR+K_RT*(I-K_TT)^(-1)*K_TR >=0.

The marginal hafnian kernels therefore remain nonnegative. The thermal
counterexample does not remove prior overlap or create priority. The
report's separate disjoint-C4 calculation also shows exponential sample
requirements for the UNMODIFIED Rademacher determinant average, with an
explicit zero-hit probability argument. It does not lower-bound improved
estimators, component factoring or other raw samplers.

No source was locally cached; report locators authenticate online versions
only and explicitly record no retained-source hash. No science code,
matrix evaluation, RNG, backend or QPU ran. P79's passed finite experiment
and P80's mathematical proof are unchanged. No publication wording,
manuscript edit or positive optimizer/hardware claim is authorized.
