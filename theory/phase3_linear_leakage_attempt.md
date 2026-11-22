# P36: exact two-photon case and an obstruction to a proof shortcut

2026-11-22, coordinator reconstruction after partial messages from physics.
The separate physics turn was quota-interrupted before committing its proof
packet. This note supplies the complete argument checked by the coordinator;
it is not presented as an author-blind independent review. General P36 for
k>=3 remains a conjecture. No novelty claim, manuscript or QPU conclusion.

## Exact sharp result when k=2

Let V be any complex orthonormal two-column frame, with complete bosonic and
distinguishable output laws. Put delta=sum_i min(|V_i1|²,|V_i2|²). Then

    TV <= delta-delta²/2,            0<=delta<=1.

Proof. Partition rows into S1, where the first column's squared modulus is
maximal, and S2, its complement; break ties arbitrarily. Let
l1=sum_(S2)|V_i1|² and l2=sum_(S1)|V_i2|². Both columns have norm one,
delta=l1+l2, and delta<=1 by the rowwise minimum bound. Groupwise Cauchy gives

    B12 <= C = sqrt((1-l1)l2)+sqrt(l1(1-l2)).

Set A=(1-l1)(1-l2), P=l1*l2. Algebra gives
C²+(sqrt(A)-sqrt(P))²=1 and A-P=1-delta>=0. By Cauchy,
sqrt(A)+sqrt(P)<=1. Hence sqrt(A)-sqrt(P)>=1-delta, so
C²<=1-(1-delta)²=2delta-delta². The full-Fock spatial-Gram inequality N1
has exactly one nonidentity permutation at k2 and yields TV<=B12²/2.
Combining these inequalities proves the statement, including endpoints.
All collision outcomes were summed in N1; no conditional distribution enters.

It is sharp at every delta in [0,1]. Take orthonormal disjoint pair vectors
w1=(1,1,0,0)/sqrt(2), w2=(0,0,1,1)/sqrt(2), and rotate the occupied columns
by cos(theta),sin(theta), 0<=theta<=pi/4. Direct ten-outcome Fock expansion
gives delta=2sin²(theta) and TV=2cos²(theta)sin²(theta)=delta-delta²/2.
This is the retained P33 family. The binary-fidelity/Cauchy ingredients are
standard; an optimal two-photon bound is not a quantum optimization advantage.

## Why the old positive-permanent route cannot prove general TV<=delta

One might try to prove per(B)-1<=2delta and invoke N1. That auxiliary claim is
false even on a physical three-mode unitary near disjoint support. Let

    U=I+(z-1)J3/3,    |z|=1,    Re(z)=65/68,

where J3 is all ones. The rank-one projector J3/3 makes U unitary. With one
photon per input, its squared entry moduli are d=50/51 on the diagonal and
e=1/102 off diagonal. Every row intensity is one; thus delta=1/17. Its spatial
magnitude Gram has diagonal one and every off-diagonal entry b=7/34. Therefore

    per(B)-1 = 3b²+2b³,
    per(B)-1-2delta = 265/9826 > 0.

This refutes the auxiliary permanent inequality, not P36. For completeness
the actual Fock TV can be evaluated as rational probabilities. Writing
t=Re(z), three triple-occupation outcomes have probabilities

    p_b(300)=6*d*e²,          p_d(300)=d*e².

Six double/single outcomes have

    p_b(210)=2*e*(2*t+1)²/9,
    p_d(210)=e*(d²+d*e+e²).

The remaining (111) outcome has

    p_b(111)=(64*t³+24*t²-24*t+17)/81,
    p_d(111)=d³+3*d*e²+2*e³.

These follow from the two repeated-row and three distinct-row permanents,
including the output factorials. They normalize exactly and give actual
TV<=delta for this witness. The companion exact-arithmetic receipt checks all
of these equalities and seven rational sharp-family cases.

A general linear proof, if one exists, must use phase cancellation or another
property beyond this positive N1 majorant. A full-state trace-distance bound
cannot supply it either: bosonic and label-dephased assignment states remain
far apart even at U=I, where the measured laws agree and delta=0. The new
numerical grid is finite evidence only. Known continuations are to analyze
occupation measurement after dominant-region dephasing, or seek a k>=3
counterexample; neither is completed here.
