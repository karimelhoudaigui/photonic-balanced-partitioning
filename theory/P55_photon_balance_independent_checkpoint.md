# P55: independent photon-balance decoder checkpoint

Frozen before reading any P55 encoding/author document. Only ROOT's decoder
definition/question was supplied. No import, executable arithmetic, simulation,
graph, test or sample was used. This is a manual derivation, not a positive
optimization/hardware claim. P53b source review took priority and is separate.

For N even,K=N/2 and arbitrary detected nonnegative integer counts n, let
M=sum n. T(n) is uniform among **all** K-subsets minimizing
|2 sum_(i in S)n_i-M|. Every event is decoded, including odd M, vacuum and
loss sectors; no condition of exact photon balance is imposed when infeasible.

## Single-hop sign for lossless full input

Take real symmetric H_ij=sqrt(w_ij), w>=0, diagonal0; U=exp(itH), one photon
in every mode, fixed finite N>=4. At identity all counts1 and T is uniform u.
A directed hop j→i has n_i=2,n_j=0 and others1, totalN. For any balanced S,
sum_S n=K+1[i in S]-1[j in S]. Minimum imbalance0 therefore requires
**the same membership for both endpoints**. Both-in and both-out are possible;
T is exactly u conditioned on edge ij being UNCUT, not forced across.

Write q=Pr_u(edge crosses)=N/[2(N-1)], W=sum w, C(S)=sum w_e X_e(S).
The previously independently derived Fock probability of each directed hop
is2t²w_e+O(t4), initial mass1-4t²W+O(t4). Thus

    mu_B,t(S)=u(S)[1-4t²(C(S)-qW)/(1-q)]+O_G(t4),
    E_B,t C=qW-4t² Var_u(C)/(1-q)+O_G(t4).

D has coefficient2 instead of4. Nonconstant cost has a favorable small-t
minimum-cut drift, but D at sqrt2*t matches the same leading law. This is
about the feasible decoded cost, not a raw quadratic moment proxy. For an
arbitrary guide A the response uses Cov(C_w,C_|A|²), not necessarily variance.
N2 is exceptional: no uncut balanced subset exists; its feasible cut cost is
constant. Real H is needed for the stated even O(t4) remainder. No uniform
in-N or finite-strength claim is made.

## Necessary classical nulls, including retained losses

For4t²W<=1, with probability4t²W choose edge proportionalw and draw u
conditional on that edge uncut; otherwise draw u. Conditional sampling is
cheap: both-in or both-out with equal probability (their completion counts
are equal by complementation), then choose the required remaining vertices
uniformly. W0 uses u. This reproduces the entire displayed leading B law,
not only its mean, so the favorable derivative alone is no advantage evidence.
Preprocessing/sampling/scoring costs must be included; this is not a general
equal-cost or finite-angle domination theorem.

A stronger occupation-level classical null is the CTMC with directed rates

    n→n+e_i-e_j at rate |H_ij|² n_j(n_i+1), auxiliary time tau=t².

It is a valid finite-state nonnegative-rate process preserving total photons.
From full input its first-jump probabilities are exactly2t²w per direction,
so its **complete count law** agrees with the optical one up toO_G(t4).
The independent-particle CTMC replaces n_j(n_i+1) by n_j and matches D's
leading response. Neither assertion identifies a full finite-time CTMC law
with quantum evolution. Event/rate-table and detector/decoder costs remain paid.

Applying any fixed stochastic loss/detection channel and then T preserves
this O(t4) agreement by TV contraction. Uniform per-photon thinning may retain
all M sectors/vacuum; it need not be conditioned on detected photon number.
This proves a leading classical **null under losses**, not the same variance
formula after loss. At eta0 all counts vanish and T is exactly u for every t.
In fact M0 or M1 gives T=u for every pattern. Threshold-only observation is
different from true counts: a single hop becomes one hole and N-1 clicks;
every balanced S then has imbalance1. Hence this threshold version has no
order-t² decoded signal, unlike the ideal PNR/count formula above.

## Exact uniform decoder DP for every count vector

Let D[j,a,b] count subsets of the first j mode LABELS of sizea and photon
totalb. Set D[0,0,0]=1 and use

    D[j,a,b]=D[j-1,a,b]+D[j-1,a-1,b-n_j],

with out-of-range terms0. Each label is included/excluded once, so no
photon-factorial/binomial multiplier belongs in this subset DP. Let B be all
attainable b with D[N,K,b]>0 attaining the minimum |2b-M|, and
Z=sum_(b in B)D[N,K,b]. Choose b with probabilityD[N,K,b]/Z. Backward at
(j,a,b), include j with probabilityD[j-1,a-1,b-n_j]/D[j,a,b], otherwise
exclude it, using unbiased integer-rank sampling rather than float rounding.
Each path telescopes to1/D[N,K,b], hence every minimizing subset has
probability1/Z. Zeros/repeated counts, odd M and unattainable exact half are
handled without a favorable coin, selected tie or graph information.

For K=N/2 complementing gives equal counts at b and M-b; at most two optimal
totals exist. A fair coin between these totals is justified only by that
symmetry, whereas individual backward inclusion choices generally are NOT
fair coins. All-zero counts produce every K-subset uniformly. Law-level
relabel covariance follows from uniformity, not identical fixed-seed paths.

Time is O(N*K*M) integer additions, with O(N) bits per count; stored-backward
memory O(N*K*M) integer cells. This is pseudopolynomial in M for arbitrary
binary-encoded counts, not polynomial in logM. For a physical shot with at
mostN injected photons, M<=N makes it polynomial in the actual photon budget.
Exact decoder uniformity does not imply an optical sampling/optimization
advantage. No code or experiment is proposed/executed by this checkpoint.
