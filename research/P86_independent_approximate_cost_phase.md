# P86: a quantitative passive dual-rail cost-phase obstruction

Primary verdict: **proved under the hypotheses below**. The proposed
lower bound for worst balanced-basis state-vector error is correct,
with its stated constants and a COMMON global phase. For a fixed
nonconstant complement-invariant cost, first-order accuracy o(|gamma|)
as gamma tends to zero is impossible in this lossless no-ancilla passive
model. This is not a probability-only or general optimizer obstruction.

Independent before-author-reading reconstruction of ROOT's supplied
candidate, 26 November 2026, beginning at
`57068159d45b0881960bfa71804a30c826d345f9` on
`research/p66-dark-barrier`. No ROOT P86 file, other P86 derivation or
verdict was read. ROOT supplied the route and constants before this
reconstruction; this is not independent discovery or a novelty claim.
Only this file is written. No scientific code/import, AST, test, RNG,
matrix numerics, backend, QPU or manuscript action was performed.

## 1. Physical objects, metric and precise claim

Let N>=4 be even, K=N/2. The physical system has 2N dual-rail modes and
N indistinguishable photons, one per qubit in each code basis input.
For a balanced ones-set S, |S|=K, write |S> for its normalized code
Fock state. K counts logical ones, not photons. Let C be any fixed
real function on these sets satisfying C(S)=C(S^c); weighted graph cut
is a special case. No graph-weight classification is assumed.

Let U be a fixed lossless passive unitary on these same 2N modes.
There are no ancillary modes, heralded branches, loss, discarded
outputs or intermediate quantum filters. Write Gamma_N(U) for its
N-photon action. For a real angle gamma define

    delta=inf_(chi in R) max_(|S|=K)
       ||Gamma_N(U)|S>-exp(i*chi-i*gamma*C(S))|S>||_2.

The phase chi is one COMMON phase across the entire balanced basis.
The maximum is over finitely many continuous functions of exp(i chi),
and that phase circle is compact, so the infimum is attained. Fix a
minimizing chi and write f_S=exp(i chi-i gamma C(S)).

Set

    C_N=4*N*(N-1)^2/(N-2),
    b_N=1+N*sqrt(C_N).

For every balanced S,T, the claim is

    delta >= |sin(gamma*(C(S)-C(T)))|/(2*b_N).                (1)

In particular, if R=max C-min C on the balanced family,

    delta >= |sin(gamma*R)|/(2*b_N).                         (2)

R is an analysis parameter, not an optimum supplied to a circuit or
encoder. The pairwise statement (1) can be stronger than the range
statement at angles where sin(gamma R) happens to vanish.

## 2. The exact P81 dependency and leakage bound

The accepted dependency is the P81 physical stability theorem in
`theory/P81_dual_rail_balanced_average_stability.md`, independent commit
`0a51544a1a449c64b87cb48e82bf637583402278`, SHA256
`7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f`.
Its unchanged bytes were hash-checked for this reconstruction. P81 uses
the same N photons, 2N physical modes and no-ancilla lossless model.

Let P_code project onto the one-photon-per-pair code. Since f_S|S>
is in the code and projection is contractive,

    ||(I-P_code) Gamma_N(U)|S>|| <= delta

for every balanced S. Its squared norm is raw code-failure probability,
including collisions and wrong-qubit photon mass. Thus the UNIFORM
INCOHERENT balanced-basis average leakage epsilon satisfies

    epsilon <= delta^2.

This bounds the complete counterfactual average required by P81, not
merely leakage on a visited input. Applying P81 produces a physical
block-permutation unitary V, with V_(a,pi(a))=Q_a for local 2-by-2
unitaries Q_a, such that

    ||U-V||_F <= sqrt(C_N)*sqrt(epsilon)
                <=sqrt(C_N)*delta.                         (3)

There is no approximate monomial or approximate graph-weight conclusion
in (3). In particular Q_a may mix its two rails, and V need not preserve
balanced logical weight exactly.

## 3. N-photon comparison without a column-to-operator shortcut

On the full N-fold one-particle tensor product, telescope
U^(tensor N)-V^(tensor N). Its N terms each contain one U-V and
otherwise unitary factors. Restricting to the symmetric bosonic sector
therefore gives

    ||Gamma_N(U)-Gamma_N(V)||op<=N*||U-V||op
                                <=N*||U-V||_F.

For each balanced basis vector separately, the triangle inequality and
(3) now imply

    ||Gamma_N(V)|S>-f_S|S>||
      <=N*sqrt(C_N)*delta+delta=b_N*delta=:e.                 (4)

We have NOT inferred an operator-norm bound delta for the target
oracle from its basis-column errors. Such an inference could introduce
a dimension factor and is invalid in general. The operator estimate
above compares the two physical passive unitaries using P81; (4) then
uses the target error only on the individual column being considered.
The photon tensor factor is N, not K or 2N.

If e>=1/2, equation (1) already follows because

    delta=e/b_N>=1/(2*b_N)>=|sin(gamma*(C(S)-C(T)))|/(2*b_N).

It remains to handle e<1/2; no continuity or small-gamma assumption
enters this branch split.

## 4. Small column error forces the pair permutation to be identity

Define A_S=<S|Gamma_N(V)|S>. The two states in (4) are normalized.
Squaring their distance gives

    2-2 Re(conj(f_S)*A_S)<=e^2,
    |A_S|>=1-e^2/2>7/8.                                    (5)

The weak scalar estimate |A_S-f_S|<=e also follows by taking the
projection onto |S>. These are phase-aligned statements with the same
chi, not a separate phase fit for every input.

Write x_a=1 if a belongs to S and zero otherwise. Since V sends each
input pair to a distinct output pair, its N-photon diagonal amplitude
is exactly

    A_S=product_(a=1..N) (Q_a)_(x_a,x_(pi(a))).              (6)

This follows by transforming the N creation operators, one per pair,
and taking the target coefficient. All output pairs are distinct; the
factors commute as bosonic creation operators, with no exchange sign
or factorial factor. Every factor has modulus at most one.

Suppose some pi(a)=b!=a. There is a balanced string S_0 with
x_a=x_b=0: choose its K ones among the other N-2 positions, possible
because K<=N-2 for N>=4. There is also a balanced S_1 with x_a=0,
x_b=1: choose the remaining K-1 ones among the other positions. Then
(6) and (5) imply respectively

    |(Q_a)_00| >= |A_(S_0)| >7/8,
    |(Q_a)_01| >= |A_(S_1)| >7/8.

But these are the two entries of one row of the unitary Q_a, so their
squared moduli sum to one, whereas 2*(7/8)^2>1. This is a contradiction.
Hence pi is identity. The construction also works at N=4, where S_0
uses both remaining positions. This argument does not presuppose
that Q_a is monomial or near diagonal.

## 5. Complement amplitude product and the sine lower bound

With pi identity, (6) becomes

    A_S=product_a (Q_a)_(x_a,x_a).

Even for nonmonomial local Q_a, this gives the EXACT invariant

    A_S*A_(S^c)=product_a (Q_a)_00*(Q_a)_11=:L,

independent of S. No division by a diagonal entry is used, so zero
diagonal entries cause no hidden algebraic exception. We only
use |A_S|<=1 and |A_S-f_S|<=e. Since f_(S^c)=f_S,

    |L-f_S^2|
      <=|A_S|*|A_(S^c)-f_(S^c)|
                         +|f_(S^c)|*|A_S-f_S|
      <=2e.

The same bound holds for T, so

    |f_S^2-f_T^2|<=4e.

The common global phase cancels in the left-hand modulus, and

    |f_S^2-f_T^2|=2*|sin(gamma*(C(S)-C(T)))|.

Thus e>=|sin(gamma*(C(S)-C(T)))|/2. Combining with e=b_N delta
proves (1) in the small-e branch; section 3 proved the other branch.
Taking the maximizing/minimizing pair proves (2). All inequalities
are non-strict in the final result, including the e=1/2 boundary.

## 6. First-order consequence and operator-norm interpretation

Fix N and a nonconstant C, so R>0. For ANY choice of passive U_gamma,
possibly discontinuous in gamma, equations (1)-(2) imply

    liminf_(gamma->0, gamma!=0) delta(U_gamma,gamma)/|gamma|
       >=R/(2*b_N)>0.

This uses the elementary limit |sin(gamma R)|/|gamma|->R.
Consequently o(|gamma|) error is impossible in this metric. The bound
holds uniformly over choices of U at each fixed angle, so optimizing
over passive unitaries cannot remove it. It is a fixed-N, fixed-cost
statement; if N or the cost function varies with gamma the constants
must remain visible. If C is constant the bound is zero and identity
with a suitable common phase gives zero error at every angle.

Let H_bal be the span of the balanced code basis, and D_gamma|S>
=exp(-i gamma C(S))|S>, viewed as a map into the full N-photon space.
Define the corresponding restricted operator error

    Eop=inf_chi ||Gamma_N(U)|_(H_bal)-exp(i chi)D_gamma||op.

For each chi, an operator norm dominates every basis-column norm;
taking the maximum and then the infimum gives Eop>=delta. Hence the
same lower bound applies to this stronger operator error. No reverse
inequality or dimension-free upper bound Eop<=delta is claimed.

## 7. Scope falsifiers and limitations

The COMMON chi is essential. If a separate phase were allowed for
every S, U=I would have zero error against the ray of every target
f_S|S> for any cost or angle. Likewise each such basis input has unit
target-state fidelity and the correct deterministic PNR output under
identity. Therefore (1) is not a lower bound on per-basis infidelity,
code leakage alone, trace distance to a target ray, or raw PNR error.
It constrains a coherently specified relative-phase oracle. A lower
bound in this vector metric does not directly imply a PNR-TV lower
bound on those basis inputs.

The result need not be positive at periodic angles. For integer graph
weights and degrees d_i, the identity C(S)=sum_(i in S)d_i minus twice
the internal edge weight gives exp(-i*pi*C(S))=product_(i in S)(-1)^(d_i),
a local degree-parity phase. Cost differences are integers and every
sine in (1) vanishes. This is a hand consistency example, not an
additional proof dependency. Conversely vanishing of the sine bounds is not
claimed sufficient for implementing a desired isolated-angle phase.
No approximate classification w_ij approximately a_i+a_j is asserted.

The theorem assumes the entire balanced basis and the physical model
of P81. It does not cover input-dependent source redesign, a requirement
on one visited string or prepared state only, ancillas, heralding,
postselection, loss, intermediate measurements/filters or nonlinear
resources. It supplies no lower bound for generic sampling optimizers
that use collisions or do not implement this cost-phase oracle. No
continuity, gate-by-gate compiler or edge-gate-count assumption is used.

KEEP the quantitative obstruction with its common-phase metric and
explicit constants. REJECT treating it as an all-approximation or
all-optical-optimizer no-go. It does not produce a positive optimizer,
device capability, novelty or equal-resource advantage; the user's
positive objective remains OPEN. No numerical plan or execution is
authorized by this proof.

Final mathematical proofreading checked compact phase minimization,
epsilon<=delta^2, P81's constant and N-photon lift, both e branches,
the N=4 permutation witnesses, local amplitude products, global phase,
the factor two in the sine identity and the column/operator distinction.
