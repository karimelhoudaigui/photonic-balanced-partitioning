# P42 — general Fock sources and unknown internal distinguishability

Root derivation; independent physics reconstruction PENDING. This extends the
source spectrum calculation, not a claim that partial distinguishability can
only reduce useful probabilities. A known counterexample forbids that shortcut.

Let the input have FIXED spatial mode occupations s_i with N=sum s_i and
arbitrary physically admissible internal states. Independent uniform loss,
with no which-loss herald used to select the current U, leaves spatial input
occupation t<=s with probability

    lambda_t = a_t eta^r(1-eta)^(N-r),
    a_t=prod_i binom(s_i,t_i), r=sum t_i.

Environment mode occupation s-t makes different t blocks incoherent. For
identical photons the conditional r-particle spatial block at t is the rank-one
Fock projector. In the presence of arbitrary internal states, trace the internal
degrees of freedom in first quantization. The normalized conditional spatial
density sigma_t is supported on the span of ordered mode tuples with occupation
t. Different t supports are orthogonal, and sigma_t<=Pi_t. Passive U evolves
the spatial density by U tensor ... tensor U, preserving orthogonality of these
support spaces. Permutation symmetry is not assumed to make sigma_t pure.

For an output projector P of finite rank R, let x_t=Tr(P sigma_t). Then

    0<=x_t<=1, sum_t x_t<=sum_t Tr(P Pi_t)<=R.

Consequently sum_t lambda_t x_t is bounded by the sum of the R largest
lambda_t, or by their total if there are fewer than R. This is a block-trace
version of the elementary Ky Fan bound, without an internal Gram estimate.

For a fixed clicked support S of size k, the required rank in each r sector is:

- identical photons: R=binom(r-1,k-1), positive Fock compositions;
- arbitrary internal states: R=k! Stirling2(r,k), ordered surjections onto S;
- PNR total=k: R=1 or R=k!, respectively.

Thus sum the largest corresponding numbers of coefficients a_t at every
r>=k, multiplied by eta^r(1-eta)^(N-r). This gives the cap b_s,k. Maximize
over ALL admissible source patterns when the controller chooses the source.
The cap is not assumed monotone in N. The budget condition L binom(2k,k)b<=1
then has exactly the same fixed-target adaptive best-cost consequence as the
root threshold theorem, under the same frontend/primitive-cost assumptions.

All products (s_i+1)<=2^N, so for N<=12 every loss remainder, eigenvalue
coefficient, threshold rank and source partition can be enumerated exactly
with small memory. Permutations of source modes do not change this spectrum;
integer partitions of N suffice for source spectra, not for graph instances.

## Two scope falsifiers to retain

For s=(4,0,0,0), eta=1/10 and a balanced splitter into two modes, the
two-click probability is1-2(19/20)^4+(9/10)^4=2167/80000. This exceeds the
single-input source cap1/100. The general bunched-source cap instead equals
the binomial probability of at least two survivors and remains valid.

For eight SINGLE input photons in DFT6 plus two deterministic spectators,
split the six active internal states into two orthogonal species of three.
The specified two active output rows have signs +++--- in their second row.
Summing probabilities of two active survivors gives6*(1/9)+9*(1/18)=7/6,
whereas the identical-input sector claim would cap that sum by1. With the
two spectators, the target is a four-click support. This refutes applying the
identical-photon spectrum bound to arbitrary internal states. The ordered
rank cap deliberately avoids this inference.

No conclusion is drawn for input superpositions across different occupations,
herald-conditioned preparation, nonuniform/path-dependent loss, recycling,
unobserved physical outputs or quantum memory. No actual QPU parameter is
certified by a Fraction calculation.
