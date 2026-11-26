# P97: factorial residual hybrid — analytical card and optimization veto

Owner `/root/p66_dark_audit`, 2026-11-26, parent `40d2e6a5729008b7292373eb158df994bdc99c3d`.
Primary route verdict: **OPEN, with no optimization pilot justified.**
KEEP the control-variate identities/bounds; REJECT their automatic promotion
to an interference witness or a graph-optimization benefit. This card itself
has not received independent proof review. No priority claim for control variates.

Inputs: P96 proof `6f4e7fb90e284a8e358c55886ddd2032d45811f9`, SHA256
`b378ebd6bb0bb6f981e9fe395938e3a43aec7775f761b81cda7b394f6dc1e94e`, and
independent review `40d2e6a`, SHA256
`a64783dee2b4903b475a8b1ea554640b4c320d9da81cf854871f219725e29d7f`.
The ROOT-supplied residual/variance candidates are rederived below; the paid
frontier progress veto is recorded separately from the estimator's validity.

## Question and immutable scope

Can a positive low-photon surrogate plus a raw quantum residual expose a useful
high-order optimization mechanism? Preserve the scientific target: better actual
graph partitions under matched total costs, not merely a smaller mean-estimation
variance. Use P96's known CF input, K photons/attempt, passive vacuum-loss T,
explicit complex T access and certified mu=Tr(T^dagger T)<=1/2.
Fix one optimum-blind deterministic balanced decoder and graph cost f(n), total loss K-|n|.
Let F be a known envelope for range(f), e.g. the total nonnegative graph weight W;
no global optimum, C*, optimal mask or known optimal partition defines F or f.
Decoder/graph features and all quenching are common paid inputs to every control.

## Exact factorial interpolation and residual

Write f0=f(0), f_j=f(e_j), f_jl=f(e_j+e_l), and f_2j=f(2e_j). Define
I2f(n)=f0+sum_j n_j(f_j-f0)
 +sum_(j<l)n_j n_l(f_jl-f_j-f_l+f0)
 +sum_j binom(n_j,2)(f_2j-2f_j+f0).
Direct substitution shows I2f=f on every N=|n|<=2 record, including bunches.
P96's exact first/second moments give E_B I2f=E_q f by collecting coefficients:
f0 has coefficient 1-mu+G/2, f_j has lambda_j-G_j, and pairs have their q masses.
Thus R(n)=f(n)-I2f(n) vanishes on N<=2, and
E_B f=E_q f+E_B R. This is a signed estimator identity, not a positive sampler.

For N>=3, rewriting the polynomial gives
I2f=((N-1)(N-2)/2)f0+(2-N)sum_j n_j f_j
 +sum_(|y|=2) binom(n,y) f(y),
where binom(n,e_j+e_l)=n_j n_l and binom(n,2e_j)=binom(n_j,2).
The pair weights sum to binom(N,2). In R the positive and negative coefficient
masses each equal (N-1)^2 and their signed sum is zero. Therefore
|R(n)|<=F(N-1)^2 1_(N>=3),
sharp for arbitrary bounded f; it is not asserted sharp for every graph decoder.
P96 immediately gives |E_B R|<=24F e3(c)<=4F mu^3.
If the requested absolute accuracy exceeds this certified bias, E_q f already
meets it without optical shots. Approximating E_q f itself still has paid errors.

## Second moment, concentration and source-photon cost

The exact polynomial identity (N-1)^4=(N)_4+2(N)_3+(N-1)^2, restricted to N>=3,
and (N-1)^2<=2(N)_3/3 imply
E R^2<=F^2[E(N)_4+(8/3)E(N)_3]
 <=F^2[576 e4(c)+96 e3(c)] =: V
 <=F^2(24mu^4+16mu^3).
The variance is <=V; V is a RAW second-moment bound, not the exact variance.
K=3, one observed mode, equal column intensity alpha, and bounded statistic
f0=f_2=F, f_1=f_(N>=3)=0 gives R=-4F on N=3. Since P(N=3)=6alpha^3,
E R^2=96F^2 alpha^3=96F^2 e3(c): that coefficient is attained exactly.
This artificial statistic supplies no graph-optimization advantage.

For K>=3 put D=F(K-1)^2; |R|<=D. For |t|D<3, the expansion and
E|R|^k<=D^(k-2)E R^2, k>=2, give
log E exp(t(R-ER))<=V t^2/[2(1-|t|D/3)].
Indeed log E exp(tR)<=E exp(tR)-1 cancels the linear term after subtracting tER;
k!>=2*3^(k-2) bounds the remaining series. Thus D here need NOT bound |R-ER|.
For n independent fresh fixed-T attempts, epsilon>0 and 0<delta<1, the two tails yield
Pr(|mean R-ER|>epsilon)<=2 exp[-n epsilon^2/(2(V+D epsilon/3))].
A sufficient count is n>=ceil[2(V/epsilon^2+D/(3epsilon)) log(2/delta)].
All n raw attempts, including vacuum and N<=2, charge K injected photons:
source cost K n, not K times the accepted-tail count. K<=2 has R=0 exactly.
Unknown finite-precision bias and setup/calibration are additional error/cost terms.

P(N>=3)<=E(N)_3/6<=6e3(c)<=mu^3. With cached low-sector scores, only tail
records need a new f evaluation, expected count <=n mu^3 for fixed T; the
worst-case count remains n. I2f arithmetic/mode processing also costs work.
For fixed K, raw empirical detection of a margin of order F mu^3 at relative constant accuracy
can still require order mu^-3 shots/photons times K and confidence factors.
A Bernoulli rare branch already needs this many attempts to be seen reliably.
Lower variance for a fixed mean is neither a delivered partition nor an optimizer.
Nor is variance uniformly reduced: the same K=3 rank-one example at alpha=1/6
with f=F on N=0,2 and zero otherwise gives Var(f)=65F^2/324, but
Var(R)=35F^2/81. This hand counterexample satisfies mu=1/2; no shot was evaluated.

## Mandatory paid frontier and exact direct-progress veto

The low sectors contain 1+m+m(m+1)/2 raw categories: 325 at m=24, including
vacuum, repeated outputs and any zero-probability categories. Evaluate their
actual balanced decoded partitions, scores and descents; archive duplicates and
all work. T/moments cost O(m^2 K) arithmetic, plus those 325 decoding/scoring
operations and their feature/calibration costs. The classical controls receive
these same features/candidates before optical discovery receives any credit.
An averaged randomized decoder cannot be substituted as one discovered partition.

Let b be the best COST ACTUALLY FOUND by this paid frontier (or a stronger shared
classical search). It is a feasible incumbent, not the global C*. Define either
h(n)=1_(f(n)<b) or h(n)=(b-f(n))_+.
Every low-sector decoded candidate has f>=b, so h=0 for N<=2. Hence EXACTLY
I2h=0, E_q h=0, and the interpolating residual R_h=h.
This particular own-function control variate therefore gives no variance
reduction at all for the actual improvement statistic beyond the paid frontier.
The only optical candidate progress is a real tail record with a better partition;
its probability is at most mu^3 and every failed source attempt is charged.
This veto does NOT rule out other control variates: known N, N^2 or other
features can correlate with h. Their benefit, fitting cost and concentration
would need separate analysis. Nor does it rule out a genuinely better tail policy.

## Falsifiers: residual is not irreducible interference

Take K=m=3,T=sqrt(eta)I with 3eta<=1/2. No source paths meet, so B=D exactly;
nevertheless f=1_(N=3) has I2f=0 and ER=eta^3>0. Three surviving photons do
not certify a three-source exchange contribution, much less a quantum advantage.

A balanced graph counterexample also gives a favorable COST sign without any
interference. This is a falsifier, not a proposed benchmark/training set.
On four vertices use the single edge {1,2}, weight one, and a
public decoder returning {1,3}|{2,4} for N<=2, {1,2}|{3,4} for N>=3.
These two partitions are fixed by labels, not an optimum oracle or training.
With the same diagonal T, f is one on low sectors and zero on the tail:
I2f=1, ER=-eta^3. Yet a classical control scores the public tail partition
directly and obtains cost zero without waiting for photons. Counting this
preselected partition as a quantum discovery would be a false positive.

For any fixed balanced spin decoder, linearity gives
R_C(n)=-(1/2)sum_edges w_uv R_(s_u s_v)(n), since I2 preserves constants.
No graph sign follows from the norm/variance bounds. For an unweighted simple
graph and its complement under the SAME decoder/T, balanced cuts sum to the
constant |V_graph|^2/4, so their residuals are pointwise negatives.
This forbids a universal favorable-sign inference from residualization alone;
it is no obstruction to every graph-dependent compiler or adaptive decoder.

## Decision, remaining gap and next admissible proof step

No execution or new optimization pilot follows from this card. The remaining
question is a physical, optimum-blind tail SEARCH mechanism whose actual better
partitions beat the whole paid frontier and stronger feasible classical search.
A next card must specify a graph family, graph-to-T/decoder rule and common paid
incumbent, then derive a full-raw improvement prediction before collecting data.
It must distinguish exchange from independent/grouped tail effects and survive
independently reoptimized D/groups<=3 plus an exact Fock classical sampler at
K<=12, with fresh graphs/seeds/relabelings/held-outs and matched total costs.
The first cheap veto is h above: any proposal offering only this I2h variance
reduction is already closed. Replacing the mechanism requires a new predata card;
no target discovered classically may be prepared and called an optimization gain.
Adaptive estimation needs fresh conditional kernels and martingale/error budgets;
the fixed-n concentration proof does not authorize a fitted/reused random table
or optional stopping. No global optimum, simulator outcome, imports, AST/code,
RNG, native/test/runner call, QPU, manuscript edit, push or delegation occurred.
