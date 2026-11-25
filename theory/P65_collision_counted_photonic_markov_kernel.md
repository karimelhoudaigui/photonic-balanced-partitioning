# P65: collision-counted photonic proposals and a scoped obstruction

25-Nov-2026. STATIC mathematics, base9cc6ca2223922d0184348c0a394b4b8bfb8d13ad.
No code, import, numerical matrix, graph experiment, simulation or QPU call.
This is not a positive optimization result or a novelty claim.

The changed mechanism is a stateful search kernel, rather than preparing
independent ranked cuts: the current feasible partition is the next input.
Interference would have to improve useful transitions through a rugged cost
landscape. An identical equilibrium distribution is not evidence against or
for such a finite-time advantage. Quantum-assisted Metropolis is an existing
framework; the prospective passive-photonic specialization needs its own
evidence and strong classical controls.

## 1. Explicit source, circuit, decoder and objective

Let G have N even vertices, symmetric zero-diagonal nonnegative weights A,
K=N/2, and
Omega={S subset [N]: |S|=K}. Keep oriented subsets for the chain; S and its
complement have the same graph-cut cost C(S), but are not silently identified
in transition probabilities. Preparing the CURRENT S is permitted common
state input, not preparation of a known optimum counted as an improvement.

Inject the normalized Fock state |1_S>, one photon at each selected vertex.
With a fixed input source pattern, a paid input permutation can route it to
S. Define a graph-dependent real symmetric single-particle matrix, for example

    H_G(lambda) = (A + lambda*(J-I)) / D,
    D = max(1, max_i degree_A(i) + lambda*(N-1)), lambda>=0.

One prospective global interferometer is its Cayley transform

    U_G(t,lambda)=(I+i*t*H_G)*(I-i*t*H_G)^(-1), t real.       (1)

For real rational graph weights/t/lambda, its entries are in Q(i). This gives
an exact small-case matrix route without floating matrix exponentiation.
H is real symmetric, so (1) is unitary AND U=U^T. The inverse exists since
the eigenvalues of I-i*t*H are nonzero. The transform commutes with vertex
permutations: relabeling A conjugates U, preserving logical transition laws.
No selected vertex labeling, known partition or C* enters (1).

This is a global graph-dependent proposal. It does not retain P63's six
commuting color totals or its three-F6 conditional width. A passive mesh can
in principle implement a unitary matrix; its compilation, depth, calibration,
precision and actual accessible QPU capabilities remain unverified and paid.
The Cayley transform by itself is not a cut-energy oracle or a new advantage.

For each physical attempt, measure ALL output counts. If they are lossless
and collision-free, the K occupied outputs define T in Omega. Otherwise the
attempt is an explicit self-loop at S. It consumes the shot and photons; no
repeat-until-valid normalization is used. On a valid T accept with

    a_beta(S,T)=min(1, exp(-beta*(C(T)-C(S)))).               (2)

Every evaluated candidate, including accepted training proposals, contributes
to the paid incumbent. A future training rule can use observed improvements
and costs, never an optimal-state mask or C*. Parameters must be frozen for
each production chain, or drawn independently of its current state from one
fixed distribution: adapting t/lambda to S generally destroys symmetry of
the combined proposal. A fixed-beta theorem is separate from a time-varying
annealing schedule used for optimization.

## 2. Exact kernel and detailed balance, including rejected collisions

For distinct S,T in Omega define

    F_B(S,T)=|per(U[T,S])|^2,
    F_D(S,T)=per(|U[T,S]|^2).                              (3)

These are UNCONDITIONAL collision-free output probabilities. Input and
output Fock factorials are one here; the full count law still has bunched
outputs with their correct factorials. The distinguishable case uses the
same input ports and optical matrix, with independent labeled photons.

Because U=U^T, F_B and F_D are symmetric. Let

    Q_X(S,T)=F_X(S,T) for T!=S,
    Q_X(S,S)=1-sum_(T!=S) F_X(S,T).                       (4)

Unitarity/stochasticity of the full physical law makes each diagonal
nonnegative. It includes both a measured S and every collided result.
Thus Q_X is a symmetric stochastic matrix. Multiplying its off-diagonals
by (2) and putting the remaining mass on the diagonal gives P_X with

    pi_beta(S) P_X(S,T) = pi_beta(T) P_X(T,S),
    pi_beta(S) proportional to exp(-beta*C(S)).           (5)

Equation(5) follows directly: each side is the common symmetric Q_X(S,T)
times min(exp(-beta*C(S)),exp(-beta*C(T))) divided by Z.
No quantum proposal probability needs to be evaluated during actual search.
All stationary energy means are therefore identical for B and D. The open
mechanism is their finite-time transport, not a different Gibbs optimum.
Irreducibility and aperiodicity are extra hypotheses. A common classical
uniform-feasible mixture can supply them, with its RNG, scoring and actual
physical-call count explicitly included. A common half-lazy version is
convenient for spectral analysis; artificial classical self-loops must not
be billed as QPU attempts or converted into a timing advantage.

If p_CF(S)>0 for all states and one instead repeats physical draws until
collision-free and forgets the
state-dependent normalization p_CF(S), then Q_cond(S,T)=F(S,T)/p_CF(S).
Using (2) without a proposal-ratio correction has stationary measure

    pi_wrong(S) proportional to exp(-beta*C(S))*p_CF(S),

when that chain is irreducible. The proper Hastings ratio contains
p_CF(S)/p_CF(T). Collision self-loops avoid this bias and pay the raw cost.

Under common uniform per-photon transmission eta and no other noise, every
off-diagonal is scaled by eta^K; losses also become self-loops. Therefore

    P_eta=(1-eta^K)*I+eta^K*P_ideal.                       (6)

The Poincare gap, and the gap of a common lazy version, scale by eta^K.
Nonuniform loss or state-dependent routing can spoil symmetry and requires
a separately justified transfer model or Hastings correction. No hardware
symmetry is inferred from the ideal construction.

## 3. A real interference effect, and its immediate classical falsifier

There is no leading weak-angle B advantage in this feasible kernel. For the
Cayley family, U(t)=I+2*i*t*H+O(t^2). If T replaces just occupied i by empty j,
the unique leading permanent path gives BOTH B and D probability
4*t^2*H_ji^2+O(t^4). Two or more replacements cost at least O(t^4).
Real H implies U(-t)=conjugate(U(t)), so the probabilities are even and
there is no cubic term. The diagonal of(4) is fixed by the off-diagonals;
thus the complete collision-rejected kernels agree through order t^2.
This is a direct finite-dimensional expansion, not a claim that their
unconditional collision probabilities agree. A proposed benefit must
therefore survive a finite-angle, higher-order comparison and retimed D.

Take only four active modes, with

    H=[[0,J2],[J2,0]], U=exp(i*t*H),
    U_cross=i*sin(2t)*J2/2.

This also arises from the Cayley form with sin(2t) replaced by
4s/(1+4s^2); s=1/2 gives the same full-transfer-bright-mode point. For two
photons initially in active modes1,2, a collision-free double replacement
to3,4 has RAW probabilities

    F_B(12,34)=sin(2t)^4/4,
    F_D(12,34)=sin(2t)^4/8.                              (7)

Both permutations have the same amplitude, so they add coherently in B
and as squared magnitudes in D. Even independently optimizing t within
this ONE Hamiltonian gives maxima1/4 versus1/8. At t=pi/4 the B mixed
one-replacement outputs vanish; F_B(12,12)=F_B(12,34)=1/4 and collision
mass1/2 is retained as self-loops. D has six CF outcomes of mass1/8 and
collision mass1/4. These statements follow from the displayed 4x4 blocks;
no graph or experiment was generated.

Embed this in N8/K4 with two unchanged spectator photons. An analytical
barrier illustration uses heavy edges12,34,56,78 of weight M and light
edges17,28,35,46 of weight h, M>h>0. At S={1,2,5,6}, C=4h; at
T={3,4,5,6}, C=0. All one-replacements increase cost by at least2(M-h).
For replacements restricted to active modes1..4 the four intermediate cuts
cost2M+2h. This example is deliberately constructed and its two connected
components reveal the optimum immediately. It is NOT an optimizer benchmark.

A classical two-replacement proposal can jump from S to T directly with
probability one when given this same active quartet. An unrestricted D
permutation can also implement that transition. Hence (7) is only a
mechanism/normalization fixture, already defeated by the strongest obvious
control. It cannot establish an optimization benefit or novelty. Only a
global kernel surviving actual independently optimized D AND correlated
classical replacements would be worth pursuing.

## 4. Two universal, limited comparisons

First, Cauchy--Schwarz over K! permutations in a permanent gives, entrywise,

    F_B(S,T) <= K! F_D(S,T).                              (8)

At a COMMON U and beta, their Dirichlet forms obey E_B(f,f)<=K!E_D(f,f).
Taking f to be a minimizing nonconstant test function for D gives the
Poincare-gap bound gap_B<=K!*gap_D; the same holds for common half-lazy
versions. This is neither a useful constant bound at growing K nor a
matched-cost comparison or optimization advantage. Independent reoptimization
of D can only strengthen an adverse comparison.

Second, a uniformly high-CF limit has a monomial replacement. The proof
below independently reconstructs ROOT's suggested estimate and strengthens
its sufficient collision hypothesis to a uniform INPUT average. The estimate
is deliberately loose; small absolute error does not control relative gaps.

**Proposition.** Fix an N-mode unitary U and 2<=K<=N. Let p_col(S) be the
probability of any collision from |1_S>. Suppose

    average_(S in Omega) p_col(S) <= epsilon.             (9)

Then a phase-adjusted permutation V exists with

    ||U-V||_F^2 <= N*(N-1)*epsilon.                       (10)

For every K-photon input state, its complete measured output distributions
under U and V have TV at most

    delta=min(1, K*sqrt(N*(N-1)*epsilon)).                (11)

If U=U^T, the equal mixture of V and V^T gives a SYMMETRIC classical
permutation proposal with the same bound after collision rejection and the
same classical Metropolis step. This is an existence/accuracy result; all
matrix construction, permutation finding and per-step costs remain paid.

**Proof of (10), without an external decomposition lemma.** Write q_ai=|U_ai|^2,
a doubly stochastic matrix. The expected number Z of unordered output photon
pairs in one mode for input S is

    E[Z|S]=2*sum_(i<j in S,a) q_ai*q_aj.

This follows by expanding a_out^dagger^2 a_out^2 in the input Fock state;
the two source labels have two creation and two annihilation orders. Also
0<=Z<=binom(K,2)*1_collision. Averaging over ALL K-subsets and using each
row sum of q equals one gives

    average E[Z|S] = K*(K-1)/(N*(N-1)) * (N-||q||_F^2).

Combining this with (9) yields

    N-||q||_F^2 <= N*(N-1)*epsilon/2.                     (12)

For completeness, any doubly stochastic matrix is a convex combination of
permutation matrices. To see existence of a positive-support perfect
matching, take a maximum matching. From an unmatched row follow alternating
positive edges. If an unmatched column is reached, augment the matching.
Otherwise the reachable columns C are matched bijectively to reachable rows
R except the initial unmatched row. All positive edges out of R end in C,
so |R|=sum_(i in R,j in C)q_ij<=|C|, contradicting |R|=|C|+1. A perfect
matching therefore exists. Subtract the minimum positive entry along it.
Unless that entry is one, divide the residual by one minus that entry to
obtain another doubly stochastic matrix with strictly fewer positive entries.
Repeat; finitely many entries can disappear. Expanding the recursion gives
the claimed convex combination, with no computational speed assertion.

Writing q=sum_l w_l P_l therefore implies some permutation P satisfies
<q,P>>=||q||_F^2. Choose V on P's support with the phases of U. Then

    ||U-V||_F^2=2*N-2*sum_(P support) sqrt(q_ai)
               <=2*(N-<q,P>)<=N*(N-1)*epsilon,

because sqrt(q_ai)>=q_ai for entries in[0,1]. This proves (10).

**Lift and classical chain.** On the K-particle tensor product, a telescoping
sum bounds ||U^tensorK-V^tensorK||_op<=K*||U-V||_op. Restricting to the
symmetric subspace cannot increase the norm. Pure-state trace distance is
at most the norm of the state difference; measurements and shared classical
processing contract TV. This proves (11), including all collided outcomes.

For symmetric U, ||U-V^T||_F=||U-V||_F. Thus mixing V and V^T preserves
(11). Their phases do not affect Fock count measurements: one proposal
permutes S by sigma, the other by sigma^-1, with equal probabilities. This
mixture is symmetric even when the selected permutation is not an involution.
The shared Metropolis rule then preserves (5). No permanent is evaluated
to sample this particular classical replacement.

For T fresh, classically controlled attempts, couple kernels at each matching
history. If the SAME bound (9) holds for every U_t chosen at every such
history, a union bound gives full trajectory TV<=min(1,T*delta). The same
bound holds for a paid-best threshold event and bounds the difference of
expected best cuts by total graph weight times that TV. The classical
replacement must reconstruct each selected permutation at its actual paid
boundary. There is no equal-wall-time theorem or numerical implementation
of that construction here.

Hypothesis (9) concerns the uniform average over ALL input subsets, not an
average over visited states, a selected start, measured CF shots or favorable
graphs. A condition p_col(S)<=epsilon for every S is sufficient but stronger.
The bound is nontrivial only when epsilon<1/(K^2*N*(N-1)); it does not veto
moderate collision probability. Its absolute trajectory bound does not
exclude an exponentially large relative improvement of a tiny spectral gap.
K=1 is excluded from the inference (12). No general passive-optimization
impossibility, asymptotic algorithmic advantage, novelty or hardware claim
follows. The elementary matching/convexity/tensor ingredients are known;
their presentation here supplies an autonomous proof, not priority.

## 5. Fresh graph-blind embeddings collapse to classical move-size mixtures

There is another exact structural falsifier, with different hypotheses from
(9). Let a physical source occupy one fixed K-subset S0. Conditional on
the current logical state S, draw a fresh uniform bijection Pi mapping S0
onto S and its complement onto S^c. Suppose the physical interferometer is
chosen BEFORE this embedding and receives no embedding-dependent graph
information. It can be globally coupled, and its parameters may depend on
G/history before Pi is drawn. Discarded collisions remain self-loops.

For each CF physical output T0 define r=|T0 minus S0|. Conditional on T0,
the logical Pi(T0) is a uniform r-replacement of S: its intersection with
S and its part in S^c are independent uniform subsets of their prescribed
sizes. The number of candidates is binom(K,r)*binom(N-K,r). Hence the
averaged physical proposal is exactly

    Q = rho_0*I + sum_(r=1..K) rho_r*R_r,

where R_r is the classical uniform r-replacement kernel and rho_0 also
contains all collision mass. All complicated interference enters only the
K+1 move-size probabilities. This identity follows by counting uniform
bijections, not by simulating the whole quantum count law.

A classical sampler given these same rho values reproduces the complete
logical chain by drawing r and the two subsets. Acquiring/learning rho,
constructing its CDF and scoring are NOT free. This is a kernel-family
containment, not a supplied equal-cost sampler or an oracle for optimal
mixture weights. Strong independently optimized classical move-size
mixtures are therefore mandatory adverse controls. A carried relabeling of
a graph-aligned U_G is different: it changes the physical U with Pi, so
the graph-blind hypothesis fails. Candidate(1) deliberately keeps that
global graph dependence and does not obtain a benefit from random labels.

## 6. Precise next discriminating question

For rational Cayley kernels (1), can an optimum-blind fixed-parameter policy
produce a finite-time, total-cost improvement over independently reoptimized
D, two-species controls, uniform/geometric multi-replacement Metropolis,
edge-guided multi-replacement search, parallel tempering and FAST? The
first small exact exercise would separate kernel transport from CF-rate
bias, random mapping, tiny-angle retiming and free input preparation. A
small gap or barrier-crossing advantage alone remains a diagnostic.

An exact N8/K4 kernel has70 rows/columns and rational CF probabilities,
including all4900 entries and row collision deficits. No such matrix has
been computed. It would qualify formulas and expose cheap replacement
kernels; it cannot establish a hard optimization benchmark because all70
feasible cuts are trivial to enumerate. New graphs, seeds, parameter grids,
raw-cost gates, execution caps and replication conditions must be frozen
in a separate reviewed card before any computation. No execution is
authorized by this note. The positive research objective remains OPEN.
