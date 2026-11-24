# P44 — factorial-moment cap with nonuniform passive loss

Date: 2026-11-24. The coordinator supplied the proposed identical-photon
chain before this lane checked it; this is not a blind reconstruction.
The present note supplies the bridge, attribution and scope checks. No
numerical run, QPU call, source installation or manuscript change occurred.
Independent proof acceptance and novelty assessment remain separate.

## 1. Physical and probabilistic contract

There is one photon in every input in A, |A|=N, and vacuum elsewhere.
First assume identical pure internal states. A passive network with a vacuum
environment and arbitrary nonuniform pure loss has system transfer matrix T,
an operator contraction. Let X=T[:,A] and

    B=XX*=T P_A T*,    eta_A=||X||_op^2<=||T||_op^2<=1.

All efficiencies included in T must really be passive loss. No conditioning
on detection, thermal environment, false clicks, active squeezing, input
multiphotons or intermediate feedforward is implicit in this definition.
The detector resolves occupations n_i, or outputs their threshold support.
Every raw source attempt, including loss/vacuum events, remains counted.

Fix k>=1 DISTINCT observed output modes S. If N<k, the relevant moment and
k-click event are zero. For N>=k, the proposed chain is

    E[prod_(i in S)n_i]
      =sum_(R subset A, |R|=k)|per T[S,R]|^2
      <=per B[S,S]
      <=||B[S,S]||_op^k
      <=eta_A^k.                                         (M1)

The intermediate local spectral norm may be smaller than eta_A. No Haar
assumption or uniform loss commutation is needed. Source count N is absent
from the final bound because the occupied columns already enter B.

## 2. Exact factorial-moment identity

Dilate T to a passive unitary including vacuum input/environment modes.
Write b_i=sum_a T_ia a_a+vacuum terms. Since the observed modes are distinct,

    prod_(i in S)n_i=(prod_(i in S)b_i)^*(prod_(i in S)b_i).

This is normally ordered. Vacuum annihilators vanish on the input state;
repeated occupied-input annihilators also vanish because each has only one
photon. For any distinct removed set R, the coefficient is per T[S,R].
The residual states with occupied sets A\R are orthonormal. Taking their
squared norm gives the equality in(M1), with no k! prefactor. It is an
intensity factorial moment, not a conditional surviving-photon probability.
Higher-survivor sectors and collisions are already included in the moment.

The same equality follows by specializing the standard normally ordered
Fock moment expansion, e.g. Monbroussou et al. v1, Appendix C Eq. C1, to
one creation/annihilation operator in every selected output mode and a
binary input occupation. Extending a unitary to a contraction here uses
vacuum dilation and normal ordering, not an unproved loss-mixture formula.

## 3. Permanent Cauchy–Binet and the positive omitted terms

Put Y=X[S,:], a k-by-N matrix. The established permanent Cauchy–Binet
identity gives

    per(YY*)=sum_(r in N^N, |r|=k) |per Y[:,r]|^2/r!,    (M2)

where columns are repeated according to occupation r and r!=prod_a r_a!.
For rectangular matrices one can pad by zero rows/columns and apply the
square identity. Every summand is nonnegative. Binary occupations r=1_R
give exactly the sum in(M1); the nonbinary occupations are the omitted
positive terms. Thus

    sum_(|R|=k)|per Y[:,R]|^2<=per(YY*).

This is an application of known Cauchy–Binet, not a new permanent identity.
Source: Chabaud–Deshpande–Mehraban, arXiv:2208.00327v3, Section 5.3,
Eq. 58 and its proof, printed p. 14.

## 4. The spectral cap is also established

For any k-by-k complex matrix C, the known operator-norm permanent bound is

    |per C|<=||C||_op^k.                                 (M3)

For the PSD matrix C=B[S,S], (M2) makes the permanent nonnegative. Then
||C||<=||B||=eta_A, proving the remaining arrows in(M1). A primary explicit
statement is Aaronson–Arkhipov's author PDF, Appendix 12, Corollary 66,
printed p. 96, following Lemmas 64–65.

For completeness, its symmetric-tensor interpretation gives the same bound.
The normalized occupation |1,...,1> on k modes has

    <1^k|Sym^k(C)|1^k>=per C.

The restriction of C^(tensor k) to symmetric tensors has norm at most
||C||^k. For C>=0 it is positive. This proves(M3) directly in the case used
here. It invokes no monotonicity of individual matrix entries or an
unproved permanent-on-top conjecture.

The eta_A^k constant is sharp given only eta_A: map k selected occupied
inputs independently to S with transmissivity eta_A and lose all other
occupied inputs completely. Then B[S,S]=eta_A I_k and the event that all
k selected photons are transmitted has probability eta_A^k, attaining
every step of(M1). This is an analytic equality case, not a new experiment.

## 5. Thermal Gaussian interpretation and its limitation

Replace every occupied input, ONLY IN AN AUXILIARY COMPARISON, by an
independent thermal state of mean one. Equivalently draw independent
standard circular complex Gaussians z_a and use a coherent input z. Its
output amplitudes Xz have covariance B. The complex Gaussian Wick identity
gives

    E_z prod_(i in S)|(Xz)_i|^2=per B[S,S].                (M4)

This is the thermal normally ordered intensity moment and, in point-process
language, the k-point intensity of a permanental Cox process. Hough et al.,
math/0503110v2, Proposition 35 and proof, pp. 223–224, provide this
Gaussian/Cox permanent interpretation. The input covariance is proper
(zero anomalous covariance); generic squeezed Gaussian states are not meant.

One can also derive the comparison term by term: for an input polynomial
annihilator P=sum_r c_r a^r, a diagonal product Fock source gives

    <P*P>_Fock=sum_r |c_r|^2 prod_a (n_a)_(r_a),

whereas mean-n_a independent thermal inputs give

    <P*P>_thermal=sum_r |c_r|^2 prod_a r_a! n_a^(r_a).

The former is bounded by the latter termwise. Binary occupations specialize
to(M1)–(M2). This is a normally ordered polynomial-moment comparison,
NOT an operator ordering or a probability-law domination by thermal light.
For example, a lossless one-photon input has P(n=1)=1; thermal mean one has
P(n=1)=1/4. It cannot replace the Fock law pointwise. A fixed-N Fock output
is not itself the auxiliary permanental process, which has unbounded counts.

## 6. Threshold support and adaptive uniform-search consequence

For the terminal threshold event E_S={support(n)=S},

    1_(E_S)<=prod_(i in S)n_i.

Consequently(M1) bounds EACH exact threshold support by eta_A^k, despite
allowing any number of detected photons and all collisions within S. It
also bounds any event that requires all modes in S to click. Additional
fixed terminal herald/rejection conditions cannot increase this raw-attempt
probability. Branch-dependent coherent/feedforward evolution is outside
the single fixed-T argument.

With D=binom(m,k), a uniform k-subset proposal dominates each physical
threshold support if D eta_A^k<=1. In balanced m=2k, eta_A<=1/4 suffices
for every k, since D<=4^k. The exact finite criterion is stronger.

The dominator is history-independent. For any FIXED good support set H,
an adaptive algorithm choosing T_t,A_t,N_t from classical history has
conditional first-hit probability at most |H| eta_bound^k if every history
obeys eta_(A_t)<=eta_bound. Fix integers n_Q>=0 and n_C>=1. The optical
algorithm executes AT MOST n_Q raw attempts; the classical control executes
AT LEAST n_C independent uniform feasible draws, or exactly that preassigned
number. A capacity to execute up to n_C draws is not sufficient. With
L=max(1,ceil(n_Q/n_C)),

    L D eta_bound^k<=1                                   (M5)

implies classical first-hit and terminal-best-cost stochastic domination
for support candidates and a common initial incumbent. Indeed p=|H|/D,
and optical no-hit probability is at least

    (1-p/L)^n_Q >= (1-p/L)^(L n_C) >= (1-p)^n_C.

The last expression is the no-hit probability for exactly n_C independent
uniform classical draws; executing at least n_C can only decrease it. This
argument does not simulate the optical history. A fixed shared decoder can
be pushed forward using the cardinality of the good-set preimage; unrestricted
history-dependent many-to-one repairs are not silently included.

This is not equal realized objective-query or wall-time domination. Optical
failures can avoid graph scoring while a uniform feasible candidate costs a
score. A common classical frontend, all its extra evaluated candidates,
training overhead, loss/heralding attempts and source photons must be
accounted for. A measured resource model must justify the optical upper
count AND the classical guaranteed count actually performed within budget
to instantiate(M5); a classical upper-count ceiling alone cannot do so.
No hardware calibration or total-time inequality is asserted here.

## 7. Internal states: separated general bound and counterexample

Keep exactly one photon per spatial input but allow an arbitrary normalized
joint internal density matrix rho. The channel acts as T tensor I_internal,
and the detectors sum over internal states. For each removed set R, let
rho_R be its reduced internal state. With an ordering of R and S define

    a_sigma=prod_(j=1..k) T_(i_j,r_(sigma(j))),
    M_R=sum_(sigma in S_k) a_sigma P_sigma,

where P_sigma permutes internal tensor factors. Direct expansion of the
normally ordered moment gives sum_R Tr(M_R rho_R M_R*). Different R leave
orthogonal spatial input occupations, including when rho is entangled.
For any internal vector v, Cauchy–Schwarz on the k! summands gives

    ||M_R v||^2<=k! sum_sigma |a_sigma|^2 ||v||^2.

Applying it to rho_R and summing yields the separately justified bound

    E prod_(i in S)n_i
       <=k! sum_(injective f:S->A) prod_(i in S)|T_(i,f(i))|^2
       <=k! prod_(i in S) B_ii
       <=k! eta_A^k.                                    (M6)

The second step only adds nonnegative NONinjective labeled assignments.
Thus an unknown internal Gram matrix does not prevent this conservative
cap. Internal-state-dependent loss/dispersion is not a T tensor I channel
and needs another model. For fully distinguishable photons the initial
sum has no coherent cross terms, and the k! prefactor can be omitted.
Neither constant is claimed optimal for intermediate distinguishability.

The stronger identical eta_A^k cap fails for partial distinguishability.
Use the already derived DFT6 direct-sum I2 example: m=N=8,k=4,
S={0,3,6,7}; active even inputs have species A, odd inputs orthogonal
species B. The sum of four-photon CF transition probabilities over survivor
sets contributing to S is 7/6. After uniform transmission eta, its exactly
four-survivor sector alone therefore gives

    P(support=S)>=(7/6)eta^4(1-eta)^4.

For 0<eta<1/28, (1-eta)^4>=1-4eta>6/7, so this exceeds eta^4 although
||sqrt(eta)U||^2=eta. This is a physical per-emission counterexample to
silently removing k! for arbitrary internal states, not just a conditional
sector counterexample. Higher-survivor contributions are nonnegative.
The equality-case transition calculation is in the sealed
P42_encoding_scope_checks.md; no new numerical run is used here.

Replacing eta_bound^k in(M5) by k!eta_bound^k gives a conservative uniform
adaptive comparison for the internal-state model of(M6).

## 8. What must actually be calibrated

eta_A is the SQUARED SPECTRAL NORM of the occupied transfer matrix. It is
not the mean detection rate or the largest single-column transmission.
A matrix with one nonzero row (1,...,1)/sqrt(N) has every column norm squared
1/N but spectral norm squared 1. A public average transmission cannot
certify eta_A<=that average.

An always-valid phase-free upper bound is

    eta_A<=||X||_F^2=sum_(a in A) sum_i |T_ia|^2.         (M7)

Calibrated upper bounds on the SUM of occupied-column transmissions can
therefore suffice, possibly clipped at 1 for a known contraction. The
maximum column alone needs the additional factor N. General internal-state
bound(M6) can alternatively use calibrated row means B_ii directly,
retaining the k! factor. Confidence, detector/noise assumptions and raw
emission denominators must be supplied before hardware conclusions.

## Disposition

The proposed identical-photon chain is a verified formal consequence of
known Fock moments, permanent Cauchy–Binet and the norm bound, with an
explicit nonuniform-loss bridge. Gaussian moment attribution is established;
neither Gaussian-law domination nor global novelty follows. The adaptive
graph-search application is conditional on its stated physical/resource
contract. The broader discovery objective remains open outside that class.

### Qualification after review: classical draws are a guaranteed count

The prior proof file SHA-256
`c8d56b08bb02f684f776369aa6d2c4c2cc35b67a8dc9c07f709915a7c34153c6`
incorrectly called n_C a classical uniform-draw ceiling. Section 6 now
requires a fixed guaranteed lower count (or that fixed number executed),
while n_Q remains an optical upper count. The no-hit comparison is unchanged
for those correct hypotheses. The earlier version remains in Git history.

A search of the local P42/P44 notes also found the historical P42 Section 8
heading referring broadly to different attempt ceilings. Its mathematical
body specifies a classical search with n_C draws, so its comparison is
valid for that executed count, not a mere classical upper bound. Those
sealed files and historical source records were not edited. This current
qualification records the semantic distinction explicitly; no new run
or change to the moment-cap proof was made.
