# P52 collective phase card: static physics review

2026-11-25. Fresh derivations/read-only review, no import, code, graph,
histogram, numerical run or hardware call. Initial ROOT card commit
`6df6e1cef4410c83e7122b7f9cce15c981b5147a`; pre-data symmetry amendment
`bec20972668d80fcf9ba4c3c65ded6c0aaa149b6`, card SHA256
`cced565588adab0c67189d747189bfe40b94e9ea5bee4810c70ee5035a091305`.
The initial version's SHA256 is
`db87b05285a54060dc4976e89cc35d73b4347ae61638a6722c1130a6a2902acb`.
Both versions were read. I authored the cited P51 moment derivation and H4
notes; reuse is disclosed, not presented as external validation of those proofs.

**Verdict:** the amended card is a coherent bounded discriminator, conditional
on exact-source review and qualification. The canonical-b4 and angle-symmetry
nulls are correct. Full-B has a provable fourth-order response, but whether
top4 or its28 crossing means retain a response outside the control hull is
still OPEN. No graph/search/hardware advantage follows at eight modes.

## Source and control invariants

Write U(theta)=(H2 tensor I4) diag(I4,D(theta)) diag(W,W), with W the REAL
unitary H4(1), D_jj=exp(i j theta). This factorization proves unitarity and
places the phase between layers. Every entry has modulus1/sqrt8. With all8
inputs occupied by indistinguishable singles, Q=J8/8, P=I8, mu=1 and
Sigma_B=2I8-J8/4. The P51 full-input theorem gives phase-invariant factorial
moments through total order3 and identical single-mode laws. This does not
say that the full law, a nonlinear decoder or a useful optimization mean is
phase invariant.

For the canonical b4 split A={0,1,2,3}, B={4,5,6,7}, the first group's frame
is[W;W]/sqrt2, independent of theta. The second is[DW;-DW]/sqrt2, equal to
diag(D,D)[W;-W]/sqrt2. These are OUTPUT row phases for that species alone,
so its entire Fock probability law is invariant. Convolving the two species
therefore gives phase-invariant full counts, hence every fixed decoder.
Other mixed groupings do not inherit this argument; all35 must remain.

D is uniform-categorical multinomial, sphere is unitarily invariant, and
the stated Gaussian covariance is exchangeable. Independent final variances
are all7/4; independent B marginals are identical across modes. Static mu=1
and pure jitter are also exchangeable. With uniformly randomized ties, these
controls all have the exact uniform70-subset law, with edge-crossing4/7.
Continuous fixed-modulus PHASE is not sphere: no general unitary-invariance
or uniform-rank law is implied for it, so its separate calibration is needed.

## A second exact phase null, before data

D(pi)W=W P_sigma, sigma=(0 2)(1 3). Hence

    U(theta+pi)=U(theta) diag(I4,P_sigma).

The fully occupied CF input is invariant under that input permutation; B
has period pi. W is real and U(-theta)=conj(U(theta)), so the count law is
also even in theta. Thus BOTH full B and every fixed decoded law at3pi/4
equal those atpi/4. For b4, period pi carries a grouping by the permutation
of LAST-half labels(4 6)(5 7), not necessarily to itself; the SET of35 laws
is preserved. Phase-coherent laws inherit the same period/conjugation null
because their input coefficients are iid and conjugation symmetric.

bec2097 preserves all four cells/seeds as a predeclared calibration null.
It must not count the fourth cell as a fourth independent physical direction.
Finite exact-support floating laws should agree within the declared roundoff
tolerance, not necessarily byte-for-byte; independent MC histograms need not
coincide. No success-dependent phase removal or extra calibration is needed.

## Full-B fourth-order response: an analytic witness

This proves one necessary link, not the rank-mean implication. For real PGF
variables set t_top=(a,b,0,0), t_bottom=(-a,-b,0,0). Then

    A=U*diag(t)U=[[0,C],[C*,0]],
    C=W*diag(a,b exp(i theta),0,0)W.

There are eight C entries(a+b exp(i theta))/4 and eight with a minus sign.
Consequently the P51 fourth-order residual is

    W2=sum_(input i<j)|A_ij|^4
      =(a^2+b^2)^2/16+a^2 b^2 cos^2(theta)/4.

The trace-dependent part of P4 for N8 and these variables is(a^4+b^4)/2.
Therefore [a^2 b^2]P4=1/8+cos^2(theta)/4. Equivalently, for
K_j=(n_j-n_(j+4))^2-n_j-n_(j+4),

    E_B[K_0 K_1]=1/2+cos^2(theta).                                (1)

To check the normalization, [a^2](1+a)^n0(1-a)^n4=K_0/2, and likewise for
b, so the mixed coefficient is E[K0 K1]/4. This observable is genuinely
phase dependent while every lower total moment is fixed. Canonical b4 cannot
reproduce this whole phase response because its full law is invariant.
Equation(1) DOES NOT prove a response after top4, a useful sign for a graph,
separation from ALL regrouped b4/phase, or an advantage.

## Decoder, confidence and closure requirements

For each occupation, select every mode strictly above the fourth-count cutoff
and a UNIFORM subset of the tied modes to reach4. The probability per admissible
choice is the reciprocal binomial tie multiplicity. This exact rational
pushforward is appropriate; a fixed priority/bucket is a different model.
Every resulting crossing vector obeys sum_(j!=i)c_ij=4 and sum_(i<j)c_ij=16.
These are cheap checks on the tie/crossing normalization, including zeros.

The6435 full patterns,330 patterns/group and35 unordered groupings have the
correct sizes. Group convolution must combine PROBABILITIES, not amplitudes
or an extra factorial. The creation-operator recurrence must account for
sqrt(n_i+1) or use polynomial coefficients times sqrt(prod n_i!) consistently.
Full normalization and hand-permanent/HOM/H4 checks are required before main.

The392-target Hoeffding/union bound applies to exact tie-averaged indicators
in[0,1], assuming the stated independent calibration draws. It is absolute,
not a rare-tail/float certificate. For a normalized nonnegative edge-weight
mean cut (positive total weight), simultaneous coordinate error<=epsilon
gives mean error<=epsilon. Zero total weight gives cost0 separately.

An optional fit using phase estimates needs residual+epsilon times the total
nonnegative phase-mixture weight, plus deterministic roundoff/source errors.
The simultaneous bound remains valid for data-dependent fitted weights; no
unrestricted negative coefficients or untracked kernel estimates are allowed.
Without phase the fit is only a finite deterministic-tolerance statement for
28 means, not70 probabilities, tails, complete sampler equivalence or scaling.
Nonnegative/sum/reconstructed-residual checks are needed beyond solver status.

Input/source projection, supported native solver options, budgets, one-worker
runner closure and the future implementation remain to be reviewed. No P52
numerical evidence has been read or generated here. The missing useful global
implication must stay open regardless of a nonzero finite residual or(1).
