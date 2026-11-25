# P84: exact balanced cut phases under passive dual-rail dynamics

Primary verdict: **proved under the exact hypotheses below**. A nonconstant
balanced cut function cannot have its exact diagonal cost phase implemented
at any nonzero angle smaller than pi divided by its balanced cost range,
using only a fixed lossless passive unitary on the 2N dual-rail modes.
A sequence of such implementations at nonzero angles tending to zero
exists if and only if the balanced cut function is constant. No continuity
of the implementing physical unitaries is assumed. There are genuine
single-angle exceptions, including integer-weight cut phases at pi.

Independent before-author-reading reconstruction of ROOT's candidate,
26 November 2026, starting at `d1749a1778f1107c3887f76b0c58cb715c4b94ec`
in `research/p66-dark-barrier`. ROOT supplied the candidate formulas
before this derivation. No other P84 source or verdict was read and no
other P84 agent was contacted. This is not independent discovery or an
originality claim. Only this file is written. No scientific code/import,
AST, test, graph generation, RNG, matrix numerics, native backend, QPU
or manuscript action was performed.

## 1. Precise physical and graph statement

Let N>=4 be even, K=N/2. There are N indistinguishable photons and
2N physical modes, with exactly one photon per dual-rail pair in a
logical code basis input. For a ones-set S of size K, write |S> for
that normalized code Fock state. K counts logical ones, not photons.

Let w_ij=w_ji be fixed real off-diagonal graph weights, with w_ii=0;
zero weights represent absent edges. Signed weights are allowed for
the mathematical theorem. Nonnegative weighted graphs are a subclass.
Use the unordered-edge cut convention

    C(S)=sum_(i in S, j notin S) w_ij,

so each crossing edge is counted once. In particular C(S)=C(S^c).
No optimum is supplied to the implementation.

At a fixed real angle gamma suppose a lossless passive single-particle
unitary U_gamma on exactly these 2N modes satisfies

    Gamma_N(U_gamma)|S>
        =a_gamma*exp(-i*gamma*C(S))*|S>                       (1)

for EVERY size-K set S, with one common |a_gamma|=1. There are no
ancillas, losses, intermediate measurements or heralded success branches.
This is an operator condition on the entire balanced subspace, not a
condition only on a visited input or one prepared coherent superposition.
Changing gamma may change U_gamma arbitrarily.

Define the finite balanced range

    Delta=max_(|S|=K) C(S)-min_(|S|=K) C(S).

Delta is used to state a mathematical obstruction; it is not queried
by a circuit, training loop or graph-encoding rule in this note.

## 2. The accepted physical rigidity dependency and diagonality

The only nontrivial external-to-this-file proof dependency is the
accepted exact part of P81, here in
`theory/P81_dual_rail_balanced_average_stability.md`, independent commit
`0a51544a1a449c64b87cb48e82bf637583402278`, SHA256
`7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f`.
Its unchanged hash was checked for this reconstruction. P81 applies to
the same N photons, 2N modes and lossless no-ancilla passive model.

Equation (1) gives zero raw code leakage on every balanced basis input.
It also leaves output logical weight K exactly fixed. Hence P81's
exact classification gives local monomial two-mode unitaries, a
whole-qubit permutation, and either no bit flips or GLOBAL complement,
with local phases. No approximate rigidity statement is being substituted.

Let sigma be the induced permutation of input qubit labels. With no
complement, diagonal action in (1) requires sigma(S)=S for every size-K
set. This forces sigma to be identity. If sigma(i)=j!=i, choose a
size-K set containing i but excluding j; then j belongs to sigma(S)
but not S, a contradiction. Such a set exists since 1<=K<=N-1.

With global complement, diagonality instead requires sigma(S)=S^c for
every size-K S. For any i, choose S containing i and sigma(i). When
these labels differ this is possible because K>=2; when they coincide
choose any balanced S containing i. Then sigma(i) lies in both sigma(S)
and S, a contradiction. This excludes the complement alternative also
at N=4, rather than treating it as an unexamined small-size exception.

Thus the physical unitary is rail-diagonal: each logical qubit has
rail phases alpha_i0,alpha_i1, with |alpha_i0|=|alpha_i1|=1. Bosonic
second quantization on the code basis gives precisely

    Gamma_N(U_gamma)|S>
       =(product_i alpha_i0)*product_(i in S)(alpha_i1/alpha_i0)*|S>.

There is no exchange sign or extra factor K in this N-photon phase.
After absorbing the common a_gamma, define

    f_gamma(S)=exp(-i*gamma*C(S))=B_gamma*product_(i in S) z_i, (2)

with B_gamma and every z_i unit modulus. Conversely any expression
of this form on the balanced sets is implemented by local rail phases,
up to the allowed common phase. Thus no nonlocal diagonal action has
been hidden by the restricted balanced input domain.

## 3. Complement symmetry, small-angle obstruction and exact scope

For the expression (2),

    f_gamma(S)*f_gamma(S^c)=B_gamma^2*product_(i=1..N) z_i,

independent of S. Since cut complement symmetry gives
f_gamma(S)=f_gamma(S^c), its square is independent of S. Consequently
for every pair of balanced sets S,T,

    exp[-2i*gamma*(C(S)-C(T))]=1,
    gamma*(C(S)-C(T)) belongs to pi*Z.                       (3)

When Delta>0 take a maximizing and minimizing pair. If
0<|gamma|<pi/Delta, then gamma*Delta is nonzero with magnitude less
than pi, and cannot be an integer multiple of pi. Equation (1) is
therefore impossible throughout this open punctured interval.
The endpoint is not excluded by this argument, and (3) alone is not
a sufficient implementation criterion at arbitrary isolated angles.

If nonzero gamma_n tend to zero and each admits (1), Delta>0 contradicts
the preceding interval for all sufficiently large n. Thus C is constant.
If C(S)=C_0 on the balanced domain, U_gamma=I works at every angle with
a_gamma=exp(i*gamma*C_0). Alternatively the common physical rail phase
exp(-i*gamma*C_0/N) implements the scalar with a_gamma=1. This proves
both directions without a differentiable, continuous or consistently
compiled family U_gamma. A sequence eventually equal to zero is not
the nonzero-angle sequence quantified here.

For completeness one can sharpen the isolated-angle condition without
using a graph optimum. From the common square in (2), compare any
balanced set containing i but not j with the set exchanging i for j.
Their ratio is z_i/z_j, so (z_i/z_j)^2=1. Hence z_i=z*eta_i with
eta_i in {+1,-1}, and

    f_gamma(S)=c*product_(i in S) eta_i.

Complement symmetry forces product_i eta_i=1, that is an even number
of negative eta_i. Conversely such a parity phase is local and
complement invariant. Thus, in this model, an isolated angle is
implementable exactly if its balanced cost-phase values coincide with
a common phase times parity on an even-cardinality vertex set. Merely
taking two possible phase values is not sufficient. This classification
does not presume that finding such an angle is useful for optimization.

## 4. Which graph costs are constant on all balanced sets?

The exact characterization for every even N>=4, including N=4, is

    C(S) constant for |S|=K
      iff w_ij=a_i+a_j for all distinct i,j                  (4)

for real vertex coefficients a_i. The coefficients need not be
nonnegative even if all edge weights are nonnegative. This statement
concerns off-diagonal weights only; the zero diagonal is not required
to equal 2a_i.

The reverse implication is immediate by direct counting:

    C(S)=K*sum_(i in S) a_i+K*sum_(j notin S) a_j
        =K*sum_i a_i.

For necessity fix distinct i,j and put R=V minus {i,j}. For every
T subset R of size K-1, compare S_i=T union {i} and S_j=T union {j}.
The edge ij crosses both cuts and cancels. Setting d_k=w_ik-w_jk gives

    0=C(S_i)-C(S_j)=sum_(k in R minus T) d_k-sum_(k in T) d_k.

All size-(K-1) subset sums of d are therefore equal. For any distinct
k,l in R choose T_0 subset R minus {k,l} of size K-2 and compare
T_0 union {k} with T_0 union {l}. This is possible even for K=2,
when T_0 is empty. It follows that d_k=d_l. Thus for all four distinct
labels,

    w_ik+w_jl=w_il+w_jk.

Relabeling gives equality of all three opposite-pair sums,

    w_ij+w_kl=w_ik+w_jl=w_il+w_jk.                          (5)

Now choose reference vertices 1,2,3 and define

    a_1=(w_12+w_13-w_23)/2,
    a_2=(w_12+w_23-w_13)/2,
    a_3=(w_13+w_23-w_12)/2.

For i>=4 put a_i=w_i1-a_1. The identities on {1,2,3,i} give
w_i2=a_i+a_2 and w_i3=a_i+a_3, while w_i1=a_i+a_1 by definition.
For distinct i,j>=4, the identity on {1,2,i,j} then gives

    w_ij+w_12=w_i1+w_j2,

so w_ij=a_i+a_j. At N=4 there is no pair of distinct i,j>=4 to check;
the preceding four-label identities already cover every edge. This
explicitly proves (4) without assuming five or more vertices.

The coefficients are unique for N>=3: if b_i+b_j=0 on every edge of
the complete index set, three distinct indices force every b_i=0.
They can also be constructed solely from graph sums. Let

    d_i=sum_(j!=i) w_ij,       W=sum_(i<j) w_ij.

Once (4) holds, W=(N-1)*A and d_i=(N-2)*a_i+A, where A=sum_i a_i.
Therefore the equivalent explicit candidate is

    a_i=[d_i-W/(N-1)]/(N-2).

Checking its off-diagonal sums is a graph-only criterion; it does not
require an optimal cut, C* or a favorable graph selection. In this
class every balanced subset already has the same cost, so the scalar
cost phase carries no balanced optimization information.

## 5. A real single-angle exception: integer-weight phases at pi

For integer edge weights, including signed integers, degrees d_i are
integers and every cut satisfies the exact identity

    C(S)=sum_(i in S) d_i-2*sum_(i<j, i,j in S) w_ij.

At gamma=pi this yields

    exp(-i*pi*C(S))=product_(i in S) (-1)^(d_i).

It is implemented by a local Z on the 1-rail of each odd-degree vertex,
with all 0-rails unchanged. This equality holds on every code basis
string, not only balanced ones, even when the balanced cost is
nonconstant. The number of odd-degree vertices is even because
sum_i d_i=2W, agreeing with section 3's parity criterion.

More generally integer multiples of pi give such local phases or the
identity. Periodic isolated angles therefore cannot be ruled out by
a statement about nonzero angles approaching zero. They also do not
make the ordinary graph cut a continuously available entangling oracle:
at these exceptional angles its phase has aliased to a local parity
function. No useful mixer/optimizer conclusion follows from that alias.

## 6. Limits, dependencies and calibrated disposition

The inference chain is exact: (1) implies P81's zero-leakage and
balanced-output premises; its physical classification plus diagonal
action gives local phases (2); complement symmetry yields (3); the
balanced exchange identities give the graph characterization (4).
The only accepted proof imported is P81's exact rigidity theorem with
the hash in section 2. The phase/combinatorial arguments here are
internal and have no numerical or external literature premise.

This is not a lower bound on the number of compiled edge gates, not
an approximate-implementation obstruction and not an assertion about
all single angles. It does not cover ancillas, heralding/postselection,
loss, intermediate filters, nonlinear resources, an enlarged source,
or a requirement imposed only on selected/visited inputs. Preparation
of one desired state is weaker than an operator identity on every
balanced basis vector. Coherent input alone does not remove that
operator requirement; replacing the requirement changes the problem.

The angle interval uses the graph's true range only in analysis. No
algorithm, source or encoder is given an optimum. A constant balanced
cost provides no meaningful test of positive graph optimization. The
isolated-angle parity exceptions and all omitted resource models must
remain visible; none is classified as impossible by this note.

KEEP the exact small-angle/accumulating-angle obstruction in the stated
physical model and the explicit constant-cut graph criterion. REJECT a
broader claim banning all passive photonic optimizers, all cost angles
or an authorized hardware capability. The user's positive optimizer
objective remains OPEN. No experiment, code qualification, new circuit
or paper action is authorized by this static result, and no novelty
or equal-resource advantage is claimed.

Final mathematical proofreading checked complement/permutation faithfulness
at N=4, photons versus logical ones, global phase, the open angle interval,
nonzero sequence quantifier, all four-point/exchange identities, uniqueness
of the vertex coefficients, signed-weight conventions and periodic angles.
