# P59: fixed-intensity N6 phase-response construction (STATIC)

25-Nov-2026. Analytic derivation only; no program, matrix evaluation, full law,
edge coefficient, graph, sample or numerical calibration has run for P59.
The actual15 decoded responses remain UNKNOWN. This note supports the fixed
prospective card, not an optimization/hardware claim or novelty statement.

## Explicit conventions and exact unitary

Outputs r=2a+i and inputs s=2b+j, a,b0..2 and i,j0..1. Use the UNNORMALIZED
H2=((1,1),(1,-1)); there is no additional1/sqrt(2). Let

    xi=exp(i*pi/3), xi^2=xi-1, omega=xi^2=xi-1,
    zeta=exp(i*phi),
    C[(a,i),(b,j)]=omega^(a*b)*zeta^(1_(b=1,i=1))*(-1)^(i*j).

The raw Diťa matrix is U0=C/sqrt(6). The FIXED real output rotation V acts
only on ordered ports(0,2)=((a0,i0),(a1,i0)), with block

    [[3/5,-4/5],[4/5,3/5]].

All other rows are untouched. Set R=5V, Q=R C and U=Q/(5sqrt(6)). This
freezes the Fourier sign, port order, rotation orientation and positive phase.
The adjoint involution is xi->1-xi and zeta->zeta^-1. For columns(b,j),(b',j'),

    (C* C)[(b,j),(b',j')]
      = sum_a omega^(a*(b'-b))
        * sum_i zeta^(1_(i=1)*(1_(b'=1)-1_(b=1)))*(-1)^(i*(j'-j)).

If b!=b', the root sum vanishes. If b=b', phases cancel and the result is
6delta(j,j'). Thus C*C=6I as an exact Laurent identity. R^T R=25I, so
**Q*Q=150I** and U is unitary for every real phi. Q has coefficients in
Z[xi][zeta]; every ENTRY is phase degree0 or1.

## q and complete diagonal counts are phi independent

The row0 entries, for a fixed b and either j, are3-4omega^b; row2 entries
are4+3omega^b. The remaining even row4 is5omega^(2b). The three odd rows
are5omega^(ab)*(-1)^j*zeta^(1_(b=1)). Consequently q=|U|^2 is EXACTLY

    row0: (1,1,37,37,37,37)/150,
    row2: (49,49,13,13,13,13)/150,
    rows1,3,4,5: (25,25,25,25,25,25)/150.

Every row and column sums to one; every phi dependence is a unit-modulus
monomial, so there is no deficit/implicit vacuum or hidden intensity channel.
For the full single-photon input1^6, all mean occupations equal one.
Distinguishable photons' ENTIRE unconditioned Poisson-multinomial count law
is fixed by these column probabilities and hence constant in phi.

For each B output mode r, its full diagonal-count generating polynomial is

    E[(1+t)^n_r] = sum_(h=0..6) h! e_h(q_r0,...,q_r5) t^h.

All single-mode PMFs, not just means, are therefore fixed. In particular
Var_B(n_r)=2(1-sum_s q_rs^2): rows0/2 have2837/1875, while rows1/3/4/5
have5/3. The C3 shift(a,i)->(a+1,i) sends row2 to row4, whose variances
differ. Thus the COUNT law really breaks the old C3 invariance pointwise;
this is stronger than only checking that V fails to commute with the shift.
It still does NOT prove a nonzero projection onto decoded cut means.

The full-square full-CF moment theorem in
`P56_full_square_third_moment_physics_check.md` (5f9ae00) applies: every joint
factorial moment of total degree<=3 is a function of q and is phi independent,
including repeated indices. Its hypotheses hold for this square unitary and
the original six distinct single-photon inputs. No CF conditioning is used.

## Source-pair cancellation and exact probability field

Let x0..x5 be commuting output creation variables. Define phase-free forms

    E0=-x0+7x2+5x4,
    E1=(7-4xi)x0+(1+3xi)x2-5xi*x4,
    E2=(3+4xi)x0+(4-3xi)x2+5(xi-1)x4,
    O0=5(x1+x3+x5),
    O1=5[x1+(xi-1)x3-xi*x5],
    O2=5[x1-xi*x3+(xi-1)x5].

The two j columns for b give(Eb+zeta_b Ob)(Eb-zeta_b Ob), where zeta_1=zeta
and zeta_0=zeta_2=1. Hence the FULL source polynomial is

    P=(E0^2-O0^2)*(E1^2-zeta^2 O1^2)*(E2^2-O2^2).

For EVERY occupation n of total6, its coefficient is c0_n+c2_n*zeta^2,
with c0,c2 in Z[xi]. The coefficient of zeta^1 is identically ZERO, not a
numerical smallness hypothesis. All462 occupations C(11,5) remain in evidence.
Parity of N_even=n0+n2+n4 is even:236 occupations are parity-allowed and226
are structural zeros, but additional zeros may occur. This is no pruning or
postselection. c0 has N_even>=2 and c2 has N_even<=4, so their interference
is supported only in N_even2/4. These are prospective invariants to check.

Let f_n=prod_r n_r!, D=150^6. The normalized Fock amplitude is
sqrt(f_n)*(c0+c2*zeta^2)/150^3. Therefore

    p_n(phi)=f_n/D*[N(c0)+N(c2)
                    +(2a_n+b_n)cos(2phi)-sqrt(3)b_n sin(2phi)],
    c2*conj(c0)=a_n+b_n*xi,
    N(A+Bxi)=A^2+A*B+B^2,  conj(A+Bxi)=(A+B)-Bxi.

There is no extra input factorial or collision-free restriction. Unitarity
requires sum_n f_n[N(c0)+N(c2)]=D and sum_n f_n(a_n+b_n xi)=0 exactly.

## Independently specified analytic sign/Fock fixture

Before calibration, adaptive supplied and ROOT independently confirmed the
occupation n=(4,2,0,0,0,0). It is a count-probability fixture, not a decoded
edge response. Restricting the factors above to x0,x1 gives

    c0_Q=25*(-1362+40omega)=25*(-1402+40xi),
    c2_Q=25*(-33-40omega)=25*(7-40xi),
    c2_Q*conj(c0_Q)=625*(-11134+55800xi).

The subscript Q denotes the unnormalized integer polynomial used throughout
this note. Equivalently, for columns before the common5 scaling, both source
coefficients are divided by5^6=15625, giving the denominator625 in
(-1362+40omega)/625 and (-33-40omega)/625. The output Fock factor is4!2!=48,
so the exact prospective derivative guard is

    p'_n(0)/sqrt(3) = -2*48*(625*55800)/150^6
                    = -124/421875.

This proves a nonzero response of ONE occupation analytically. Aggregation
with the decoder can cancel it; none of the15 edge derivatives follows from
this fixture alone. Its sign also fixes the chosen rotation/phase convention.

## Exact decoder response and rational curvature

For each n, use UNIFORM ties among ALL3-subsets maximizing sum_(r in S)n_r.
Let kappa_e(n) be its exact crossing probability. The possible tie counts
C(t,3-h) lie in{1,2,3,4,6,10,20}, with LCM60. The generic LCM(1..20) is
232792560; neither that value nor a reused420 should be assumed as the tie
normalizer. Use Fraction exactly, while recording/checking the actual LCM.

Write the decoded mean, for every one of15 edges, as

    f_e(phi)=u_e+F_(e,2)zeta^2+conj(F_(e,2))zeta^-2,
    F_(e,2)=alpha_e+beta_e*xi
            =sum_n kappa_e(n)*f_n*(a_n+b_n xi)/D.

Thus v_e=2alpha_e+beta_e and r_e=-2beta_e are rational, and

    f_e(phi)=u_e+v_e cos(2phi)+(sqrt(3)/2)r_e sin(2phi),
    d_e=f'_e(0)=sqrt(3)r_e.

This agrees with the general positive-harmonic rule
d_e/sqrt(3)=-sum_(h>0)h B_(e,h). Freeze ALL15 r_e at phi0=0; none is yet
computed. Decoder identities imply sum_(e incident to r)u_e=3 and incident
sums of v_e and r_e zero; total edge means sum to9 for every phase.

A rational global curvature bound, using sqrt(3)<2, is

    B_e=4*(|2alpha_e+beta_e|+2|beta_e|)=4*(|v_e|+|r_e|).

For NONNEGATIVE graph weights A_e, set h_A=sum A_e d_e and
M_A=sum A_e B_e. If M_A>0, choose phi(A)=-h_A/M_A. Taylor with this global
bound gives f_A(phi(A))<=f_A(0)-h_A^2/(2M_A). If M_A=0 then h_A=0; choose0.
If h_A=0 the rule gives no strict improvement. The displayed gain is only
conditional on the actual response and says nothing about classical benefit.
For rational A the certified gain is3(sum A_e r_e)^2/(2M_A), a rational;
implementing/approximating the real phase still has a cost/error obligation.
The chosen bound also gives |h_A/M_A|<=sqrt(3)/4 when M_A>0, so this is a
bounded local step without an outcome-dependent angle cap or rescan.
