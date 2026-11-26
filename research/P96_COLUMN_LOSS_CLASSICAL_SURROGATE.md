# P96: a positive two-photon surrogate under a certified column budget

**Analytical status:** the proposed formulas hold under the assumptions below;
the total-variation expression is an equality, not merely a tail estimate.
Independent proof audit and primary-source attribution are still pending.
This derives ROOT's candidate, with no experiment or novelty claim.

## 1. Model and claim

The input has one indistinguishable photon in each of K distinct known modes,
vacuum elsewhere. A fixed passive network with vacuum environment has observed
occupied-input transfer matrix T in C^(m by K), C=T-dagger T<=I. Unobserved
outputs are traced out. All observed occupations n, including vacuum, loss and
collisions, belong to the raw probability law P_B; N=sum_j n_j<=K.
Assume the actual column intensities c_i=C_ii have certified budget
mu=sum_i c_i=Tr C<=1/2. T is explicitly available to the classical control.

Set A=TT-dagger, lambda_j=A_jj, p_ji=|T_ji|^2, and

    g_jl=E_B[n_j(n_l-delta_jl)]
        =lambda_j lambda_l+|A_jl|^2-2 sum_i p_ji p_li.             (1)

Let e_j be a single-photon occupation, and define q to vanish for N>=3:

    q(e_j+e_l)=g_jl                   (j<l),
    q(2e_j)=g_jj/2,
    q(e_j)=lambda_j-sum_l g_jl,
    q(0)=1-mu+(1/2)sum_jl g_jl.                                 (2)

Then q is a normalized nonnegative classical distribution and

    TV(P_B,q)=E_B[(N-1)^2 1_{N>=3}]
             <=(2/3)E_B(N)_3<=24 e_3(c)<=4 mu^3,                 (3)

where TV=(1/2)sum_n|P_B(n)-q(n)|, (N)_r is a falling factorial,
and e_r(c)=sum_{|I|=r}product_{i in I}c_i. Empty/impossible sums are zero.
These claims include K=0,1,2; they do not condition on a photon-count sector.

## 2. First and second moments, including repeated outputs

Normally ordered signal moments can use b_j=sum_i T_ji a_i: annihilators of
the vacuum inputs contribute zero. Distinct input occupations are one each,
so E a_i-dagger a_h=delta_ih and lambda_j=sum_i p_ji. This first moment is
also the same-circuit distinguishable-particle mean; the second moment is not.

After applying b_l b_j, the remaining input states are orthogonal for distinct
unordered removed input pairs {i,h}. Consequently, for every j,l, even j=l,

    g_jl=sum_{i<h}|T_ji T_lh+T_jh T_li|^2>=0.                   (4)

Expanding (4) gives (1): the two complete products include each i=h term
twice, hence the subtraction2 sum_i p_ji p_li. For j=l, (4) is
4 sum_{i<h}p_ji p_jh. Thus q(2e_j) needs the factor1/2; off-diagonal pairs
j<l are listed once. This retains bosonic interference and all bunching.

## 3. Positivity and normalization

Since A is positive semidefinite and Tr A=mu, ||A||<=mu. Summing (1) over l
gives the exact identity and bound

    G_j:=sum_l g_jl
       =mu lambda_j+(A^2)_jj-2 sum_i p_ji c_i
       <=2mu lambda_j.                                         (5)

Here A^2<=mu A and the subtracted term is nonnegative. Therefore
q(e_j)>=lambda_j(1-2mu)>=0; the pair masses are nonnegative by (4),
and q(0)>=1-mu>=1/2. If G=sum_jl g_jl, the total masses in sectors
0,1,2 are respectively1-mu+G/2, mu-G, G/2. Their sum is exactly one.
No clipping, signed weights, failed proposal or rejection normalization is used.

## 4. Exact variation distance

Write H={N>=3}. For each j, the identity n_j-sum_l n_j(n_l-delta_jl)
=n_j(2-N) yields

    q(e_j)=P_B(e_j)-E_B[n_j(N-2)1_H]<=P_B(e_j).                 (6)

For pair occupations q(n)>=P_B(n): their factorial weights equal one on the
specified N=2 occupation, vanish for other N<=2 configurations, and are
nonnegative on H. Also

    q(0)=P_B(0)+E_B[((N-1)(N-2)/2)1_H]>=P_B(0).                (7)

Thus the only deficits q<P_B occur at the single-photon configurations and
on H, where q is zero. For two normalized distributions TV equals the sum
of deficits. Using sum_j n_j=N, this is

    P_B(H)+E_B[N(N-2)1_H]=E_B[(N-1)^2 1_H].                    (8)

In particular, replacing (8) by just P_B(H) would miss the displaced mass
in sectors0,1,2. For integers n>=3, (n-1)^2<=(2/3)(n)_3, with equality at3.
This proves the first inequality of (3).

## 5. Factorial moments and the coefficient24

Choose environmental columns R with R-dagger R=I-C. The full occupied
columns [T;R] are orthonormal and can be completed to a passive unitary.
For real z>=0, weight the observed components by sqrt(z). The squared norm
of the product of these K creation operators is the permanent of its Gram
matrix, by expanding bosonic commutators. The distinct-input Fock state has
normalization one. Its generating polynomial is therefore

    F(z)=E_B z^N=per(I+(z-1)C)
        =sum_{I subset [K]}(z-1)^|I| per(C_I).                 (9)

The final equality expands each identity-or-C factor; a permutation fixes
every index outside I. Differentiating this finite polynomial at1 gives

    E_B(N)_r=r! sum_{|I|=r}per(C_I).                            (10)

Each Gram principal permanent is nonnegative, being a bosonic squared norm.
Cauchy-Schwarz gives |C_ih|<=sqrt(c_i c_h). Each permutation product in
per(C_I) has modulus at most product_{i in I}c_i; there are r! such products.
Hence E_B(N)_r<=(r!)^2 e_r(c). With r=3, (2/3)*(3!)^2=24.
Finally mu^3>=6 e_3(c). This completes (3), including zero columns.

## 6. Edge cases, sharpness and failed extension

K=0 gives certain vacuum; K=1 makes (1) identically zero. For K<=2, H is
empty, so q=P_B exactly, actually for every physical T without the trace
cutoff. Orthogonal observed columns have diagonal C: (10) reduces to
r! e_r(c), the factorial moments of independent survival Bernoullis. Spatial
output counts can still interfere; diagonal C does not equate q with D.

For K=3,m=1,T=(sqrt(alpha),sqrt(alpha),sqrt(alpha)), 3alpha<=1/2,
(9) is1+3alpha t+6alpha^2 t^2+6alpha^3 t^3, t=z-1. Thus

    P_B=(1-3a+6a^2-6a^3, 3a-12a^2+18a^3, 6a^2-18a^3, 6a^3),
    q  =(1-3a+6a^2,       3a-12a^2,       6a^2),  a=alpha.

Equation(8) gives TV=24alpha^3=24e_3(c) EXACTLY. This physical rank-one
family proves the coefficient24 cannot be reduced. More generally take
T_1i=sqrt(mu/K). For each fixed K>=3, (9) and (8) give
TV=24 binom(K,3)(mu/K)^3+O(mu^4) as mu decreases to0. Taking this limit
first, then K to infinity, makes TV/mu^3 tend to4. Thus the universal
coefficient4 is also sharp in this sequential leading-order sense.

The trace cutoff cannot simply be removed: K=3,m=1,T_1i=1/sqrt(3) is
physical but mu=1 and (2) gives q(e_1)=-1/3. More generally the rank-one
equal-column q(e_1)=mu[1-2mu(1-1/K)] can be negative for any fixed
mu>1/2 up to1 when K is sufficiently large. This is outside (3)'s hypothesis.

## 7. Classical cost and permissible interpretation

Compute A, the p-row products, lambda and (1) in O(m^2 K) arithmetic;
(2) has1+m+m(m+1)/2 finite categories, with O(m^2) additional storage beyond
T and decoder state. It is a genuinely correlated classical law, not D or a
physical small-species/pair-source sampler. An arithmetic/oracle description
does not certify finite-bit rounding, exact categorical RNG, measured memory
or matched total running time. No approximate negative mass may be clipped
without a separate certified error allowance; implementation is not supplied.

For the HYPOTHETICAL certified c_i=eta,K=12, eta=.02, (3) gives
24 binom(12,3)eta^3=.04224 per raw attempt. This is not a Lucy calibration
or an inference from mean efficiency. It already gives a vacuous capped
96-attempt union bound. Individual column bounds imply a trace bound Keta,
not the false spectral bound ||T||^2<=eta. Actual phases/T access and
certification of the column budget are necessary, paid inputs to this control.

Any same fixed randomized classical decoder contracts TV, including vacuum/
collision handling and quenching. Under fresh CF/vacuum inputs and a common
policy using only observed classical history, conditional per-step bounds
epsilon_t(h) imply transcript TV<=min(1,sum_t sup_h epsilon_t(h)). This follows
by sequential maximal coupling until the first mismatch. It excludes coherent
inter-attempt memory, hidden physical side information, rare-herald
renormalization and claims about identical wall-clock trajectories. All T
compilation/calibration/setup, categorical draws, mode processing and scoring
must be paid. No optimizer advantage, full-law equality, novelty, hardware/QPU
certificate or universal impossibility is claimed; the positive goal is OPEN.
