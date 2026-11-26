# P146-B — Balanced majority decoding of every occupation

27-Nov-2026. ANALYSIS ONLY; branch research/p146-b-decoding starts at ROOT
fbefdb4d15120cb550178a83014d59141022939a. Previous research branch preserved.
Read attachment dd2300f9, AGENTS, P55 card/result, P94, P103, P105, P142 and
P145 analysis/growing-coherence proof. No import/AST/code, graph draw, numerical
evaluation, RNG, test, native/QPU call or manuscript/register edit occurred.
This is a self-derived candidate/obstruction, awaiting non-author proof review.
Original optimization goal: OPEN. The small construction below is REJECTED as
an optimizer, despite an exact useful third-order physical contrast.

## 1. An all-shot map with bounded decoding work

Pair the graph's N=2L vertices publicly as(l,+),(l,-). For s in{+1,-1}^L,
S(s) selects(l,s_l); it is always a balanced L-set. This restricts the search
to a disclosed paired code; classical controls may also search outside it.
Let v_a in{+1,-1}^L, a=0,...,r-1, be a shared library of feasible parent
partitions, and s0 the incumbent. Parents come from public marks or PAID
classical search; none may be selected using C*, optimum masks or hidden cuts.

For EVERY detected occupation n>=0, including losses and vacuum, set

    z_l(n)=sum_a n_a v_(a,l),
    s_l(n)=sign(z_l(n)) if z_l!=0, and s0_l otherwise.                (1)

Return S(s(n)); optionally accept it only when its ONE newly scored cut improves
the incumbent. Collision multiplicities are votes, never physical failures.
Vacuum returns the incumbent. All emitted photons and attempts remain charged.
Evaluation needs O(Lr) integer work, O(Lr) library storage and one graph score;
there is no subset optimizer or minimum-cost completion inside(1). Skipping
zero n_a reduces work but is not an unmeasured runtime claim. Ties, pairings,
parent orientations and marks transport together under relabeling.

Graph-to-parameter example for a growing-library continuation: write the EXACT
paired cut as C(s)=c-(1/2)sum_(l<h)J_lh s_l s_h, where
J_lh=sum_(sigma,tau) sigma*tau*w_((l,sigma),(h,tau)). Within-pair edge weights
enter c in full; between-pair weights enter c with factor1/2. Make J symmetric,
zero diagonal, and set H_ab=v_a^T J v_b/W for a!=b, H_aa=0, with
W=max(1,max_a sum_b |v_a^T J v_b|). Then H is real symmetric with norm<=1;
U(t)=(I-itH)(I+itH)^(-1) is a specified passive unitary. Known CF inputs are
a public K-subset of its r modes. All graph contraction/library/Gram/inverse/
mesh costs are shared and paid. This compiler is a conventional Cayley map,
not a new physical interaction. NO beneficial sign is proved for this map.

Unlike P55, counts label entire parents, not vertex defects to be balanced by
a global DP. Unlike P94, the result is not a function of parity: (3,0,0) and
(1,2,0) have identical parity but return different parents when v0!=v1.
Unlike P142's quadratic occupation extension, decoded cuts need not be degree2.

## 2. Exact third-order lemma, including every collision

Take K=r=3, all CF inputs, and the balanced Fourier tritter
F_(j,a)=omega^(ja)/sqrt(3), omega^3=1, omega!=1. Let
m=Maj(v0,v1,v2), coordinate by coordinate. If a mode has at least two photons,
(1) returns its parent; the sole CF record(1,1,1) returns m. These exhaust
ALL ten three-photon occupations; nothing is postselected or normalized away.

For any utility u of the decoded partition define ubar=(u(v0)+u(v1)+u(v2))/3.
The complete decoded law for B, D and EACH fixed interfering pair is

    E_X u=(1-p_X)*ubar+p_X*u(m),
    p_B=1/3, p_D=2/9, p_12=p_13=p_23=1/9.                         (2)

Derivation: B gives each(3_j) probability6/27=2/9 and suppresses all six
(2_j,1_h), since1+omega+omega^2=0. Its CF permanent has square1/3.
D gives each triple1/27 and each doubled record3/27. A pair gives each triple
2/27; each doubled record is(2/9)*(1/3)+(1/9)*(1/3)=1/9, and its CF mass1/9.
Thus the mass returning EACH parent is2/9,7/27,8/27 respectively. This proves
(2), including all occupation factorials, zeros and collisions.

Consequently the same-circuit third-cycle contrast is

    I3(u)=E_Bu-E_12u-E_13u-E_23u+2E_Du
         =(4/9)*(u(m)-ubar).                                    (3)

An occupation polynomial of degree<=2 has I3=0: normal ordering selects at most
two distinct CF source labels. Therefore a nonzero(3) is a genuine dependence
on higher collective moments, not a quadratic-mean reinterpretation. The
TRITTER physics is already in P145; the changed object is the all-shot decoder.

Hand graph demonstrating useful collision mass: L=3, unit edges
{(1,+),(2,+)} and{(1,+),(3,-)}, all other weights0. Choose graph-independent
parent words v0=(+,+,+),v1=(+,-,-),v2=(-,+,-), m=(+,+,-), incumbent s0=v2.
Their balanced cut costs are1,1,2,0. Hence gain u=[2-C]_+ is1,1,0,2, and

    J_B=10/9, J_D=26/27, J_pair=22/27, I3(gain)=16/27.              (4)

Collisions contribute4/9 to J_B. Indeed J_B>2*P_CF=2/3: P145's bound on
CF-only accepted utility cannot apply to this decoder. The physical bound on
P_CF itself remains untouched. Every cut here is <=2, so gain is exactly
2-C on ALL records: the useful third-order contrast does not require clipping.
This is an analytical toy, not a graph selected from a numerical population.

## 3. Decisive countercontrol and a second obstruction

Compute m directly in O(L) and score it once. On the hand graph it gives gain2,
strictly beating(4). A D monomial circuit routes the three photons to the three
distinct parent modes, producing(1,1,1) and the SAME m deterministically.
It needs no optimum knowledge: m follows from the supplied parents alone.
Thus separately reoptimized D and classical majority crossover REFUTE any
optimizer conclusion from(4). Parent costs/discoveries are already credited;
the tiny graph is also classically trivial. In the lossless K3 case there are
at most four decoded candidates, regardless of the graph's size. Equation(2)
also gives an exact classical B-law mirror: choose m with probability1/3,
otherwise choose a parent uniformly, then score ONLY that one result. No
enumeration of four graph cuts is hidden in this same-law replacement; its
actual wall cost still requires measurement, not an arithmetic declaration.

A tempting cheap parent generator also fails structurally. Suppose every
parent is either s0 or s0 with ONE paired bit flipped. Let M=sum n_a and N_l
be the votes assigned to parents flipping bit l. Equation(1) flips l iff
N_l>M/2; ties hold s0. The sets of such parent modes are disjoint, so
sum_l N_l<=M and at most one l can pass that strict threshold. Every outcome
is therefore the incumbent or one known single-bit mutant, even with loss.
It cannot escape a paired one-flip local minimum at ANY photon number or U.
This is a proof-level veto, not a mean or small-time approximation.

Growing K and overlapping multi-bit parents evade that last lemma, but no
useful-sign theorem follows. The null U=I already makes a known public-subset
majority offspring; credit it before any optics. Fixed K retains P145's exact
classical raw-PNR mirror, with (1) as a common decoder. Increasing r alone
does not remove it. Growing K does not itself prove hardness or practical
benefit: paid exact-law samplers, tensor-width and loss replacements remain
mandatory controls. Classical tractability alone is not a timed veto.

## 4. Source overlap and controls

Bounded primary search27-Nov-2026: majority-crossover/spin-glass and bosonic-
decoding queries, then exact primary passages. No global novelty assessment.
No fetched copyrighted full text/cache was saved; retained SHA:NONE.

Carsten Witt, TCS940(2023),18-42, DOI10.1016/j.tcs.2022.08.014:
[publisher version at DTU](https://backend.orbit.dtu.dk/ws/files/299208814/1_s2.0_S0304397522004881_main.pdf),
PDFp6/printedp22, section2.2 and Algorithm1, explicitly defines majority-vote
crossover on a multiset and applies it after parent local search. Authentication,
definition and algorithm extraction VERIFIED; (1) is that known classical
operation after translating multiplicities to repeated parents for odd nonzero
total. The tie/vacuum convention is separately specified here. Its Jump
runtime theorems are NOT graph-bisection theorems and are not imported.

Brádler--Wallner [2112.09766v1](https://arxiv.org/html/2112.09766v1),
section2.2 Eq1/section2.3 Eq4: all-occupation parity coarse-graining and sampled
objective optimization are existing photonic ideas. VERIFIED adjacent scope,
not this majority map; the HTML header has mixed date metadata, so no new
version-priority inference is made. P94's established parity controls persist.
Arrazola--Bromley [1803.10730v2](https://arxiv.org/html/1803.10730v2),30-Jul-2018,
Eqs1-2 and GBS-Tweak paragraphs: dense-subgraph proposals use Gaussian sources
and fixed-k CF selection. VERIFIED adjacent scope, not an all-shot balanced
decoder or a matched-control advantage. MBQC is not used by construction(1).
DOI access initially failed; the authenticated DTU publisher PDF resolved it.
Search-found voting symmetry papers were not fully checked or used as lemmas.

Required comparisons: independently retune D and ALL proper source partitions
on the same compiler/policy budget; use identical parent library, pairing,
orientation, loss/tie decoder and preprocessing credits. Include classical
majority crossover, mutation/multiswap/KL, population/EDA, count-CTMC controls,
and an exact-law optical mirror charged for compilation/precision/sampling.
No free pool portfolio, postselection, known-solution preparation or empirical
claim follows from a same-U contrast. Score/library building must be priced.

## 5. First unresolved implication and disposition

KEEP equations(1)-(3) and the collision-utility counterexample for independent
audit. REJECT the small tritter family and single-mutant libraries as optimizer
routes. A growing-library continuation is OPEN, not authorized for a pilot:
it requires an optimum-blind paid parent/graph compiler whose useful raw law
beats direct classical crossover AND independently tuned D/groups at total cost.
The first test should be an analytic sign/counterexample for that implication,
not a scan of arbitrary circuit parameters. No such favorable theorem is found.

The small physics construction uses3photons/3spatial modes and no ancillas or
in-shot feed-forward; a scalable example could use odd K<=r<=24, but source
number, PNR multiplicity/attempt visibility and calibration remain UNKNOWN
on Lucy. Neither detector nonlinearity nor classical majority implements a
coherent cost Hamiltonian. All losses still decode, but may erase the signal;
no loss robustness follows from the ideal lemma. Discovery goal remains OPEN;
no code, new numerical campaign, paper update or QPU step is justified here.
