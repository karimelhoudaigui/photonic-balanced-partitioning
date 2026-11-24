# Independent reconstruction — useful grouped bosonic outcomes

Reviewer: p41_adaptive. Parent supplied only the target statement, not its
author's proof or proposed construction. This derivation was written without
reading theory/P41_encoding_grouped_domination.md. Shared broad project context
is disclosed; the reviewer did not author the R2 mechanism or its code.

## Claim card and verdict

Let V be an m-by-k complex isometry. The input is k identical photons, one in
each of the k distinct occupied columns. Let G1,...,Gk be pairwise disjoint,
nonempty sets of output modes. A useful outcome x=(x1,...,xk) has xg in Gg
and exactly one photon in each group; all other output modes have zero
photons. Its physical unconditioned probability is

    p_B(x)=|per(V_x)|^2,

with V_x containing those k distinct output rows. The input and output Fock
factorials are all one. No success-normalization or heralding denominator is
included.

**Verdict: proved as written for this ideal input/readout and arithmetic-model
interpretation of O(mk).** An explicit classical sampler below has q(x)>=p_B(x)
for every useful x and always emits one element of each group. This verdict
does not assert novelty, implement a numerical test or extend automatically
to whole adaptive search trajectories.

## Independent construction

1. Draw k independent uniform signs z_j in {-1,+1}.
2. Compute alpha=Vz and a_g=sum_(i in Gg)|alpha_i|^2.
3. In each group independently choose xg with probability
   |alpha_xg|^2/a_g. If a_g=0, choose any fixed group element instead.

The zero-group convention defines a normalized sampler for every sign vector;
it never requires a division by zero. Constructing alpha costs O(mk), and
group sums plus direct categorical draws cost O(m). No graph score, optimum,
partition mask, permanent, rejection loop or exponential enumeration is used.

For every sign vector, isometry gives ||Vz||^2=k. Disjointness implies
sum_g a_g<=k. AM-GM therefore gives product_g a_g<=1. Whenever all a_g>0,

    q(x|z)=product_g |alpha_xg|^2 / product_g a_g
           >= product_g |alpha_xg|^2.

If one a_g=0, the right-hand product is zero and the inequality remains true
under the stated convention.

For fixed x define the degree-k homogeneous polynomial

    F_x(z)=product_g sum_j V_(xg,j) z_j,
    chi(z)=product_j z_j.

In the expansion of E[chi(z)F_x(z)], a term survives only if every occupation
exponent n_j is odd. Each surviving n_j is at least one, while sum_j n_j=k,
so necessarily n_j=1 for every j. These are exactly the k! permutation terms:

    E_z[chi(z) F_x(z)] = per(V_x).

Since |chi|=1, Cauchy-Schwarz yields

    |per(V_x)|^2 <= E_z |F_x(z)|^2 <= E_z q(x|z)=q(x).

This completes the proof. One sign may be fixed by global sign symmetry;
using k signs is already sufficient and has the same complexity. A construction
with roots of unity of order k+1 also works by Fourier orthogonality, but is
unnecessary. Rademacher signs avoid an ideal continuous phase sampler.

## Obligations checked and interpretation

| Obligation | Disposition |
| --- | --- |
| Correct bosonic amplitude/object | PASS: distinct input/output modes, no Fock normalization factors |
| Group normalization and zero cases | PASS: explicit convention and pointwise zero RHS |
| Missing output modes | PASS: disjoint group intensity sum is at most k, not asserted equal |
| Destructive cross terms | PASS: extraction uses a single Fourier character; Cauchy-Schwarz controls all other terms without claiming they are individually positive under signs |
| k=1 | PASS: one categorical group draw dominates the unconditioned probability, even if group excludes some modes |
| k=0 | Outside useful nonempty-group formulation; vacuum may be treated separately |
| k>m or empty group | No isometry/useful tuple respectively; not a normalized useful-output instance |
| Numerical precision | Exact arithmetic theorem; finite-precision implementation needs its own error analysis |
| Novelty | NOT ASSESSED: parity extraction is a known-style permanent estimator ingredient |
| Whole adaptive optimization advantage | NOT ESTABLISHED by this theorem alone |

An independent-group sampler based only on mean intensities is not sufficient
in general. The random coherent sign field supplies essential classical
correlations. For instance a selected 3-by-3 block J/3 completed by I-J/3 to
an isometry gives a selected useful bosonic probability4/81 above the naive
mean-intensity product1/27. The correlated sampler proof avoids that false
shortcut. This hand counterexample is analytic, not an executed computation.

## Exact safe consequences for cost and search

For a fixed V and group system, any nonnegative useful-outcome reward r(x)
satisfies E_q r >= sum_x p_B(x)r(x). In particular, from current cost c,
r(x)=max(c-C(x),0) gives no-smaller expected one-step accepted gain. The
classical sampler is optimum-blind: the comparison is uniform in r, and r
is evaluated only on its sampled feasible candidate. Every physical failure
or non-useful bosonic output contributes zero gain and remains charged.

Likewise a target-set hit probability is no smaller for each fixed circuit.
For a predetermined sequence of fresh circuits (or shared exogenous choices),
independent classical draws have no-smaller probability of at least one target
hit. These conclusions do not require knowing the target set to generate
samples.

The computational resource unit is an O(mk) classical draw from a known matrix
V. Producing/fitting V, graph feature extraction, circuit compilation, training
and scoring remain charged to the relevant method. This is no unconditional
wall-time, energy, allocation-credit or hardware speedup comparison. If V is
an inaccessible unknown device rather than given data, the sampler cannot be
implemented from its statement alone.

## Adaptation: a necessary non-extension

Pointwise dominance at a matching history does not automatically give an
efficient simulation of the quantum algorithm's adaptive history. A possible
thinning construction would require p_B(x)/q(x), whose evaluation can involve
hard permanents or a hard expectation. Its existence as a probability ratio
is not an O(mk) classical algorithm.

Even greedy improving policies need care. Abstractly, take current state S
of cost3, a trap A of cost2, and target T of cost0. A kernel B proposes T
with probability.1 and fails/holds with.9. A pointwise-dominating useful
kernel Q proposes T with.1 and A with.9. From A both kernels hold. B reaches
T within two steps with probability.19; Q reaches it with probability.1.
The extra Q outcome changes the future policy's state. This is a counterexample
to the logical inference from per-history useful-outcome domination to arbitrary
adaptive hitting-time domination; it is NOT a physical counterexample to the
proved photonic bound. A classical archive/multistart strategy can help, but
its guarantee and cost would need a separate argument.

Similarly, a quantum-trained final V can be reused by this classical sampler,
but training that V is part of total cost. The theorem alone does not construct
a cheap classical procedure reproducing its adaptive training trajectory.
Independently reoptimized feasible controls remain necessary in experiments.

## Scope beyond ideal grouped readout

* Pure passive loss: if the detected single-particle matrix obeys V*V<=I,
  the same argument applies to the event where all k injected photons are
  detected in distinct groups. The norm inequality replaces equality. It does
  not cover thermal photons, dark counts, uncontrolled extra emissions or a
  mitigated/recycled output law without a justified physical model.
* Heralding: p_B conditioned on success is not bounded by this q in general.
  The theorem compares unconditioned preparation/acquisition attempts and
  cannot erase their failure cost. Additional source success probability at
  most one only lowers unconditional useful probability.
* Partial distinguishability or general internal entanglement: not assumed
  by this scalar proof. A separate internal-state model and cost analysis are
  needed before extension.
* Full k-of-2k collision-free readout: no fixed groups cover every k-subset.
  Averaging over uniform perfect matchings only yields

      q(S) >= [2^k / binom(2k,k)] p_B(S),

  because exactly k! of the (2k-1)!! matchings split a fixed balanced subset.
  That coefficient decays exponentially. Thus this averaging does not prove
  unit-coefficient domination of every ordinary CF bisection outcome.

## Review provenance and next step

This is an independent raw reconstruction of the parent's precise statement,
not acceptance of an unseen author's proof. No numerical command was executed
for this audit. The parity, AM-GM and source-amplitude steps were reconstructed
directly. Compare the author's pinned revision only after this file is frozen;
record any mismatch separately. The full research target remains open beyond
the exact grouped, fixed-history result and its stated consequences.
