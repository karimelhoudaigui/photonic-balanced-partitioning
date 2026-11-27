# P146 — Independent review of the resource-to-algorithm veto

27-Nov-2026, P66. Primary verdict: **proved as written in the stated algebraic
scope**. Identity(1), the purge counterexample and one-wire transfer are correct.
The full all-branch optimization algorithm remains INCOMPLETE, as the source
explicitly says. No new optimizer, implementation or performance conclusion.

FULL117-line original251988d828d38feb337ae5a32f71e08feca7a907,
research/P146_ALGORITHM_BRIDGE_VETO.md, SHA256
cfa727e86c7811ff78133e529428f214597a2a2e8e07ba424ad07bc0bb1dad26.
Independent non-author hand reconstruction; earlier A review is separate.
Only this review written. No import/AST/program/numerical evaluation, graph,
RNG/test/native/runner/QPU or scientific raw-data access. No author edits.

## Mean identity and signs

Use exactly U=exp(+i sum theta_uv Z_uZ_v), |+> input,
R=product exp(-i beta_u X_u), zero local fields, and corrected local byproducts.
R-dagger Z_a R=c_a Z_a+s_a Y_a. The ZZ contribution has zero |+> expectation.
For O=Z_aY_b, the direct generator Z_aZ_b anticommutes with O and
(Z_aZ_b)O=-i X_b. Thus U-dagger O U has the term -sin(2theta_ab)X_b.
Averaging the other b-neighbor rotations contributes
product_(k!=a,b)cos(2theta_bk)=P_b^a. All other terms retain a non-X Pauli
and vanish in the product |+> expectation. This verifies the MINUS sign.

The direct edge commutes with Y_aY_b. Condition on the remaining uniform
Z eigenvalues z_k and set A=sum theta_ak z_k, B=sum theta_bk z_k.
Each single Y expectation is -sin(2A) or -sin(2B), so their product is
sin(2A)sin(2B). The cosine difference identity and independent z_k give
(Q_- - Q_+)/2. Multiplication by c_a s_b,s_a c_b,s_a s_b gives exactly(1).
An absent direct edge is theta_ab=0; triangles/common neighbors still enter
the YY term. For one isolated edge, Q_-=Q_+=1 and the result is
-sin(2beta_a+2beta_b)sin(2theta_ab), the stated equal-beta specialization.
Isolated spectator vertices, zero beta and vanishing cosine factors
cause no singularities; the formula uses products, not unsafe divisions.

Let g_C count COST pairs and Delta_I the maximum degree of the INTERACTION
graph supporting theta. Each P/Q needs at most O(Delta_I+1) scalar factors,
using its two endpoint neighbor lists. The mean cost therefore takes
O(g_C*(Delta_I+1)) arithmetic after paid input/setup. There is no need for
cost/resource edges or degrees to agree. Dense interaction graphs still give
a polynomial bound; sparse resource degree must not replace Delta_I for an
unrelated algorithm interaction graph. Preparation-edge count g_A is a third
quantity unless the compiled model identifies them explicitly.

This is an arithmetic identity, not constant-time exact transcendental
arithmetic. Certified trigonometric evaluation, coefficient/angle bit sizes,
precision accumulation, classical parameter search and compilation are not
an implemented finite-bit or measured wall-time result here.
For C=C0-sum J_ab Z_aZ_b the source's J is the displayed logical coefficient.
For a physical paired cut with aggregate K_ab=sum sigma*tau*w_(aσ,bτ), use
J_ab=K_ab/2. This convention matches A's angle gamma*K_ab/2; no factor conflict.

No-local-fields is essential, not cosmetic. With only local rotations
exp(i h_a Z_a), exp(i h_b Z_b) before R, the two-spin mean is
s_a s_b sin(2h_a)sin(2h_b), generically nonzero although(1) with theta0 gives0.
Uncorrected weighted Z byproducts act as such fields. The source excludes
them explicitly; an actual residual/implementation must enforce that premise
or derive the appropriate field-aware expression before using this control.

## Purge counterexample and MBQC transfer

Projecting RX1(beta)e^(i theta Z1Z2)|++> onto Z1=z gives the unnormalized
second-qubit vector M_z|+>/sqrt2 with
M_z=cos(beta)e^(iztheta Z2)-i sin(beta)e^(-iztheta Z2).
M_z-dagger M_z=I-z sin(2beta)sin(2theta)Z2, so each z has probability1/2;
the normalized vector and conditional populations in the source follow.
At beta=theta=pi/4 the surviving computational state is |1> or |0>, not a
Z-rotated |+>. Thus the original known weighted-resource invariant is gone.
To realize this within A's TWO-ENDPOINT macro purge, append an unused third
data vertex and let the failed new edge join1 to3: purging1,3 still leaves
the bad state on2. The two-bit calculation alone concerns deleting1, not
literally a failed two-endpoint macro on an otherwise empty two-bit graph.
Neither calculation refutes A's offline diagonal preparation theorem.

For input a|0>+b|1>, a fresh |+> and CZ give a|0>|+>+b|1>|->.
The stated measurement bra gives [a|+>+(-1)^s e^(-i alpha)b|->]/sqrt2
=e^(-i alpha/2)X^s H Rz(-alpha)|psi>/sqrt2. Both signs, global phase and
normalization are correct; each effect is I/2 for arbitrary entangled input.
The CNOT-Rz-CNOT and H-Rz-H decompositions also have the correct signs.
All ideal outcomes are used, but their byproducts must change later angles
or final interpretations. A one-wire identity is not a full entangling
pattern, universal resource graph, finite-bit compiler or erasure strategy.

Primary bounded check: [Raussendorf--Browne--Briegel v2](https://arxiv.org/pdf/quant-ph/0301052v2),
14-Jan-2003, II.D Scheme1/Eqs40-47 and II.H/Eqs138-140, supports the known
ideal circuit-to-cluster composition and polynomial resource-overhead context.
Those passages were inspected, not the entire37-page proof. No copy retained,
SHA:NONE. The source's supplementary weighted/non-Clifford citation was not
re-audited here and is not needed to derive the elementary identities above.

Remaining gap is accurately stated: supply the complete paid resource graph,
measurement schedule/byproducts and every computation-time loss/timeout branch.
Offline |+>-resource recovery neither repairs arbitrary algorithmic data nor
bounds the full execution cost. This review authorizes no numerical or hardware
step and does not convert preparation progress into optimization advantage.
