# P41/R3 — oracle-envelope loss and combinatorial entropy

Checkpoint: refinement of P41_obstruction_loss_cost_certificate.md, after the
exact L1 probe. Status: analytic derivation, independent audit pending. Known
survival, counting and exponential-Markov ingredients are not claimed new.
No actual Lucy calibration or hardware conclusion is inferred here.

## A. Quantified finite statement

Fix an undirected weighted graph on2k vertices, k>=2. Its set of optimal
oriented balanced strings has size g>=2, because complementation preserves
cut cost. Write D=binom(2k,k) and p0=2/D. A uniform feasible sampler needs
neither C* nor an optimum mask, and has actual success pG=g/D>=p0 per draw.

An optical trial prepares at most Nmax>=k fresh photons and loses each
independently with uniform survival eta. A successful output must contain at
least k genuine surviving photons. Allow arbitrary graph-informed preparation,
interferometer, internal statistics and adaptive choices of later trials.
There is no quantum memory, uncharged heralding, error correction, mitigation
counted as a physical detection, or classical completion from fewer photons.

The optical conditional success probability, after any previous history, is
bounded by

    a=P[Bin(Nmax,eta)>=k].                                (A1)

Even knowing the optimum and preparing it perfectly after survival cannot
beat this envelope. Actual physical attempts, not nonempty provider shots,
are the trial unit. All graph-quality structure is optimistically replaced
by conditional success1; no Haar or random-graph hypothesis enters.

Induction on failure histories gives, for at most nQ attempts,

    P_Q(success)<=1-(1-a)^nQ.                             (A2)

For nC independent uniform feasible draws,

    P_C(success)>=1-(1-p0)^nC.                            (A3)

The events here are *discoveries through this sampling stage*. A common
fixed classical front end may be charged to both. Its discoveries are credited
separately. A hybrid that solves the graph in classical preprocessing is not
bounded by (A2) as a statement about its entire success event. Nor does this
comparison reconstruct a quantum-dependent adaptive classical front end.

## B. Matched costs and exact floors

Given positive fixed primitive costs cC,cQ and remaining budget T, put
nC=floor(T/cC), nQ=floor(T/cQ). If nC>=1, set L=ceil(nQ/nC). Then the fully
rational condition

    L a<=p0                                               (B1)

is sufficient for the lower bound (A3) to dominate the upper bound (A2).
Indeed (1-a)^L>=1-La>=1-p0 by Bernoulli's inequality, hence

    (1-a)^nQ >= (1-a)^(L nC) >= (1-p0)^nC.

The same guarantee holds if cC is a deterministic upper bound on the cost of
each classical draw and cQ a deterministic lower bound on each optical trial.
Observed average wall times alone do not establish these bounds; random-time
budgets need their own concentration or stopping argument.

No logarithmic approximation or ignored floor is needed. If nQ=0 domination
is immediate. If nC=0<nQ, no such certificate is asserted. The sharper exact
condition is nC[-log(1-p0)]>=nQ[-log(1-a)]. A rate comparison alone is not
a guarantee for arbitrary small finite budgets.

For aligned budgets with cC/cQ an integer L, (B1) permits a classical draw
to be L times slower than a physical optical attempt. Both preparation cost
and graph scoring belong in the measured primitives or a separately charged
front end. Ignoring optical training costs only makes its upper bound more
optimistic; supplying a trained circuit to a classical comparator for free
does not establish matched whole-algorithm cost.

## C. Universal quarter-survival corollary for Nmax=k

Here a=eta^k. Since D<4^k,

    eta<=1/4  ==>  2a<=2/4^k<p0.                          (C1)

Thus one classical draw dominates even the optimistic success envelope of
two optical trials. This holds for every graph and any k>=2, at aligned
budgets permitting at most two physical trials per classical draw. In
particular it holds at equal primitive trial count. The finite sharp threshold
for the one-for-one envelope comparison is eta<=(2/D)^(1/k).

This quarter is an end-to-end independent-photon survival threshold for this
cardinality encoding and objective. It is not a circuit-per-layer noise
threshold or an approximation theorem for the full output distribution.

## D. Capped source overhead and exponential cost ratios

If eta=0, then a=0 and domination is immediate without logarithms. Otherwise
suppose Nmax<=alpha k for fixed alpha>=1 and0<eta<1/alpha. For alpha>1 define

    I(alpha,eta)=alpha D_Ber(1/alpha || eta)
      =-log(eta)-(alpha-1)log(1-eta)
        -alpha log(alpha)+(alpha-1)log(alpha-1).

Markov applied to exp(t Bin(Nmax,eta)), t>=0, gives

    a<=exp(-tk)(1-eta+eta exp(t))^(alpha k).

The minimum uses exp(t)=(1-eta)/[(alpha-1)eta]>1 and yields

    a<=exp[-k I(alpha,eta)].                              (D1)

For alpha=1 use the exact endpoint I(1,eta)=-log eta.
No limit approximation is used in (D1), and Nmax need not equal alpha k.
Because p0>=2*4^(-k), if

    delta=I(alpha,eta)-log4>0,

then

    a/p0 <= (1/2)exp(-k delta).                           (D2)

Consequently every integer L<=2exp(k delta) satisfies (B1). A classical
primitive may be exponentially slower per candidate within this envelope;
any polynomial cost ratio is eventually insufficient to rescue this optical
sampling stage. This is a statement about success and measured cost, not
about classical reproduction of the quantum distribution.

For alpha=1, delta=-log(4eta)>0 exactly when eta<1/4. For alpha=2 and eta<1/2,

    I(2,eta)=-log[4eta(1-eta)],
    delta>0 iff eta(1-eta)<1/16,
              iff eta<(2-sqrt(3))/4.

The second boundary is smaller because extra input photons can compensate
loss. An unbounded source, variable squeezing or a decoder using fewer than k
photons changes the premise and cannot be silently declared ruled out.

## E. Meaning for this project

P37 concerns actual Haar-averaged feasibility and source optima; (A)-(D) give
an oracle envelope for any graph-dependent output law under the stated loss
and encoding assumptions. This is additional scope, not a new physical law.
It can close a proposed *loss/cost regime* for a fixed-photon hardware sampler,
including ideal conditional graph enrichment, after calibration/cost hypotheses
are established. It does not close ideal eta=1 optimization, all encodings,
the whole adaptive hybrid pipeline, or the unrestricted P41 discovery target.

The separate phase-proxy approach under investigation by root may give a
stronger pointwise comparison that retains the graph signal. These arguments
have different hypotheses and neither may inherit the other's conclusions
without a proof and cost audit. External prior-art scope is recorded in
research/P41_obstruction_loss_sources.md; novelty remains unresolved.
