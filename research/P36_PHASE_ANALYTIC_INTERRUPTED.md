Retained interrupted physics draft. No final return/commit was delivered for this continuation. The bounded calculation did complete and its original manifest validates in its worker. General k3 remains OPEN. Root later reconstructed pinching/dual/cone arguments separately in theory/phase3_pinching_dual.md.

Original SHA256: 119829a3fc5f457a480e209dd7155c8f8478f8f5e34a75af125e17c9e3aba40e

# P36: phase-aware attempt at the linear dominant-leakage bound

Base `de77a1404cbab6f98d3187bad4ab42b772789f29`, worktree/branch
`phase3-linear-leakage-attempt`, reviewer/researcher `/root/physics`.
No uncommitted files were present when this route was resumed after P37.
This note preserves the earlier calculations before adding the new reduction.
No manuscript, production source, shared status or QPU is in scope.

## Exact target and status

For any complex Stiefel frame V[m,3], let p_B be its complete three-boson
occupation law from distinct singly occupied inputs and p_D the law of three
independent labeled draws through the same columns, forgetting labels. Set
q_ia=|V_ia|^2 and delta=sum_i(sum_a q_ia-max_a q_ia). The requested inequality is

    TV(p_B,p_D) <= min(1,delta).

**The general three-column assertion remains conjectural in this checkpoint.**
The phase-aware identity and reductions below are exact, but the final
inequality for arbitrary connected three-column frames is not proved here.
Data from other routes are not being adopted as proof.

## Preserved partial result: one/two occupied columns and independent blocks

One column gives p_B=p_D. For two columns write r_i=min(q_i1,q_i2),
h_i=max(q_i1,q_i2). Then sum r_i=delta, sum h_i=2-delta, and

    B12=sum_i sqrt(r_i h_i) <= sqrt(delta(2-delta)).

The previously proved full-Fock permanent certificate yields
TV<=B12^2/2<=delta-delta^2/2<=delta. Here 0<=delta<=1. This also proves the
target for an arbitrary number of columns when every connected component of
the occupied-column spatial-support overlap graph has size at most two:
the physical laws factor over components, delta is additive, and product TV is
at most the sum of component TVs. This is not a proof for a connected
three-column block.

## Preserved obstruction: a positive spatial-Gram proof cannot suffice

Consider U=I+(z-1)J3/3, |z|=1. This is unitary because J3/3 is a projection.
For an integer t>=2 choose Re(z)=1-9/[2(t^2+2)]. Then

    q_diag=t^2/(t^2+2), q_off=1/(t^2+2),
    delta=6/(t^2+2), B_off=(2t+1)/(t^2+2).

For t large enough delta<1. Nevertheless, writing b=B_off,

    Per(B)-1-2delta
      = [28t^3+3t^2+36t-40]/(t^2+2)^3 > 0.

Thus Per(B)-1<=2delta is false for physically valid unitary frames, including
arbitrarily small delta. At t=10, delta=1/17 and B_off=7/34. The conjectured
TV inequality is not refuted: the failure is in the stronger positive-Gram
surrogate. Any proof using only that surrogate loses needed phase cancellation.

## Preserved connected family A: symmetric tritter phase

For U=I+(z-1)J3/3 put x=Re(z), A=(5+4x)/9, B=(2-2x)/9.
In the nontrivial region delta<1 one has x>1/4, diagonal dominance, and
delta=6B=4(1-x)/3. Let Delta=p_B-p_D. Direct three-photon amplitudes give

| Occupation type | Multiplicity | Delta per occupation |
|---|---:|---|
| (3,0,0) and permutations | 3 | 5 A B^2 |
| (2,1,0) and permutations | 6 | -2(x-1)(20x^2+14x-7)/243 |
| (1,1,1) | 1 | 4(x-1)(5x+4)(8x+1)/243 |

The final entry is negative for x>1/4. Define d0=(9-sqrt(21))/5, the zero
of the second row expressed in delta. Consequently

    TV = delta - (13/12)delta^2 + (5/18)delta^3, 0<=delta<=d0,
    TV = 5delta^2(3-delta)/36, d0<=delta<1.

Both expressions are at most delta on their domains. Outside delta<1 the
requested bound is trivial; if the off-diagonal entries become row maxima,
the actual delta remains at least one. This proves the target on this family.
It also supplies the physical counterexample to the positive-Gram shortcut.

## Preserved connected family B: two real beam splitters sharing a photon

Let c=cos(theta), s=sin(theta), 0<=theta<=pi/4, x=s^2, and

    U = [[c,-sc,s^2], [s,c^2,-cs], [0,s,c]].

This is a product of two orthogonal plane rotations and is exactly unitary.
For delta<1 its row maxima are the diagonal entries and
delta=4x-x^2, with 0<=x<2-sqrt(3). At larger x<=1/2, the actual delta is
at least one: it remains 4x-x^2 until x=(3-sqrt(5))/2, and is 1+x after
the middle row changes its maximizing column.

The exact signed occupation differences (indices0,1,2) are:

| Ordered occupation list | Delta |
|---|---|
| 000 | 5x^3(x-1)^2 |
| 001 | -x^2(x-1)(15x^2-20x+6) |
| 002 | -x(x-1)(6x^2-6x+1) |
| 011 | x(x-1)^2(15x^2-10x+1) |
| 012 | 4x(x-1)(3x^2-3x+1) |
| 022 | x(x-1)^2 |
| 111 | -5x^2(x-1)^3 |
| 112 | -x(x-1)(6x^2-6x+1) |
| 122 | -x^2(x-1) |
| 222 | 0 |

Here each list denotes a single Fock occupation, not all ordered particle
labelings; input/output factorials were included before forming these values.
Put a=(5-sqrt(10))/15, b=(3-sqrt(3))/6, and
F(x)=4x(1-x)(3x^2-3x+1), D011 and D002 equal to their table entries.
On [0,a], [a,b], [b,2-sqrt(3)] respectively,

    TV=F,  F-D011,  F-D011-2D002.

The corresponding delta-TV differences factor as

    3x^2(4x^2-8x+5),
    x[15x^4-28x^3+12x^2+3x+1],
    x[15x^4-40x^3+36x^2-11x+3].

All are nonnegative: in the second bracket group x^2(12-28x); in the
third group x^2(36-40x) and 3-11x. These are positive for
x<2-sqrt(3)<3/11. Thus this connected three-photon family also obeys the
conjecture. It is not a reduction of arbitrary unitary three-column frames.

## Lifting these families to arbitrarily many physical modes

Replace each output mode g of a three-mode family by a disjoint group of
physical modes with probabilities pi_(i|g), using V_ia=sqrt(pi_(i|g))U_ga
(fixed output phases are immaterial). This is an isometry with orthonormal
columns. Summing within each group preserves delta exactly. Given a group
occupation, both laws split the photons inside each group by the same
multinomial kernel. The groups are a deterministic function of physical
occupations, so TV is exactly preserved, not merely decreased. Hence both
families extend to arbitrary finite m>=3 with such disjoint splittings.
General frames need not factor this way; no general-m theorem follows.

## New phase-aware decomposition

For a formal vector z define Q_a(z)=sum_i q_ia z_i and
C_ab(z)=sum_i conjugate(V_ia)V_ib z_i. The complete Fock probability generating
polynomial is

    P_B(z)=Per(V^dagger diag(z) V),   P_D(z)=Q_1(z)Q_2(z)Q_3(z).

Expanding the six input permutations, with all Fock factorials, gives

    P_B-P_D = C12 C21 Q3 + C13 C31 Q2 + C23 C32 Q1
              + C12 C23 C31 + C13 C32 C21.

Equivalently let q_a be the probability measure on single-mode unit vectors,
and mu_ab=sum_i conjugate(V_ia)V_ib delta_(e_i). All complex mu_ab have
total mass zero by orthogonality. On three-photon occupations,

    p_B-p_D = sum_(a<b) mu_ab * conjugate(mu_ab) * q_c
               + 2 Re(mu_12 * mu_23 * mu_31).

Convolution is commutative on occupation counts. This exact signed identity
keeps the three-cycle phases and their cancellations with pair terms. Taking
absolute values of the five contributions separately reproduces a positive
Gram bound and is already obstructed above.

## New universal reduction of the nontrivial range

For each occupation, Cauchy applied to its six permanent amplitude terms gives
p_B(t)<=6p_D(t). Both laws normalize to one, so
sum_t min(p_B(t),p_D(t))>=1/6 and TV<=5/6. Thus for k=3 all delta>=5/6
are already settled. Only 0<=delta<5/6 needs the phase-aware argument.
This is a universal upper bound, not a sharpness assertion.

## Further reduction and open obligation

To be completed in the continuing attempt: dominant-group pinching leads to
three positive 3-by-3 effects E_g=V^dagger P_(S_g)V, sum_g E_g=I. A bound on
the resulting finite-dimensional measured-state discrepancy would imply the
occupation inequality. It is not legitimate to replace orthogonality by mere
bistochastic moduli: that relaxation discards phase closure constraints.

Status: partial theorems and exact phase-aware decomposition established by
direct derivation; the general connected three-column inequality remains open.
The note will be extended with the precise pinching operator and its remaining
inequality, and bounded independent algebra checks.
