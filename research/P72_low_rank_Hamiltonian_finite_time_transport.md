# P72: finite-time transport from low-rank Hamiltonian coupling

25-Nov-2026. STATIC independent derivation from the coordinator's proposed
claim, after the P71 source was frozen. No scientific code, import, matrix
computation, numerical approximation, random draw, test, calibration, new
data, native call, QPU operation or manuscript edit. The worktree's unavailable
Git index is not retried.

**Verdict: proved as written below, ready for independent review.** A single
Hermitian propagator with low-rank inter-block Hamiltonian coupling has a
controlled approximate optical cross rank. This supplies a finite raw-event
bound even when its exact optical cross rank is full. The exponential
consequence requires the stated norm-time and coupling-rank regime; it is
not an arbitrary-time, all-graphs or positive-optimizer result.

Pinned mathematical dependencies:

- P69 `research/P69_low_rank_transport_obstruction.md`, SHA256
  `37e59633734c16277ed2649c4761fa84a86a8006b164fd4263963e37d7759de4`;
- P71 `research/P71_approximate_cross_rank_transport.md`, SHA256
  `c320f925b53f68738931da93ef28bb0a2f84f887988404153f974dae8b6cfe03`.

The polynomial rank, Taylor remainder and singular-value approximation
lemmas are proved here. P71 provides its proved unitary CS truncation and
K-photon trace/TV bound, not an assumption that the Taylor polynomial is
physically unitary. No external theorem or attribution claim is used.

## 1. Finite model and statement

Fix logical blocks CA,CB, each of size d=2L, L>=2. The source is the
normalized CF state with L distinct occupied modes per block, K=2L photons
in total. The two good output events are full CF occupation of CA, or CB,
as in P69. Use one Hamiltonian during one coherent propagation:

    H=[X Z; Z^dagger Y],   H=H^dagger,
    rank(Z)<=h,           tau=|t|*||H||op,
    U=exp(i*t*H),         t real.

Here h is an integer coupling-rank bound, distinct from the P66 graph's
matching edge-weight symbol. In the present note h always means coupling
rank, 0<=h<=d. The within-block X,Y may depend arbitrarily on the graph,
current subset, labels and marked past data, but the chosen H is fixed
DURING this single propagator.

For an integer p>=0 define

    Q_p(H)=sum_{k=0}^p (itH)^k/k!,
    E_p(tau)=exp(tau)*tau^(p+1)/(p+1)!.

For h>=1 and q=p*h<d, the optical cross singular value satisfies

    s_(q+1)(U_CA,CB)<=min(1,E_p(tau)).

Consequently the raw bosonic good-event probability obeys

    P_U(good)<=min(1,p_Lq+sqrt(2)*K*E_p(tau)),

where p_Lq is the exact P69 bound and p_L0=0. A slightly sharper expression
replaces sqrt(2)*E_p by delta(min(1,E_p)), with delta from P71. For q>=d
only the trivial bound one is asserted by this choice of p.

If h=0, H is block-local, U is block-local and the good event is impossible
from the L/L source. If t=0, U=I and the good event is also impossible.
These exact cases are stated separately rather than inferred from a
potentially vacuous approximation. For p=0, Q_0=I and q=0; the finite bound
still holds with E_0=exp(tau)*tau. No positivity of t or invertibility of
X,Y is assumed.

## 2. A common Krylov range, not a sum of unrelated rank estimates

Write R_k=(H^k)_CA,CB. Since H^0=I, R_0=0. Block multiplication gives

    R_(k+1)=X*R_k+Z*(H^k)_CB,CB.

Let

    K_p=span{X^a*v : v in range(Z), 0<=a<=p-1},  p>=1,
    K_0={0}.

Induction proves range(R_k) subset K_k. The base k=0 holds. For the
inductive step, X*range(R_k) lies in span of powers 1 through k of X
applied to range(Z); the second summand lies in range(Z) itself. Their
sum is therefore in K_(k+1).

The spaces K_k are nested, so EVERY term in the off-diagonal block of
Q_p has range inside the SAME K_p. It follows that

    rank((Q_p)_CA,CB)<=dim(K_p)<=min(d,p*h).

Bounding each power separately and then summing their rank bounds would
give an unnecessary quadratic factor in p. The common-range induction is
the reason the linear p*h estimate is valid. No covariance, regularity,
fixed dark subspace or unmarked controller was used.

## 3. Operator Taylor remainder

Finite-dimensional Hermitian spectral decomposition makes U unitary and
ensures convergence of the operator exponential series. Submultiplicativity
of the operator norm gives

    ||U-Q_p||op<=sum_{k=p+1}^infinity tau^k/k!.

For m=p+1 and j>=0, (m+j)!>=m!*j!, so

    sum_{k=p+1}^infinity tau^k/k!
       <=tau^m/m!*sum_{j=0}^infinity tau^j/j!
       =E_p(tau).

This includes tau=0, where the remainder is exactly zero. Compression to
the fixed input/output blocks cannot increase operator norm, hence

    ||U_CA,CB-(Q_p)_CA,CB||op<=E_p(tau).

The polynomial need not be unitary, stochastic or a physical optical map.
It is used ONLY as a low-rank linear approximation for this inequality.

## 4. Singular-value lemma, proved by a dimension argument

Let M be any d by d matrix and R have rank at most q<d. Let W be the span
of the top q+1 right singular vectors of M. These vectors can be obtained
by diagonalizing the positive Hermitian M-dagger M; no singular-value
approximation theorem is being assumed. Then dim(W)=q+1, while

dim ker(R)>=d-q, so W intersects ker(R) nontrivially. Choose a unit vector
v in that intersection. Expanding it in those right singular vectors gives

    ||Mv||>=s_(q+1)(M),
    Rv=0, so ||Mv||=||(M-R)v||<=||M-R||op.

Thus s_(q+1)(M)<=||M-R||op. Apply this with M=U_CA,CB and
R=(Q_p)_CA,CB. Section 2 supplies its rank bound and section 3 its error.
The additional minimum with one follows because U_CA,CB is a compression
of a unitary, hence has operator norm at most one.

## 5. Return to a UNITARY comparison and the raw event law

P71 constructs a genuine unitary V of cross rank at most q satisfying

    ||U-V||op<=delta(s_(q+1)(U_CA,CB))
               <=sqrt(2)*E_p(tau),
    delta(s)=sqrt(2-2sqrt(1-s^2)).

Its proof uses complete CS rotations and truncates small sine/cosine pairs
while retaining unitary local basis changes. This is not the substitution
V=Q_p, which would invalidate a physical count-law comparison.

The symmetric K-particle tensor telescoping bound and trace-distance
measurement contraction in P71 give

    TV(P_U_fullPNR,P_V_fullPNR)<=min(1,K*||U-V||op).

P69 bounds the SAME good event under V by p_Lq, proving the finite claim.
There is no additional one-half multiplying K: it is already incorporated
in the definitions of trace distance and TV. All collided and other output
counts remain in the normalization. A conditional no-collision law is not
being compared.

For reference, for q>=1,

    a_Lq=min(1,q(q+1)...(q+L-1)/L^L),
    b_Lq=1 if q>=L,
    b_Lq=min(1,((L+q)/(2q))^q*((L+q)/(2L))^L) if 1<=q<L,
    p_Lq=min(1,2*a_Lq*b_Lq).

When q>=L this probability bound can be trivial even if q<d. A useful
asymptotic regime therefore keeps q below a fixed fraction of L.

## 6. Fixed coupling rank and sublinear norm-time

Fix an integer h>=1 independent of L and a constant 0<alpha<1. Choose

    p=floor(alpha*L/h),    q=p*h<=alpha*L<L.

For all sufficiently large L, p>=1 and p+1 is of order L. P69 implies

    p_Lq<=2*exp(-L*I(alpha)),
    I(alpha)=(1+alpha)log(2)-(1+alpha)log(1+alpha)+alpha log(alpha)>0.

Indeed the target-tail exponent is I(q/L), which is at least I(alpha);
the source-projection probability is at most one. This deliberately uses
a sufficient bound rather than optimizing the polynomial degree.

Now assume tau_L=o(L). Put m=p+1 and rho=tau_L/m. For tau_L>0, the
elementary factorial integral gives m!>=(m/e)^m, hence

    log E_p(tau_L)
       <=tau_L+m*(1+log(tau_L/m))
       =m*(rho+1+log rho).

Since rho->0 and m/L tends to alpha/h>0, the right-hand side divided by L
tends to minus infinity. Thus E_p<=exp(-omega(L)); the case tau_L=0 is
already exact. Multiplying by K=2L does not change this super-exponential
upper-error conclusion. The raw good-event probability therefore satisfies

    P_U(good)<=exp(-L*I(alpha)+o(L)).

The positive constant I(alpha) is explicit. This remains a source/target
and warmstart obstruction, not a lower bound for solving the graph by all
methods. Arbitrary marked/current within-block detunings are allowed ONLY
when their contribution to ||H|| still satisfies the stated norm-time bound.
Large detunings cannot be declared free and omitted from tau in this proof.

## 7. A finite small-linear-norm-time window

There is also a simple explicit window. Let p>=1 and c>0 satisfy

    c+log(e*c)<0,    gamma=-(c+log(e*c))>0.

If tau<=c*p, with m=p+1, then e*c<1 and

    E_p(tau)<=exp(c*p)*(e*tau/m)^m
              <=exp(c*p)*(e*c)^m
              <=exp(c*p)*(e*c)^p=exp(-gamma*p).

For fixed h and p=floor(alpha*L/h), this yields an exponentially small
error in L. Combined with the P69 term, a sufficient raw-event rate is

    P_U(good)<=exp(-min(I(alpha),gamma*alpha/h)*L+o(L)).

This is a dimensionless norm-time condition, not a measured optical duration,
classical computation budget or a device calibration. No assertion is made
that an actual platform realizes these chosen Hamiltonians or bounds.

## 8. Growing coupling rank: do not replace L/h by L

If h=h_L grows, p=floor(alpha L/h_L) need not be of order L. Under
h_L=o(L) and tau_L=o(L/h_L), the same argument gives only

    log E_p<=-omega(L/h_L)

in general. That need not be of order -L. For example the symbolic scaling
h_L=ceil(sqrt(L)), tau_L=sqrt(L)/log(L) has p asymptotic to alpha*sqrt(L).
The elementary upper/lower factorial integral inequalities then give

    log E_p=-alpha*sqrt(L)*log log(L)+O(sqrt(L)),

which is sublinear in L. This is an example showing the REMAINDER GUARANTEE
is insufficient for an exp(-constant*L) conclusion, not a constructed
counterexample to the actual physical event bound.

When h_L is comparable to L, p can remain bounded; even E_p->0 need not
make K*E_p small. The finite formula remains the safe statement. More
generally an exponential-in-L consequence needs an actual condition such as

    tau_L+(p+1)*[1+log(tau_L/(p+1))]<=-c0*L,
    p*h_L<=alpha*L,

for some fixed c0>0,0<alpha<1, with tau_L=0 treated separately. The small-
linear window gives exp(-gamma*p), which is exponential in L for fixed h
but generally weaker when h grows. No stronger growing-rank conclusion is
silently inferred.

## 9. Fresh adaptive attempts and the graph cost barrier

For the P66 engineered original or connected graph family, start in one
of its four bad whole-clique states. Each has L occupied vertices in each
fixed target block. The only strict improvements are the two full-block
targets. Every feasible subset outside the bad states and those targets is
uphill by at least the proved positive graph gap g. Only accepted CF
optical proposals update the current source; collisions are paid self-loops,
with no external candidates or restarts.

Before each fresh attempt j, the marked controller may choose a different
Hermitian H_j, t_j, coupling rank bound h_j and polynomial degree p_j. Set
q_j=p_j*h_j and use the finite bound only when q_j<d; otherwise use the
trivial one. A conditional good-event upper bound is

    b_j=min(1,p_{L,q_j}+sqrt(2)*K*E_{p_j}(tau_j)).

Here p_{L,q_j} is the P69 constant indexed by L and q_j. If h_j=0 or
t_j=0, set b_j=0. Otherwise use b_j=1 when q_j>=d and the finite expression
when q_j<d. The choices must be made before observing that shot. At zero
temperature, first-exit bookkeeping yields

    Pr(improvement by T)<=min(1,sum_j E[1[no earlier accepted exit]*b_j]).

For deterministic uniform envelopes one can replace b_j by those envelopes
and drop the indicator. At finite temperature add the conditional term
exp(-beta_j*g) inside the same expectation; deterministic schedules/lower
bounds give the familiar sum of such escape terms. Fully random predictable
quantities cannot be inserted as an unconditional numerical right-hand side
without expectations or deterministic almost-sure bounds.

In particular, if h_j<=h for fixed h and
sup_{j<=T_L, history still bad} tau_j(history)/L tends to zero, the common
analysis choice p=floor(alpha*L/h) gives section 6's exponential hazard
estimate uniformly over all those histories. A polynomial number of fresh attempts then has vanishing improvement
probability, provided accepted thermal exits are controlled too. This says
nothing about the chance of entering the prescribed warmstart from a
uniform start, or actual P65 ER/RR cases, annealing schedule and budgets.

A product of multiple different coherent propagator segments is not covered
by pretending there was one fixed low-rank-coupled H. Its net effective
optical rank/error would need a separate justified bound. Likewise,
intermediate measurement/feedforward, different input states, additional
modes, nonunitary filters or a different decoder change the model.

## 10. Scientific disposition

The full algebraic cross rank in P69's exp(itH) counterexample remains
correct; it does not imply a large probability of collective transfer.
The present finite bound quantifies why tiny new singular channels can be
insufficient over a photon/attempt budget. Once the error term is large,
this theorem itself becomes uninformative rather than refuting the route.

All statements are ideal raw-probability mathematics. No numerical success,
matched-cost advantage, independent experimental replication, physical
source feasibility, QPU readiness or novelty is certified. The elementary
classical certificate for the engineered graph family remains available.
The user's requested positive photonic optimization result remains open.
