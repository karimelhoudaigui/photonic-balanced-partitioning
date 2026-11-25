# P80: an exact rational killed-walk variant of the even-loop sampler

Primary verdict: **proved as stated below**. For every finite rational,
real symmetric entrywise nonnegative contraction Z, the resolvent-vector
construction supplies rational substochastic transitions without a Perron
eigenvector oracle or component decomposition. Its ideal Poisson/log-series
proposal process samples the complete raw Gaussian PNR law exactly. The
expected planned transition count is at most m^2 times the mean emitted
photon number. Rational setup and rational transition coins can be handled
exactly; this note does not prove the bit complexity of the entire sampler.

Independent static reconstruction of ROOT's candidate, 26 November 2026,
starting at `efd402ab542dfe6a616daffcef1631be453b0060` on
`research/p66-dark-barrier`. ROOT supplied the proposed formulas and
inequality before this derivation. No other P80 author source, proof or
verdict was read, and no other agent was contacted for this reconstruction.
This is a before-author-reading derivation, not an independent discovery
or a novelty claim. Only this file is written. No scientific code, import,
AST, test, graph generation, random draw, numerical query, native backend,
QPU or manuscript action was performed.

## 1. Exact source and the rational resolvent vector

Let m>=1 be finite and let Z be an m-by-m symmetric matrix with rational,
nonnegative entries and r=||Z||op<1. Diagonal entries, zero rows, reducibility
and bipartite support are allowed. The target is the full number law of

    |psi_Z>=det(I-Z^2)^(1/4) exp(a^dagger Z a^dagger/2)|0>.

The vacuum, collisions, all total photon numbers and subsequent failures
of any classical acceptance rule remain part of that raw law.

Define, exactly over the rationals,

    v=(I-Z)^(-1) 1=sum_(t>=0) Z^t 1.

The inverse exists because r<1. The equality with the Neumann series holds
in operator norm. Every summand is entrywise nonnegative, and the t=0
summand is 1, so v_i>=1. The infinite sum proves positivity but need not
be evaluated to compute v: rational linear algebra gives the inverse
times 1 exactly. In particular

    Zv=v-1.

Put V=max_i v_i. If Z=0, then v=1 and the source is deterministic vacuum;
return that record before evaluating any expression divided by kappa.
If Z is nonzero, some entry of Z1 is positive, hence V>1. In this case

    kappa=max_i (Zv)_i/v_i
         =max_i (1-1/v_i)=1-1/V in (0,1).

Thus v and kappa are rational, with finite positive denominators. No
eigenvalue or eigenvector is needed to choose these algorithm parameters.
The norm r will occur only in a proof of their resource bound.

## 2. Substochastic transitions and the absorbing state

For Z nonzero define, on the original m modes,

    P_ij=Z_ij v_j/(kappa v_i).

All entries are rational and nonnegative. The row sum is

    sum_j P_ij=(v_i-1)/(kappa v_i)<=1.

Introduce one additional CLASSICAL absorbing state dagger, with transition
probability

    P_(i,dagger)=1-sum_j P_ij,
    P_(dagger,dagger)=1,
    P_(dagger,j)=0 for every original mode j.

This makes an ordinary stochastic chain. The added state is a simulation
device, not an optical ancillary mode or a changed Gaussian source. Once
a proposal dies it cannot return to any original root. Partial visits
from such a proposal contribute no output photons.

A zero row of Z has v_i=1 and dies at its first transition. A row attaining
V has zero death probability. Unequal rows or disconnected components
require no special branch. Z may be reducible, and no coordinate of v
vanishes, unlike a global Perron vector on disconnected components.

As a consistency check, r<=kappa can also be proved without a Perron
theorem. Given any eigenvector x with eigenvalue eta, choose i maximizing
|x_i|/v_i>0. Nonnegative entries and Zv<=kappa v give

    |eta| |x_i|<=sum_j Z_ij |x_j|
                   <=(|x_i|/v_i)(Zv)_i<=kappa |x_i|.

Z is symmetric, so its operator norm is the maximum |eta|. This check is
not required to evaluate the sampler's rational parameters.

## 3. Full Gaussian PGF and positive even-loop intensities

For completeness, no external loop theorem is a premise. Real orthogonal
diagonalization reduces the pair-exponential squared norm to products of

    sum_(n>=0) binom(2n,n)(s^2/4)^n=(1-s^2)^(-1/2).

This proves the state's normalization, including signed eigenvalues s.
For z_i in [0,1], put D=diag(z_i). Number weighting by
product_i z_i^(N_i/2) replaces Z by B=sqrt(D) Z sqrt(D), whose norm is
at most r. Taking its squared norm yields the complete PGF

    G(z)=sqrt(det(I-Z^2))/sqrt(det(I-B^2))
        =sqrt(det(I-Z^2))/sqrt(det(I-(DZ)^2)).

For positive D, DZ is similar to B; determinant continuity covers zero
coordinates. Square roots are the positive real roots. In particular
G(1)=1 and G(0)=sqrt(det(I-Z^2)), the actual vacuum probability.

The absolutely convergent trace-log gives

    log G(z)=sum_(l>=1)
            [Tr((DZ)^(2l))-Tr(Z^(2l))]/(2l).

Absolute convergence follows from ||B||,||Z||<=r<1 and the bound
|Tr(B^(2l))|,|Tr(Z^(2l))|<=m*r^(2l). Expand each trace over rooted closed
tuples w=(i_0,...,i_(2l)) with i_(2l)=i_0. Define

    weight(w)=product_(t=0..2l-1) Z_(i_t,i_(t+1)),
    c_i(w)=#{t in {0,...,2l-1}: i_t=i},
    nu_w=weight(w)/(2l).

The equal terminal index is not counted a second time. There is no extra
quotient by rotation, reversal or periodicity. Then

    log G(z)=sum_closed_w nu_w*(product_i z_i^(c_i(w))-1).

All nu_w are nonnegative, and

    sum_w nu_w=-1/2 log det(I-Z^2)<infinity.

Therefore these are legitimate finite-total compound-Poisson intensities.
Their jumps have even total photon number and include all repeated visits
and diagonal self-loops. Equality of these convergent PGFs identifies
the entire count law, rather than selected coefficients or moments.

## 4. Exact killed-walk proposal process

For nonzero Z set L_k=-log(1-kappa^2)>0 and Lambda=m*L_k/2.
The ideal random construction is:

1. Start the output counts at zero and draw J from Poisson(Lambda).
2. Independently for each of J proposals draw l>=1 with probability
   kappa^(2l)/(l*L_k), and a uniform root i_0 among ALL m original modes.
3. Plan 2l transitions of the augmented chain in section 2. Once dagger
   is reached, the proposal may be discarded immediately; it can never
   return to its root. Charge its entire planned 2l length in the bound.
4. Keep an alive path only if i_(2l)=i_0. Add its departure-visit counts
   i_0,...,i_(2l-1), retaining repetitions. Every other proposal contributes
   the zero output vector, including all its temporary visits.
5. Return the sum after all proposals. No optical acceptance event is
   required to define a raw output record.

The length probabilities sum to one because
sum_(l>=1) x^l/l=-log(1-x), applied to x=kappa^2<1.
Each proposed alive closed tuple w has probability product_t P_(i_t,i_(t+1))
conditional on l and root, with

    product_t P_(i_t,i_(t+1))
       =kappa^(-2l) weight(w)*v_(i_(2l))/v_(i_0)
       =kappa^(-2l) weight(w).

It consequently has Poisson intensity

    Lambda * [kappa^(2l)/(l*L_k)] * (1/m)
             * product_t P_(i_t,i_(t+1))
      =weight(w)/(2l)=nu_w.

Death probabilities do not enter this product: the specified path is
alive throughout. The substochastic row sums are exactly completed by
death, so there is no additional path normalization. A dead or unclosed
mark has PGF one. For iid proposal mark PGF F, the elementary identity
E F(z)^J=exp(Lambda*(F(z)-1)) therefore gives exactly G(z).

This proves the full raw PNR law. Uniform root selection and population
m*L_k/2 must be kept together. Choosing only a nonzero component or
renormalizing a substochastic row without its death probability would
change the law. The classical return rejection is not CF postselection,
and no hafnian evaluation, graph optimum or photon-number conditioning
is used. J and every length are finite almost surely, so one raw sample
terminates almost surely in this ideal model.

## 5. Planned work, rational emitted mean and the dimension bound

The exact expected planned transition count is

    Wplan=E[J]*E[2l]=m*kappa^2/(1-kappa^2).

It includes all later steps that are skipped if a proposal dies early.
Actual generated transitions cannot exceed the planned count. Since each
proposal plans at least two transitions, E[J]<=Wplan/2.

The mean emitted photons of ONE source is

    nbar=Tr[Z^2(I-Z^2)^(-1)]=sum_(l>=1)Tr(Z^(2l)).

This follows by differentiating G(u,...,u) at u=1, or summing loop jump
sizes. It is rational for rational Z, and can itself be computed with
exact rational matrix algebra. If Z=0 it is zero. For nonzero symmetric Z,
some eigenvalue has magnitude r, so nbar>=r^2/(1-r^2), without any need
to identify a positive eigenvector.

To control kappa, use v-1=(I-Z)^(-1) Z1 and Euclidean/operator norms:

    V-1<=||v-1||_2
        <=||(I-Z)^(-1)||op * ||Z||op * ||1||_2
        <=sqrt(m)*r/(1-r)=a.

All denominators are positive. The map x/(1+x) is increasing for x>=0,
so kappa=(V-1)/V<=a/(1+a). The map x^2/(1-x^2) is increasing for
0<=x<1. Consequently

    kappa^2/(1-kappa^2)
       <=a^2/(1+2a)
        =m*r^2/[(1-r)*(1-r+2*sqrt(m)*r)]
       <=m*r^2/[(1-r)*(1+r)]
        =m*r^2/(1-r^2)
       <=m*nbar.

The middle inequality is in the displayed direction because

    1-r+2*sqrt(m)*r >= 1+r

is equivalent to 2*(sqrt(m)-1)*r>=0. This holds for all m>=1 and r>=0.
For nonzero Z the divisions are valid; the separately handled Z=0 case
also satisfies the final bound. Thus

    Wplan<=m^2*nbar,        E[J]<=m^2*nbar/2.

No lower bound on a positive entry, connectivity, spectral gap, Perron
coordinate or photon-number postselection probability was used. The
factor m here is an additional worst-case dimension factor relative to
the Perron version of P78; it is not a claim that the two proposals have
the same resource cost.

## 6. Rational setup and exact local coins: what is proved

The setup v,kappa,P,death is entirely rational and finite. It does not
approximate eigenvectors. A polynomial bit-size statement for this setup
can be justified explicitly. Suppose each rational input numerator and
positive denominator has at most B bits. Choose Q as the product of all
input denominators, with log2 Q<=m^2*B. Then

    M=Q(I-Z),       Mv=Q1

has integer entries with O(m^2*B+B) bits. A k-by-k determinant has at most
k! products of k such entries, so every minor of the augmented integer
matrix [M | Q1] is at most 2^(O(k*(m^2*B+B+log k))) in absolute value.
Cramer's rule therefore
bounds the numerator/denominator sizes of each v_i by a polynomial in
m,B, not by its possibly large numerical magnitude. Rational maxima,
kappa and the products/quotients defining P and death preserve polynomial
bit size.

These representation bounds can be attained by polynomially many exact
arithmetic operations: M is symmetric positive definite because every
eigenvalue of I-Z is positive, so its leading elimination pivots are
nonzero. Successive Schur-complement entries, including the right-hand
side, are ratios of minors, by
det([[A,b],[c,d]])=det(A)*(d-c*A^(-1)*b). Exact elimination with reduced
fractions, or fraction-free elimination, therefore has polynomial-sized
intermediates and O(m^3) arithmetic operations; back substitution remains
polynomial-sized as well. Integer arithmetic and gcd reductions on these
bit lengths give polynomial bit cost for the SETUP. This is not a claim
that a determinant expansion over m! terms is an efficient algorithm.

No value of r is computed for setup or the transition definition. If a
future implementation must certify the input promise, exact symmetry,
nonnegativity and positive definiteness of I-Z and I+Z suffice; these
are rational checks. An uncertified physical matrix estimate is a
different input-certification problem.

Each row of the augmented chain is a rational probability vector. It
admits exact finite-bit coins: take a common positive denominator q,
form its nonnegative integer weights summing to q, and draw uniformly
from {0,...,q-1}. Drawing ceil(log2 q) unbiased bits with rejection of
integers at least q takes fewer than two attempts in expectation for
q>1; q=1 is deterministic. Prefix weights then select the exact outcome,
including death. Row common denominators and prefix weights have
polynomial bit lengths in m,B. Thus irrational Perron ratios are not
hidden in a transition oracle.

## 7. Sampling primitives and physical/resource limits

The full sampler still uses Lambda=-m/2 log(1-kappa^2) and normalized
log-series probabilities. Rational kappa and rational P do not make
these parameters rational. This proof assumes the stated ideal exact
Poisson/log-series draws; it supplies neither a full exact finite-bit
random-variate algorithm with a bit-work bound nor a rounded sampler's
certified TV contract. Those are separate obligations. This changed
algorithm removes the Perron-data premise, not every sampling premise.

Wplan counts transitions, not total time. Source setup, matrix reading,
random-variate generation, row selection, output initialization, counts,
graph scoring and any classical acceptance rule must be charged. Storing
a proposed path and adding its visits only on return costs O(l) work,
with unbounded random storage; rejected work remains paid. Dense row
scans may cost O(m) per transition, or require paid preprocessing. For a
fixed Z, legitimate immutable setup may be reused; changing Z must pay
its new setup. No deterministic time/output-memory cap is established.

When kappa approaches one, expected work may be large, and nbar itself
can be large. A bound polynomial in m and nbar is not automatically a
bound polynomial in the input's bit length. Vacuum or very weak sources
do not make the dimension-dependent setup or output initialization free.
The emitted nbar, rather than detected or accepted photons, is the
statistic in the resource comparison. This note gives no measured
hardware cost or equal-clock optimizer comparison.

## 8. Edge cases, scope and disposition

- Z=0 is handled before division by kappa: deterministic raw vacuum.
- A positive diagonal singleton Z=[s] gives v=1/(1-s), kappa=s and no
  death. Its PGF is sqrt((1-s^2)/(1-s^2*z^2)); the m=1 bound is exact.
- For Z=[[0,s],[s,0]], v is constant and kappa=s. The alive chain swaps
  the modes, every even path closes, and the output PGF is
  (1-s^2)/(1-s^2*z_1*z_2). This is a symbolic check, not a numerical run.
- Zero rows, mixed zero/nonzero components and unequal components use
  the same global rational construction. No division by a vanishing
  Perron coordinate or implicit reweighting of roots occurs.
- Diagonal pairs, repeated visits, bipartite period two and negative
  eigenvalues of Z are all compatible with the positive even-walk proof.
- Independent colors can be generated by independent instances; their
  means and full costs add. Applying the same classical CF/complement
  rule afterwards preserves both accepted and failed probabilities.
  Rare conditional sampling still pays the necessary raw repetitions.
- General signed/complex final pair matrices, displacement, arbitrary
  subsequent interferometry, quantum filtering and adaptive changes of
  the measurement are not covered by this nonnegative real source law.

KEEP this as a substantive rational killed-walk algorithmic variant of
P78, with the exact-law proof and the m^2*nbar planned-transition bound.
The remaining implementation task is the separately specified
Poisson/log-series finite-bit and total-resource contract. No scientific
execution is authorized by this derivation. No novelty, all-Gaussian
classicality, all-photonic no-go, positive optimizer result or QPU
capability is claimed.

Final hand proofreading checked the resolvent's positivity, the direction
of every inequality, rationality, death/return convention, trace factors,
root population m, zero and singleton boundaries, setup-bit claim and
the remaining random-primitive/resource assumptions. Only this independent
proof and text/Git integrity checks accompany its freeze.
