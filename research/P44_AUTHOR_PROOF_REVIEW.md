# P44 exact-hash independent proof review

Reviewed 2026-11-24, after the independent reconstruction freeze
`2d15012abdfdb96cac6fface3eac326a0d3f191a`. Its file SHA256 is
`2078117e9f890c8cc8c14222c76990aeea800877a06fcb9af2e9b3630efd56ff`.
No author P44 proof was read before that freeze. No numerical run supports
this analytic verdict.

Target: root `theory/P44_nonuniform_loss_moment_obstruction.md`, reported
commit `b87e677`, observed SHA256
`5407871a6afe5f6d7eb478792c88b73c964918bd593dbd19ef6d56e82204730b`.
The complete source and its SHA256 were read after the reconstruction freeze.

**Verdict: proved as written**, within the stated passive, vacuum-environment,
fixed-CF-source model. The robust internal-state variant additionally requires
the same spatial transmission matrix for all internal degrees. The cost/search
consequence is conditional on the explicitly guaranteed P42 budgets and shared
frontend, rather than a hardware timing statement.

## Normalization and physical obligations

- (M2) follows by normal ordering ACTUAL canonical output modes before dropping
  vacuum environment annihilators. Distinct input hole sets leave orthogonal
  residual input occupations. The removal amplitude is one permanent; no
  external k! or surviving-sector normalization is present.
- (M3) retains repeated input columns and their factorial denominator. A direct
  Fock-basis derivation in the independent reconstruction establishes that
  denominator from normalized repeated-occupation amplitudes. Dropping those
  additional nonnegative terms gives the needed inequality, not equality.
- (M4) uses a unit Omega_k and per(G)=<Omega_k,G tensorpower k Omega_k>.
  Restricting the occupied-input transmission to rows S cannot increase its
  norm, so the author's sharper occupied-input eta0 is valid, not just the
  full-matrix eta_max used in the original card. Positive tensor spectra give
  the stated eta0^k cap.
- (M5) remains valid for correlated internal states: purify them, group by the
  same spatial hole set, and resolve output internal labels. Each routing
  vector has norm1 because the input product of the selected mode numbers is1.
  Hilbert-space Cauchy gives k! times the nonnegative injection sum, then the
  row-intensity product. No single-Gram/product-internal assumption is required.
- N<k gives zero; eta0=0 gives zero for k>=1; the file assumes k>=1 and
  therefore has no empty-product ambiguity. Fully distinguishable product
  labels remove routing cross terms, but arbitrary partial states do not.

## Decoder extension checked separately

For any classical, possibly graph/history-dependent decoder D, the sole
condition needed for its particular output S is

    {D(observation)=S} subset {n_i>=1 for every i in S}.

It follows pointwise that this output probability is at most the all-S-click
probability and hence the moment cap. Additional clicks, collisions, discarded
outputs and unobserved external modes do not affect that implication. The
decoder need not inspect every physical output or require the rest empty.
No probability is conditioned on a decoder-success denominator. Completing
unclicked vertices, false-positive detector models or same-attempt herald
conditioning would violate premises rather than improve this bound.

For the source's at-most-one-candidate attempt, favorable candidate events are
indexed by a fixed set of k-subsets. Their conditional hit probability is at
most g*b. With nC>0, nQ>0 and L=ceil(nQ/nC)>=1, the (M6) condition gives the
same fixed-target first-hit bound and sublevel-set stochastic domination as
P42. The nQ=0 case is separately trivial. Interpret D=binom(2k,k) and g using
the same oriented k-subset convention; complement symmetry then causes no
missing factor. A decoder may perform classical work, whose costs and extra
discoveries still require the separate credits specified by the source.

The eta0<=1/4 equal-attempt sufficient condition follows from D<=4^k without
a uniform-loss commutation. For unknown internals the k! condition stays
explicit, and does not yield that dimension-uniform threshold. All of these
are model statements. No measured Lucy transmission or calibrated spectral
upper bound was supplied or inferred.

## Provenance and limits

The ingredients are standard; this review does not settle novelty or external
attribution. The independent reconstruction supplies detailed proofs rather
than adopting the author's status label. Earlier noise/P40 authorship and
P33/P37 review participation are disclosed; this is a new analytic derivation,
not an independent execution of those authored components. No manuscript,
source, raw result or previous receipt was changed. A proposed small numerical
validation is separate finite evidence and cannot replace this proof.

Checks actually performed: full author-file reading, observed SHA256, comparison
to the frozen derivation, direct decoder-event implication and edge-case/cost
checks. No mathematical code or physical run was executed for this review.
