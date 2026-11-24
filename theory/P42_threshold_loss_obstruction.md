# P42 — an adaptive threshold-search obstruction from a lossy source spectrum

Root derivation2026-11-24, refined by the adaptive lane's independently
reconstructed rank cap. Candidate proof; exact independent audit and novelty
assessment pending. This is NOT a calibrated Lucy hardware verdict.

## Model and output event

The graph has m=2k vertices, k>=2. Each fresh attempt prepares one IDENTICAL
photon in N DISTINCT input modes, k<=N<=Nmax. There are M>=max(m,N) physical
modes. A passive unitary can depend arbitrarily on the graph and classical
history. Independent uniform photon survival eta commutes with that unitary.
There is no quantum memory, uncharged heralding, recycling or dark-count
replacement. All physical output modes are observed, or extra outputs are
explicitly required empty and their rejection charged.

A useful outcome clicks exactly k graph modes S, and no other mode. Every
positive occupation of those k modes is accepted: collisions and every
surviving photon number ell>=k are INCLUDED. This is threshold encoding, not
the stricter exactly-k-PNR encoding. The candidate is the clicked k-subset.
The model does not include completing a smaller observed support classically.

Only newly measured candidates are compared; classical candidates found by
the front end have their own credited cost. Equivalently, start both searches
from a common incumbent/front-end state and compare the incremental sampler.
Partial distinguishability requires a different argument and is not assumed.

## Spectral cap, no Haar hypothesis

Commuting loss to the input gives the UNNORMALIZED ell-photon block

    rho_ell = eta^ell (1-eta)^(N-ell) Pi_(A,ell),

where Pi_(A,ell) projects onto the binom(N,ell) orthonormal input Fock states
with ell single occupations chosen from the N source modes. Tracing the
environment kills cross terms between different lost subsets. Its nonzero
eigenvalue is w_N,ell=eta^ell(1-eta)^(N-ell). Passive ell-particle evolution
is unitary and preserves this spectrum, however U was selected.

At fixed ell the projector onto exactly clicked support S has rank
binom(ell-1,k-1), by positive compositions of ell into k modes. For two
projectors P,Q, Tr(PQ)<=min(rank P,rank Q): expand either trace in an
orthonormal basis and each projection expectation is in[0,1]. Therefore

    Pr(clicked support S) <= b_N,k(eta),
    b_N,k(eta) = sum_(ell=k)^N min(binom(N,ell),binom(ell-1,k-1))
                                 eta^ell (1-eta)^(N-ell).           (1)

All missing sectors are failures, not renormalized away. For N=k this is
eta^k. For strict PNR total=k, keep only ell=k and obtain the sharper cap
eta^k(1-eta)^(N-k). This cap is sharp per individual bitstring, attained by
a suitable permutation routing; the threshold cap need not be attainable.

Let b=max_N b_N,k over the explicitly allowed source sizes. Then(1) holds
conditionally at EVERY classical history, even for adaptive U and N. It
also holds for randomized controller choices by averaging. No optimum,
optimal mask or graph score is required to compute the bound.

## Exact finite-budget search consequence

Let D=binom(m,k). Uniform feasible classical sampling hits ANY fixed set A
of useful k-subsets with probability p=|A|/D. Every quantum attempt has
conditional hit probability <=|A|b. Write nQ for an upper bound on charged
fresh quantum attempts and nC>0 for a guaranteed number of classical draws.
Let L=ceil(nQ/nC), with L=0 if nQ=0. If

    L D b <= 1,                                               (2)

then the quantum failure probability is at least

    (1-p/L)^nQ >= (1-p/L)^(L nC) >= (1-p)^nC

when L>0, using Bernoulli's inequality. A zero-attempt quantum run is trivial.
Thus uniform feasible classical search has no smaller first-hit probability.
Taking A={S:cut_G(S)<=c} for every fixed c proves stochastic domination of
the final best cost, including all complement symmetries and graph labels.
The uniform reference rate is fixed rather than evaluated at divergent
histories: unlike a history-dependent phase-proposal substitution, there is
no hidden adaptive coupling assumption.

An equivalent all-budget condition can be given per blocks of at most L
quantum attempts. Extra quantum training costs only make its generous upper
bound less favorable. Fixed/guaranteed cost bounds can set
nQ=floor(B/cQ_lower), nC=floor(B/cC_upper). Mean latencies do not establish
these deterministic budgets. Attempts, nonempty vendor shots, photons and
score evaluations are distinct. One classical draw consumes one feasible
score; any smaller binding query cap must be reflected in nC. Equation(2),
not equal names for incompatible units, is the actual cost certificate.

## A uniform analytic low-loss regime

Dropping the minimum in(1), and for eta<1/2 extending the positive sum to
infinity, gives

    b_N,k <= (1-eta)^N [eta/(1-2eta)]^k
           <= [eta(1-eta)/(1-2eta)]^k,  N>=k.

The generating identity used is sum_(ell=k)^infinity binom(ell-1,k-1)r^ell
=(r/(1-r))^k for0<=r<1, obtained by multiplying k positive geometric series.
Since binom(2k,k)<=4^k, equal proposal budgets L=1 are certified whenever

    0<=eta<=(3-sqrt(5))/4 approximately0.190983.

This is a sufficient dimension-uniform range, not a sharp efficiency threshold.
Finite Nmax and exact rational arithmetic in(1)-(2) can strengthen it. PNR
total=k has the simpler sufficient eta<=1/4. These are source/detection model
statements, not an inference of the effective efficiency of any QPU account.

## Scope and contribution status

The source-mixture spectrum, projector trace bound and first-hit inequalities
are elementary/established ingredients. This note proposes their composition
as a gate for adaptive balanced threshold search, beyond P37's Haar feasibility.
No claim of globally new mathematics is made before exact-source comparison.

The result does not prohibit ideal high-transmission algorithms, non-Fock
resources, arbitrary postprocessing/decoders, access to lost-photon identities,
nonuniform/correlated loss, quantum memory, dark-count substitutions or coherent
feedforward. It does not turn a classical front end's discovery into a QPU
failure. It also does not justify asserting a wall-time advantage from a
single unmeasured device parameter or an internal ideal simulator benchmark.

The manuscript and all P33/P37/E05b raw evidence remain unchanged. Numerical
tables illustrate the exact finite certificate; they are not hardware data.
