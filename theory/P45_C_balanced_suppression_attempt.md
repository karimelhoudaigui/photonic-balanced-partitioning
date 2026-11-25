# P45-C: balanced collective proposals and an exact classical countercontrol

Owner physics, 2026-11-25. Base worktree revision
`58850769d4c8ef508c7a1d1cc9bb6b7f6bcf7198`. This is new analytic work;
P42--P44 evidence is unchanged. No P45 numerical code/run/raw exists.
The original positive-search objective remains OPEN. The result below closes
one specified symmetric construction, not all passive/interfering proposals.
Derivations are author self-checks pending a claim-first independent review.

## Target and discriminator

An anchor S0 is found by charged classical descent to a 1-swap minimum, without
optimum labels. Occupied modes are graph vertices in S0; empty modes are its
complement. A proposal must be scored by its UNCONDITIONAL probability of
strict improvement and accepted gain per physical attempt, with all failures
charged. Conditional CF enrichment alone is insufficient. Any already scored
improving block exchange is credited to the common classical incumbent.

The relevant comparison includes the same-graph/block distinguishable kernel,
independent pairs, uniform feasible core, graph-aware nonlocal block proposals,
species groups of at most three photons, and exact classical reproduction
where feasible. Fixed six-photon blocks have924 CF supports in12 modes, not64;
64 is only the one-per-matched-pair subspace, which is not assumed. Their full
Fock law has12376 occupations. An exact-block classical control must include
all924 candidates or the demonstrated smaller support, and charge preprocessing
and scoring. Spectators do not increase the coherent component size.

The nearest previous record, root `reports/PHASE2_STRUCTURED_PROBE.md`, was
read for context. Its bounded two/three-photon replacement result already
precludes treating a new constant-size boson/distinguishable gap as a scalable
optimization mechanism. No previous numerical result is rerun or recertified.

## Route C1: a genuine balanced effect with a polynomial replacement

For b>=2 define

    rho^2=(b-2)/(2(b-1)), rho>=0,
    beta=(1-rho)/b, gamma=sqrt(1-rho^2),
    B=rho I+beta J, C=gamma(I-J/b),
    U=[[C,B],[B,-C]].

The input has one photon in each of b old modes, with b empty new modes.
B,C are commuting Hermitian matrices, BC=CB, B^2+C^2=I. Consequently U is
unitary. Since (B^2)_aa=(1+(b-1)rho^2)/b=1/2, every source photon has exactly
half its one-particle mass in old modes and half in new modes. There is no
weak interaction angle or Haar assumption.

This family has real interference enrichment. At b=3,
B has diagonal2/3 and off-diagonal1/6. Its full-new-block amplitude is

    per(B)=(2/3)^3+3(2/3)(1/6)^2+2(1/6)^3=13/36.

Thus the raw full-transfer probability is169/1296, compared with1/8 from
independent balanced pairs: ratio169/162. The same-B distinguishable full-
transfer probability is per(|B|^2)=691/7776, smaller again. These are exact
hand derivations, not a numerical experiment. They are not evidence of search
advantage: a classical random whole-block exchange already assigns probability
1/2 to that move, and its cost can be scored directly. If b is the WHOLE
balanced anchor, full transfer merely gives its complementary partition and
does not improve an undirected cut. A partial-block illustration would need
at least one occupied spectator outside the block.

### Exact CF-plus-failure sampler for ALL b

The scalable obstruction is stronger than constant-block enumeration. A CF
output selects b DISTINCT rows from the old/new pair-indexed2b modes. At each
index there are zero, old-only, new-only, or both selected rows. Let their
counts be e,u,v,d. Photon count and pair count imply

    e=d, b=2d+u+v.

Each selected row r has the form

    M_(r,j)=d_r delta_(index(r),j)+c_r,
    old: d_r=gamma, c_r=-gamma/b,
    new: d_r=rho,   c_r=beta.

In the permanent expansion choose h rows to use their diagonal term. At most
ONE can be chosen from a given pair index, since diagonal choices must use
distinct columns. For a fixed choice, the remaining constant rows contribute
(b-h)! times their c_r product. Therefore

    per(M)=sum_(h=0)^b (b-h)! [z^h] P(z),
    P(z)= product_index [ product_(rows at index)c_r
              +z sum_(r at index) d_r product_(other rows at index)c_r' ].

Empty-index factors are1. For the four index types this reduces to

    P(z)=(c_old+z gamma)^u (beta+z rho)^v
         [c_old beta+z(gamma beta+rho c_old)]^d.

Degree-b polynomial multiplication computes the coefficients in O(b^2)
arithmetic. Hence every CF support in a given (d,u,v) orbit has the same
amplitude, and its orbit has size

    M_(d,u,v)=b!/(d! d! u! v!).

There are only O(b^2) orbits. Their total probability is

    P_CF=sum_(2d+u+v=b) M_(d,u,v) |per(M_(d,u,v))|^2.

The following classical proposal reproduces the ENTIRE candidate kernel,
including its failed attempts, without graph-optimum information:

1. Compute the orbit probabilities in O(b^4) arithmetic preprocessing.
2. Return failure with probability1-P_CF, just as collisions do physically.
3. Otherwise select an orbit with its probability weight, then uniformly assign
   its d double, d empty, u old-only and v new-only indices to the b labels.
4. Score the resulting feasible graph candidate using the common graph oracle.

Orbit multiplicities sum to binom(2b,b), covering every CF support. The random
label assignment takes O(b) work after preprocessing. The arithmetic quantities
lie in Q(rho,gamma), of degree at most4 over Q; bit/sampling precision still
needs its usual explicit implementation contract. This is an exact arithmetic
probability description, not a double-precision certificate or an experiment.
Only CF outcomes and their complement failure are aggregated; no polynomial
sampler for the uncollapsed full colliding Fock law is claimed.

This control works at growing b, not merely b<=3. For fresh history-dependent
anchors the same construction gives the same next candidate/failure law;
induction reproduces any update policy that observes only that collapsed
history and its charged graph scores, with the stated preprocessing cost.
A policy using the detailed failed collision pattern is NOT covered by this
candidate/failure replacement. A graph-dependent diagonal gauge D gives
B'=DBD*, C'=DCD* and cannot alter number probabilities. In this positive
two-eigenvalue seed, exact per-column balance also forces the special
rank-one eigenvector to have flat magnitudes; varying its phases is just such
a gauge. This does not assert the same result for every rank-one matrix or
every other degenerate eigenvalue choice.

**Disposition C1:** this family's CF-plus-failure use is unsuitable as a
nonclassical proposal subroutine, even though its raw optical enrichment is real. Its
closure is an explicit polynomial replacement proof, not a universal no-go.
No small pilot or parameter retuning is justified for this resolved question.

## Route C2: projector mixer, gauges and the growing-size obstruction

For b=2q and a q-by-q unitary W, put

    H=[[0,W],[W*,0]], P=(I+H)/2, Q=I-P,
    U(W)=[[Q,P],[P,-Q]].

H^2=I and diag(P)=1/2. P,Q are orthogonal projectors, so U is unitary and
exactly50/50 in total occupied/vacant one-particle mass. W can connect all
2q input photons before detection; the balanced construction does not require
weak angles. It remains passive linear optics.

Two exact null controls precede any graph-benefit claim. For diagonal unitaries
D_A,D_B and D=diag(D_A,D_B), replacing W by D_A W D_B* gives

    U(W')=(D directsum D) U(W) (D* directsum D*).

CF input Fock states and terminal number probabilities are invariant under
these input/output phases. Also U(conj(W))=conj(U(W)), so its ENTIRE number
law is unchanged. In particular W=exp(i tau C), C real symmetric, gives the
same law for C and -C. One cannot infer a universal preference for negative
swap synergies merely from the sign of that generator. A classical block
selector can of course depend on those signs; its work is then the mechanism
to credit and control. This is a kernel symmetry, not a constructed universal
counterexample for every nonnegative graph ensemble.

If W has bounded-size diagonal blocks after row/column permutations, U has
bounded coherent components. A W block of size r produces2r photons in4r
physical modes. Direct exact replacement costs only a fixed amount per
component when r is bounded. A core of six photons therefore gives no scalable
separation by itself. Likewise, product internal species groups of size<=3
admit direct classical full-law simulation per species, followed by summing
their occupations INCLUDING inter-species collisions. This physical control
is distinct from restricting U's spatial connected components.

For arbitrary growing q, the shared permutation or bounded-component argument
need not hold. No efficient classical simulator for all such W is proved here;
absence of this particular proof is also not a hardness theorem or a search
benefit. The new bottleneck is useful graph-correlated mass on MANY unscored
candidate exchanges, after phase/gauge, nonlocal matching and low-species
controls, with raw CF/failed-shot cost retained.

### A phase witness beyond one-particle intensities is still insufficient

The explicit four-mode complex Hadamard family, z=exp(i phi), is

    V(phi)=1/2 [[1,1,1,1], [1,z,-1,-z],
               [1,-1,1,-1], [1,-z,-1,z]].

It is unitary and every entry has squared magnitude1/4 for every phi.
Grouping columns{1,3} and{2,4} in the permanent gives

    per(V(phi))=(1+z^2)/4,
    |per(V(phi))|^2=cos(phi)^2/4.

Hence genuine multiphoton probabilities can change while every one-particle
intensity, and the distinguishable probability3/32 of this CF pattern,
stays fixed. The effect is not explained by a row/column phase gauge. But
this is a four-mode finite diagnostic, and in its stated all-input/all-output
form it has only one CF support: it is not a graph-search proposal. No probe
of it is run. This witness motivates a phase-matched control, not an advantage.

## Graph information, accounting and next bottleneck

For graph cut C(x)=d^T x-x^T A x and disjoint paired swaps
delta_p=e_(v_p)-e_(u_p), their subset cost change is

    Delta C(z)=sum_p g_p z_p +sum_(p<q) J_pq z_p z_q,
    J_pq=-2 delta_p^T A delta_q.

All g,J derive from G and S0, not C*. However, selecting a subset after
explicitly evaluating this quadratic has already done a classical proposal.
Every actually scored mask updates the credited common incumbent; spectral,
matching and exact-core candidates require their scored costs. Evaluation-only
labels must never feed parameter/block selection. Random graph labels, input
pair orders and ties are fixed before outcomes; no favorable graph selection.

Required controls for a future G,S0->W map include a shared uniform-feasible
core and nonlocal block/matching/DP proposals, exact distribution or best of
all924 CF outputs for fixed b6 with all preprocessing charged, and physical
species groups<=3. A classical covering law with the same cheap suppression
constraint is necessary but need not reproduce the optical weights.

Suppression alone does not provide graph bias. For example, the Fourier
zero-transmission rule constrains an output-label sum modulo a port number.
Uniform CF subsets satisfying that residue can be counted/sampled by a
classical size-and-residue DP; this does NOT reproduce all optical weights.
Tichy et al., published [PRL104,220405](https://doi.org/10.1103/PhysRevLett.104.220405),
Eq.(6) and its appendix in [arXiv:1002.5038v1](https://arxiv.org/pdf/1002.5038v1),
were inspected for that established suppression rule. It is a sufficient
zero rule, not a complete characterization of allowed probabilities or an
optimization theorem. The fetched PDF's generated front-date differs from
its2010 arXiv footer; no binary version hash or complete-source audit is claimed.

The remaining positive obligation is a growing, non-gauge G,S0->W construction
with a provable or reproducibly tested raw improvement enrichment that the
charged classical controls do not explain. The raw rate must not collapse
with b or be purchased by uncharged classical block optimization. P43's mean
oracle and P44's low-transmission obstruction remain separate constraints.
The hollow, centered full-source construction in a new P46 note changes the
transport bottleneck and is the authorized continuation; it is not a success
in this note. No run is planned while encoding has numerical priority.

## Handoff

Closed narrowly: C1's symmetric CF-plus-failure kernel has the explicit
polynomial classical replacement above. Preserved: real small interference
enrichment, exact gauge/conjugation symmetries, full-core candidate counts.
Open: growing-rank graph programming and useful improvement probability, or
decoders/policies that use detailed non-CF patterns rather than merged failure.
Next action: analyze full-source hollow spectrum and collision/transport
invariants in P46; do not rerun the C1 finite enhancement or call the whole
photonic route impossible. A blind reviewer should receive the separate claim
card BEFORE this author derivation; no P45 numerical raw exists to forward.
