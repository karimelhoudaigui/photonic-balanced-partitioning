# Late-2026 loss results: exact-source and application audit

Checked 2026-11-22, starting 12:38 UTC, with `mathbox:literature-check`.
Isolated branch `research/late2026-loss-review`, base
`d402374b21a812de1d1b5658fac37d294a20a035`. Only this report is changed in
tracked files; source PDFs, extracted text and metadata are retained in the
worktree's ignored `.local/references/` cache. No manuscript, experiment,
shared ledger, paid service or QPU was changed or used.

The P37 regime definitions were read in
`theory/phase3_loss_source_selection.md`, SHA256
`fda5160d1d4eb232f67eae09cfcfabf3024822ea1e0720ef639267374a642807`,
and `research/P37_LOSS_SOURCE_CONTRACT.md`. P37 compares Haar-averaged
threshold feasibility for distinct-photon sources N near m, including the
boundary eta=1-lambda/m. It is not itself a theorem about sampling
complexity, trained interferometers, or graph-quality enrichment.

## Outcome and claim boundary

Both checked preprints state classical approximate-sampling theorems for
distinct single-photon inputs with arbitrary additional vacuum modes,
including N=m. Both retain the complete photon-number output law and
collisions. Their polynomial-time guarantees require a fixed nonzero loss
rate and Haar-typical interferometers; this is a material restriction.

Angrisani–Mhiri additionally state near-full-filling concentration around
an explicit circuit-independent reference. The relevant norm, finite
constant, and reference are identified below. This is stronger than merely
evaluating the Haar mean, but it concerns unconditioned output data and
does not automatically control rare accepted outputs or a trained circuit.

**Authentication and theorem extraction: verified. Source-dependent regime
translation: verified with the stated hypotheses. Independent proof of
either complete sampling theorem: not performed.** The strongest near-full
argument and several dependencies were inspected in detail, with remaining
leaves identified below. These source checks do not establish a numerical
NO-GO for a small QPU experiment, an efficient sampler for every trained
optimizer, or a novelty claim for the project.

## A: Angrisani–Mhiri, exact version and statements

Armando Angrisani and Hela Mhiri, *Polynomial-time classical simulation of
boson and fermion sampling under thermal loss*,
[arXiv:2611.08444v1](https://arxiv.org/abs/2611.08444v1), 2026-11-05,
83-page primary PDF. The relevant input is (II.2): one photon in each of
n<=m distinct modes, with n=N in project notation. Noise is identical in
all modes: transmissivity eta and thermal bath occupation beta. Beta=0
is pure loss; bosonic beta is allowed polynomial growth in m.

The standing assumption before **Theorem III.1**, PDF p. 3, is eta constant
bounded away from one. For epsilon,alpha in (0,1), the theorem states a
classical randomized sampler with

    Pr_(U Haar)[TV(Q_U,P_U)<=epsilon] >= 1-alpha,
    runtime poly(m,epsilon^(-1),alpha^(-1)).

The polynomial is not uniform in a transmissivity approaching one.
**Theorem III.2** gives, for a specified U satisfying ideal-output flatness
chi²(p_ideal,U || u_N)<=m^O(1), a quasipolynomial sampler with runtime
(m/epsilon)^O(log(m/epsilon)). **Corollary III.3** improves this to polynomial
under homogeneous loss after Omega(log m) passive layers, with fixed
per-layer transmission and the same flatness condition. These are different
guarantees, not a universal fixed-U polynomial theorem.

### Runtime and finite precision behind the Haar theorem

The end-to-end statement is **Theorem H.4**, PDF p. 83, (H.19)–(H.22).
For Fock inputs, the supplied parameters include

    s=eta/[1+(1-eta)beta],
    a_D <= s^(D+1)/(1-s),
    S_D <= 2 sum_(j=1..min(D,N)) (3 e² s)^j,
    C_ref <= (1-s)^(-1).

Here a_D bounds a Haar-mean squared weighted-L2 approximation residual,
S_D bounds integrated estimator variance, and C_ref bounds a reference
second moment. A sufficient schedule makes a_D<=alpha epsilon²/64. With
the notation of H.4, the bounded arithmetic work per output is

    (A+E_max) poly(m,N,K_*,D,J) 2^O(D),
    A+E_max = O(C_ref/(alpha epsilon) log(16/epsilon)
                + S_D/(alpha epsilon²)
                  log²[16 C_ref/(alpha epsilon²)]).

At fixed loss, D=O(log[1/(alpha epsilon²)]) suffices, capped at the exact
degree N. The finite-precision discussion is Appendix H.1–H.3: numerical
threshold errors, random bits and proposal-count tails have separate
budgets. Pure loss has K_*=N and no reference-count tail. The claims assume
classical access to the circuit description and sufficiently accurate
matrix/scalar data; they are not algorithms using only quantum readouts.
No implementation or practical wall-clock estimate is supplied by this audit.

## A's strongest near-full statement: norm, reference, finite constant

**Proposition III.4**, PDF p. 3, assumes h=m-N=O(1). Its proof is Appendix
F.1.6, PDF pp. 53–54, (F.47)–(F.57). Let u_l be the normalized uniform law
on all m-mode Fock occupations with l photons, whose cardinality is
d_l=binom(m+l-1,l). Define

    mu = N_(eta,beta)^(tensor m)(u_N).

The degree-D approximation q_D,U is generally signed. Its weighted residual
is exactly

    a_D(U) = sum_x [P_U(x)-q_D,U(x)]²/mu(x)
           = sum_(j>D) Gamma_j W_j(U).               (F.47)

Inverses are restricted to reference support. The source writes diagonal
states and trace norms; here all quantities are classical occupation laws.
Put a_D^H=E_U a_D(U). Weighted Cauchy–Schwarz gives

    E_U ||P_U-q_D,U||_1² <= a_D^H.

At D=0, q_0,U=mu is positive, normalized and independent of U, so a_0(U)
is chi²(P_U||mu). Consequently

    E_U TV(P_U,mu)² <= a_0^H/4.

The factor 1/4 must not be dropped. Neither a_D(U) nor a_D^H is itself
TV². For D>0, q_D,U need not be a probability distribution and requires the
source's positive sampling construction.

The proof supplies the finite bound

    a_D^H <= (1/m) sum_(j>D) j(h+j-1) eta^j.          (F.55)

For bounded h and fixed eta<1, it is O(eta^(D/2)/m), with a constant depending
on eta and the bound on h. At degree zero the sum simplifies to

    a_0^H <= C_h(eta)/m,
    C_h(eta)=h eta/(1-eta)²+2 eta²/(1-eta)³.

Thus E TV<=min(1,sqrt[C_h(eta)/(4m)]), and
Pr(TV>t)<=C_h(eta)/(4m t²). These are translations of the source's norm
bound, not new concentration theorems.

### Exact normalized reference at beta=0

For pure loss, the reference sampler in (F.71)–(F.73), PDF p. 56, reduces to

    mu(x)=binom(N,l) eta^l(1-eta)^(N-l)/binom(m+l-1,l),
    l=|x| in {0,...,N}.

Equivalently, draw l~Bin(N,eta), then draw uniformly from weak compositions
of l into m parts. This includes the vacuum with probability (1-eta)^N.
It is the exact Haar-average law for the fixed source N, not the law of
independent photons through a particular U.

Thresholding is a deterministic map, so all full-law TV guarantees transfer
to threshold strings without increasing error. For j>=1, the reference
probability of exactly j clicks is

    binom(m,j) sum_(l=j..N)
      binom(N,l) eta^l(1-eta)^(N-l)
      binom(l-1,j-1)/binom(m+l-1,l).

At j=0 it is (1-eta)^N. In particular j=m/2 reproduces P37's exact binomial
mixture S_N. Given j, its occupied subset is uniform. This identifies the
reference precisely; it is not a fresh graph-optimization benefit.

### Finite constants: no small-device conclusion from the asymptotic alone

The following are exact evaluations of C_h/m at h=0 and m=64. They are
arithmetic, not simulations or measured performance.

| eta | C_0(eta) | a_0^H upper bound C_0/64 | E TV² upper bound C_0/256 | Capped E TV upper bound |
|---|---:|---:|---:|---:|
| 1/2 | 4 | 1/16 | 1/64 | 1/8 |
| 9/10 | 1620 | 405/16 | 405/64 | 1 |

At eta=0.9, this bound is already trivial after capping at one. Even the
eta=0.5 mean-TV bound is an unconditional ensemble bound, not a certificate
of small relative error for selected feasible outputs. No numerical QPU
NO-GO follows from this table.

## What was inspected in the near-full argument, and what was not

The checked chain is C.21–C.22 and Theorem C.3 (norm conversion/orthogonal
expansion), Lemma F.2 and Proposition F.3 (degree contractions), Proposition
F.4–F.5 (Haar degree energies), then F.52–F.57. The decisive near-full steps
are explicit:

    H_j=||Pi_j(rho_in^(j)-I/d_j)||_2²
       <= binom(N,j)^(-1)-d_j^(-1),
    binom(N,j) H_j
       <= 1-prod_(r=0..j-1)[1-(h+2r)/(m+r)]
       <= j(h+j-1)/m,
    E_j <= s^j binom(N,j) H_j <= eta^j j(h+j-1)/m.

The first step uses normalized reductions uniform on occupied j-subsets
and the exact-degree orthogonal projector annihilating identity. The second
is a product/union bound. The third uses the binomial factorial moment and
factorial ratios at most one in (F.44). Summing gives the bound above.
These local inequalities, the direction of the norm conversion, and the
eta-dependent constant were checked; the entire 83-page proof was not.

The Haar energy identity (F.39) is adapted from Mhiri et al., *Boson sampling
beyond the dilute regime: second moments and anti-concentration*,
[arXiv:2604.14323v1, HTML (434)](https://arxiv.org/html/2604.14323v1).
That primary formula was read. The prefactors match because, with
d_j=binom(m+j-1,j),

    [d_j/(d_j+d_(j-1))] (m+j)^(overline j)
        = (m+j-1)^(overline j).

The proof of that external irrep identity and all earlier representation
theory were not re-audited. The Hahn basis's external orthogonality theorem,
all colored-estimator variance calculations, and every finite-precision
subroutine were not independently reconstructed. H.4's schedule and error
allocation were read as source dependencies, not certified by fresh tests.
This is a bounded source check, not a claim of independently proving A.

## L: Lim, precise average-case theorem and loss dependence

Youngrong Lim, *Boson sampling is fragile to loss*,
[arXiv:2611.01434v1](https://arxiv.org/abs/2611.01434v1), 2026-11-01,
39-page primary PDF. **Theorem 1**, PDF p. 3, covers n=N distinct single
photons and every mode count M=m>=N, with all output collisions. At fixed
0<eta<1 and 0<epsilon<=1/2, it states

    E_(U Haar) TV(P_U,Q_U)<=epsilon,
    worst-case arithmetic work per sample <=poly_eta(m,N,epsilon^(-1)).

Appendix A.2 makes the quantifier explicit: the circuit is drawn once and
held fixed; setting mean error to epsilon alpha yields a probability-alpha
exceptional set for a desired circuit error epsilon. The sampler does not
identify bad circuits. Polynomially many subsequent readouts can be covered
by reducing per-sample error by the readout count. Thresholding contracts TV.

Relevant supporting passages checked: §B.3, (B.18)–(B.23), PDF p. 15,
computes reduced purity binom(N,j)^(-1) and bounds the discarded sector
mean-L2 residual by eta^(D+1)/(1-eta). Appendix C.3 gives evaluation cost
poly(m,N,D) exp[O(D_eff)], with D_eff=O(D+log(1/epsilon)) at fixed loss;
Appendix D.1 and D.5 handle clipping, rejection caps and error allocation.
In particular (D.4), PDF p. 29, chooses the correlation cutoff D (called L
in that paper) with

    D+1 >= log[256/((1-eta)epsilon²)]/(-log eta).

Appendix D.4 discusses finite random bits and polynomial precision overhead.
These source statements were extracted; neither the randomized evaluator
nor the whole sampler was implemented or independently proved here.
Appendix F.1 explicitly requires separate tail and variance bounds for a
specified structured interferometer. The Gaussian and nonuniform-loss
extensions were not needed for, and are not adopted into, this Fock audit.

## Fixed loss and the P37 boundary are different limits

At fixed eta<1 and N=m-O(1), the mean lost count is Theta(m). The two source
polynomial-time theorems cover that Haar setting. A's degree-zero reference
approximation also converges in this regime.

For eta=1-lambda/m with fixed lambda>0 and N=m-h, the mean lost count tends
to lambda. Neither polynomial statement is uniform in this substitution.
More concretely:

- A's finite degree-zero majorant has C_h(eta)/m=Theta(m²) when h is fixed,
  since its second term is asymptotic to 2m²/lambda³. It becomes vacuous.
- L's sufficient cutoff (D.4) is of order m log m for inverse-polynomial
  target accuracy, before capping at the exact degree N=Theta(m). The
  exponential-in-degree evaluation bound then supplies no polynomial claim.

These are failures of the stated sufficient estimates, not hardness proofs.
At lambda=0 the setting is lossless and outside the fixed-nonzero-loss
theorems. L's Appendix G.1 separately discusses why its runtime bound does
not cover logarithmic loss; that does not establish hardness of P37's
specific near-full threshold task. P37's Haar-mean mixture remains exact
in its own boundary regime independently of these approximation theorems.

## Trained U, finite portfolios, and one additional readout

For an arbitrary trained U(G), Haar-average guarantees alone are
**inapplicable**. Training can bias the circuit distribution, and a fixed
circuit need not satisfy A's polynomial-flatness condition. A circuit family
with a separately proved flatness bound can invoke the appropriate
quasipolynomial theorem; applying it is **conditional** on that missing
certificate. L likewise needs circuit-specific correlation and variance
bounds. None is supplied by “the initialization was Haar”.

A concrete obstruction to a universal circuit-independent reference is
U=I, beta=0, N=m-h with fixed h. Every surviving photon occupies a distinct
output, so P_I(collision-free)=1. The reference has

    mu(collision-free)=E_(l~Bin(N,eta))
        [binom(m,l)/binom(m+l-1,l)] ->0

at fixed eta in (0,1): l is Theta(m) with high probability and the displayed
ratio decays exponentially there. Thus full-law TV(P_I,mu)->1. Even with
threshold data alone, let K be the click count. Then

    E_I K/m ->eta,
    E_mu K/m = E[l/(m+l-1)] ->eta/(1+eta).

Since K/m lies in [0,1], threshold TV is at least eta²/(1+eta)+o(1).
This is an internal counterexample to dropping the Haar qualification,
not an assertion that the identity circuit is hard to simulate. Its ideal
output also has chi²(p_ideal,I||u_N)=binom(m+N-1,N)-1, so it fails A's
polynomial-flatness hypothesis in this regime.

There is a narrower portfolio implication. Fix the instance, N=m-h and eta.
Draw a list of L Haar candidate circuits with those same parameters. Every
candidate must have a Haar marginal; independence suffices but is not needed
for the following sum bound. Write d_j=TV(P_(U_j),mu). Then

    E max_(j<=L) d_j² <=sum_j E d_j² <=L C_h(eta)/(4m).

Suppose any procedure, even graph-aware and history-dependent, selects an
index J from this list. Preserve the **entire selection/history law** and
all its classical and physical costs. Replacing just **one new independent
readout** P_(U_J) by mu changes that resulting joint law by at most

    E d_J <=min(1,sqrt[L C_h(eta)/(4m)]).

The bound tends to zero when L/m->0 at fixed h,eta. It also holds after the
same threshold or graph-dependent postprocessing channel is applied to
both readouts. It does not simulate the process choosing J, reproduce its
history for free, or cover arbitrary continuous training of the candidates.
Changing N across candidates also changes the reference and requires a
separate contract. This portfolio inference is elementary postprocessing of
the cited mean bound, not a theorem attributed to A or L or a novelty claim.

Conditioning is another gate. If a full-law error is epsilon and acceptance
has probability p>epsilon, a conservative conditional-TV bound is
2epsilon/p. Therefore the unconditioned bounds cannot automatically replace
the accepted, exactly-m/2-click law or control its relative success
statistics. Rare-event precision and rejection costs must be included.
Neither this portfolio argument nor source concentration supplies those
costs for a trained graph solver.

## Audit ledger, retained artifacts, and remaining gate

| Requested implication | Verdict | Required qualification |
|---|---|---|
| Distinct Fock inputs, N near m, fixed uniform loss, Haar-typical full-law sampler | Verified source statement and translation | Classical circuit description; source proof is relied upon, not independently reproved. |
| Same guarantee for threshold data | Verified formal corollary not stated | Deterministic postprocessing; unconditioned data. |
| Near-full circuit-independent reference, fixed eta | Verified source statement and norm translation | Mean/typical Haar guarantee with explicit C_h(eta); finite bound can be trivial. |
| eta=1-lambda/m with O(1) mean losses | Inapplicable fixed-loss theorem; no conclusion from its estimates | Need a different uniform bound or algorithm. |
| Every fixed trained optical optimizer | Inapplicable from Haar claims alone | Need trained-ensemble/circuit-specific certificates; A's flatness route is quasipolynomial under its assumptions. |
| Selection among an a priori Haar portfolio, one fresh readout | Verified elementary conditional construction described above | Selection/history and all costs retained; no automatic simulation of selection. |
| Accepted balanced output or QPU wall-clock NO-GO | Unverified | Acceptance precision, runtime constants, implementation and matched-budget comparison remain. |

Retained exact primary artifacts in this worktree:

| Source | PDF SHA256 | Extracted-text SHA256 |
|---|---|---|
| A, [2611.08444v1 PDF](https://arxiv.org/pdf/2611.08444v1) | `7dfb76ea2d6c0fc965af37cb05968d2fe71aea04fc44773f733241745765a227` | `a77c973ce928de2fa9309adaa776c93e289c050ffc78fa2460b0050432a1d6da` |
| L, [2611.01434v1 PDF](https://arxiv.org/pdf/2611.01434v1) | `148712797e3b1e45da2c0fc9e265be339cf68215946dead4368141e591a00639` | `cc9a281d74073247e7c44e3f05c6e3e6690203dfd4e1759c20f8d895a1dd422d` |

Each directory `.local/references/angrisani_mhiri_2611.08444v1/` and
`.local/references/lim_2611.01434v1/` contains `source.pdf`, `source.txt` and
`source.json` with identifier, authors, version, URL, date, retention basis
and hashes. Extraction used pypdf 6.4.0 with Python 3.9.6. Hashes and ignored
status were checked; no full source is tracked. These local files are not
automatically transferred by cherry-picking this report.

This is a focused check of two November 2026 preprints and the identified
Haar-energy dependency, not a search establishing priority or absence of
other results. No source theorem has been independently proved by reading
it. Before a strong project conclusion, the remaining gate is an independent
review of the relevant source proof dependencies plus a regime-appropriate,
implemented and budgeted comparison. No global novelty, hardness, advantage
or finite-device impossibility follows from this audit.
