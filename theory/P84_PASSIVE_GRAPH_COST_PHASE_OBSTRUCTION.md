# P84: an exact passive graph-cost phase is continuously trivial

26 November 2026. **Primary verdict: proved as written below**, using the
reviewed P81 exact balanced-feasibility classification as a named input.
This new static derivation and self-review are not an independent P84
review, discovery/novelty certification or a generic optimizer no-go.
Only this file is written. P79 is frozen and untouched; no code, scientific
import, AST, test, RNG, matrix numerics, backend, QPU or manuscript action
was performed. All examples and algebra below are by hand.

## 1. Claim card and physical contract

Let N>=4 be EVEN and K=N/2. A graph has N logical vertices, symmetric
real edge weights w_ij=w_ji for i!=j, and no relevant self-loop terms.
Signed weights are allowed; nonnegative graph weights are a subclass.
Set w_ii=0 by convention and define the undirected cut cost

    C(S)=sum_(i in S,j not in S) w_ij,   |S|=K.

There are 2N physical modes (i,0),(i,1) and N indistinguishable photons,
ONE per logical rail pair. Logical ones count K, not the photon number.
The normalized code basis state is

    |S>=product_i a_(i,1_{i in S})^dagger |vac>.

For an angle gamma, a single fixed lossless passive U_gamma in U(2N)
implements the exact cost phase if, for EVERY balanced S simultaneously,

    Gamma_N(U_gamma)|S>
       =exp(i chi_gamma)*exp(-i gamma C(S))*|S>.             (1)

chi_gamma is an arbitrary common phase independent of S. The map may
depend on the graph and gamma but not on the input S. There are no
ancillary modes/photons, losses, heralds, postselection, intermediate
filters or nonlinear operations in this net map. Photon counts and
rail-pair labels are the same on input and output.

This is the usual all-basis phase-oracle condition, not agreement on one
chosen basis input, visited subset or one coherent balanced superposition.
Condition (1) automatically specifies the action on all their coherent
linear combinations. Its all-basis premise lets us form the counterfactual
uniform incoherent ensemble needed by P81; that ensemble need not actually
be prepared for this algebraic argument.

THEOREM. The following are equivalent under this contract:

A. There is a sequence gamma_n -> 0 with gamma_n!=0 for EVERY n,
   and such a U_(gamma_n) exists for EVERY n.
B. Such a U_gamma exists at EVERY real angle.
C. C(S) is constant over all balanced S.
D. There are real a_1,...,a_N such that w_ij=a_i+a_j for EVERY i!=j.

No continuity or differentiability of gamma -> U_gamma or chi_gamma is
needed. In particular any open interval of angles near zero suffices for
A. More generally any nonempty open interval is impossible for a
nonconstant cost, by the pointwise modular condition proved below.

For one isolated angle there are genuine exceptions: the necessary
condition is modular, not equality of real costs. We exhibit one in
section 7 rather than silently discarding that distinction.

## 2. Exact named dependency and implication graph

P81 exact balanced-feasibility classification: for even N>=4, a fixed
lossless passive unitary on these same 2N modes that sends EVERY balanced
code basis state into the balanced code with probability one must be a
whole-pair permutation, local monomial rail phases, and either no flips
or a GLOBAL bit complement. Its statement concerns all inputs, not leakage
on a visited subset. Its N=2 exception is not imported into N>=4.

Exact source: `theory/P81_dual_rail_balanced_average_stability.md`,
section 7, original commit `0a51544a1a449c64b87cb48e82bf637583402278`,
358 lines, SHA256
`7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f`.
Its independently reconstructed exact refinement is section 6 of
`research/P81_independent_dual_rail_stability.md`, original commit
`13ce8144b49ec91e916e9ca3f7b178c3490547bf`, SHA256
`b9261878a61760ab68a44c2519c2a76712f13673d73c21eee92eafac4b2f4fb0`.
The exact-source audit `theory/P81_EXACT_HASH_REVIEW.md`, integrated at
base commit `29cc86840c44c008b860ababeebc3da7c00f3c9c`, SHA256
`5abfd4c9e5fa86452b83fae995cbe754ddf35e39bc74b0007bc1033c1bcb64e0`,
passes that precise refinement. The exact-refinement passages and all
three source hashes were read/checked; P84 does not change or empirically
re-estimate P81.

The dependency graph is:

    (1) for every balanced basis input
       -> exact balanced feasibility -> P81 classification
       -> diagonality kills nontrivial permutation and global flip
       -> physical rail phases -> multiplicative subset phase
    C(S)=C(S^c)
       -> square of every phase is the same
       -> gamma*(C(S)-C(T)) lies in pi*Z
       -> accumulating angle set forces constant real cost
    constant balanced cut
       -> swap identities -> four-distinct-vertex identities
       -> additive edge weights w_ij=a_i+a_j
       -> constant balanced cut, and a common passive optical phase.

Only the first classification is a named prior-project input. All later
implications are proved internally below. There is no external citation,
numerical leaf, conjectural overlap bound or novelty premise.

## 3. Diagonality forces the physical pair action to be trivial

At each angle satisfying (1), exact balanced feasibility holds. Apply P81
and write tau for its permutation from input pairs to output pairs. The
deterministic output bits satisfy

    y_(tau(i))=x_i xor sigma,   sigma in {0,1}.

Here sigma=1 is the GLOBAL complement, not freely selected local flips.
Condition (1) requires y=x for all weight-K strings.

If sigma=0 and tau(i)!=i, choose a K-subset containing i but not tau(i).
It exists because 1<=K<=N-1. Then x_i!=x_(tau(i)), a contradiction.
Thus the no-flip branch forces tau to be the identity.

If sigma=1 and tau(i)=i, any balanced input with x_i=1 contradicts
x_i=1-x_i. If tau(i)!=i, choose a balanced subset containing BOTH i and
tau(i). This is possible because K>=2. It contradicts
x_(tau(i))=1-x_i. Consequently no globally complemented permutation
can fix every balanced basis state. This argument already works at
N=4,K=2; there is no six-state degeneracy allowing a hidden complement.

Therefore U_gamma itself is diagonal on all physical rails, with entries
alpha_(i,0),alpha_(i,1) of modulus one. Bosonic permutation signs do not
appear; the occupied-mode creation operators commute. Put

    z_i=alpha_(i,1)/alpha_(i,0),
    B=exp(-i chi_gamma)*product_i alpha_(i,0).

Then (1) gives, at this angle,

    f_gamma(S):=exp(-i gamma C(S))=B*product_(i in S) z_i.     (2)

Thus the cost PHASE is affine in the bits modulo2pi at a fixed angle.
Equation (2) makes no continuous choice of arguments of B or z_i and
does not incorrectly turn this modular affinity into real affinity.

## 4. Complement symmetry removes continuous nontrivial cost phases

Every undirected cut satisfies C(S)=C(S^c). Since K=N/2, both subsets
belong to the domain. Multiplying (2) for S and S^c gives

    f_gamma(S)*f_gamma(S^c)=B^2*product_(i=1..N) z_i.

The left side is f_gamma(S)^2. Hence for EVERY two balanced subsets S,T,

    exp[-2i gamma*(C(S)-C(T))]=1,
    gamma*(C(S)-C(T)) in pi*Z.                              (3)

This is an exact pointwise invariant. If a nonzero difference D existed,
the allowed gamma would lie in the discrete lattice (pi/D)*Z. It cannot
contain a sequence of nonzero angles tending to zero or any nonempty open interval.
Equivalently, along gamma_n->0, eventually |gamma_n D|<pi; (3) would force
gamma_n D=0, contradicting gamma_n!=0 and D!=0. Thus A implies C.

A useful sharpened single-angle statement avoids any continuity premise.
Let R=max_S C(S)-min_S C(S)>0. A realizable angle must obey

    gamma*R in pi*Z.

In particular NO angle with 0<|gamma|<pi/R is realizable. The entire
set of possible angles is contained in the intersection of the lattices
required by all cost differences. This condition is NECESSARY, not claimed
sufficient. It permits antipodal phases at an isolated admissible angle;
it does not assert f_gamma itself is constant there.

## 5. Characterization of graphs with constant balanced cut

Assume C is constant on all K-subsets. Write

    d_i=sum_(j!=i) w_ij,
    C(S)=sum_(i in S) d_i -2*sum_(i<j, i,j in S) w_ij.

For distinct i,j and T excluding them with |T|=K-1, compare T union{i}
and T union{j}. Their equal costs imply

    d_i-d_j=2*sum_(k in T)(w_ik-w_jk).                     (4)

For four distinct i,j,k,l, choose T0 of size K-2 excluding all four.
This is possible at every even N>=4 since 0<=K-2<=N-4. Use (4) with
T=T0 union{k} and T=T0 union{l}, then subtract:

    w_ik-w_jk=w_il-w_jl.

Permuting the four labels gives all three matching sums equal:

    w_ij+w_kl = w_ik+w_jl = w_il+w_jk.                     (5)

There is no large-N-only step here. At N=4, T0 is simply empty.

Conversely (5) produces additive vertex parameters explicitly. Define

    a_1=(w_12+w_13-w_23)/2,
    a_2=(w_12+w_23-w_13)/2,
    a_3=(w_13+w_23-w_12)/2,
    a_r=w_1r-a_1 for r>=4.

The first three edges already have w_ij=a_i+a_j. Applying (5) to
1,2,3,r gives

    w_2r=w_1r+w_23-w_13=a_2+a_r,
    w_3r=w_1r+w_23-w_12=a_3+a_r.

For distinct r,s>=4, apply it to 1,2,r,s:

    w_rs=w_1r+w_2s-w_12=a_r+a_s.

At N=4 there is only one r>=4, so this last class of edges is empty;
the earlier checks already cover all six edges. This proves C implies D
without an N=4 exception.

If w_ij=a_i+a_j, its cut cost is

    C(S)=(N-K)*sum_(i in S)a_i + K*sum_(j not in S)a_j
        =K*sum_i a_i,                                    (6)

which is constant at K=N/2. Thus D implies C. The parameters are unique
for N>=3: a zero sum b_i+b_j on every distinct pair forces each b_i=0
by any triangle. A direct recovery/certificate formula is

    W=sum_(i<j) w_ij,
    a_i=[d_i-W/(N-1)]/(N-2),
    C_bal=K*W/(N-1).

These formulas apply to the additive class, not every graph. For
nonnegative edge weights the constraint is a_i+a_j>=0; the individual
a_i need not be nonnegative. Self-loop weights are irrelevant to cuts
and are not subject to this offdiagonal characterization.

## 6. Converse physical realization and exact theorem completion

If C(S)=c for all balanced S, take

    U_gamma=exp(-i gamma c/N)*I_(2N).

It is passive and lossless; its N-photon action is exactly
exp(-i gamma c) on EVERY N-photon state. Thus C implies B, and B trivially
implies A. All four statements in section 1 are therefore equivalent.
Up to the allowed common phase, identity optics already implements this
cost oracle. The constant cost contains no balanced-optimization signal.

## 7. Boundary counterchecks and non-claims

* N=4 check. The three complementary balanced cuts are constant iff
  w_12+w_34=w_13+w_24=w_14+w_23. These are precisely (5), and the above
  four a_i reconstruct all six edges. The complement-permutation escape
  is separately excluded by section 3, not assumed absent by genericity.
* Nonuniform constant-cost graph. A star with unit incident edges and
  all other edges zero is additive with a_center=1 and other a_i=0.
  Every balanced cut has cost K. The theorem does NOT say only uniform
  complete graphs have constant balanced cuts.
* Single-angle counterexample to an overstrong no-go. If every w_ij is
  an integer, then for every bit string

      C(x)=sum_i d_i x_i -2*sum_(i<j) w_ij x_i x_j.

  At gamma=pi this gives exp(-i pi C(x))=product_i(-1)^(d_i x_i).
  Local rail phases alpha_(i,0)=1, alpha_(i,1)=(-1)^d_i implement it.
  For N=4 with only w_12=1, balanced costs are0 or1, yet this isolated
  angle is passive. It reveals parity, not a continuous exact cost oracle.
* At gamma=0 identity works for every graph; one angle0 cannot replace
  the nonzero accumulating-angle premise. At N=2 P81's classification
  fails, but the two balanced cut values are equal trivially. No N=2
  physical classification or new extension is claimed here.
* Approximation is different. Identity optics is already within
  |gamma|*sum_(i<j)|w_ij| of a small-angle target on this diagonal code,
  since |exp(-it)-1|<=|t|. No quantitative approximate-oracle lower bound
  follows from this exact result. It is not a leakage-estimation theorem.
* Ancillas, heralding/postselection, losses, nonlinear/nonpassive gates,
  state-dependent maps and agreement on only a selected input change
  the premises. Their preparation, failure and photon costs remain real;
  this theorem neither rules them out nor declares them available/free.
* No assertion about an arbitrary passive optimizer, a different graph
  encoding, entangled source resources, approximate coherent algorithms,
  or measured/reset hybrids follows. In particular P65 benchmarks and
  the user's positive optimizer objective are not resolved by this oracle
  representability obstruction.

## 8. Obligation status and review boundary

| Obligation | Status | Basis |
| --- | --- | --- |
| Physical modes/photons, uniform all-basis premise | passed | Section1 and (1) |
| Exact feasible classification | named reviewed input | P81 section7, exact hashes above |
| Logical action faithful including N=4 | passed internally | Containing/excluding both labels in section3 |
| Modular phase, global phase and complement | passed internally | Product identity (2)-(3), no logarithm branches |
| Parameter regularity | passed internally | None needed; lattice/accumulation argument |
| Additive-weight characterization and N=4 | passed internally | Swaps (4), four-point (5), explicit reconstruction |
| Converse and constant-cost meaning | passed internally | (6) and common optical phase |
| Isolated angles, approximate maps, source restrictions | explicit boundaries | Section7 |
| Novelty, positive optimizer, hardware validation | out of scope | No such claim or execution |

No remaining internal implication is left open in the normalized theorem,
conditional only on the precisely stated reviewed P81 classification.
The present audit of the new derivation is a SELF-REVIEW; independent P84
reconstruction/exact-source audit is the next review obligation. Only file
reads, skill/instruction reads, hash checks and isolated Git operations
accompany this static proof. No scientific computation supports or replaces
any universal step. Paper, shared state, P79 and QPU access are untouched.
