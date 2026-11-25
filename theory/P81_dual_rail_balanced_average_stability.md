# P81: dual-rail stability from balanced-basis average leakage

Primary verdict: **proved under the hypotheses stated below**. A fixed
lossless passive unitary with small raw dual-rail leakage averaged over
the entire uniform incoherent balanced code ensemble is close to a
whole-qubit permutation followed by local two-mode unitaries. The bound
and the N=2 exception proposed by ROOT are correct. No ancilla, heralding,
loss, coherent-source or visited-input extension is implicit.

Independent static reconstruction of ROOT's candidate, 26 November 2026,
starting at `d1b54fff7219bd129253a76ff42e2a7d7c7428da`, branch
`research/p66-dark-barrier`. ROOT supplied the candidate formulas before
this derivation. No other P81 source or verdict was read and no other
agent was contacted. This is a before-author-reading reconstruction,
not independent discovery or a novelty certification. Only this file is
written. No code, scientific import, AST, test, RNG, matrix numerics,
native call, QPU or manuscript action was performed. No P79 output was
read. Every example and identity below is hand algebra.

## 1. Physical objects, input ensemble and normalized statement

Let N>=4 be even. There are N logical qubits, each with two physical
rails, hence 2N physical modes. Every code basis input has exactly ONE
indistinguishable photon in each rail pair, and thus N photons in total.
For x in {0,1}^N write

    |x>_code=product_(b=1..N) a_(b,x_b)^dagger |0>.

Let K=N/2 count logical ones; it is NOT the number of photons. The
specified input ensemble is the incoherent mixture

    rho_bal=binom(N,K)^(-1) sum_(|x|=K) |x><x|.

It is not a coherent Dicke state. U is a fixed unitary on these 2N
physical modes, acting passively and conserving photon number, with no
ancillary modes, heralding, discarded outcomes or intermediate filter.
Let n_a denote total output photons in rail pair a. Define

    epsilon=Pr_(rho_bal,U){some n_a!=1}.

This is a RAW failure probability, retaining all within-rail collisions
and all wrong-qubit photon mass. It is not conditional on accepted
shots, and not an average over a selected set of visited basis strings.

Write U_ab for its 2-by-2 block from input pair b to output pair a,
R_ab=U_ab U_ab^dagger, t_ab=Tr R_ab and B_ab=t_ab/2. There exists a
permutation pi and local 2-by-2 unitaries Q_a such that the unitary V with
V_(a,pi(a))=Q_a and other blocks zero satisfies

    ||U-V||_F^2 <= 4*N*(N-1)^2/(N-2) * epsilon.                 (1)

For ANY common N-photon density matrix rho, its complete raw PNR laws
under U and V obey, with TV=(1/2) sum of absolute probability differences,

    TV(P_U^rho,P_V^rho)
      <= min(1,N*||U-V||op)
      <= min(1,2*N*sqrt[N*(N-1)^2*epsilon/(N-2)]).              (2)

The closeness assertion is statewise; an efficient classical sampler for
an arbitrary entangled rho is not asserted. The input premise defining
epsilon is the full specified counterfactual ensemble for this fixed U.

## 2. Bosonic pair moment and the factor six

For an occupied input mode i let u_i be its two-component restriction
to output pair a. For two distinct occupied modes define

    q(u_i,u_j)=||u_i||^2*||u_j||^2+|u_i^dagger u_j|^2 >= 0.

This is the relevant bosonic exchange kernel. Indeed

    n_a(n_a-1)=sum_(alpha,beta in pair a)
                    b_alpha^dagger b_beta^dagger b_beta b_alpha.

Expanding the b operators through U and taking a Fock expectation with
one photon in each occupied input mode leaves, for each ordered i!=j,
the two annihilation/creation matchings. The direct matching gives the
product of squared norms and the exchange matching gives the squared
inner product. Repeated input modes contribute zero because each input
mode initially has at most one photon. Thus for any code basis input,

    E_x[n_a(n_a-1)]=sum_(b!=c) q(u_(b,x_b),u_(c,x_c)).

The sum is ORDERED. In the two-photon case q itself is the probability
that both photons fall in pair a, and the factorial moment is 2q.

As an auxiliary analytic ensemble, average over ALL 2^N code basis
strings uniformly, still with N photons. Each choice of the two rail
bits at b!=c then has probability 1/4. Since

    sum_(mu,nu) q(u_(b,mu),u_(c,nu))
       =t_ab*t_ac+Tr(R_ab R_ac),

the all-code average moment is

    F_a,all=(1/4) sum_(b!=c) [t_ab*t_ac+Tr(R_ab R_ac)].

Unitarity gives sum_b R_ab=I_2 and sum_b t_ab=2. Adding then removing
the b=c terms yields exactly

    F_a,all=[6-sum_b(t_ab^2+Tr(R_ab^2))]/4.                   (3)

The six is 2^2+Tr(I_2^2)=4+2. It is not an extra photon-number factor.
Each R_ab is positive semidefinite and <=I_2, so
sum_b Tr(R_ab^2)<=sum_b Tr R_ab=2. Equation (3) therefore implies

    F_a,all >= 1-sum_b B_ab^2.                               (4)

For a hand normalization check, take two qubits and
U=(1/sqrt(2))*[[I_2,I_2],[I_2,-I_2]]. For either output pair, both
R blocks are I_2/2, so (3) gives 3/4. Equal selected rail bits give
moment 1, whereas unequal bits give 1/2; the all-code average is indeed
3/4. This check of (3) does not use the N>=4 comparison below.

## 3. Balanced versus all-code averaging, and raw leakage

For distinct input qubits b,c, the uniform weight-K=N/2 ensemble has

    Pr(00)=Pr(11)=(N-2)/[4*(N-1)],
    Pr(01)=Pr(10)=N/[4*(N-1)].

These follow by sampling two locations without replacement among K
ones and N-K zeros. Their minimum is positive for N>=4. Every kernel
q in section 2 is nonnegative, so termwise comparison with the all-code
weight 1/4 gives

    F_a,all <= (N-1)/(N-2) * F_a,bal.

Let F_all=sum_a F_a,all and F_bal=sum_a F_a,bal. For any output number
record, sum_a n_a=N and

    0<=sum_a n_a(n_a-1)<=N*(N-1)*1_{code failure}.

It vanishes on the code. Off the code its upper bound follows from
sum_a n_a^2<=(sum_a n_a)^2=N^2. Hence

    F_bal <= N*(N-1)*epsilon,
    F_all <= N*(N-1)^2/(N-2)*epsilon.                        (5)

This step uses the entire incoherent balanced ensemble. Coherent
superpositions can have input off-diagonal contributions to the moment;
a favorable visited subset can omit some positive kernels entirely.
Neither is a replacement for the premise used in this proof.

## 4. Weighted assignment, proved without an external leaf

B is nonnegative with every row and column sum one: the row identity
comes from UU^dagger=I and the column identity from U^dagger U=I.

First any doubly stochastic matrix has a positive-entry perfect matching.
For a set R of rows, its mass |R| can enter only its neighbor columns,
whose total column capacity is their cardinality. Thus every such set
has at least |R| neighbors. To prove this suffices, take a matching of
maximum size. From an unmatched row follow alternating unmatched edges
to columns and matched edges back to rows. A reachable unmatched column
would yield an augmenting path and a larger matching. Otherwise all
reachable columns are matched to reachable rows, while the starting row
is an extra unmatched reachable row. All neighbors of the reachable
rows are reachable columns. This contradicts the preceding capacity
inequality. The maximum matching is therefore perfect.

Choose such a permutation in the support and subtract its permutation
matrix times the minimum of its selected entries. The residual is
nonnegative, with a common row/column sum, and loses at least one support
entry unless it is zero. Reapply the same support argument after scaling
any nonzero residual by its common sum. Finitely many support deletions
produce

    B=sum_j alpha_j P_(pi_j),   alpha_j>=0,   sum_j alpha_j=1.

Consequently the alpha-weighted average of selected B entries is

    sum_j alpha_j sum_a B_(a,pi_j(a))=sum_(a,b) B_ab^2.

At least one permutation pi therefore satisfies

    sum_a B_(a,pi(a)) >= sum_(a,b) B_ab^2.                   (6)

For a fixed convention one can choose the lexicographically first
maximum-weight permutation; it necessarily satisfies (6).
These are finite existence constructions. No matching calculation,
numerical decomposition or graph-optimization experiment is performed.

## 5. Off-block mass, local polar factors and the physical unitary

For the chosen pi put M_a=U_(a,pi(a)) and define the off-block mass

    delta=sum_(a,b!=pi(a)) ||U_ab||_F^2
         =2*[N-sum_a B_(a,pi(a))].

Summing (4) and using (6) gives

    delta <=2*[N-sum_(a,b)B_ab^2] <=2*F_all.                 (7)

Each M_a is a contraction since it is a submatrix of U. To construct a
unitary polar extension even at zero singular values, diagonalize
M_a^dagger M_a with orthonormal eigenvectors w_j and eigenvalues s_j^2,
0<=s_j<=1. For s_j>0 the vectors z_j=M_a w_j/s_j are orthonormal.
Complete missing z_j in the output pair's orthogonal complement, and
define Q_a w_j=z_j. Then Q_a is a full two-mode unitary and

    ||M_a-Q_a||_F^2=sum_j(1-s_j)^2
                    <=sum_j(1-s_j^2)=2-||M_a||_F^2.

The construction covers rank zero and rank one blocks. Putting these
Q_a in the pi blocks gives a unitary V: each input and output pair occurs
exactly once. The selected and off-block matrix entries are disjoint, so

    ||U-V||_F^2=delta+sum_a ||M_a-Q_a||_F^2
               <=2*delta<=4*F_all.

Equation (5) proves (1). This is a statement on the same 2N physical
modes, not a logical replacement that hides photon loss or extra flags.

## 6. N-photon lifting and the absolute PNR error

The N-boson Hilbert space is the symmetric subspace of the N-fold
one-particle tensor product, with normalized Fock states identified
isometrically. The passive action Gamma_N(U) is the restriction of
U^(tensor N); no factorial or extra dimension factor enters its norm.
The telescoping expansion of U^(tensor N)-V^(tensor N) has N terms,
each containing one U-V and otherwise unitary tensor factors. Therefore

    ||Gamma_N(U)-Gamma_N(V)||op<=N*||U-V||op.

For two normalized pure outputs phi,psi, their trace distance is
sqrt(1-|<phi,psi>|^2)<=||phi-psi||. Convex decomposition gives the same
upper bound for a common mixed input. Taking a complete PNR measurement
cannot increase trace distance: for any event its diagonal projector is
an effect, and its probability difference is bounded by trace distance.
Taking the largest event difference proves the TV bound in (2), using
||U-V||op<=||U-V||F. No factor two is lost. An overall optical phase can
make the vector-norm bound loose but never invalidates the inequality.

All counts, including code failures, are in this comparison. A common
classical decoder contracts TV. Conditioning on a rare accepted event
does not inherit the same bound without an acceptance-probability cost.
The error is absolute, not relative to a rare target probability or to
an optimizer's potentially small performance gap.

## 7. Exact boundary and the additional balanced-output restriction

If epsilon=0, (1) gives U=V. Nonnegative averaging also means every
balanced basis input individually has zero code leakage. Thus the
physical unitary is exactly block-local up to a whole-qubit permutation.
It cannot implement a deterministic entangling logical gate between
dual-rail qubits under these hypotheses. This is not a statement about
postselected or heralded gates.

Suppose additionally every balanced basis input has output logical
weight K with probability one, rather than merely remaining in the code.
For a fixed such input, V gives independent Bernoulli output bits with
parameters p_a=|Q_a[1,x_(pi(a))]|^2. A deterministic total implies

    0=Var(sum_a y_a)=sum_a p_a*(1-p_a).

Each p_a is therefore zero or one. Every input bit takes both values
somewhere in the balanced ensemble, so both columns of each Q_a have
one unit-modulus entry; unitarity makes their nonzero rows different.
Every Q_a is monomial, with local phases and either no flip or a flip.

Pull the set of flipped output pairs back to an input set F via pi.
For every input ones-set S of size K the output weight is |S symmetric
difference F|. Preservation of K requires |S intersect F|=|F|/2 for all
such S. If F is nonempty and not all qubits, choose b in F, c outside F
and a set T of K-1 other qubits. The sets T union {b} and T union {c}
contradict this constant intersection size. Thus F is empty or all N.
Conversely those two choices preserve K=N/2. The exact feasible-basis
actions are whole-qubit permutations, optional GLOBAL complement and
local basis phases. Arbitrary many-body phases are not supplied.

## 8. Why N=2 really is exceptional

Name the two pairs (a_0,a_1) and (b_0,b_1). Let U be the physical mode
permutation swapping a_1 with b_0 and fixing a_0,b_1. Balanced input 01
occupies a_0,b_1 and is fixed. Balanced input 10 occupies a_1,b_0; the
two occupied modes exchange and the bosonic Fock state is also fixed.
Hence balanced-average leakage is zero.

Input 00 instead maps a_0,b_0 to a_0,a_1, and input 11 maps a_1,b_1
to b_0,b_1. Both leave the code. This U is not a whole-pair permutation
with local pair unitaries: one rail of an input pair stays while the
other moves to the other pair. The two missing joint bit patterns have
zero probability in the balanced ensemble, exactly where the comparison
factor (N-1)/(N-2) fails. Bosonic commutation adds no fermionic exchange
sign to the fixed input 10. Thus N>=4 is necessary for this assertion
with the stipulated even balanced input family.

## 9. Classical comparator and a controlled adaptive consequence

For a known product code basis input, V sends each photon's pair to a
distinct output pair and applies only its local Q_a. PNR sampling is
exactly independent Bernoulli sampling followed by the pair permutation.
There are no overlapping output-pair paths between different photons;
the bosonic and distinguishable-particle PNR laws agree for this input.
A known cheaply sampled incoherent mixture of basis inputs is handled
by first sampling its classical label. The uniform balanced mixture is
one example: choose a uniform K-subset, then sample the local outputs.
The original physical source and any nontrivial mixture-generation cost
are still paid. No coherent Dicke preparation is declared free.

For arbitrary entangled input, (2) is still true but V need not have an
efficient known sampler: hardness could be in that input's amplitudes.
Thus a small-primitive local comparator is a source-dependent conclusion,
not a classical simulation theorem for every N-photon state.

Consider a measured/reset T-shot protocol with a common classical
count-driven controller. At EACH common history and shared random mark,
the chosen net U must satisfy the same full uniform-balanced-average
premise, with its value epsilon_h. A fresh common known input source
and the same decoder are used conditionally on that history; there is
no differing hidden coherent quantum memory between the protocols.
Choose V_h measurably as above; finite permutation ties and polar-basis
extensions can use fixed deterministic conventions. Explicitly the full-
rank local polar factor M(M^dagger M)^(-1/2) is continuous. On a rank-one
stratum choose its right singular vector from the first nonzero column
of M^dagger M with the corresponding coordinate positive, then complete
each two-dimensional basis by its canonical orthogonal vector. At rank
zero use I_2. These piecewise continuous choices are measurable. Put

    eta_h=min(1,2*N*sqrt[N*(N-1)^2*epsilon_h/(N-2)]).

Couple the next raw count distributions maximally whenever the prefixes
agree. Their chance of first divergence at that step is at most eta_h.
The common-prefix indicator is bounded by one, and its U-history
marginal is the true U protocol. Consequently

    TV(full U transcript, full V transcript)
       <=min(1,sum_(j=1..T) E_U[eta_(H_(j-1),mark_j)]).

A uniform per-step envelope gives the usual sum of those envelopes.
This also applies to any common classical final statistic or stopping
rule within the same raw-shot cap. It does not replace epsilon_h by
leakage on the single visited input, nor compare protocols with unequal
guaranteed shot budgets or equalize CPU/hardware costs. A coherent
unmeasured circuit or additional physical filter is outside this
measured/reset coupling claim.

## 10. Calibrated disposition

KEEP the quantitative physical stability theorem, its exact local/pair-
permutation boundary, the additional feasible-basis classification and
the explicit N=2 falsifier. Its TV coefficient is of order N^2*sqrt(epsilon);
very small uniform-average leakage is needed for a useful error bound,
and errors accumulate over controlled repeated shots. An observed small
visited-only leakage rate is not the required certificate.

No ancilla, monitored success branch, loss/postselection or stronger source
extension has been proved. No novelty, all-linear-optics no-go, practical
equal-cost advantage or physical device capability is claimed. The user's
positive optimizer objective remains OPEN. Future empirical estimates of
epsilon would require their own raw ensemble and uncertainty contract;
none was constructed or executed here.

Final mathematical proofreading checked the ordered bosonic moment,
factor six, pair-pattern probabilities, Hall/decomposition argument,
polar zero-singular-value extension, N-photon/trace/TV constant, exact
feasible-boundary classification, N=2 labels and history/source limits.
