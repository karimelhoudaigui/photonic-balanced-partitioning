# P39: the sharp two-photon curve does not bound the three-photon pinched state

Post-hoc auxiliary theorem,2026-11-22, author Astra. Exact derivation and
separate scalar-root check; fresh independent review is unavailable after
agent quota. No novelty, graph-quality or quantum-advantage claim.

There exists an orthonormal nine-mode, three-column frame with dominant-support
leakage delta=18/25 and

    D_pinched >24493/50000 >288/625=delta-delta²/2.

This refutes only the universal **curved pinched-state** envelope. It does not
refute D_pinched<=delta, measured TV<=delta, or even the curved measured-TV
envelope. A stronger intermediate metric must not be substituted for the
actual optical sample distance. No original P36 claim is retroactively changed.

## Physical frame and effects

Put e=3/25,d=19/25,p_ga=d for g=a and e otherwise. For g,r,a in {0,1,2},

    V_(g,r),a=sqrt(p_ga/3) exp(2pi i r a/3).

The Fourier sum over r is zero for distinct a,b and three for a=b. Thus
V^dagger V=I, since d+2e=1. Every row in group g has its strict largest
squared entry at a=g, and the coarse effect is E_g=diag(p_g0,p_g1,p_g2).
Each row intensity is1/3 and delta=3(1-d)=6e=18/25. This is a valid
passive-optical occupied frame; it can be completed to a unitary. There is
no source conditioning, ignored collision or favorable graph instance.

## Twenty-seven sectors and a scalar eigenvalue test

The pinching reduction in phase3_pinching_dual.md gives D_pinched=sum_t F(G_t)/6.
All G_t here are diagonal with entries w_pi=product_j p_(t_j),pi(j).
The sector classes and their multiplicities are:

| Group tuple type | Number | Six diagonal weights |
|---|---:|---|
| all equal | 3 | de² six times |
| two equal | 18 | d²e,de²,e³ each twice |
| all distinct | 6 | d³ once,de² three times,e³ twice |

For positive weights w, sqrt(G)(J-I)sqrt(G)=zz^dagger-diag(w), z_i=sqrt(w_i).
It has one positive eigenvalue lambda. Its eigenvector equation gives

    sum_i w_i/(lambda+w_i)=1.

The left side is strictly decreasing on positive lambda, from6 to0. Thus if
sum_i w_i/(r+w_i)>1 at a positive rational r, then lambda>r. This conclusion
requires no approximate root finding or diagonalization.

The all-equal class has lambda=5de² exactly. For the other two classes use
r_A=43/400 and r_B=7/50. Direct rational substitution gives

    2(d²e)/(r_A+d²e)+2(de²)/(r_A+de²)+2e³/(r_A+e³)>1,
    d³/(r_B+d³)+3(de²)/(r_B+de²)+2e³/(r_B+e³)>1.

Their exact positive residuals are retained by the scalar-check receipt.
Therefore

    D_pinched >(5/2)de²+3r_A+r_B
              =24493/50000,
    24493/50000-288/625=1453/50000>0.

This is a strict analytic counterexample. The primary calculation independently
uses rational Rayleigh vectors for all27 sectors and obtains the stronger
lower0.490108163..., with exact numerator/denominator retained. Its eigensolver
display is about0.490108288..., but neither decimal is a proof leaf.

## Measured law and scope

One new full-law Perceval comparison on the completed nine-mode unitary checks
all165 three-photon occupations against explicit coherent routing, retaining
the distinguishable law too. Maximum probability discrepancy2.78e-17; measured
TV is approximately0.265153, below both the curved number0.4608 and delta0.72.
The completion seed20261220 does not choose V or tune its result.

The physical check corroborates conventions but is not needed for the rational
matrix inequality. The example was motivated by a previous diagonal-effect
diagnostic and is explicitly post hoc, not a preregistered optimization result.
It closes the attempted curved pinching route; the linear pinching and measured
conjectures remain OPEN. Manuscript and QPU gates remain closed.
