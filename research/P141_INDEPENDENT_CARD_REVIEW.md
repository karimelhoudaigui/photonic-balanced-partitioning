# P141 — Independent prospective-card review

26-Nov-2026; P66, not the card author. Audited, NOT executed. Own parent
4a82c48bc0787099c8273b7952852b905d83b615. Target FULL 142-line commit blob
deb8d9ae24af4a9e39553b00c2a25a09fdb3ad56:
research/P141_FINITE_MAGNETIC_SCREEN_CARD.md, SHA256
4daa33822164d1298202b5a15e0dd86a5ec68abc626606f5a292fa62936033cd.
Computation-audit skill/checklist applied. Only text/metadata read; no import,
AST, factory, graph, matrix evaluation, RNG, raw output, native or QPU call.
P138 and all earlier results remain unchanged. P66 authored P138/P134, so this
is non-author review of THIS card, not independent derivation of those sources.

Verdict: ACCEPT the bounded design, with no mathematical card blocker found.
This is neither source approval nor code/execution authority. The implementation,
exact closure, serialization, guards and binding still require separate reviews.

## Encoding, fixed null and loss bookkeeping

The eight receivers exclude S0 and have a fixed order. Full-graph two-hop
weights are symmetric; rank signs reverse on exchanging endpoints and rho has
unit modulus. Thus L is Hermitian. Its absolute row bound nu gives ||H||<=1.
No receiver-only truncation of the two-hop sum is allowed. Mark transport is
covariance of this construction, not an empirical relabeling experiment.

Put A=E^dagger H^2 E. Direct expansion gives F^dagger F=I+kappa^2 A;
the two linear terms cancel because H is Hermitian. Q=(I+F^dagger F)^-1
exists, and V=[F;-I] has V^dagger V=Q^-1. Consequently VQV^dagger is an
orthogonal projector and U=I-2VQV^dagger is exactly unitary. Last-four source
columns are [2FQ; I-2Q]=[T;-D_dump], with T^dagger T+D_dump^dagger D_dump=I.
At kappa=0, T=E and D_dump=0: EVERY profile outputs R with unit probability,
and h_R=0. There is exactly one shared null, not four parameter trials.

For nonempty species blocks A_j, all-signal probability is product_j per(G_Aj).
Subtracting the summed signal-CF mass gives signal collisions; dump is one
minus all-signal. The bins are raw, mutually exclusive and exhaustive. For full PNR,
ANY dump photon wins classification even if receiver photons also bunch.
Dump here is an explicit unitary output register, not a measured Lucy loss model.
All physical loss/detector/source/latency costs remain unvalidated.

## Independently reconstructed counts and hands

Each graph has one null plus 2*2*4 settings; index14 is alpha=1,rho=i,kappa=1.
The 34 grid contexts plus two hands give 36 matrix contexts. Per context,
sum_l C(4,l)C(8,l)=1+32+168+224+70=495, hence 17820 subpermanent rows.
The 15 nonempty source subsets give 540 Gram rows; the empty permanent is one
and is also included in the amplitude-cache construction. Bell(4)=15 profiles
split as B, six 2+1+1, three 2+2, four 3+1, D. Thus 15*70*36=37800 CF rows,
540 profile totals, and 15*2=30 independently retuned envelopes.

Per graph: current cut, S0 helper, eight singleton helpers and 70 whole cuts
give 80 calls. Thus 160 whole-cut calls, 140 candidate formulas, 16 independent
field checks and 56 two-hop sums of 24 products are consistent. Helpers are
imbalanced and NEVER eligible incumbents; all 70 lifted candidates are feasible.
Six MT seeds are fixed, distinct, DEV-only, with no filtering or redraw.

The complete four-photon population on twelve modes is C(15,4)=1365.
Two selected-B contexts add 140 C4 rows; selecting after all means is expressly
auxiliary and first-tie deterministic. Adding ALL listed categories gives
58443 records. Task decomposition is 1+1+2+34+1+2+2+1+1=45; the graph/features
task is joint, not two separately counted tasks. Prefix failure cannot be PASS.

ID has T=E,D_dump=0 and CF probability one for every profile. For HOM, the
two active columns have G=(8/9)I; spectators are transmitted deterministically.
All-signal is 64/81, dump 17/81. The active permanent cancels when sources
0/1 share a species, giving CF zero; otherwise CF is 32/81. These cases test
both coherent cancellation and group separation, not graph improvement.

## Lossless coefficient bound and implementation obligations

Since S0 has eight vertices, |d|<=75. The 22 possible common neighbors imply
t<=550, b<=555, and nu<=75+7*555=3960. Here L is Gaussian-integer and nu is
integer. For kappa=p/2, p<=8, write B=(LE)^dagger LE and
M=8nu^2 I+p^2 B. Then Q=4nu^2 adj(M)/det(M), and
T=(8nu^2 E+4ipnu LE)adj(M)/det(M). The factors 2nu also cancel in every
block of U=I-2VQV^dagger. Thus all T/U entry denominators divide det(M).
Since 0<=B<=nu^2 I, eigenvalues of M are at most 72nu^2<2^31;
det(M)<2^124 follows. This does NOT bound a whole JSON record/file by itself.

A context LCM D therefore supports exact amplitudes D^-l, Gram permanents
D^-2l and four-photon CF/profile/C4 values D^-8. Full-PNR probabilities need
the additional product of occupation factorials. Code must distinguish these
domains, retain complex parts/zeros, and explicitly define delta orientation:
e.g. delta=first-second, allowing second=first-delta even on a failure. Matrix
references must reconstruct BOTH operands, not just a Boolean or shared result.
DP/Ryser and convolution/24-path buckets must be actually independent paths.

Before execution: enforce aggregate records47MiB plus joint-final1MiB, log4MiB,
FSIZE48MiB, CPU180/wall240 and zero retries. The 52MiB sum refers to scientific
files plus logs; runner metadata must be separately accounted for. Logical
256MiB is a plan, not hard RSS/AS or affinity. Byte fit and current free space
must be checked; the determinant bound is not a substitute for output guards.
Archive available operands before assertion/limit exit and mark remaining work
NOT_RUN. No resource interruption can justify missing contexts or a new cap.

The inactive v2 TEMPLATE must say randomness.used=true, generator and ALL SIX
literal seeds. Rehash the eleven critical external roles before scientific
imports, require the core NetworkX backend and empty effective priorities.
Keep source provenance explicit: a P134-derived engine is not an independent
replication. Fresh binding/paths/authority and independent frozen-source review
remain mandatory; this review supplies none of them.

## Interpretation that survives this review

The compiler uses graph features, never scores/minima/optimal masks. All 70
feasible costs and setup are credited to every control: this finite pool is
already solved classically. Every proper profile has its OWN best of the same
17 settings. NO_SIGNAL rejects only this finite screen; FOLLOWUP is not a
continuous-control win. C4/J4 has no automatic utility-causality implication.
Neither decision establishes practical optimization, relabeling robustness,
held-out replication, native validation, hardware feasibility or novelty.
optimizer_advantage=false, the paper freeze and the separate QPU gate are intact.
