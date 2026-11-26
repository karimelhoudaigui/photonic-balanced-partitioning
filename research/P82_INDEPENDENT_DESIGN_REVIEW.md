# P82: exact-source independent design audit before implementation

26 November 2026. **Primary verdict: incomplete, with the smallest missing
implication being a total-cost high-order basin advantage over fixed strong
classical controls.** The displayed ideal circuit, full raw law, D repair
law and exact r=2 identities pass the internal reconstruction below.
These are structural checks, not a positive optimizer result or execution
authorization. The registered first classical veto and its budgets must be
frozen before author code, qualification or any main.

Only this review is written. No implementation, scientific import, AST,
test, RNG, matrix numerics, native call, probability query, hardware/QPU or
paper edit occurred. P84/P85 and P79 remain unchanged.

## 1. Exact artifact, dependency and independence boundary

All145 lines of `research/P82_HARDWARE_COMPATIBLE_ESCAPE_DESIGN.md` were
read in `.local/p65-independent-audit`, exact clean commit
`f7cb5d99fa35b6ab9e6ff60839f985d81ea87001`, SHA256
`c008f60143a1c4b0e81dcec1ba7a07c28d89244b10d4d69695070d27b0916723`.
The frozen design is not edited. ROOT supplied the route, its r=2 formula
and the proposed veto questions; this is an independent-agent AFTER-SOURCE
audit, not blinded reconstruction, independent discovery or agreement-based
proof. The separately authored P82a draft was NOT read and its author was
NOT contacted. This review makes no claim about what that unsealed draft
already resolves.

P82 uses a graph on2K vertices, K photons and2K optical modes, K=2d>=4
even. Its current S has K selected vertices and T=S^c has K. This direct
vertex-occupation model is not the protected all-balanced dual-rail oracle
in P81/P84. The target is the full raw, collision-retaining repaired basin
law, with a shared capped classical refinement, not a Gibbs distribution.
The algebra below uses exactly those objects, without a C* or optimum mask.

## 2. Circuit: unitarity, flatness and genuine internal phases

For the stated odds o_j=rho(1+eta h_j), rho>0 and0<=eta<1, h_j ranges
from-1 to1; d>=2 makes its denominator d-1 nonzero. Hence o_j>0 and
0<p_j=o_j/(1+o_j)<1. The same profile occurs once in each input half.
For C=diag(sqrt(1-p_i)) and D=diag(sqrt(p_i)),

    C^2+D^2=I,  CD=DC,
    [[C,iD],[iD,C]]^dagger [[C,iD],[iD,C]]=I.

The receiving matrix factors as

    W_phi=(H_2 tensor I_d)*diag(I_d,D_phi)*diag(F,F).

Each factor is unitary, so the complete2K-mode matrix in the design is
unitary. Each W entry has modulus1/sqrt(K); the occupied input columns
are exactly[C;i W D]. No inverse receiving mesh, nonunitary filter or
hidden ancilla is needed for this ideal matrix.

This phase dependence is not all row/column gauge. For rows a_r^sigma,
a_s^tau with r!=s and columns (0,j),(1,k), the gauge-invariant cross ratio is

    W_(r sigma,0j) W_(s tau,1k)
    --------------------------------
    W_(r sigma,1k) W_(s tau,0j)
      =(tau/sigma)*exp[i(phi_s-phi_r)]*F_rj F_sk/(F_rk F_sj).

All entries are nonzero, and relative phase changes alter this invariant.
A COMMON shift of all phi is an input-half column phase and is gauge;
only relative phases are informative. Discrete permutation equivalences
are not ruled out. This passes the stated nongauge test without claiming
that every phase vector defines an inequivalent optimizer.

## 3. Full normalized raw law and decoder corners

Fix the paid port marks. Observing a kept output forces its original
occupied input column because C is diagonal; kept counts are0/1. If R
is the set of missing kept vertices, its surviving receiver state is W
acting on one photon in each input port in R. There are no cross terms
between different measured R. For r=|R| and receiving counts |y|=r,

    q_R=product_(i in R)p_i * product_(i in S\R)(1-p_i),
    P_B(R,y)=q_R*|per W[y,R]|^2/product_a y_a!.

Input occupations in R are all1, so there is no omitted input factorial.
The kept occupations also have factorial1. The splitter phase i^r is a
common amplitude factor within this measured branch and disappears in
its probability. Unitarity of W normalizes the conditional Fock law;
sum_R q_R=1 normalizes the joint law. Thus R can be sampled first from
independent Bernoulli(p_i) coins even for indistinguishable photons.

The decoder chooses a uniform(r-h)-subset of T\B_y, h=|B_y|. This exists
because h<=r<=K and gives exactly K selected vertices without rejecting
a shot. Its coin denominator is binom(K-h,r-h). The repaired photons
are only classical candidate labels; they are not physical extra photons.

At r=0, the conditional receiving record is actual vacuum and X=S.
At r=K, the repaired candidate is always T regardless of y; its raw cut
equals C(S). Raw count records must still be preserved if a future
experiment promises the full raw law. Such a branch is not automatically
a null descent outcome unless the refinement is complement-covariant;
see section8. Loss would invalidate inference of R from missing kept
photons unless separately modeled and charged as loss, not as a transfer.

## 4. D comparator: exact conditional distribution, not a quantum gain

Flat intensities give

    per |W[y,R]|^2=r!/K^r,
    P_D(y|R)=r!/[K^r*product_a y_a!].

This is a multinomial count law from r independent uniform receiver
positions. Uniform repair is equivariant under every receiver permutation;
the resulting size-r subset is therefore uniform. Precisely,

    P_D(Y|R)=1/binom(K,r),  |Y|=r.

Independence from the IDENTITY of R is conditional on r. Unconditional
independence cannot hold because |Y|=|R|. This is a wording clarification,
not a failure of the displayed D law. D's cheap uniform-subset sampler
need not pay to simulate optical bunches when only its candidate law is
used. Independently optimized D families outside flat W remain mandatory
later; this exact comparator alone is not the positive acceptance gate.

## 5. Re-derived r=2 cancellation and surviving coefficient

For every fixed removed pair, flatness gives P_B(y_a=2|R)=2/K^2.
Receiver a clicks with probability2/K-2/K^2. Bunches at every other
receiver repair into a with total probability2/K^2; hence

    P_B(a in Y|R)=2/K

for EACH R. Linear and removed/received cross terms in a quadratic cut
therefore have no phase dependence.

Under equal loading R is uniform conditional on r=2. Row orthogonality
and flatness imply for distinct receivers a,b

    sum_(i<j)|per W[{a,b},{i,j}]|^2=1-2/K.

The direct contribution after averaging R is(1-2/K)/binom(K,2);
repair from a bunch at a or b adds4/[K^2(K-1)]. Their sum is
1/binom(K,2). Also P(i in R,a in Y|r=2)=4/K^2. These moments prove the
phase-independent MEAN CUT. They do not prove equality of the full
fixed-mark joint law(R,Y): conditional pair correlations can still vary.

For nonuniform loading q_R=q0*o_i*o_j in the two-photon branch, with
q0=product_(i in S)(1-p_i). Write sigma,tau in{+1,-1}. For a mixed input
pair (0,j),(1,k), the interference in output pair(r sigma,s tau) is

    (sigma*tau/2)*Re[exp(i(phi_s-phi_r))
                         F_rj F_sk conjugate(F_rk F_sj)].

Summing its q0*o_j*o_k weights gives

    (q0*sigma*tau/2)*|A_rs|^2*cos(phi_s-phi_r),
    A=F diag(o) F^dagger.

Same-half inputs and bunch repair are phase blind. Since a cut contributes
-2w_ab to a received pair, the four signs combine to the exact unconditioned
sector mean term

    -q0*sum_(r<s) Q_rs*|A_rs|^2*cos(phi_s-phi_r)=-q0 E(phi).

There is no extra conditioning normalization. At d=2,
|A_12|^2=(o_1-o_2)^2/4, agreeing with the design's K=4 formula.
Q and J are real symmetric. The coordinate contribution to E is
Re[exp(-i phi_r) H_r], maximized by phi_r=arg(H_r) when H_r!=0.
Thus each exact update is nondecreasing in E for every set of marks;
it strictly improves when its ACTUAL nonzero field is not aligned.
H_r=0 gives no strict-improvement guarantee even if other couplings exist.
These are exact-arithmetic statements, not unqualified float guarantees.

## 6. Additional all-r null control at eta=0

This internal consequence strengthens the required cancellation diagnostic;
it is NOT a claim about the nonuniform compiled algorithm. At eta=0,
A=rho I exactly, so every offdiagonal J and H is exactly zero. The
compiler keeps its independently drawn initial phases and therefore does
not depend on graph labels in the uniformly random receiving ordering.

Conditional on R and all unlabeled port data, let Y_ports be the repaired
size-r receiving subset. The independent uniform permutation from ports
to T maps ANY such subset to a uniform r-subset of T. Thus after the
declared receiving marks are averaged,

    P_B(R,Y)=p^r*(1-p)^(K-r)/binom(K,r),  p=rho/(1+rho),

exactly the flat-D/uniform-r-swap candidate law for EVERY r. This is a
decoded-candidate statement: full Fock counts, repair work and photon
resources can differ. A common refinement depending only on the candidate,
graph and fresh independent descent coins preserves this distributional
identity; a refinement that also uses private optical marks changes that
premise and must expose them to its controls.

There is a concrete prospective numerical hazard. Forming F diag(rho)
F^dagger in floating arithmetic can leave tiny nonzero offdiagonals. Squaring
them makes J tiny but nonzero, while arg(H) can still change a phase by O(1)
and inject graph dependence at eta=0. A future source must enforce the
analytic eta=0 branch J=0/keep-initial-phases, or freeze an explicitly
different justified zero-field model BEFORE execution. It cannot exploit
roundoff to violate this exact control silently. The separately authored
card/code was not read; this is an obligation, not an allegation about it.

## 7. Main design blocker: the compiler merit is not the raw high-order merit

The surviving r=2 coefficient is a polynomial classical XY objective.
Its improvement gives NO inequality for the complete mean, a large-r law,
the probability of entering a better basin, or improvement per total cost.
With future fixed bounds0<p_min<=p_i<=p_max<1,

    P(|R|=2)=q0*sum_(i<j)o_i o_j
       <=binom(K,2)*[p_max/(1-p_max)]^2*(1-p_min)^K.

It can therefore be exponentially small under macro loading. Conditioning
on r=2 would destroy the requested raw-attempt accounting. The two-photon
compiler may correlate with a useful high-order mechanism, or may hurt it;
neither direction follows from its coordinate monotonicity.

Fixed r<=r0 conditional receiver laws can be enumerated using
binom(K+r-1,r)=O(K^r0) tiny-permanent outputs GIVEN R. Enumerating every
removed subset as well costs another O(K^r0) factor; do not label that
joint exhaustive computation O(K^r0). Sampling R first avoids that extra
enumeration. Exact small-species controls and phase-hyperplane candidates
must receive the same graph/compiler features and all of their paid best
states. A small B-versus-flat-D fixture is not an irreducible benefit.

## 8. Mandatory first-veto and controller details before author code

1. Freeze one deterministic FIRST DEV comparison against the SAME fixed
   strong FASTMULTISWAP, frontier, sketch and zero-optics allowances (plus
   the declared compiler-rounding control). Pin their actual source versions,
   graph/seed schedule, loading/configuration policy, score/time/iteration
   caps, tie rules and credit for every scored candidate. The design's broad
   names are not a detailed executable contract. P82a may supply this, but
   its draft has not been inspected and no completion is presumed.
2. Be favorable to B: zero assumed optical latency, and give each fixed
   classical mode B's own paid classical compiler/repair/descent allowance,
   with its adapter/setup paid. Keep simulation-backend cost as a separate
   research-compute ledger; do not confuse it with future QPU latency. If
   one fixed cheap mode beats B on every predeclared DEV anchor, reject
   before D/species expansion or hardware. Passing this veto is not positive
   evidence. No free per-graph choice of favorable mode, seed or portfolio.
3. For each R, every repaired optical candidate is among binom(K,r)
   recipient subsets. A paid exhaustive frontier dominates its RAW score
   pathwise. To compare refined endpoints, apply/pay the same capped
   refinement to EVERY candidate, with a shared per-candidate descent-coin
   field for a coupling. Independent arbitrary realized coins do not give
   literal pathwise endpoint domination. Conditioning on a common incoming
   incumbent/history must not change one side's refinement definition.
4. Define the refinement's return as the BEST scored feasible candidate,
   including intermediate, incumbent and rounding candidates. A terminal
   state of a nonmonotone search is not automatically that object. Freeze
   all score-cache, partial-scan, restart and tie costs; do not assume
   unlimited descent-to-stationarity is free or polynomial.
5. Raw cut classes identify r and K-r by complementation. At K=4 all
   classes are within two swaps. At K=6, binom(6,2)^2=225 two-swaps and
   binom(6,3)^2=400 three-swaps, together with smaller swaps, cover all
   raw cut classes. But an arbitrary capped stochastic refinement need
   not commute with complement. Require complement-covariant ties/coins
   or pay both orientations as cheap classical candidates. In particular
   any gain from refining T at r=K is replicable without optical transfer.
   Only min(r,K-r)>3 supplies the intended NEW raw displacement; K>=8 is
   necessary, not sufficient for a surviving high-order advantage.
6. Before expanding beyond the first veto, require independently optimized
   D outside this flat family, bounded-species controls, strong correlated
   feasible search, fresh graph seeds/relabels, matched total budgets and
   independent replication. Uniform relabels are not independent graphs.
   No exact C*, target mask or known optimal partition enters training.

These are material protocol obligations before implementation/main, not
reasons to edit the sealed mathematical design or invent a successful run.

## 9. Old-bound scope and hardware/readout boundary

The receiving cross block i W D has full bank-to-bank rank K with singular
values sqrt(p_i)>0. That bypasses a low-cross-rank assumption in THESE
banks, without proving ranks in arbitrary target partitions. More directly,
the event is a classically repaired candidate, not the old literal full-CF
target. P69–P72 must still be applied to any diagnostic satisfying their
actual raw-target premises; this audit does not erase them.

P81/P84 require a fixed unitary preserving every balanced logical-basis
input/code; P82 does not supply that counterfactual promise and retains
pair/code leakage. Its direct finite-Fock source is not the Gaussian
pair-state input of P77–P80. Random individual port marks and graph-current
features provide covariance in law, not the pathwise symmetry premises of
P67/P68. No transpose coin or reversibility claim repairs those differences.
P59/P63/P65 remain prior controls/negative precedents, not supporting
performance data revalidated by this static audit.

The decoder requires kept-port support and receiving support. Ideal
lossless R/r inference does not turn undetected photon loss into a valid
transfer. A real experiment needs source/attempt/loss accounting and a
readout contract; a passive matrix alone does not authenticate today's
Lucy/TGCC input photon number, modes, losses or PNR allocation. No physical
availability, credentials or QPU job was checked or authorized here.

## 10. Static local Perceval API advice, not runtime qualification

Pinned installed Perceval sources were READ ONLY. No module was imported
or object constructed. Source locators/hashes under site-packages/perceval:

| Source | SHA256 |
| --- | --- |
| backends/_clifford2017.py | 8dad1b8f389f346bde1b902f21d74e1466eabb258aeb0e92f827ff745d27329b |
| backends/_naive.py | aaa26604b0866eeba61aaca80e83afe4df689711f4ce3bf965db1da74314ef4d |
| backends/_abstract_backends.py | 53f7c4db865c2e643b9ab461da0c71b2fbb9dc1a450ad917936ca0f4e25538f1 |
| utils/_random.py | d56c9fc42986ee3e16f3d1110962044b3a91dcb7023315ca7db8a5aa21a2cea4 |

`Clifford2017Backend` exposes set_circuit, set_input_state, sample and
samples. The wrapper forwards the computed unitary and Fock input to
Exqalibur and sample() to its native sampler. A prospective ideal sampler
can first draw R from its known classical Bernoulli law, set the K-mode
receiving W circuit with Fock input1_R, and request ONE full receiving count
sample. This realizes the conditional law, then the same repair, without
enumerating all binom(K+r-1,r) outputs on every main shot. r=0 has a unique
actual vacuum record; do not invent a sampled nonzero receiving pattern.

NaiveBackend.prob_amplitude repeats the target rows/input columns and
divides by sqrt(product input/output factorials); it is appropriate for
tiny hand-checked full-law qualification, not an assumed cheap full-r-sector
main enumeration. Clifford's compiled implementation/physics/reproducibility
has NOT been qualified here; the Python wrapper alone is not that proof.

`perceval.utils.random_seed(explicit_integer)` statically calls Python
random.seed, NumPy's legacy global seed, and xq.set_seed. It does not
explicitly seed existing new Generator instances; mark/repair streams need
their own frozen seeds. Passing None requests a time-based seed and must be excluded.
Freeze native seeding order and configuration/readback1 around actual
calls. samples(count) is documented as parallel batching; it cannot consume
future adaptive-controller inputs before they exist. Exact native and
independent tiny-point checks belong to a later separately authorized
qualification, with all failures/prefixes preserved and zero retries.

## 11. Audit handoff

The ideal algebra passes at the stated scope, including the stronger
eta=0 decoded-law control, which itself needs exact-source independent
review before being used as a load-bearing extra claim. Full raw high-order
basin benefit remains OPEN. The primary verdict is incomplete because
neither the structural identities nor the generic design specify a passed
first fixed strongest-classical veto. The cheapest next step is the
separately frozen first-veto card and its audit BEFORE author code; this
review does not authorize it, implementation, tests or main. No new
experimental result or positive scientific gate is asserted.
