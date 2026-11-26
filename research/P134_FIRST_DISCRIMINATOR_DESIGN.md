# P134 — Prospective rational-frame discriminator: DESIGN ONLY

2026-11-26; P66, parent f09300740aa2fe59fba83c400ae9b71740ecb484.
No graph/mark/weight was drawn, no matrix evaluated, and no code was written.
This is a proposed card for ROOT decision; source freeze/reviews and separate
execution authority are required before ANY factory/import/evaluation.
P130 outcomes were not opened. P133 and all negative results remain unchanged.

## 1. Two fresh DEV contexts, fixed independently of cut quality

Use the existing pinned CPython3.11.15/NetworkX3.6.1 graph-factory convention:
ER1341001 = nx.gnp_random_graph(24,0.4,seed=1341001);
RR1341002 = nx.random_regular_graph(4,24,seed=1341002).
One call each; no connectivity filtering, replacement graph or retry.
For canonical sorted min/max edges, use random.Random(1342001/1342002),
respectively, assigning successive randint(1,5) weights; these are exact integers.
Independently shuffle list(range(24)) with random.Random(1343001/1343002).
S=first12 marks; R=first4 of S; B=first6 of S^c, in mark order; p=first4 of B.
These are DEV, not held-out graphs. The new integer seeds were checked as text
against existing research paths; no RNG instance was constructed for this card.

Let S0=S\R, d_j=sum_(h outside S0,h!=j)w_jh-sum_(i in S0)w_ji and
W=1+max_(j in B)|d_j|+sum_(j<h in B)w_jh. Source: four CF photons in
the LAST four inputs of P133's ten-mode unitary, six other inputs vacuum.
Grid: beta outer (0,1/2), kappa inner (0,1/2,1,2): eight points per graph.
Use EXACT Gaussian-rational F_ja=delta_(j,p_a)(1-beta*d_j/W)+i*kappa*w_(j,p_a)/W,
H=F^dagger F,Q=(I+H)^(-1),T=2FQ,D=(I-H)Q,U=I-2[F;-I]Q[F;-I]^dagger.
Archive F/H/Q/T/D/U; require U^dagger U=I and T^dagger T+D^dagger D=I exactly.
No exponential, square root, eigensolver, calibration or optimal partition enters.

## 2. Complete receiver costs and species controls

Freeze all 15 receiver four-subsets Y in lexicographic order, with lifted
S_Y=S0 union Y and EXACT C_Y=C(S0)+sum_(j in Y)d_j-2sum_(j<h in Y)w_jh.
Check each cost by a separate whole-graph edge-cut sum. Record current C(S).
Count 34 whole-edge cut calls (current/baseline/15 candidates per graph) and
30 incremental candidate formulas; the prototype is already included, not free.
Compiler/grid construction may not consult a minimum/argmin or optimal-state mask.
The full 15-score frontier and the prototype score are credited to every control;
this physics qualification therefore cannot demonstrate optimizer advantage.
At beta=kappa=0 the known prototype receiver set occurs deterministically in
ALL species arms; its utility is a classical candidate, not preparation benefit.
For every kappa=0 point only that receiver set can be CF; all species laws agree.

Enumerate all 15 source partitions by the restricted-growth strings
0000,0001,0010,0011,0012,0100,0101,0102,0110,0111,0112,0120,0121,0122,0123.
0000 is B; all 14 others, including D=0123, are mandatory proper-group controls.
For each partition pi and CF Y, independently calculate

    p_pi(Y)=sum_(disjoint Y_A covering Y, |Y_A|=|A|) product_(A in pi)
                                                    |per T[Y_A,A]|^2.       (1)

Compare with an independent path-amplitude bucket formula: compute the 24
A_sigma=product_j T_(Y_j,sigma(j)); bucket permutations by their source-color
sequence at outputs under pi, then sum squared absolute bucket sums. No output
factorial occurs for CF Y. For every cached row/source-subset permanent, compare
independent subset DP and Ryser; retain exact complex values and all zeros.
No producer module, native backend or optical sampler is used.

With G=T^dagger T, all-signal mass is product_(A in pi)per G[A,A].
CF mass=sum_Y p_pi(Y); collisions=all-signal minus CF; dump=1 minus all-signal.
Require each nonnegative and CF+collisions+dump=1. Loss/collision events hold S;
no CF/sector normalization. Unmodeled external source/detector loss is excluded,
not silently inverted. Every modeled attempt costs four photons and all setup.

## 3. First uncertain high-order signal and grid-only decision

For B also archive each CF single-four-cycle coefficient C4(Y): sum
A_sigma*conj(A_rho) over pairs with sigma o rho^(-1) a single four-cycle.
There are six such relative permutations and 24 terms each, 144 ordered terms.
The result is real, signed and absent from EVERY proper source partition at
the SAME setting; double-transposition terms are not called genuine four-cycles.
Record J4=sum_Y h_Y*C4(Y), h_Y=max(0,C(S)-C_Y). Do not clip negative C4/J4.
This measures a four-input contribution; it does not identify its sign with Xi
or claim that positive J4 defeats a retuned control.

For each graph and EACH of the 15 profiles separately, maximize exact raw
I_pi=sum_Y p_pi(Y)h_Y over the SAME eight-point grid, breaking ties by first
grid index. Report raw improvement probability as a secondary quantity only.
If either graph has I_B<=max_proper I_pi: NO_STRICT_GRID_SIGNAL.
Flag a zero-improvement frontier as an uninformative opportunity; never replace it.
If both are strict but either selected B J4<=0: GRID_SIGNAL_NOT_POSITIVE_4CYCLE.
If both are strict and both selected J4>0: GRID_4CYCLE_FOLLOWUP_ONLY.
All outcomes preserve all settings/controls. No continuous/global reoptimization,
held-out replication, practical cost win or quantum advantage follows from this grid.
The credited deterministic frontier has utility >=every raw expected utility.

## 4. Hands, full physical normalization, and complete population

Two ten-mode/four-photon hands use F=[I4;0_(2-by-4)] and
F=[([[1,i],[i,1]] directsum I2);0_(2-by-4)]. Both retain every profile/Y.
First: prototype CF mass one, collisions/dump zero, C4=0. Second: all-signal
64/81 and dump17/81 in all profiles. If photons1,2 share a species block,
CF=0/collisions64/81; otherwise CF=32/81/collisions32/81. C4=0 throughout.
These are algebra hands, not favorable graph utility examples.

At ER1341001,beta=1/2,kappa=1,B ONLY, enumerate ALL 715 ten-mode occupations
of four photons using full U, with p=|per U[n,last4]|^2/product n_j!.
Sum to one and compare CF/collision/dump bins with the corresponding context.
Keep this fixed point even if its graph happens to make it degenerate; no substitute.
This is exact arithmetic, not a native call; a future native check needs a new gate.

Counters: 16 grid+2 hand matrix contexts; 270 profile totals; 4050 CF/profile
comparisons; 270 C4 rows. Per context cache sum_l binom(4,l)binom(6,l)=210
row/source permanents including empty: 3780 DP/Ryser rows. Also 270 nonempty
principal-Gram DP/Ryser rows. Add 2 graph contexts,30 cost rows,715 full-PNR
rows,1 full-PNR-total row,2 hand completion rows,30 profile-grid envelopes,
2 graph decisions and1 provenance row: NOMINAL 9441 rows. Missing zeros or
an incomplete profile/grid cannot yield a successful signal status.

## 5. Proposed bounds and next gate

One worker; CPU60s/wall90s; six thread env vars1; Python -B; science16MiB
(records15MiB plus reserved finals1MiB), logs4MiB, combined20MiB; logical256MiB PLAN only,
no hard RSS/affinity claim. Zero failed retries/precision escalations. Six registered
MT streams serve two topology/weight/mark contexts; photon RNG/native/FPRAS
draws zero. First unexpected failure/resource cap stops with raw prefix and
remaining tasks NOT_RUN; scientific mismatches retain evidence and cannot pass.
Missing finals after a hard resource kill are inconclusive, never a prefix pass.
Future source/TEMPLATE/binding must enforce fresh outputs, actual pins, exclusive
files, every count, capped results and raw sealing BEFORE interpretation.

No timing calibration, native follow-on, large-pool DEV or QPU is authorized.
A later r12 practical study must pay/share all features, source/pool selection,
inversion/compilation, four-photon attempts, scores and training; include independently
retuned D/groups, exact-law classical mirror, FAST/pair/beam and the full frontier
when its measured grant permits. A finite negative result rejects only this grid;
a finite signal advances only a design hypothesis, not the user's final goal.
