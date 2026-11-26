# P87: identity is first-order optimal for a passive cut-phase oracle

ROOT candidate and hand derivation. Independent before-source reconstruction
and exact-source review are pending. No new numerical experiment is used.
This sharpens P86 for fixed dimension; it does not concern general sampling
optimizers, the P82 decoder or probability-only basis measurements.

## 1. Contract and proposed sharp asymptotic statement

Use the P86 setting: even N>=4, N photons on2N dual rails, a single fixed
lossless passive U on the same modes, no ancillas/heralding/loss/filters,
and every balanced |S|=N/2 code basis state. The fixed real cost satisfies
C(S)=C(S^c). Define exactly the COMMON-phase column metric

    delta(U,gamma)=min_chi max_S
      ||Gamma_N(U)|S>-exp(i chi-i gamma C(S))|S>||_2,
    delta_*(gamma)=inf_(U in U(2N)) delta(U,gamma),
    R=max_S C(S)-min_S C(S).

The proposed sharp theorem is

    lim_(gamma->0,gamma!=0) delta_*(gamma)/|gamma| = R/2.     (1)

Identity optics attains the same first-order coefficient. The analogous
infimum of the COMMON-phase operator norm restricted to the balanced
subspace has this same limit. No continuity, generator bound or consistent
choice of U_gamma is assumed. N and C are FIXED in this limit; the finite
constants below can grow factorially with N.

The extrema and midpoint are used only to state/analyze the metric.
Identity optics requires no optimum, mask, cost oracle or graph information;
the fitted common phase is an unobservable reference, not an implementation
resource supplied to a training procedure.

## 2. Dependencies and finite constants

Use accepted P81's quantitative physical stability theorem, exact source
`theory/P81_dual_rail_balanced_average_stability.md`, original0a51544,
SHA2567fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f.
P86's independently reconstructed small-error argument is repeated here
where needed, so no additional conjectural leaf is imported.

Put

    s=sqrt[4N(N-1)^2/(N-2)], b=1+N*s, delta0=1/(2b),
    d=s+sqrt(2N)*b, E=(N!-1)*d² > 0.

For all U and gamma, a finite bound implying (1) is

    delta(U,gamma) >= min(delta0, q(|sin(gamma R)|)),
    q(t)=(sqrt(1+2E*t)-1)/(2E)=t/[1+sqrt(1+2E*t)].          (2)

The same inequality holds with any cost difference replacing R. Large
constants make this an asymptotic obstruction, not a claimed practical
error threshold or a dimension-uniform bound.

## 3. Small oracle error forces physical off-diagonal mass O(delta)

Fix U and a minimizing chi, which exists on the compact phase circle.
Write delta=delta(U,gamma), f_S=exp(i chi-i gamma C(S)). The target lies
in the code, so raw leakage on each input is at most delta². P81's
uniform incoherent balanced average therefore has epsilon<=delta².
It gives a physical pair-permutation/local-block V satisfying

    ||U-V||_F<=s*delta,
    ||Gamma_N(V)|S>-f_S|S>||<=b*delta=:e  for every S.

The second estimate uses tensor telescoping between U,V, never a
column-to-operator shortcut for the target oracle.

Assume delta<delta0, so e<1/2. Normalization gives
|<S|Gamma_N(V)|S>|>=1-e²/2>7/8. If one input pair b!=a is sent to a,
balanced patterns x_a=x_b=0 and x_a=0,x_b=1 force both entries of a single
row of Q_a to have magnitude>7/8, impossible by its row norm. Both patterns
exist even at N4. Thus V's pair permutation is identity, as in P86.

Its diagonal amplitude is then product_a Q_a[x_a,x_a]. Each factor has
magnitude at most one, so the same overlap bound forces every selected
diagonal entry to have magnitude>=1-e²/2. Every rail is selected somewhere
in the full balanced family. Unitarity of each2x2 block consequently gives

    |Q_a[0,1]|², |Q_a[1,0]|²
       <=1-(1-e²/2)²<=e².

Here e<1/2 makes the lower diagonal bound positive. Let off(U) mean the
PHYSICAL mode off-diagonal matrix, not merely off-block entries. Then

    tau=||off(U)||_F
       <=||U-V||_F+||off(V)||_F
       <=s*delta+sqrt(2N)*e = d*delta.                     (3)

No physical diagonal phases are fixed or set to one by this argument.

## 4. Bosonic diagonal amplitudes differ from diagonal products only quadratically

For a code input S, let I(S) be its N distinct occupied physical rails.
The normalized input and target are the same collision-free Fock state,
so its exact diagonal amplitude is

    A_S=per(U[I(S),I(S)]), B_S=product_(i in I(S)) U_ii.

All factorial denominators are one here. A nonidentity permutation in
that permanent moves at least TWO labels. Its product contains at least
two physical off-diagonal entries, each bounded by tau, while every other
matrix entry has magnitude<=1 by unitarity. Thus

    |A_S-B_S| <= (N!-1)*tau² <= E*delta².                  (4)

This bound does NOT require tau<=1: choose two moved factors and bound
the remaining actual unitary entries by one. Both |A_S|<=1 (a unitary
N-photon amplitude) and |B_S|<=1. Complementary logical S,S^c occupy
exactly all2N physical rails once in their combined products, giving

    B_S*B_(S^c)=product_(i=1..2N)U_ii=:L,
    |A_S*A_(S^c)-L|<=2E*delta².                           (5)

No division by U_ii or by a possibly zero amplitude is used.

## 5. Relative-phase invariant, finite bound and sharp limit

The oracle column error gives |A_S-f_S|<=delta. Complement symmetry gives
f_(S^c)=f_S. Combining this with (5) yields

    |f_S²-L| <= 2delta+2E*delta².

Comparing S,T cancels the same L and gives

    |sin(gamma*(C(S)-C(T)))| <= 2delta+2E*delta².           (6)

For delta<delta0 the positive quadratic root is q in (2). For
delta>=delta0 the minimum in (2) is already no larger than delta.
This proves (2) uniformly over all physical U, including discontinuous
families. Taking infima preserves that bound. Since q(t)/t->1/2 and
|sin(gamma R)|/|gamma|->R, the lower limit in (1) is at least R/2.

For the reverse bound choose U=I and chi=gamma*(max C+min C)/2. At
sufficiently small |gamma|, every phase difference is within the centered
arc and its maximum distance is attained at the cost extrema, so

    delta_*(gamma) <= 2sin(|gamma|R/4).

The upper limit is therefore at most R/2. If R=0 the error is identically
zero with a fitted common phase. This completes (1).

For the restricted balanced-subspace operator metric, each fixed-chi
operator norm dominates the largest column norm, hence its infimum over
chi,U is at least delta_*. Identity's restricted error is diagonal and
has the same centered maximum above. The identical squeeze proves R/2
for the optimized operator metric as well; no reverse column inequality
is inferred for a general U.

## 6. Meaning and boundary

Arbitrary passive mixing cannot improve upon doing nothing at FIRST
ORDER for this coherently specified cost-phase task. This is a fixed-N
limit, not a claim that identity is optimal at finite angle, that isolated
parity aliases are impossible, or that every passive optimization method
fails. Approximate maps with error O(|gamma|) remain possible. No cumulative
algorithmic error lower bound is inferred merely by summing step errors.

The common phase, all-balanced-input operator task and absence of extra
physical resources are essential. Basis-state fidelity/PNR alone cannot
observe the relative cost phase and receive no such lower bound. Ancillas,
heralding, nonlinear resources, state-dependent encodings and P82's
collision-repair sampling mechanism have different contracts.

This candidate supplies no novelty certificate, graph optimizer advantage,
device capability or hardware authorization. Paper/main/QPU remain frozen.
