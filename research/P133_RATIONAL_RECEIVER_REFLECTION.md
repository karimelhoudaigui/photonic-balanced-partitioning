# P133 — Rational receiver reflection: manual engineering derivation

2026-11-26. ROOT proposed this variant; P66 reconstructed it manually.
Parent c8b99b374ce20cc1f6f16c700c07de5dbdfb9899. No code/run or P130 data read.
This changes no P132 byte and makes no novelty or positive-optimizer claim.

## Exact rational unitary, with the correct occupied columns

For ANY F in Q(i)^(r-by-k), let H=F^dagger F, Q=(I+H)^(-1),
D=(I-H)Q, V=[F;-I_k], and P=V Q V^dagger. I+H is positive definite,
even if F is rank deficient, so its inverse exists and remains Gaussian-rational.
Since V^dagger V=I+H, P^dagger=P and P^2=P. Therefore

    U=I_(r+k)-2P,       U^dagger=U,       U^dagger U=I,
    U=[[I_r-2FQF^dagger, 2FQ], [2QF^dagger, I_k-2Q]].   (1)

Put T=2FQ. H commutes with Q, and D=2Q-I, hence the LAST k columns
of U are exactly [T;-D], not [T;D]. Prepare one photon in each of those
k input modes, all other inputs vacuum. The first r outputs are receivers;
the last k are dump ports. Their exact occupied-source Gram matrices obey

    T^dagger T=4HQ^2,    D^dagger D=(I-H)^2 Q^2,
    T^dagger T+D^dagger D=I.                            (2)

No environment square root, matrix exponential or Gram inverse square root
is computed. Rational inversion and forming U have polynomial bit complexity
in the fully encoded F/dimensions; actual mesh synthesis/precision remains paid.
For each singular value s of F the signal singular value is 2s/(1+s^2),
at most one, with equality at s=1. Neither full rank nor large entries of F
promise high transmission. Small/large singular values can both attenuate.

For a receiver CF k-set Y, p_B(Y)=|per(T_Y)|^2 and
p_D(Y)=per(|T_Y|^2). Summing every normalized full-U Fock outcome gives one.
If all other occupations hold the incumbent, including dumps and collisions,
the hold mass is exactly 1-sum_Y p(Y), without a success denominator.
r6,k4 costs ten modes/four photons and has 15 receiver-CF states.
r12,k4 costs sixteen modes/four photons and has 495; extra device loss is separate.

## Graph compiler and a non-gauge-positive hand example

For the graph compiler assume r>=k>=1. Reuse P132's exact residual fields
d_j and weights w_jh, with w_jj=0.
Take p_a as the first k public receiver marks, W=1+max|d|+sum_(j<h)w_jh,

    F_ja=delta_(j,p_a)*(1-beta*d_j/W)+i*kappa*w_(j,p_a)/W,
    0<=beta<=1/2, kappa>=0.                             (3)

For rational graph data/beta/kappa this is rational, optimum-blind and explicit.
The prototype block is A0+iB0, with A0 real diagonal and A0> I/2, B0 real
symmetric. Re[x^dagger(A0+iB0)x]=x^dagger A0 x>||x||^2/2.
Thus its smallest singular value exceeds 1/2; (3) has full column rank.
This fact does not prove a useful cut bias. At beta=kappa=0, F is the
prototype injection, H=I, T=F and D=0: a deterministic KNOWN receiver set.
That endpoint is a credited classical candidate, never optimization benefit.

Take k=r=2, beta=0 and kappa*w12/W=1. Then

    F=[[1,i],[i,1]], H=2I, Q=I/3,
    T=(2/3)[[1,i],[i,1]], D=-I/3,
    T11*T22*conj(T12)*conj(T21)=-16/81.                 (4)

The nonzero negative rectangle product is invariant under input/output phases,
and is impossible for an entrywise nonnegative matrix. T is not gauge positive.
This fits a connected nonnegative four-vertex graph: current S={3,4}, R=S,
receivers {1,2}, all edge weights 1/2 except w12=1 give d1=d2=2,W=4;
choose kappa=4. It is a compiler witness, not a favorable graph benchmark.
Indeed per(T)=0 while the same-T D receiver coincidence is 32/81.
Escaping positivity therefore does not even guarantee a favorable local contrast.

## Screens and what remains open

P99 does not automatically apply: this is a fixed complex rational reflection,
not its dense REAL symmetric weak-time family with a certified coupling floor,
source/complement orientation and admissible doubled time. A special subfamily
meeting every P99 premise must still receive that control; no blanket escape.
P109 DOES apply whenever an admissible cT exists with c^(2k)>=k! and the same
CF/hold contract. F->aF generally changes each singular value differently,
so it is not automatically such a scalar rescaling or an available control.
Measured attenuation alone does not license removal of hardware loss.
P126 applies if the actual T is rational gauge positive; (4) disproves that
premise for the whole family. P129 still supplies its norm-certified full-law
approximation wherever informative; the sign of entries supplies no exemption.

The engineering change is computing the rational projector reflection directly,
rather than P132's inverse-root compilation. This is still a static passive mesh
(abstractly U=exp(-i*pi*P)), not a new instrument class or a novelty claim. k4 needs all
14 proper input-species partitions (Bell(4)-1), independently retuned, including
D, plus static exact-law classical sampling, FAST/pair/beam/frontier controls.
All prototypes, O(r^2) features, inversions, preparation, rejected attempts,
photons, compiled precision and scoring are paid and shared. A finite four-photon
raw-law evaluation and graph-utility sign remain OPEN; no population/search is registered.
No empirical advantage, hardware account/PNR certificate, QPU call or paper edit
follows. Only this derivation was written; no import/AST/test/RNG/native occurred.
