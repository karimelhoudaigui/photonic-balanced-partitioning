# P49: actual feasible-mean training, fresh policy evaluation, FAST envelope

Prospective contract,25-Nov-2026. Authoritative ROOT card **dc85fa5b49b095de3ba39c37f35d0cada70b47dd**
(initial7b791bf); physics review **f898028e3b9f38d4e520ddde100a34285e01369d**.
New files import P48 immutable. P33/P37/E05b and all later negatives survive.
No P49 DEV graph has been generated, no training/evaluation has run at this
freeze. This is a new question, not a repeat or accepted positive from P48.

## Hypothesis and exact source family

Does coherent source-mode mixing plus training the ACTUAL mean feasible cut
produce a useful law beyond separately optimized D, partial coherence,
ordinary coherent fields and fast feasible search? Lowering an occupation
proxy, retaining a prepared partition, or B>D alone does not establish this.

Use P48's fixed, marked-Laplacian first K eigenmodes E, with its carried-priority
pivot gauge fixed BEFORE mixing, and r=K=N/2 source photons. Define

    G(theta,phi)=[[cos theta,-exp(i phi)sin theta],
                  [exp(-i phi)sin theta,cos theta]],
    R=G_even @ G_odd,

even pairs(0,1),(2,3),... and odd pairs(1,2),(3,4),... . The rightmost odd
layer acts first. Four bases in order: graph-blind Fourier, E, E R(pi/4,0),
E R(pi/4,pi/2). No other angle/phase or learned continuous parameter enters.
An isolated |11> pair at pi/4 has amplitudes
(-exp(i phi)|20>+exp(-i phi)|02>)/sqrt(2), U[output,input]. The complex
coherence test at phi=.37 fixes conjugation/sign; probabilities alone cannot.
Overlapping layers do not factor into independent NOON pairs.

P=VV* and mu are invariant under right-unitary mixing, but q=|V|^2 and
bosonic/D/species/phase laws and Gaussian covariance generally change. Every
context recalculates q, ALL PMFs, covariance, factor and structural mask using
P48; none is incorrectly cached from P/mu. Spherical laws alone are invariant.
Occupied eigenmode gauge BEFORE R is physically meaningful; column phase AFTER
V is a CF-state null. There is no Haar source-basis averaging.

Use P48's orthonormal vacuum completion and fixed CF ports0..K-1. Every raw
count/collision remains useful through the SAME marginal PIT and feasible
completion. No herald, CF conditioning, known partition, C*, optimum mask or
energy conditioned on success. Optical maps never use Cref or a sampled
training partition. Mark coefficient.001, all N-1 gaps saved, occupied/boundary
gap guard1e-12, source/eigen/unitary residual3e-12, zero/near-degenerate cases
retained without redraw. Any incomplete numerical population is inconclusive;
no training/evaluation positive is accepted on successful survivors.

## Paid objective, independent grids and evaluation isolation

For each graph let W=max(1,sum_(i<j)A_ij). Loss is the mean of cut(S)/W,
including EVERY worse/better feasible shot. Average graph means equally across
the four DEV graphs. Policy selection uses exact

    (1/4) sum_graph Fraction(sum_cuts,draws*W).

Each model independently minimizes this loss, first canonical policy ID for
exact ties. Gains, Cref, success labels and extrema never enter selection.
Every policy/loss/cut/cost survives. Allocation per graph:

| Models | Meaningful policies | Training draws/policy | Total train |
|---|---:|---:|---:|
| B,D,b4,Gaussian,continuous phase | 4 bases x lambda0/1 =8 |4|32|
| Sphere | Fourier/E x lambda0/1 =4 |8|32|
| IID | lambda0/1 =2, no source basis |16|32|

Canonical IDs enumerate basis then lambda. IID basis is null, not a redundant
Fourier circuit. b4 groups CONTIGUOUS source ports of at most4 before outcomes,
matching the local mixing architecture; there is no random grouping/tuning.
Continuous angles are used for all phase production and nonpolynomial rounding.
P48's qualified subunit coherent helper remains unchanged, with explicit
Fraction row-repair diagnostics and no rescaling of any mu<1 row.

Training uses trial0 in role491100. After GLOBAL model-specific selection,
32 FRESH evaluation draws per graph use two new role491200 seeds,16 each,
at that FIXED policy. No update/reselection follows evaluation. Counts:
128 training+128 evaluation=256 proposals/arm,3840 simulated photons per
optical arm (1920 per stage). These are still DEV graphs, not held-out.

Cref is frozen before the FIRST training shot. Training incumbents stay
model-specific. A paid training partition may be retained in that model's
deployment best, with its full training resource cost; it never refreshes
common Cref, another arm's information or a physical input. Report separately
chosen-policy fresh mean/best, own training incumbent, total paid deployment
best and experimental versus retrospective deployable-policy ledgers.

## Shared frontend and five diagnostic searches

All four bases are prepared before any training. Same P48 common discoveries:
capped8-scan best-swap anchor, all K^2 anchor swaps, signed top/bottom rounding
of r+1 marked eigenvectors, top/bottom mu and every q column, labelled
maximum-product rectangular assignment with floor1e-300, zero/greedy and
vacuum-mid-PIT decoders for ALL four bases. Every actual cut/sorting/matrix
cost is shared and credited before any photon sample. Assignment is a labelled
product, not the permanent D support sum. The optical family ignores them.

Legacy searches anneal,spectral+swap,KL,shared-Delta matching and spectral
coherent rounding each have their OWN total6400/11072 informative score
ceiling per N26/N34 graph. Preserve two seeded half-campaign restarts at
3200/5536 each. Their paid minima may be combined within that one baseline;
no free five-baseline portfolio. The coherent baseline uses all four source
bases and its inherited deterministic phase/sphere cycles. These score units
remain diagnostics, not equivalent CPU prices or a hardware advantage.

## FAST control and explicit zero-optical-time envelope

FAST source **0bc492e2442e9b5146fa52e275ed058dbfa9832e**, SHA256
**018fef36d67ce31f14e9ed3e2e200ac11605dbffe9ed3670284862f3c9ba3fff**,
API9765ff9. Independent qualification15 PASS, receipts82de1cb/a46038f preserve
a prelaunch schema refusal and its contract-only correction. The algorithm
and tests were unchanged. The imported helper is never edited here.

Pass int64 A (conversion charged in shared frontend), free common incumbent,
its verified integer cost, and **rank[vertex]**, not an ordered vertex list.
For EACH graph grant CPU seconds equal to the measured B classical WALL:

    common bracketed compute + B train/eval PIT/decoder/fitness bookkeeping
    + one-quarter B global selection wall.

Optical backend setup and count-generation time receive ZERO grant. This
generously assigns optical sampling zero latency. Raw/context/trace JSON and
list serialization are outside these clocks; legacy per-query JSON cannot
inflate the allowance. Initial anchor rule is copied with compute/log brackets
and independently checked against immutable P43. Numeric helper construction
includes its Decimal diagnostics inside measured preparation; that explicit
current-implementation envelope is not a minimal optimized deployment price.
Full shared preparation is charged ONCE and offered to all methods; selected
basis setup is only a subset bound and is not added a second time.

Granting CPU from observed WALL is an explicit conservative convention, not
a CPU/wall identity. A small measured caller adapter cost is subtracted before
the solver CPU allowance. No extra solver wall safeguard is used; the global
runner wall cap remains. Max proposals100,000,000 is a guardrail, NEVER a
matched resource unit. An early cap or safeguard makes acceptance comparison
inconclusive. Compare only returned deadline-admissible **best_cut/best_subset**,
never a late overall-completed discovery. Compact clocks/masks/counters are
saved after solve; serialization is outside compute. Some setup/repeated cut
calls consume CPU without a new informative discovery, as the helper records.

No practical/hardware benefit is established by one timing run. If a future
signal leaves a nonzero time allowance, it is merely a conditional break-even
envelope until preparation, QPU latency, losses and total resources are measured.

## Fixed population, projection, preflight and decisions

Four NEW DEV graphs, no replacement: N26/r13 ER4902601,RR4902602 and
N34/r17 ER4903401,RR4903402; ERp=.35,RRdegree4,weights1..9. New role namespaces
491010 anchor,491020 marks,491030 Fourier order,491040 priority,491100 train,
491200 eval,491300 legacy,491400 FAST. Training trial0, evaluation/legacy
trials0/1. No P49 graph has been opened before source/spec/test/contract freeze.

Resource projection from P48 bytes/timings BEFORE outcomes: four-context JSON
approximately14.9MB, raw approximately6.3-8MB, summary/compact FAST traces a
few MB, projected total approximately23-28MiB below32MiB. Same256 proposals/arm
and same legacy campaign totals; twice the marginal preparation plus bounded
FAST grants project below CPU60/wall90. This is a projection, not an observed
P49 run. Any unexpected resource failure remains inconclusive, no retry/cap
increase or silent truncation. Planned arrays<=256MiB, one thread/worker.

Preflight planned27 new integration cases plus15 FAST qualifications. Fixtures
cover G/R/null/order/unitarity, complex HOM coherencephi.37, fixed projector
but changed q/laws/mask, source gauge/relabeling, ALL-shot/equal-graph Fraction
loss and ties, evaluation leakage/missing cases, meaningful grids/fresh roles,
contiguous b4, setup/count versus post/JSON clocks, own paid incumbents,
FAST rank/allowance/deadline/cap behavior, immutable anchor equivalence and
fresh four-context recomputation. No DEV outcome is in these fixtures.

Source/helper/spec/contracts/tests are committed before numerical work;
distinct physics and caller/resource reviews precede targeted preflight,
then coordinator authorization for ONE main. CPU60/wall90/thread1/log32MiB,
script checks data bytes. No Darwin hard-memory/affinity guarantee. All raw,
partial, negative and failed results survive. No QPU, credentials, external
messages, paper/PDF or GitHub publication now. REJECT or INCONCLUSIVE unless
a reproducible signal merits FOLLOW-UP. No accepted positive on these four
DEV graphs; program-alpha, reserved graph, independent sampler/total-cost
gates remain mandatory before paper/GitHub SIMULATION VALIDATED,QPU PENDING,
then authorized hardware preparation. No such gate is opened by this contract.
