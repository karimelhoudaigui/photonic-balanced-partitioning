# Full-input complex Hadamards: universal moments through order three

2026-11-25. Fresh analytic derivation from ROOT's P51 claim card, before reading
any author P51 proof. No code, import, numerical experiment, graph or hardware
call. **The order<=3 invariance is proved below.** The fourth-order residual
is also identified exactly. No novelty, useful optimizer gain or classical
hardness is claimed; independent proof review is still required.

## Source and generating function

Let U be an N by N complex Hadamard UNITARY, |U_ia|^2=1/N, N>=1. Inject one
perfectly indistinguishable photon into EVERY input (r=N). Let n denote the
complete output occupation, retaining collisions. U* denotes conjugate
transpose and U uses output/input indices. For formal variables z_i,

    G_U(z)=E[prod_i z_i^(n_i)]=per(U* diag(z) U).                    (1)

Indeed prod_i z_i^(n_i) is the Fock action of diag(z); conjugate by U and
take its matrix element on the normalized all-single-photon input. That
matrix element is the permanent, with no input/output factorial prefactor.
The identity extends polynomially from the diagonal operator to formal z.

Put z_i=1+t_i, A=U*diag(t)U and T_j=sum_i t_i^j. Expand

    G_U(1+t)=per(I+A)=sum_(h=0)^N P_h(A),
    P_h(A)=sum_(S subset [N], |S|=h) per(A[S,S]).                   (2)

The h part is homogeneous of degree h. For a multi-index ell,

    E[prod_i (n_i)_(ell_i)] = prod_i ell_i! * [t^ell] P_(|ell|)(A). (3)

The diagonal and traces satisfy

    A_aa=m=T_1/N,
    Tr(A^j)=T_j,    (A^j)_aa=T_j/N.                              (4)

The last identity uses BOTH full square unitarity and flat entry moduli.
For symbolic complex t use products A_ab A_ba, not conjugation; for real t,
A is Hermitian and those products are |A_ab|^2.

## Degrees one, two and three

The fixed-point and two-cycle terms give

    P_1=T_1,
    P_2=T_2/2+(N-2) T_1^2/(2N).                                 (5)

For completeness let W_1=sum_(a<b) A_ab A_ba=(T_2-Nm^2)/2, and let C_3
be the sum of the TWO oriented three-cycle products on each unordered triple.
Trace expansion, with repeated indices counted, gives

    T_3=Nm^3+6m W_1+3 C_3,
    P_3=binom(N,3)m^3+(N-2)m W_1+C_3.

Hence exactly

    P_3 = T_3/3 + (N-4) T_1 T_2/(2N)
          + (N^2-6N+12) T_1^3/(6N^2).                           (6)

Every coefficient of (5)–(6) is independent of U. Thus ALL joint factorial
moments of TOTAL order<=3 are invariant, not just marginal moments or a
selected covariance. No order-three counterexample exists in this model.
For N<3, the absent homogeneous parts vanish using the identities among the
power sums in the available variables; only existing distinct indices apply.

Explicit checks from coefficient extraction (distinct i,j,k where present):

    E[n_i]=1,
    E[(n_i)_2]=2(N-1)/N,
    E[n_i n_j]=(N-2)/N,
    E[(n_i)_3]=6(N-1)(N-2)/N^2,
    E[(n_i)_2 n_j]=2(N-2)(N-3)/N^2,
    E[n_i n_j n_k]=(N^2-6N+12)/N^2.

Setting all t_i=t gives P_h=binom(N,h)t^h, as fixed total N requires. Setting
only one t nonzero gives the single-mode generating function

    G_i(z)=sum_(h=0)^N h! binom(N,h) ((z-1)/N)^h.                  (7)

Therefore ALL one-mode occupation distributions are invariant as well, even
though general higher joint moments need not be.

## Exact fourth-order residual

For N>=4 define w_ab=A_ab A_ba, W_2=sum_(a<b) w_ab^2,
q=T_2/N, R=q-m^2. The sum M_2 of w_ab w_ac over unordered pairs of distinct
edges meeting at a vertex is

    M_2 = (1/2) sum_a (sum_(b!=a) w_ab)^2 - W_2
        = N R^2/2-W_2.                                         (8)

Here sum_(b!=a)w_ab=(A^2)_aa-m^2=R; this second constant-diagonal identity
is essential at order four. The sum D_2 of products on disjoint edge pairs is

    D_2=(W_1^2-W_2)/2-M_2.

Let C_4 sum all six oriented four-cycles on each four-set. Classifying the
indices in Tr(A^4) gives

    T_4=Nm^4+12m^2 W_1+2W_2+12m C_3+4M_2+4C_4,
    P_4=binom(N,4)m^4+binom(N-2,2)m^2 W_1+(N-3)m C_3+D_2+C_4.

Eliminating M_2,D_2,C_4 yields

    P_4 = W_2 + T_4/4 + (binom(N,4)-N/4)m^4
          + (binom(N-2,2)-3)m^2 W_1 + (N-6)m C_3
          + W_1^2/2 - N R^2.                                  (9)

Everything on the right except W_2 depends only on N and T_1,...,T_4.
Thus for any two such Hadamards, as a homogeneous polynomial,

    P_4(U)-P_4(V)=W_2(U)-W_2(V).                               (10)

For real t, W_2=sum_(a<b)|A_ab|^4. If summing all ordered entries instead,
that sum is 2W_2+Nm^4; the diagonal part is invariant. Equations (8)–(9)
also explain why using only Tr(A^4) would miss this possible variation.
The prior H4 family gives an explicit difference: its moment
E[n0 n1 n2 n3]=cos^2(phi)/4 varies while all lower-order moments remain fixed.
That example's decoded law has an exact classical mixture sampler; (10)
does not promote it into an optimization advantage.

## Crucial source restriction

r=N is not expendable. Take H4(z) from the earlier checkpoint but occupy only
its first TWO columns. Q is still flat on those columns, but

    Pr(n0=n1=1)=|1+z|^2/16

already varies at total order2. Its compressed projection is not fixed as z
varies; Tr(A^2) is no longer the full-space T_2. Nor does the theorem compare
B with D: their second moments differ even in the full-input setting.

A conditional generalization through order3 is possible for rectangular
frames with the SAME projection and equal column intensities within each row:
their compressed A matrices are unitarily similar and share a constant
diagonal, so the cycle argument applies with permanent size r and the trace
power sums Tr(A^j), rather than the full-space sums sum_i t_i^j. This does not
assert that arbitrary truncated Hadamards have that fixed
projection. No higher-order, partial-source or hardware scope is inferred.
