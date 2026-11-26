# P90 prospective design: source-bound, nonflat graph scattering

**DESIGN ONLY.** One changed architecture is specified, with an exact
interference/cost channel and an explicit classical veto. No positive
optimizer, novelty or hardware claim is made. No parameters, seed grid,
experiment contract, implementation or execution is allocated. P82 and
its frozen pilot are untouched; no pilot outcomes were read.

ROOT supplied the question and P89 boundary before this static design.
The mathematics below is hand algebra, not an independent discovery
claim or numerical evidence. All costs refer to feasible balanced cuts;
no C*, optimal-state mask or known optimum enters the proposed compiler.

## 1. The flat r2 barrier really must be changed

For two distinct removed source columns i,j of a K-mode receiver V,
put `c_a=V_ai conj(V_aj)`, `d_a=|c_a|^2`, `D=sum_a d_a`.
Compare indistinguishable B with distinguishable D at this same V,
using the same uniform collision repair. For a repaired pair `{a,b}`,

    Delta P_ab=2 Re(c_a conj(c_b))+(d_a+d_b)/(K-1),
    Delta Pr(a in Y)=(D-K d_a)/(K-1).                      (1)

The first term is the exchange term in the two-by-two permanent.
Bunching adds `d_a` beyond D at output 2a; repair spreads it uniformly
over the other K-1 receivers. Summing pair probabilities uses
`sum_a c_a=0` by column orthogonality and proves the second identity.
All outcomes are retained; no acceptance denominator appears.

In a flat receiver `d_a=1/K^2`, so every one-vertex difference is zero,
for each removed pair, even with source-aware internal phases. Thus
source-aware phases alone cannot change the r2 cross-edge mean against
the same-unitary D law. Only receiving-pair correlations remain there;
the old receiving-graph XY term already captures a classical low-order
channel. A new claim cannot relabel that term as an optimization result.

## 2. Changed architecture: preserve the graph meaning of each column

Keep finite K-photon Fock input, K vacuum receiver inputs, splitters,
a receiving passive mesh and full-count collision repair. Introduce a
unitary `V_(G,S)` whose columns are labeled by actual source vertices
in S and rows by actual receiver vertices in T. If sigma and tau are
the random physical input/output port orders, compile

    W_ports[a,i]=V_(G,S)[tau(a),sigma(i)].                 (2)

The port permutations are now transported physical coordinates. They
cannot average away the circuit's source-to-receiver correspondence.
With unchanged label-blind splitting, R remains marginally uniform
at fixed r, but its receiving law is the repaired bosonic law from
the particular labeled columns `V[:,R]`:

    P(R,Y|G,S,r)=nu_(G,S,R)(Y)/binom(K,r).                 (3)

For nonflat V the conditional law can depend on R already at r1;
that one-photon dependence is classical and must be credited as such.
The intended quantum contribution is the exchange structure beyond it.
This is not a receiver permutation: V is a coherent nonflat unitary.

One explicit optimum-blind graph initializer uses fixed paid priority
orders `s_i` and `t_a`. Let

    ell_v=degree_v-2 sum_(u in S) w_vu,
    M_ai=ell_(t_a)-ell_(s_i)+2 w_(s_i,t_a),
    H=(M+M^T)/2+i(M-M^T)/2,
    V0=exp[-i H/max(1,||H||op)].                           (4)

H is Hermitian, so V0 is a genuine passive unitary. The pairing of
source/target indices uses only the declared priority, carried through
graph relabelings. M accesses the whole graph and contains actual
one-swap deltas. Those K-squared feasible candidates must be materialized,
credited and exposed to the classical controls; they are not free
photonic preparation. Matrix construction, norm/exponential, mesh
decomposition, routing and all later adaptation are also paid.

A source-bound nonflat mesh initialized by (4), with any later training
using only observed raw costs/basin entries, is the proposed family.
No training schedule or angles are selected here. D gets independent
reoptimization of the same full-graph family and source settings.
Loading changes are unnecessary to break P89's independence. If later
loading becomes vertex dependent, its marginal removal steering is a
separate classical feature requiring its own identical-feature control.

## 3. The nonflat exchange term is linked to full graph cost

For a fixed removed pair R, the candidate cut has the form

    C((S\R) union Y)=A_R+sum_(a in Y) L_a(R)
                     -2 sum_({a,b} subset Y) w_ab,
    L_a(R)=degree_(G[T])(a)+2 sum_(s in R)w_sa-sum_(s in S)w_sa.

Consequently (1) gives the exact B-minus-same-V-D raw r2 mean

    sum_a L_a(R)*(D-K d_a)/(K-1)
      -2 sum_(a<b) w_ab*[2 Re(c_a conj(c_b))+(d_a+d_b)/(K-1)]. (5)

Unlike the flat case, its first term can involve the actual cross edges
and which source labels were removed. R in this analysis is not a
compiler input: V is always compiled before the split. Equation (5)
has no generally favorable sign and does not prove the proposed graph
initializer will improve it. It identifies a channel to falsify.

There is even an all-attempt hand witness, rather than a postselected
one. Take K4 with V a balanced two-mode mixer on source columns 0,1
and receiver rows 0,1, and identity on 2,3. Let the sole graph edge join
source s2 to receiver t2. With a common splitter probability p, B differs
from D only when both active inputs transfer. If R=01, collision repair
includes t2 with probability 1/3 under B versus 1/6 under D. If R=013,
the probabilities are 1/2 versus 1/4. If s2 transfers, t2 is already
occupied and that edge contributes equally; all other cases agree.
Summing the complete split law therefore gives

    E C_B-E C_D
      =-p^2(1-p)^2/6-p^3(1-p)/4
      =-p^2(1-p)(2+p)/12 < 0  for 0<p<1.                 (6)

This illustrative family member is not a claim that (4) generates it,
nor a useful benchmark: its one-edge graph is classically trivial.
It shows a full-Fock, raw-cost exchange effect without discarded shots.
Every repaired vertex is classical decoding, not a physically prepared
extra photon. The entire witness is reproduced by an exact two-photon
group control. It is therefore explicitly insufficient for acceptance.

## 4. The only prospective positive hypothesis and its vetoes

The hypothesis concerns a genuinely growing interfering receiver sector:
source-bound nonflat scattering could create useful coordinated R/Y
basin entries that survive the shared capped quench at lower **total**
cost than the independently optimized controls. It does not assert
that an r2 mean gain extrapolates to the complete distribution or that
one-photon source correspondence is quantum.

Mandatory nulls must include independently reoptimized distinguishable
photons; exact fixed-small-r sampling and bounded indistinguishable
groups; classical bunching/repair controls; a paid correlated feasible
search receiving the entire compiler/features; the recipient frontier
whenever it fits; and strong from-raw FAST/continued-descent controls.
The tiny witness (6) must fail the two-photon-group veto by construction.
Passing B versus D at a shared circuit is never sufficient.

An additional ablation erases the source-column correspondence while
retaining the same matrix/profile resources. It separates P89's lost
coordination from generic receiving correlations, but is not itself a
strong classical control. Intensity-only and small-group controls must
also separate coherent exchange from graph-informed one-body routing
and from the repair rule's cheap classical bias.

Any later comparison must pay compiler candidates, all setup and
training, raw attempts and injected photons, routing, collision repair,
quench and scored neighbors. Match or independently optimize the
replacement-radius distribution; a change in r is not interference
advantage. Fresh unplanted graphs, independent seeds, graph relabeling,
held-outs and independent replication remain required before hardware.
Any required weak/negative result is preserved, never repaired by
choosing a favorable graph or preparing a known partition.

The receiver can be compiled from ordinary passive splitters/phases;
no squeezing, helper photons, projected logical gate or nondestructive
measurement is assumed. Actual Lucy/TGCC mode/input/detector capability
and loss accounting are not established by this design. Lost samples
cannot silently be treated as collision deficits. No QPU action follows.

This design changes the P89 coupling premise and the flat-r2 barrier
in a mathematically identifiable way. It is one prospective route,
not an accomplished optimizer or a general escape from classical
simulation. Priority and its relation to existing bosonic quantum-walk
optimizers remain unresolved pending a bounded primary-source check.
No experiment, contract, code, parameter search, graph
generation, import, RNG, backend, main outcome or manuscript was used
or changed. All displayed identities were checked by hand; no claim
of novelty or positive total-resource advantage is made.
