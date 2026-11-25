# P78 candidate: a full raw Gaussian count law from even Poisson loops

25 November 2026. ROOT static derivation, pending independent reconstruction,
exact-source review, finite validation and bounded literature comparison.
No code, test, RNG, probability query, circuit, hardware or manuscript action
has been executed for P78. This candidate does not assume P75's general
Gaussian overlap conjecture. It concerns an explicitly restricted class of
pair matrices and counts, not classicality of the quantum state itself.

## 1. Exact target and the missing bridge

Let Z be a finite m-by-m REAL SYMMETRIC ENTRYWISE NONNEGATIVE matrix with
||Z||op<1; diagonal entries and zero edges are allowed. The pure
zero-displacement Gaussian pair state is

    |psi_Z>=det(I-Z^2)^(1/4)*exp(a^dagger Z a^dagger/2)|0>.

Target: construct its COMPLETE unconditioned PNR count law, including vacuum,
bunching and all photon numbers, by positive classical random operations.
This is stronger than P77's exact CF conditional sampler in range-limited
positive graphs. Its first uncertain implication is the full multivariate
PGF/loop identity; no efficient hafnian evaluation is assumed.

The proposed cost theorem counts ideal arithmetic/sampling transitions in
terms of the source's actual MEAN photon number. It is not yet a finite-bit
or measured wall-time theorem. Output counts have unbounded support; no
truncation or conditioning is inserted into the exact model.

## 2. Raw photon-count generating function

For z_i in[0,1] let D=diag(z_i), and apply product_i z_i^(n_i/2) to the
state before taking its squared norm. Each creation operator is multiplied
by sqrt(z_i), so its new pair matrix is B=sqrt(D) Z sqrt(D). It is a real
symmetric contraction. The pair-exponential norm is det(I-B^2)^(-1/2),
proved by diagonalizing B and multiplying the one-mode binomial series.
Thus the normalized photon-count PGF is

    G(z)=sqrt[det(I-Z^2)/det(I-B^2)]
        =sqrt[det(I-Z^2)/det(I-(D Z)^2)].

The determinant conversion follows by cyclic products, first for positive
z_i and then by continuity at zero. All square roots are positive. At
z=1, G=1; at z=0, G=sqrt(det(I-Z^2)), the actual vacuum probability.

Since ||Z||<1, the trace-log series converges absolutely. This yields

    log G(z)=sum_(l>=1) [Tr((D Z)^(2l))-Tr(Z^(2l))]/(2l).

Each trace is the sum over ROOTED closed walks
w=(i_0,i_1,...,i_(2l)=i_0), with repetitions allowed, of

    weight(w)=product_(j=0..2l-1) Z_(i_j,i_(j+1)),
    monomial(w)=product_(j=0..2l-1) z_(i_j).

All weights are NONNEGATIVE, even though Z may have negative eigenvalues.
Consequently logG has the form sum_w mu_w*(monomial(w)-1),
mu_w=weight(w)/(2l). This is exactly the PGF of independent Poisson
numbers of rooted even walks, each contributing its vertex-visit count.
The total accepted-loop intensity is finite:

    sum_w mu_w=sum_(l>=1)Tr(Z^(2l))/(2l)
              =-1/2 log det(I-Z^2).

Rooting/orientation are retained in this formula. Dividing by orbit counts
again would be an error; repeated/periodic words already have their correct
trace multiplicities and the factor1/(2l). Equality of PGFs on[0,1]^m
determines the discrete count law. No individual hafnian is computed.

## 3. Sampling loops without enumerating exponentially many walks

First assume Z's support graph is connected and Z is nonzero. Let
r=||Z||op in(0,1), and choose a strictly positive eigenvector v with Zv=rv.
These facts follow elementarily: maximize the symmetric Rayleigh quotient,
replace a maximizing vector by its absolute values, and use connectivity
in the eigenvector equation to rule out zero coordinates. Also
|x^T Z x|<=|x|^T Z |x|<=r||x||^2, so no negative eigenvalue has larger
absolute value than that top eigenvalue.

Define the stochastic matrix

    P_ij=Z_ij*v_j/(r*v_i).

Its rows sum to one, and it is reversible with weights v_i^2. Connectivity
does not require aperiodicity; bipartite examples are allowed.

Generate the following independent proposal process:

1. J is Poisson with mean Lambda=-m/2*log(1-r^2).
2. For each of J proposals choose l>=1 with logarithmic-series probability
   `r^(2l)/[l*(-log(1-r^2))]`.
3. Choose i_0 uniformly from the m modes; generate2l transitions under P.
4. Keep the proposal only if its final state equals i_0. Add one photon
   for each visit i_0,...,i_(2l-1); otherwise discard its temporary visit
   counts. Rejected loops retain their classical cost.

For a specified rooted closed walk, its proposed intensity is

    Lambda*Pr(l)*(1/m)*product_j P_(i_j,i_(j+1))
      =r^(2l)/(2l)*product_j P_(i_j,i_(j+1))
      =weight(w)/(2l).

The eigenvector ratios telescope around a closed walk. Poisson marking
and thinning give exactly the independent accepted-loop intensities from
section2. This can be seen directly by the PGF of a Poisson number of iid
marks; no independence is inferred from a single accepted quantum shot.

For reducible Z, simultaneously permute modes into its support components
and run them independently. A zero component gives deterministic vacuum.
A singleton with positive diagonal is a valid component. The Gaussian
state, PGF and determinant factor over these blocks, so concatenating the
component count vectors gives the full law. No irreducible source is
assumed when claiming the componentwise version.

## 4. Cost in terms of actual mean photons

The expected number of PROPOSED Markov transitions is exactly

    Lambda*E[2l]=m*sum_(l>=1)r^(2l)=m*r^2/(1-r^2).

The Gaussian mean emitted photons are, from the same norm/PGF derivative,

    nbar=Tr[Z^2(I-Z^2)^(-1)]
         =sum_(l>=1)Tr(Z^(2l)) >= r^2/(1-r^2).

Therefore expected proposed transitions<=m*nbar. Expected proposal count
is at most m*nbar/2 because -log(1-r^2)<=r^2/(1-r^2).
For several components, sum m_c*nbar_c<=m*nbar. Poisson count/length
generation, temporary visit counts and rejection are included as work;
sampling a dense P row can use paid preprocessing/alias tables, or pay
O(m) per transition without claiming that preprocessing free.

This is a real-arithmetic/probability-law bound, conditional on access to
the stated Perron data and exact random primitives. Computing/representing
r,v and P, algebraic/irrational probabilities, finite precision, certified
TV error, random bits and large-integer counts need a separate controlled
implementation. No polynomial bit-complexity or practical runtime is
claimed yet. Near r=1 the mean photon count itself diverges and appears
explicitly in the bound; it is not replaced by a nominal accepted count.

## 5. Hand checks and precise physical scope

For one mode Z=[s], every proposed walk closes. The PGF is
sqrt((1-s^2)/(1-s^2*z^2)), the squeezed-vacuum even-count law, not a
Poisson photon law. For a two-mode pair Z=[[0,s],[s,0]], P alternates
deterministically, giving G=(1-s^2)/(1-s^2*z_1*z_2): equal geometric
occupations, including bunching. Thus both the single-mode binomial
coefficient and two-mode pair counts have the correct factor1/2 convention.
These are hand identities, not executed validation.

Independent P73 colors can be sampled independently and then subjected
to their SAME full-count acceptance/decoding, retaining failures. This
does not imply an efficient sampler conditioned on a rare CF event or
small cut: that conditioning may still cost exponentially many raw draws.
The proposed result removes the P77 min-positive-entry/dynamic-range
requirement for raw sampling, not postselection costs.

The state can remain nonclassical under other measurements or subsequent
interferometers. Only fixed output PNR laws with the stipulated Z are
covered. Generic complex/signed pair matrices, displacement, non-Gaussian
inputs and adaptive quantum mixing are outside this construction; loop
weights need not be nonnegative there. It is not a sampler for arbitrary
Gaussian boson sampling or the project's passive CF-Fock optimizer.

No measured total-resource advantage over a QPU follows from ideal
polynomial transition counts. Setup, photon generation, detector/color
resolution, graph work, classical throughput and source failures need
actual ledgers. A finite validation should check bunched sectors and raw
normalization, not just selected CF targets or successful-shot means.

## 6. Disposition pending adversarial checks

KEEP AS CANDIDATE the exact full-PNR loop representation and explicit
proposal sampler, pending independent reconstruction and finite validation.
The needed first checks are determinant/PGF ordering, walk multiplicities,
the Perron transition change of measure and real-versus-bit cost scope.
A bounded source comparison must distinguish raw count laws from the
CF-conditioned graph-subset algorithms in the existing literature. No
failed literature query will count as novelty evidence.

If accepted, this would give a constructive classical explanation for
the entire nonnegative-pair-matrix source subclass, including sparse
matrices. It would not prove every photonic approach impossible or meet
the requested positive optimizer goal. Paper/main/QPU remain frozen.
