# P44 — click-moment obstruction for general passive contractions

Root derivation, 24 November 2026. This is a proposed strengthening of P42,
not a hardware calibration or a universal ideal-optimization impossibility.
Independent card-only reconstruction has been requested before this author
file is read. External attribution remains OPEN; the ingredients are known.

## Physical model and target

One attempt starts with N photons, one in each of N DISTINCT spatial input
modes A. First take the photons perfectly identical. A passive spatial network
with vacuum environments has a transmission matrix T on accessible modes:
output annihilators are T times input annihilators plus vacuum-environment
terms. T is a contraction. This includes nonuniform input, path and detector
attenuation and any passive mixing; it excludes gain, nonvacuum noise,
dark-count replacements and nonlinear or same-attempt herald-conditioned
operations. Let eta0 be an upper bound on ||T[:,A]||_op^2 (using ||T||_op^2
is sufficient). This is a spectral intensity-transmission bound, not a mean
column transmission. The current T can depend on the graph and past classical
history, provided the same upper bound applies to every permitted choice.

Let S be any k DISTINCT measured output modes, k>=1. Define the normally
ordered moment mu_S=E[prod_(i in S) n_i]. All losses and collision events remain
in the expectation. No outcome law is renormalized. For N<k the moment is zero.

We prove

    Pr(every mode in S clicks) <= mu_S <= eta0^k.          (M1)

Consequently this cap covers direct exact-support decoding AND any decoder
whose emitted k-subset consists entirely of modes that really clicked. There
may be additional clicks, collisions, rejected modes or unobserved external
outputs. Classically filling unclicked vertices is a different model.

## Moment, permanent Cauchy–Binet and a spectral upper bound

Put B=T[S,A], a k-by-N matrix. Normal ordering and vacuum environmental input
give

    mu_S = sum_(R subset A, |R|=k) |per(B[:,R])|^2.       (M2)

Indeed applying the k distinct output annihilators to the input Fock state
selects k distinct occupied source modes. For a given R the k! routings add
to its permanent. Different R leave orthogonal hole occupations; their squared
norms add. There is no k! multiplier outside this sum.

The permanent Cauchy–Binet identity, including REPEATED columns, gives

    per(B B*) = sum_(r>=0, sum r=k)
                 |per(B[:, repeated columns r])|^2 / prod_a r_a!.  (M3)

This follows by expanding each matrix entry in the permanent product and
grouping the k selected intermediate indices by multiplicity. Each grouped
assignment is counted prod r_a! times by the repeated-column permanent, so
the stated factorial denominator is necessary. All terms are nonnegative.
The collision-free choices r_a in{0,1} reproduce (M2); other terms only add.
Thus mu_S<=per(G) for G=B B*.

Now 0<=G<=eta0 I_k. Let Omega_k be the normalized symmetric sum of the k!
ordered words (pi(1),...,pi(k)) with each basis vector used once. Then

    per(G)=<Omega_k, G tensorpower k Omega_k> <= eta0^k.  (M4)

The tensor operator is positive with norm at most eta0^k. Finally the
indicator of all S modes occupied is bounded pointwise by prod n_i. This
proves (M1). Neither Haar averaging, a uniform-loss commutation nor enumeration
of the lost photons is needed. A permutation routing chosen k inputs to S
with intensity eta0 attains eta0^k for that specified S; this is a sharp
single-event bound, not an optimum-blind way to discover a good partition.

## Unknown internal states: a separate, weaker universal cap

Suppose the N distinct spatial inputs carry arbitrary normalized internal
states, including correlations, and the SAME transmission T acts on all
internal degrees. Source occupations remain fixed CF. Purify the internal
state if necessary. For each k-source hole set R, an output-annihilation
amplitude is a sum of k! routings c_pi v_pi; each internal routing vector
has norm1. Spatial hole sets are orthogonal. Cauchy gives

    ||sum_pi c_pi v_pi||^2 <= k! sum_pi |c_pi|^2.

Summing over R and relaxing distinct source assignments to all assignments,

    mu_S <= k! sum_(distinct a_1,...,a_k) prod_i |B_i,a_i|^2
         <= k! prod_i sum_a |B_i,a|^2 <= k! eta0^k.      (M5)

The probability cap may be clipped at1. Perfectly distinguishable photons
obey the stronger eta0^k cap by their independent-particle assignment formula.
The identical-photon cap MUST NOT be extrapolated monotonically through all
partial internal states. The retained DFT6-plus-two-spectators construction
has a four-click contribution at least(7/6)eta^4(1-eta)^4, larger than eta^4
for sufficiently small positive eta. Unknown internal states therefore use
(M5), or a separately proved sharper internal-state certificate. Internal-
dependent transmission or source occupation superpositions are not covered
by the displayed routing proof. No arbitrary-partial-state numerical campaign
is substituted for that quantifier.

## Adaptive balanced-partition search

For m=2k let D=binom(2k,k). Assume fresh attempts, classical histories, no
same-attempt herald normalization, and a common frontend/incumbent credited
to all methods as in P42. Every history-dependent passive network/source
choice has the declared eta0 bound. A permitted candidate decoder outputs
at most one k-subset and every selected vertex has an actual click.

For a fixed target set of g partitions, the conditional optical hit
probability is at most g*b, where b=eta0^k for identical photons, or
b=min(1,k!*eta0^k) for unknown internals. If nQ is an upper bound on charged
attempts, nC>0 guaranteed uniform feasible draws, and L=ceil(nQ/nC)>=1, then

    L*D*b<=1                                                (M6)

implies uniform feasible search stochastically dominates the final best newly
measured cost. Proof: for p=g/D, quantum failure is at least
(1-p/L)^nQ >=(1-p/L)^(L nC)>=(1-p)^nC. The target can be every cost-sublevel
set. nQ=0 is trivial. Costs, floors and score limits require guaranteed bounds;
expected latencies do not instantiate nQ/nC. Extra classical candidate
discoveries need their own credited search, rather than appearing free in
the optical event. A batch returning several candidates must charge them
or receive its own union-factor bound.

For equal counts, eta0<=1/4 is sufficient for every k and N in the identical
model since binom(2k,k)<=4^k. This strengthens P42's threshold eta<=1/5
sufficient range and removes its uniform-loss assumption. The exact P42
PNR/source-conditioned tables can still be tighter in their own model.
For unknown internals use the explicit k! criterion; no constant eta1/4
statement is asserted uniformly in k for that model.

## Limits and interpretation

The normally ordered moment bound compares a CF Fock input to a thermal/
permanental moment envelope; it is NOT pointwise domination of all complete
Fock probabilities or all graph-search decoders. It explains why arbitrarily
programming passive interference cannot concentrate enough physical k-click
events in a low-transmission regime to beat a feasible classical reference.
It does not rule out high-transmission optics, arbitrary classical completion,
different quantum resources or nonlinear/heralded mechanisms with their full
cost. No measured Lucy transmission, gate capability or cost is inferred.

The manuscript, historical results and original P42 inputs remain unchanged.
Independent exact-hash proof audit and numerical checks have not yet been
recorded for this file; they belong in separate receipts. Global novelty of
the composed search obstruction remains a source-checking obligation.
