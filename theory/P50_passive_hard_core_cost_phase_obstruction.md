# Passive hard-core cost phases — scoped analytic checkpoint

2026-11-25. ROOT derivation after P49, before P50 numerical evidence. This is
an auxiliary obstruction for a proposed cost-phase route, NOT the requested
positive optimizer result, a new novelty claim or a rejection of P50's
collision-retaining decoder. Status: self-derived; independent audit pending.

## Model and exact no-leakage statement

Let U be an N by N passive unitary, acting by a_i(out)=sum_a U_ia a_a(in).
Let 2<=r<=N and let H_CF,r be the span of ALL binary occupations of r photons
in these N modes. Assume the full number-preserving Fock action Gamma(U)
maps H_CF,r into H_CF,r with probability one for EVERY state in this subspace.
There is no conditioning, internal species, occupied ancilla or alternative
code subspace. Then U is monomial: one modulus-one entry per row and column.

Proof. For a CF basis input indexed by A, |A|=r, annihilation gives

    a_i(out)^2 |A> = 2 sum_(a<b in A) U_ia U_ib |A minus {a,b}>.

The residual basis states in this sum are pairwise orthogonal. Thus

    E_A[n_i(n_i-1)] = 4 sum_(a<b in A) |U_ia|^2 |U_ib|^2.             (1)

No leakage into collisions makes the left side zero. All summands are
nonnegative. Every pair a!=b belongs to at least one r-subset A; hence
U_ia U_ib=0 for every row i and every pair a!=b. Each row has at most one
nonzero entry, and unitarity forces exactly one modulus-one entry in each
row and each column. Conversely every such U permutes the binary occupation
basis and attaches products of one-mode phases, so satisfies the hypothesis.
This proves the characterization, including r=N. It fails for r=1, where
every passive unitary is collision-free, as it must.

The same calculation for only ONE fixed input A gives a narrower familiar
fact: zero collision probability implies disjoint supports of the occupied
columns. Each possible output then identifies at most one input assignment,
so the indistinguishable and distinguishable occupation laws coincide.
It does NOT force unused columns or the entire unitary to be monomial.
This agrees with the exact zero-collision limit of the prior replacement
certificate, rather than constituting a separate novelty claim.

## Consequence for a continuous balanced graph-cost oracle

Let N=2K, K>=2, C(S) the weighted undirected graph cut for |S|=K. Consider
trying to implement exp(-it C) exactly on the WHOLE balanced CF subspace by
a continuously differentiable passive family U(t) near t=0, with no loss,
collision leakage, measurement or postselection. A physically irrelevant
global phase on the encoded subspace is allowed. Such an implementation is
possible only if C is constant on balanced partitions.

Indeed the first statement forces every U(t) to be monomial. Continuity fixes
its permutation locally; a family implementing identity at t=0 may be taken
diagonal locally (an immaterial fixed relabeling can be removed). Its generator
on binary occupations has the form c+sum_(i in S) h_i, with real coefficients.
Differentiating the requested phase at0 therefore forces

    C(S)=c+sum_(i in S) h_i.                                        (2)

But C(S)=C(S-complement) for every cut, and both sets have K entries. Equation
(2) implies 2 sum_(i in S) h_i=sum_i h_i for EVERY K-subset. Comparing subsets
which differ by replacing i by j shows h_i=h_j for all i,j. Thus (2) is
constant. A nonconstant balanced graph-cut phase cannot be this deterministic
passive operation. This is a generator/no-leakage obstruction, not a theorem
about all measurable passive photon proposals.

The continuous-phase qualification matters. For integer edge weights, the
isolated phase t=pi has the alias

    exp(-i pi C(S))=exp(-i pi sum_(i in S) degree_i),

since C(S)=sum_(i in S)degree_i-2 sum_(i<j in S)w_ij. It IS a product of
one-mode phases even when C is nonconstant. It does not refute the continuous
oracle result; isolated phases modulo2pi cannot be differentiated as a family.
No stronger finite-angle exclusion is inferred.

## Scope and remaining route

The hard-core Johnson/XY generator is the projected hopping generator, but
exp(-it PHP) and P exp(-it H)P need not agree at finite t. The latter can leak;
final postselection does not establish deterministic projected evolution.
The characterization explains why simply naming passive hopping a balanced
cost-oracle/mixer does not solve this problem.

It does NOT cover P50's all-count ranking, operations which allow collisions,
heralded or measurement/feedforward constructions, occupied ancillas, genuine
nonlinearities, or dual-rail code spaces (a proper subset of all CF patterns).
Those routes require their own transformation and total success/loss/resource
accounting. No hardware capability or universal impossibility is concluded.
The finite-strength interaction route remains OPEN; this checkpoint closes
only its deterministic, passive, all-CF, no-leakage implementation shortcut.
