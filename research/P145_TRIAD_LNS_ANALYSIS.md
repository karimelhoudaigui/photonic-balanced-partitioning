# P145 — Three-photon LNS: exact triad signal and the missing algorithmic bridge

26-Nov-2026. MANUAL ONLY, self-reviewed candidate for independent review.
Pinned project base: 2fdf942192faec1377563e70d31d9c5d2d0b8c3a; new isolated
branch research/p145-triad-lns preserves the preceding research branch.
Read the c47aafb3 user attachment, P65, P138–144, P33 contract/density source
and applicable AGENTS/proof-audit instructions. No import/AST/program,
numerical/symbolic evaluation, RNG, test, graph draw, native/QPU or paper edit.
P33/P37/E05b and all positive physical contrasts/negative results stay intact.

Primary verdict on “I3>0 implies a useful optimizer”: REFUTED below.
The same-circuit three-cycle identity is exact. A useful collective RAW
contrast is constructed, but it fails a stronger routing/classical control.
The prescribed adjacency-plus-boundary ansatz fails identically on that barrier.
A constant-size measured PLNS kernel also has a constructive classical mirror
under explicit representation assumptions. No advantage or novelty is claimed.

## 1. Exact residual, and the complement trap

Let x be the current balanced cut of an undirected nonnegative graph. Choose
a six-vertex block B with three currently selected vertices R; freeze the
outside assignments. Selection must not use C*, optimal masks or an unpaid
best block. Put h_i=sum_(j outside B) w_ij(1-2x_j). For z in {0,1}^6,

    C(z,x_out)=C_out+sum_i(deg_B(i)+h_i)z_i
                              -2sum_(i<j in B)w_ij z_i z_j.           (1)

C_out is the imbalanced all-zero-block helper cost, not a feasible incumbent.
Each feasible output has sum z=3. Define gain u(Y)=[C(x)-C(Y,x_out)]_+.
All collisions/loss/invalid records hold x and have zero RAW utility.
Fields, block selection, scores, synthesis and every attempt/photon are paid.

Internal edges are invariant under z -> 1-z. The boundary difference is
sum_i h_i(1-2z_i). Consequently CONSTANT h (including h=0) makes every
three-set and its block complement equal-cost. Every two-replacement target
is the complement of a one-replacement neighbor; the three-replacement target
is the complement of R. A one-swap local minimum is then already optimal
over all 20 candidates. Its accepted gain is identically zero for EVERY
optical law. A six-vertex isolated local-minimum test cannot demonstrate
barrier escape. Nonconstant boundary fields remove this particular obstruction;
they do not guarantee a useful interferometer. Global complement invariance
does not justify complementing ONLY a block while fixing its outside.

P65 already proposes a measured current-state photonic proposal chain;
P138/P141 use incumbent-residual RAW gains; P142 already specifies 3-in-6
with full-graph boundary fields. Calling this PLNS does not create a new
physical class. The proposed graph map H=alpha*A_B+beta*diag(h) is a concrete
different compiler from P141's reflection, not a new source/instrument class.

## 2. What I3 isolates, exactly

Fix the SAME transfer, input R, detector/decoder, graph and utility in all
five arms. D has three orthogonal tags; P_ab has only a,b identical; B has
all three identical. Include no uncounted helpers. For a complete count n,
repeat its output rows o_j, put a_sigma=product_j W_(o_j,sigma(j)), and define

    E_pi(n)=(1/n!)*sum_sigma a_sigma*conj(a_(pi composed sigma)),
    n!=product_j n_j!,       c=(123).

The permutation expansion gives p_D=E_e, p_ab=E_e+E_(ab), and

    p_B-p_12-p_13-p_23+2p_D=E_c+E_(c^-1)=2Re E_c.                    (2)
    I3(u)=J_B-J_12-J_13-J_23+2J_D=sum_n u(n)*2Re E_c(n).             (3)

Thus I3 is a SIGNED exchange contribution, not a probability, sampler,
Sorkin/Born-rule interference order, or advantage certificate. At loss it
uses a common physical dilation; for u supported on full-survival CF, the
same terms can be computed from the signal transfer without renormalization.
Subtracting separately OPTIMIZED J values does NOT isolate three-cycles.
Report the same-setting diagnostic and each arm's independently optimized
performance separately. Five sampled arms each pay their own three photons,
training/probes and uncertainty; a noiseless exact-law identity is not a
statistical or independent physical replication result.

Normal ordering selects at most two source labels for occupation degree<=2.
Therefore I3(f)=0 for EVERY polynomial f of occupation degree<=2, including
the extension (1), at any fixed common passive transfer. Let g=C(x)-C(n)
using that algebraic extension, V=valid receiver CF and I=its complement.
Since u=g_+*1_V and I3(g)=0,

    I3(u)=-I3(g*1_I)+I3((-g)_+*1_V).                               (4)

The invalid-sector redistribution and acceptance cutoff can carry a genuine
RAW utility effect; they may not be silently omitted or called a downhill
unconditional quadratic energy. The extension is not a physical cut on
collisions. This specializes P142's moment warning to the five-arm diagnostic.

For U(t)=exp(-itH), H Hermitian, U(0)=I, P139 applies per fixed block/curve:
admitted D(3t) dominates B(t) in some nonuniform positive local window, K=3.
Common gain/hold and all records are essential. P143 extends the weak-null
restriction to specified finite tag-blind instruments, including counted
helpers. Neither theorem rules out finite-strength useful contrasts, measures
equal wall cost, or establishes dominance of complete adaptive LNS searches.

## 3. A global strict local minimum and an exactly solvable falsifier

ROOT supplied this nonnegative 12-vertex realization; the cases below were
reconstructed manually. Let R={0,1,2}, Q={3,4,5}, A={6,7,8}, D0={9,10,11}.
Inside R and Q put clique edges w>0; inside A and D0 put clique edges 3w;
join EACH Q vertex to vertex6 by weight3w. Every other edge is zero.
Current x=R union A is balanced and has cut9w. Use B=R union Q, so
h_R=0, h_Q=-3w. Replacing q vertices gives

    Delta C(q)=2w*q*(3-q)-3w*q=w*(3q-2q^2).                       (5)

For q=0,1,2,3 the gains are 0,0,2w,9w. This is not a six-vertex
complement-symmetric example. All 36 GLOBAL balanced one-swaps strictly
increase the cut; the complete classes are:

| Removed -> added | Multiplicity | Delta C/w |
|---|---:|---:|
| R -> Q |9|1|
| R -> D0 |9|8|
| 6 -> Q |3|2|
| {7,8} -> Q |6|5|
| 6 -> D0 |3|3|
| {7,8} -> D0 |6|12|

Yet Q union A has cut0. Components expose this solution classically; it is
an intentionally easy barrier, not a selected DEV/held-out instance. Balanced
monochromatic spectator cliques can embed it in a larger graph without any
new photons, but do not remove that classical veto.

For the ATTACHMENT'S H=alpha*A_B+beta*diag(h), R and Q are disconnected
in A_B and remain invariant for every alpha,beta,t. Photons injected in R
never reach Q. Its RAW gain is IDENTICALLY ZERO for all five source models.
Correct boundary fields alone cannot create nonedge hopping. Adding a dense
mixer changes the compiler; a P65-style background mixer is already known
in the project and is not itself a new mechanism.

For a separate known optical fixture let omega^3=1, omega!=1 and
F3_(j,a)=omega^(j*a)/sqrt(3), j,a=0,1,2. Choose

    H0=[[0,F3^dagger],[F3,0]], H0^2=I,
    U(theta)=exp(-i*theta*H0)=[[cI,-isF3^dagger],[-isF3,cI]],
    occupied columns=[cI;-isF3], p=s^2, c^2=1-p, 0<=p<=1.           (6)

This PUBLIC mixer is NOT the failed adjacency compiler and is not graph
training. It is used solely to falsify an inference from a triad witness.
For the all-Q CF event REMOVE the common transfer factor (-is)^3: the six
assignment amplitudes then consist of three omega and three omega^2 factors
over sqrt(27). Their coherent square is
1/3, D is6/27=2/9, and each one-pair law is1/9. Both oriented three-cycle
terms contribute2/9, so the isolated CF contribution is4/9.

Every two-by-two F3 permanent has squared modulus1/9, versus D2/9.
Retained R rows fix their source labels. The following probabilities are
TOTALS over CF states in a replacement stratum, with no CF denominator:

| q and number of targets | B | D | a fixed P_ab |
|---|---|---|---|
|0,1|(1-p)^3|(1-p)^3|(1-p)^3|
|1,9|3p(1-p)^2|3p(1-p)^2|3p(1-p)^2|
|2,9|(1-p)p^2|2(1-p)p^2|(5/3)(1-p)p^2|
|3,1|p^3/3|2p^3/9|p^3/9|

In q2, exactly three targets move the interfering pair; six do not. This
explains the pair total. Unlisted RAW collision mass holds x and is paid.
Multiplying by the gains from (5) gives the exact manual identities

    J_B=w*(2p^2+p^3), J_D=w*(4p^2-2p^3),
    J_ab=(w/3)*(10p^2-7p^3), I3=4w*p^3>0 for p>0.                  (7)

B>D at the SAME setting iff p>2/3; B>P_ab iff p>2/5. Even allowing
each arm its OWN p, max J_B=3w, max J_D=2w and max J_ab=4000w/3969
(the pair maximum is at p=20/21). This is a genuine finite-strength RAW
contrast ONLY in the artificially restricted fixed-F3/variable-p family.

A physically legal monomial full transfer R->Q instead gives D gain9w.
It is a separate routing control, not asserted to lie in exp(-it[alpha*A_B
+beta*diag(h)]) or in (6). Classical block search/component recognition also
gets9w. At p=1 the fixture merely changes the collision-free yield of a
FORCED known Q preparation: that is explicitly NOT optimization benefit.
Thus even positive useful I3 AND restricted retuned-pair superiority can
fail both the known-solution/preparation gate and the strong-classical gate.
The tritter physics is known; this is no novelty or algorithm-positive claim.

## 4. A finite-strength classical mirror, including adaptive PLNS

Suppose each call prepares a fresh prescribed 3-CF-photon source, with no
retained quantum memory. The controller uses each measured 6-mode block only
via its 20 feasible outputs Y and the invalid hold atom. Given its THREE
occupied signal columns T, compute p_Y=|per T[Y,:]|^2 using SIX products per target;
put p_fail=1-sum_Y p_Y. Physical contraction guarantees nonnegative mass.
Sampling these 21 categories produces EXACTLY the optical update law.
No cost C(Y) is used in constructing this sampler: score only the sampled
candidate, just as the optical arm. It does not sneak in 20 graph-score calls.

For a supplied Gaussian-rational T this is constant-many exact rational
operations with their bit cost charged; a shared denominator yields integer
categorical weights and an unbiased-bit sampler. Exact sampling need not
have a deterministic finite wall cap. For exp(-itH), obtaining sufficiently
certified amplitude probabilities is an additional precision obligation,
not an exact-transcendental arithmetic oracle. Matrix/feature construction,
sampling and precision costs must be measured; no equal-wall win is proved.

Induct on the transcript: copy the SAME classical block/parameter policy,
sample its current conditional 21-outcome kernel, and apply its SAME scoring
and acceptance update. The entire adaptive transcript law then agrees, not
merely a one-step mean. With conditional TV error<=epsilon_l, coupling gives
total transcript TV<=sum_l epsilon_l. This is a model-conditioned mirror,
not a statement about unknown/calibration-mismatched hardware.
If the policy uses detailed invalid records, the coarse FAIL mirror is
insufficient: sample all56 lossless PNR outcomes, or a specified full physical
loss dilation before tracing its loss modes. Independent loss coins are not
an automatic replacement. Fixed three photons still keep these explicit
finite laws tractable; every added mode/record/precision cost must be counted.

## 5. Certificates, changed alternatives and next decision

P33 requires CF input, orthonormal FULL occupied columns and the SAME B/D
device/observation. Its M is EXPECTED unordered collision pairs, not collision
probability; its density floor includes every nonzero output mean. The sharper
d_c(M) branch requires M<c^2/2. For 0<=u<=R_gain, common decoding gives
|J_B-J_D|<=R_gain*TV<=R_gain*Phi(d_c(M)) in its certified regime.
One may take R_gain=C(x) for nonnegative cuts. Paid certificate computation,
floating-vs-certified bounds, common loss dilation and setup remain explicit.
It certifies an absolute-error classical replacement only; failure certifies
neither useful I3, hardness, retuned advantage nor QPU readiness.

Two changed directions, NOT authorized pilots or new-discovery claims:

| Route | Change beyond measured tiny PLNS | First load-bearing falsifier |
|---|---|---|
| Coherent growing block | Grow the number of jointly interfering photons/retained quantum state; compose overlapping windows WITHOUT terminalizing each into a fixed three-photon classical kernel. Global passive proposals already occur in P65, so this alone has no priority. | A bounded-width/tensor/exact sampler, proper-group controls or paid multi-exchange search reproduces the useful distribution. More modes at fixed three photons alone remain polynomially enumerable. |
| Occupation-dependent instrument | A specified genuine cost interaction or retained-state measurement/feed-forward mechanism, with every helper/herald branch paid; no mere classical reweighting or known-solution preparation. P65C/P116/P140 already expose resource/classical traps. | P143's common tag-blind analytic deterministic-null premises invoke its weak obstruction; otherwise require a finite-strength graph-utility sign that survives complete D/group/classical retuning. Fixed-size Hilbert space alone is still classically simulable. |

For a three-photon hardware-size study the defensible next check is the
exact kernel/cost falsifier above, not a claimed optimization pilot. Any
actual run needs a separately frozen population, source review and authority.
The open useful question is a resource mechanism escaping the classical
mirror; a new label, graph size100 or more sampled blocks does not supply it.
Lucy source/PNR/full-attempt/calibration/latency capabilities are UNVERIFIED;
no feed-forward API or QPU call is inferred. Attachment citations not already
authenticated by P65/P144 are not imported as proof or novelty evidence.
Only this note is changed; all derivations need non-author review before use.
