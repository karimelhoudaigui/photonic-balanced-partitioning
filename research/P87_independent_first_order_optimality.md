# P87: identity is first-order optimal for passive balanced cost phases

Primary verdict: **proved under the hypotheses below**. For fixed even
N>=4 and a fixed real complement-invariant balanced cost C with range R,
the optimized worst-column error with one common global phase satisfies

    lim_(gamma->0, gamma!=0) delta_star(gamma)/|gamma|=R/2.

Identity, up to the metric's common phase, attains this first-order
coefficient. The proposed finite-angle lower bound and constants are
valid. The same leading limit holds for the optimized restricted operator
norm. This does not assert pointwise optimality of identity at finite
angle, a dimension-uniform asymptotic, or a sampling/optimizer no-go.

Independent before-author-reading reconstruction of ROOT's candidate,
26 November 2026, starting at
`36ff60481e259438fd9d4cf58ef6953109572384`, branch
`research/p66-dark-barrier`. ROOT supplied the route and proposed constants.
No other P87 source, derivation or verdict was read or contacted. This
is not independent discovery or a novelty claim. Only this file is
written. No scientific code/import, AST, test, RNG, matrix numerics,
backend, QPU or manuscript action was performed.

## 1. Metric, constants and exact finite-angle claim

There are N indistinguishable photons and 2N physical dual-rail modes,
with one photon per pair in a code basis state. Let K=N/2 count logical
ones, not photons. For every S subset {1,...,N} with |S|=K, denote that
normalized code Fock vector by |S>. Let C(S)=C(S^c) be fixed and real.
It need not be a graph cut for this theorem; weighted cuts are included.

U is any lossless passive unitary on these same 2N modes. No ancillary
modes, heralding, loss, intermediate filters or discarded outcomes are
allowed. Define

    delta(U,gamma)=inf_chi max_(|S|=K)
       ||Gamma_N(U)|S>-exp(i chi-i gamma C(S))|S>||_2,
    delta_star(gamma)=inf_U delta(U,gamma),
    R=max_(|S|=K)C(S)-min_(|S|=K)C(S).

The phase chi is COMMON to every S. For fixed U,gamma a minimizing
phase exists: a finite maximum of continuous functions on the phase
circle is continuous and that circle is compact. Fix such a phase,
put delta=delta(U,gamma), and f_S=exp(i chi-i gamma C(S)).

Use the constants

    C_N=4*N*(N-1)^2/(N-2),
    s=sqrt(C_N),      b=1+N*s,
    d=s+sqrt(2*N)*b,
    E=(N!-1)*d^2,     delta_0=1/(2*b).

They are strictly positive and finite at fixed N>=4. Define, for x>=0,

    r_E(x)=[sqrt(1+2*E*x)-1]/(2*E)
           =x/[sqrt(1+2*E*x)+1].

The uniform bound proved below is

    delta(U,gamma)
       >=min(delta_0,r_E(|sin(gamma R)|)).                   (1)

The same statement holds with R replaced by any C(S)-C(T) inside the
absolute sine. E is conservative and can grow factorially with N;
its magnitude must not be hidden in finite-angle or growing-dimension
interpretations.

## 2. P81 supplies a local comparator; the needed facts are rederived

The accepted dependency is P81 in
`theory/P81_dual_rail_balanced_average_stability.md`, independent commit
`0a51544a1a449c64b87cb48e82bf637583402278`, SHA256
`7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f`.
The hash was checked unchanged. P86's independent reconstruction also
remains unchanged at commit `36ff60481e259438fd9d4cf58ef6953109572384`,
SHA256 `cf156f61e2c47864c024cc471d6e1fc873aec18158ba5a4c70898d456eb8342a`.
The required permutation/error steps are proved again here, rather
than importing any other P87 argument or a Lie-algebra statement.

Projecting each column error outside the one-photon-per-pair code
shows that every balanced basis input has raw leakage at most delta^2.
The uniform incoherent balanced average epsilon therefore satisfies
epsilon<=delta^2. P81, with exactly the same N-photon/no-ancilla
physical model, gives a block-permutation unitary V, with local blocks
V_(a,pi(a))=Q_a, satisfying

    ||U-V||_F<=s*sqrt(epsilon)<=s*delta.                     (2)

The tensor telescoping bound, restricted to the symmetric N-boson
space, is

    ||Gamma_N(U)-Gamma_N(V)||op<=N*||U-V||op<=N*||U-V||_F.

For every balanced S separately,

    ||Gamma_N(V)|S>-f_S|S>||<=b*delta=:e.                    (3)

This is not an operator bound for the target oracle inferred from
column errors. It combines the actual physical-unitary norm estimate
(2) with the target error only on the particular column in question.

For delta>=delta_0, (1) is immediate. Assume henceforth delta<delta_0,
so e<1/2. Write A_S^V=<S|Gamma_N(V)|S>. Normalization and (3) imply

    |A_S^V|>=Re(conj(f_S)*A_S^V)>=1-e^2/2>7/8.              (4)

For the logical bit string x of S, creation-operator expansion gives

    A_S^V=product_a (Q_a)_(x_a,x_(pi(a))).

If pi(a)=b!=a, choose balanced strings with respectively
(x_a,x_b)=(0,0) and (0,1). Both exist at N>=4, including N=4.
All factors have modulus<=1, so (4) would force both |(Q_a)_00|
and |(Q_a)_01| to exceed 7/8, contradicting their row's unit norm.
Thus pi is identity in the branch being considered.

## 3. Physical off-diagonal mass is O(delta)

Now V is block LOCAL, but its two-mode Q_a need not be diagonal.
For each qubit a and each bit value x in {0,1}, some balanced S has
x_a=x. Since the product A_S^V has modulus at most each factor,

    |(Q_a)_xx|>=1-e^2/2.

Both local diagonal entries are thus controlled, using all balanced
inputs. Unitarity gives for each off-diagonal entry

    |(Q_a)_(x,1-x)|^2
      =1-|(Q_a)_xx|^2
      <=1-(1-e^2/2)^2<=e^2.

There are two such entries per qubit. Let offdiag refer to entries
off the ordinary PHYSICAL 2N-by-2N matrix diagonal, including rail
flips within a pair, rather than merely off-block entries. Then

    ||offdiag(V)||_F<=sqrt(2*N)*e.

The off-diagonal projection contracts Frobenius norm, so (2) yields

    tau:=||offdiag(U)||_F
        <=||U-V||_F+||offdiag(V)||_F
        <=[s+sqrt(2*N)*b]*delta=d*delta.                    (5)

No claim tau<=1 is made or needed. These are physical matrix entries,
not off-diagonal amplitudes in the exponentially larger logical space.

## 4. The collision-free permanent and its quadratic remainder

For each S let J_S consist of the N occupied PHYSICAL input rails,
one selected rail in every pair. The exact same-mode return amplitude is

    A_S:=<S|Gamma_N(U)|S>=per(U[J_S,J_S]).

To check normalization, expand the product of the N transformed creation
operators. The target has N distinct occupied modes, all occupations
one. Its coefficient is the sum over N! bijections between distinct
input and output modes. Both normalized Fock factorial products equal
one, hence no division by N!, square root or other factor is present.

The identity-permutation contribution is

    B_S=product_(i in J_S) U_ii.

Every nonidentity permutation moves at least two labels. Since the
physical labels in J_S are distinct, it contains at least two factors
U_ij with i!=j. Each of these has modulus<=tau; every remaining factor,
whether diagonal or not, has modulus<=1 by unitarity of U. Selecting
two moved factors therefore bounds the entire product by tau^2.
This argument is valid also when tau>1; it does not replace a higher
power of tau by tau^2. Summing N!-1 terms and applying (5) gives

    |A_S-B_S|<=(N!-1)*tau^2<=E*delta^2.                    (6)

This is an exact finite expansion, not a Taylor series for U and not
an assumption that U_gamma approaches a chosen matrix continuously.
All complex signs and any cancellations are retained in A_S; the
triangle inequality only supplies a conservative remainder bound.

## 5. Complementary physical rails and the sharpened phase bound

J_S and J_(S^c) are disjoint and together contain ALL 2N physical
rails. Thus

    B_S*B_(S^c)=product_(i=1..2N)U_ii=:L,

independent of S. The use of N photons is essential: complementary
logical ones-sets do not describe K-photon sources. No diagonal entry
is divided out; L can vanish without invalidating the argument.

Unitarity bounds |A_S|<=1, and |B_S|<=1 follows entrywise. From (6),

    |A_S*A_(S^c)-L|
      <=|A_S|*|A_(S^c)-B_(S^c)|+|B_(S^c)|*|A_S-B_S|
      <=2*E*delta^2.

Projecting the original column error gives |A_S-f_S|<=delta.
Complement invariance and the COMMON chi imply f_(S^c)=f_S, whence

    |A_S*A_(S^c)-f_S^2|<=2*delta,
    |f_S^2-L|<=2*delta+2*E*delta^2.

Comparing S,T and canceling the common phase in the modulus yields

    2*|sin(gamma*(C(S)-C(T)))|
        =|f_S^2-f_T^2|<=4*delta+4*E*delta^2,

or

    |sin(gamma*(C(S)-C(T)))|<=2*delta+2*E*delta^2.           (7)

The quadratic polynomial on the right is increasing for delta>=0.
Solving it gives delta>=r_E(|sin(gamma*(C(S)-C(T)))|) in the
delta<delta_0 branch. The other branch has delta>=delta_0, establishing
the minimum in (1) for ALL passive U. Taking a maximum/minimum cost
pair yields the range version. No branch condition or normalization
constant is dropped on passing to the infimum over U.

## 6. Matching identity upper bound and the sharp limit

If R=0, identity has zero error after choosing a common phase, and
the asserted limit is zero. Suppose R>0 and put m=(max C+min C)/2,
used solely for analysis of the metric. For U=I choose chi=gamma*m.
Then

    |||S>-exp(-i*gamma*(C(S)-m))|S>||
       =2*|sin(gamma*(C(S)-m)/2)|.

For |gamma|R<=2*pi, monotonicity of sin on [0,pi/2] and
|C(S)-m|<=R/2 imply

    delta_star(gamma)<=delta(I,gamma)<=2*sin(|gamma|R/4).    (8)

Identity itself does not compute m, a cut optimum or any graph feature.
Choosing chi in this proof fixes the free common phase in the error
definition, not a hidden optimum-dependent circuit or encoder.

The lower bound (1) holds uniformly for every U, so it holds for
delta_star. At fixed N the constants E and delta_0 do not depend on
gamma. With x=|sin(gamma R)|, r_E(x) tends to zero and

    r_E(x)/x=1/[sqrt(1+2*E*x)+1] ->1/2.

Thus eventually the minimum in (1) is r_E(x), and its ratio to
|gamma| tends to R/2. Equation (8) has the same ratio limit. Squeezing
proves

    lim_(gamma->0, gamma!=0) delta_star(gamma)/|gamma|=R/2.

The proof permits completely discontinuous choices of U_gamma and
does not require existence of a minimizing U for each gamma. It does
not claim that identity is exactly optimal at finite nonzero angle;
other unitaries may change higher-order errors. The factorial E can
make the displayed finite-angle lower bound weak. No uniform claim
in a simultaneous N->infinity, gamma->0 regime follows.

## 7. Qualified sharp operator-norm version

Let H_bal be the balanced code span and D_gamma its diagonal cost
phase, viewed as a map into the full N-photon Hilbert space. Define

    Eop(U,gamma)=inf_chi
       ||Gamma_N(U)|_(H_bal)-exp(i chi)*D_gamma||op,
    Eop_star(gamma)=inf_U Eop(U,gamma).

For any fixed chi, the operator norm dominates the maximum norm of
its basis columns. Hence Eop(U,gamma)>=delta(U,gamma), and the optimized
operator error has the same lower bound (1). For identity, the difference
is diagonal on H_bal, so its operator norm IS the maximum scalar column
error; the choice in (8) gives the same upper bound. Therefore

    lim_(gamma->0, gamma!=0) Eop_star(gamma)/|gamma|=R/2.

There is no general upper bound Eop<=delta inferred from basis columns,
nor equality of these two optimized errors at finite angles. The
operator statement is restricted to the balanced domain where C is
defined, not an unstated extension to the full photon Hilbert space.

## 8. What is and is not obstructed

This metric tests coherent relative phases. If each basis vector were
allowed its own fitted global phase, identity would have zero error
for every cost and angle. Likewise identity has perfect per-basis
fidelity and the same deterministic PNR counts as a diagonal cost
oracle. The theorem is not a probability-error or basis-PNR-TV lower
bound, and not a generic sampling-optimizer limitation.

Complement symmetry is essential: a nonconstant additive vertex cost
C(S)=sum_(i in S)h_i can be implemented by local rail phases at every
angle, but generally violates C(S)=C(S^c). Periodic isolated-angle
aliases are also compatible with this small-angle limit. No approximate
graph-weight classification or edge-gate compiler lower bound is proved.

The entire balanced basis, common phase and P81 physical model remain
required. Ancillas, heralding, loss, intermediate measurement/filtering,
nonlinear resources, input/source redesign and a task imposed on only
one prepared or visited state are outside this proof. Neither state
preparation costs nor equal classical/optical clocks are made free.

KEEP the first-order optimality statement and its qualified operator
version. No novelty, all-optics no-go, hardware capability or positive
optimizer advantage is inferred. The user's positive objective remains
OPEN. This static result authorizes no scientific execution or new
numerical plan. P86's frozen proof is preserved unchanged.

Final hand proofreading checked physical versus block off-diagonals,
both local columns at N=4, permanent/Fock normalization, the two-moved-
labels bound without tau<=1, complementary physical rails, the common
phase, quadratic branches, analysis-only range and fixed-N limits.
