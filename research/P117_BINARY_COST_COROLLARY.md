# P117: binary-cost stochastic-order corollary

2026-11-26. Independent MANUAL derivation, no computational execution.
Dependencies: P101's specified graph, filled four-photon CF input and
all-output decoders; P114's explicit-polynomial theorem at b61b6a9 and
independent proof review f52bef0. ROOT reports the independent P113
identification COMPARE_PASS at original raw seal
`ac82cd0d1dc8a1a21ec5475180e821d881c6f78a`; that receipt is an evidence
dependency, not a second raw audit performed here. The theorem
below is stated conditional on that physical identification and ideal model.
No new source, circuit, training rule or hardware result is introduced.

## Statement and one-attempt proof

For either frozen decoder, let C_a denote the raw decoded graph-cut cost
under a in {B,D}, at the SAME admissible transfer
T=F diag(1,x,xy,y)F^dagger, x,y in [0,1]. Every output is decoded; vacuum,
partial loss and collision events are retained. P101's graph has only
the two feasible cost values 2 and 3. Put q_a=Pr(C_a=2). Then exactly

    E C_a=2q_a+3(1-q_a)=3-q_a,
    f=E C_B-E C_D=q_D-q_B.

P114 gives f>=0 everywhere and f>0 except (x,y)=(0,0),(1,1).
Consequently D stochastically dominates B in the sense of LOWER cost:
its cost CDF is at least B's at every real threshold t. Below 2 both
CDFs are zero; on [2,3) they equal q_D and q_B; at/above 3 both are one.
Off the two endpoints this is a strict difference on [2,3). For P101's
finite strength b>0, the physical curve lies away from these endpoints.
This is a probability statement about actual decoded costs, not subtraction
of observed B/D counts to manufacture a new sampling distribution.

The equivalence between mean and stochastic order uses binary support.
It is generally false for decoders/graphs with three or more different
costs. No analogous assertion is inferred for such tasks from P114 alone.

## Independent fixed-budget repetitions

Take N>=1 fresh INDEPENDENT attempts within each arm, with the unchanged
source, transfer and decoder. Fresh independent tie randomness is included
in the trial law. Cross-arm independence or a physical coupling is not
needed to compare their marginal distributions. Let M_a=min_(t<=N) C_a,t.
For the identical fixed setting,

    Pr(M_a=3)=(1-q_a)^N,
    Pr(M_a=2)=1-(1-q_a)^N,
    E M_a=2+(1-q_a)^N.

Since q_D>=q_B, D has a no-larger probability of cost 3, no-larger
expected minimum and an everywhere no-smaller cost CDF. If f>0 the order
is strict on [2,3) for every finite N>=1, including q_D=1. At N=0 one
needs a declared incumbent/fallback; no empty-set minimum is assumed.
If a feasible incumbent of cost C0 is retained, replace M_a by min(C0,M_a).
This monotone transformation preserves the weak order. With C0=2 both
retained costs are already 2, so a strict improvement claim would be false.

## Predetermined nonidentical point sequence

The same conclusion holds for fixed settings theta_1,...,theta_N declared
BEFORE measurement, provided each B/D pair obeys the corresponding
one-attempt inequality q_D,t>=q_B,t and trials are independent within an
arm. Each theta_t must remain in the proved transfer/decoder/model family.
The settings may differ across t but are shared between B and D. Then

    Pr(M_a=3)=product_(t=1..N)(1-q_a,t).

Factorwise order proves the desired weak order. Strictness is not automatic
for every schedule: an earlier guaranteed cost-2 result can already make
both minima 2. A sufficient strictness condition is q_B,t<1 for all t and
q_D,t>q_B,t for at least one t. An exogenous common random schedule can be
conditioned on first and then averaged if it satisfies the same assumptions.
This is NOT an adaptive policy or changing-incumbent trajectory theorem.
Outcome-driven circuits, stopping/resource rules, drift or correlated
source emissions require a separate joint-law argument; marginal orders
alone cannot justify the product formula.

## Training-oracle, loss and resource boundaries

Cost 2 is an analytical label for the lower of this graph's two feasible
costs. Its retrospective identification with the best cut can be checked
by the three-candidate classical frontier. Neither the compiler, source,
sampler nor decoder is given C*, an optimal-state mask or a known optimal
partition during training. The corollary evaluates a frozen rule; it does
not authorize using the analytical event to choose favorable settings.
Every classical control receives the same public graph/features and pays
its scoring/setup costs. An allowed same-setting D control is sufficient
for this distributional comparison; finding or retuning controls is not free.

The ideal prepared input has exactly FOUR injected photons per attempt,
so N such injections cost 4N photons before the channel. All subsequent
losses remain charged. Under this deterministic common ledger the attempt
and injected-photon budget comparisons coincide. This does not establish
matched source latency, compilation, decoder or total wall-clock cost.

If a common preparation-success probability s supplies the declared CF
input and every other whole-attempt branch uses the SAME uniform balanced
fallback, q_a,effective=s q_a+(1-s)/3. The gap is s f, preserving weak order
and strict order when s>0,f>0. Such preparation attempts/failures must be
recorded. If their actual injected photon numbers or durations vary, a fixed
photon/time budget needs the joint common resource ledger; dividing by a
mean preparation cost does not prove the above fixed-budget distribution.

Intrinsic passive-filter loss is included in P114's raw model. A common
additional photon-by-photon attenuation, detector noise or source mismatch
is NOT automatically a whole-attempt uniform fallback. Partial-loss records
can decode usefully, so their gap need not simply scale as eta^4 f. No loss
inversion or automatic transfer to an unverified hardware model is claimed.
The corollary applies when the actual compared laws satisfy its model and
binary-support/order hypotheses; extensions need a new error/loss analysis.

Disposition: a fixed-source/fixed-family and independent-attempt obstruction
for this graph and these all-output decoders. It is neither a universal
photonic no-go nor a matched-total-cost or hardware result. Frozen P113/P114
are unchanged. No import/AST/test/RNG/script/native/QPU/paper operation ran.
