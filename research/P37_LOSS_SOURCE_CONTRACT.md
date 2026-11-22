# P37: loss-aware source selection for the Haar threshold baseline

Checkpointb5a1eba,2026-11-22. Continuation of the exact P32 resource audit.
No manuscript, noisy optimizer campaign or QPU. This compares optical source
protocols for feasibility, not graph optimization or a quantum advantage.

Fix even m>=8,k=m/2, distinct single-photon inputs with k<=N<=m, independent
uniform survival eta in (0,1), and threshold acceptance of exactly k clicks.
All attempts, including total loss, remain in the denominator. Choose N
independently of the Haar interferometer. The known lossless Haar mean is
h(L)=C(m,k)C(L-1,k-1)/C(m+L-1,L), zero below k. The lossy mean is
S_N=E[h(L)], L~Bin(N,eta). Compare S_N and S_N/N separately. Interpreting
N/S_N as an expected waiting photon cost requires independently refreshed
Haar draws per attempt; it is not E_U[N/p_U] on a fixed random device.

Proposed finite theorem to audit: for any such eta, per-attempt maxima lie
in {m-1,m}, separated by one critical eta. Per-photon maxima lie in
{m-3,m-2,m-1,m}, with three strictly ordered transitions. Their root
characterizations use exact binomial differences and the single sign change
of h(L+1)-h(L), or h(L+1)/(L+1)-h(L)/L. Endpoint eta=1 retains the known
lossless optima; eta=0 has no successes and no finite waiting cost.

Candidate boundary asymptotic, requiring its own derivation: at
eta=1-lambda/m with fixed lambda, the per-attempt last-source transition
has m*(1-eta_critical)->1. The three per-photon transitions have limits1,2,3.
No fixed-loss exponential-rate or general noisy-complexity claim is part of
this first finite phase-diagram experiment.

Validation: exact Fraction arithmetic, no Monte Carlo. All integer source
choices k..m at m8/10/12/16/24/32/48/64 and fixed eta1/4,1/2,3/4,9/10,99/100,1,
plus eta=1-lambda/m at lambda1/4,3/4,5/4,7/4,9/4,11/4,13/4,15/4.
Compute the known independent coefficient formula as a crosscheck. Locate
critical roots by40 exact bisections, retaining sign brackets, not claiming
algebraic closed forms. Use additional m128 only for transition convergence;
no full Fock law is simulated at these sizes. All grid cases retained.

Falsifier: a maximizer lies outside the candidate sets, the prescribed phase
ordering fails, the exact positive sums disagree, or a sign bracket is invalid.
Preserve failures. One CPU thread,120-second run cap, no model download.
Proof and finite validation are separate. Novelty remains unassessed until
exact source comparison; known Haar counting or elementary sign arguments
are not advertised as discoveries.
