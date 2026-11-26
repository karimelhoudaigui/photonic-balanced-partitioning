# P89: source-label blindness, uniform removals and the raw cut mean

**Primary verdict: the proposed factorisation and mean identity are
proved under the fresh uniform-mark assumptions below.** Current P82a
cannot steer which labeled source vertices are removed, even after
conditioning on the repaired receiving subset and its size. This is
not a no-go for the quench, its full adaptive optimizer or interference
advantages in another architecture.

ROOT supplied the candidate and formulas before this independent static
reconstruction. No other P89 source or verdict was read. This is not
independent discovery or novelty certification. No outcomes, generated
DEV graphs, seed values or experiment records were inspected. Every
example below is hand algebra, not a simulation or an algorithm change.

## 1. Exact source boundary and probabilistic premise

The inspected implementation is `research/P82a_split_scatter_veto.py`
at `94f80b94f75317524c202ce9ef5bf932d78ddc5e`, SHA256
`7e1a0d037f5fe0a6af036c1b2a92e765981c93e8d473535984e6f07ea7acfbbc`.
The current file and committed blob match. The relevant full compiler,
mark/split ordering, receiver, decoding and dependency methods were
inspected, along with the complete source previously audited at
`892ea965` and the full intervening source diff. The P82 design hash is
unchanged: `c008f60143a1c4b0e81dcec1ba7a07c28d89244b10d4d69695070d27b0916723`.

Fix a current partition S,T of a 2K-vertex weighted undirected graph,
with `|S|=|T|=K`, `K>=2`. P82 uses K photons, not K logical qubits.
Write `sigma:{0,...,K-1}->S` for the source port ordering. Assume it is
uniform and independent of every other fresh mark: target ordering,
initial phases, portwise split coins, native randomness and repair.
This is a statement about the ideal proposal's random-mark law. It is
not a theorem that a fixed deterministic PCG/hash seed realizes exact
independence, or that a finite pilot estimates this law without error.

Let P be the subset of removed **port indices**, `r=|P|`. Its distribution
may be nonuniform across same-size port subsets, as with eta>0. What
matters is that it does not depend on sigma. The labeled removal set is
`R=sigma(P)`. Given P and other marks, the receiving count law and its
graph-blind repair produce a labeled r-subset `Y subset T` without
reading sigma. The proposal is `X=(S\R) union Y`.

The actual compiler reads `source_order` only through its length.
Its graph accesses use target_order vertices only, so its circuit
depends on `G[T]`, target marks, initial phase marks and fixed profile,
not on `G[S]`, cross edges or source labels. Split coins use a port
profile, and the conditional native source is P, not sigma(P). The
received/repaired Y ignores kept-bank labels. These are exact code
dependencies; no sampling or numerical approximation establishes them.

Conditioning on a realized sigma, an acceptance event, a resource-stop
selection, or the completed-only subset of failed attempts is not the
averaging used here. An ideal lossless raw proposal with the declared
fresh marks is the object under study.

## 2. Factorisation proof and exact removal obstruction

Condition on all other randomness, including P, target marks, native
counts and repair. This fixes Y and r but leaves sigma uniform. For
any fixed r-subset `R0 subset S`, exactly `r!(K-r)!` of the K! source
orderings map P onto R0. Therefore

    Pr(R=R0 | all other marks) = 1/binom(K,r).

Averaging the other marks at fixed r proves

    Pr(R=R0,Y=Y0 | G,S,r)
       = mu_(G[T],r)(Y0)/binom(K,r).                       (1)

The law mu includes every port-removal weight, quantum receiving
occupation, collision, repair and target/phase mark. It need not be
uniform for eta>0 and is not asserted efficiently classically samplable.
No assumption on the order or complexity of bosonic interference is
used in the permutation argument.

In particular, for any Y-dependent prescribed desirable removal set
`R0(Y,G,S)` of size r,

    Pr(R=R0(Y,G,S) | Y,G,S,r)=1/binom(K,r).

For any family A(Y) of desirable r-subsets the probability is exactly
`|A(Y)|/binom(K,r)`. Thus a unique desired removal cannot be enriched
above uniform, even conditional on the received subset. At K8,r4 the
unique-set value is 1/70; this is **not** a bound of 1/70 on optimization
success, since many removal sets may be good and a quench can change X.
Unconditionally a fixed R0 has mass `Pr(r)/binom(K,r)`. The r law is
fixed by the portwise splitter probabilities, not by graph labels.

## 3. Exact raw quadratic cut mean

Use unordered internal edge sums `W(S)=sum_(i<j in S) w_ij` and
`Wcross=sum_(i in S,j in T) w_ij`. Put `d_S(j)=sum_(i in S)w_ij` and
`p_j=Pr_mu(j in Y)`. We allow real symmetric weights for this identity;
the implemented nonnegative integer graphs are a subclass.

For an internal S edge, uniform R separates its endpoints with probability

    a_r=2r(K-r)/[K(K-1)].

For a cross edge i,j, condition on Y. Independence in (1) gives its
crossing probability

    (1-r/K)(1-1_(j in Y))+(r/K)1_(j in Y).

Adding all edge classes yields exactly

    E[C_G(X) | G,S,r]
      = a_r W(S)+(1-r/K)Wcross
        + E_mu[cut_(G[T])(Y)]
        +(2r/K-1) sum_(j in T) d_S(j) p_j.                (2)

Here `cut_(G[T])(Y)` cuts Y against `T\Y`, not against the full graph.
At r=K/2, for even K,

    E[C_G(X)|r]
      = K/[2(K-1)] W(S)+Wcross/2
        +E_mu[cut_(G[T])(Y)].                            (3)

The explicit cross-edge contribution is constant with respect to the
receiver law. Only the receiving induced-subgraph term can change this
raw half-replacement mean. At r0 and rK, (2) returns Wcross, as required
by X=S and X=T. No approximate moment or postselection denominator is
used. A common complement canonicalization preserves the raw cut, so
it does not change the mean identity.

## 4. Which assumptions can fail in a changed compiler?

**Source-label dependence can create removal/receiver correlations.**
For a simple passive counterexample let f be a fixed bijection S->T
and let a changed compiler route input port j to the output labeled
`f(sigma(j))`. It is a permutation unitary, defined before P is observed.
Then collision-free Y equals f(R) exactly. At `0<r<K`, R is still
marginally uniform, but R and Y are perfectly coupled rather than
independent. This changes the fixed flat family and is not a result
about the current code. It shows why sigma-blindness is substantive.

A counterexample also exists **within the flat K4 receiver family**.
Let its phases be `(1,z)` with z=+1 or -1, and keep the P82 d2 odds
`(a,b,a,b)=(1/2,3/2,1/2,3/2)`. Fix one labeled source s*. Its source
port j* is uniform among four. For one prespecified target ordering,
set z=+1 if `j* in {0,2}` and z=-1 otherwise, before any split.
For every other target ordering set z=+1 independently of sigma.
This branch is fixed by marks, not chosen after any outcome.

For the one marked ordering let Y0 be its two labeled plus ports and
write `q0=product_i(1-p_i)=16/225`. Its collision-free probability for
input pair P is `(1+cos phi)/8` for P=02,13; `(1-cos phi)/8` for
P=03,12; and zero for P=01,23. Repair from bunches contributes 1/12
to Y0 for every P and either phase, so contributes no covariance.
Weighting the port pairs by `q0 o_i o_j` and averaging j* gives

    Pr(Y0,r2)_CF=q0/2,
    Pr(s* in R,Y0,r2)_CF=q0/8.

The covariance relative to `Pr(s* in R|r2)=1/2` is therefore `-q0/8`
on that ordering. Under a uniform target permutation it occurs with
probability 1/24; all other branches are sigma-blind and have zero
such covariance. Hence the full raw covariance is `-q0/192=-1/2700`,
not zero. This verifies failure of (1) after target marks as well.
It is a hand-calculable changed law, not a positive optimizer result.
In particular fixed-input flat r2 repaired one-vertex marginals remain
1/2; this example does not by itself improve the cross-edge mean.

**Cross-edge access alone does not break the factorisation.** If the
receiver compiler reads Gcross but still ignores sigma, the same proof
gives R independent of Y and uniformly distributed at fixed r. Only
the restriction `mu=mu_(G[T],r)` fails: mu may now depend on the whole
graph. For example keep the same K4 nonuniform profile and select
phases 0 or pi by a cross-edge bit, using a fixed graph on T. The
known exact raw r2 receiving one-edge mean differs by `-8/225`, so
the two receiving laws differ although G[T] is unchanged. This is
source-blind but cross-informed. Formula (2), including (3), still
holds; a changed receiver alone does not restore source steering.

Allowing the splitter profile itself to depend on sigma/source features
can instead break even marginal uniform removal. That is a different,
explicitly graph-dependent classical source-selection mechanism and
must be charged and exposed to controls, not declared an interference
benefit.

## 5. Quench, trajectory and scientific limits

The exact one-step formula determines only the raw quadratic mean.
The receiving term uses its first and second inclusion moments, but
their efficient computation is not proved; graph-blind collision repair
can retain higher-count structure. No classical full-law algorithm,
runtime advantage, hardness claim or optimum certificate follows.

The graph-dependent quench maps X to a nonlinear function of its entire
subset. Its value, every scored neighbor, the incumbent update and
future current states need not obey (2). Acceptance or conditioning on
a good cost can also make removed labels nonuniform. Even while (1)
holds anew at each history with fresh independent marks, the controller
can learn/select graph-dependent basins over time. Neither a global
optimizer no-go nor a whole-trajectory performance inequality is proved.

The current code's source-label blindness is therefore a precise design
limitation, with a concrete family of ways to break it. Those examples
do not alter or authorize the frozen pilot. Full-cost controls, fresh
seeds/held-outs, independent replication and hardware validation remain
necessary for any positive claim. The positive research objective stays
open. No existing negative or validated result is changed.

Only file/instruction reads, hashes, source diff and isolated document/Git
operations accompany this proof. No import, AST, test, RNG/seed evaluation,
generated graph, numerical matrix/probability computation, backend,
experiment outcome, QPU or manuscript was used. Final hand proofreading
checked label versus port variables, conditional r, source/receiver
independence, edge counting, both endpoint cases, half replacement and
the changed-compiler counterexamples.
