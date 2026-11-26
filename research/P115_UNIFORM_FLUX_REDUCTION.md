# P115: uniform weighted complement-cycle flux reduction

26 November 2026. **STATIC SPECTRAL DERIVATION, not a sign certificate.**
This develops only ROOT's proposed C4 reduction. No P114 source/result is
assumed or read. Any square-positivity transfer below is explicitly conditional.
No optimization, universal no-go, hardware or novelty claim follows.

Context read in full: P101 source69e4a6fe434a677acfc5a7e616471990b16db86b,
research/P101_FINITE_FILTER_ALL_OUTPUT_CARD.md113l, SHA256
65e4199fb468d02eec4155072a60b8d7818ee0d57ef6205e83c2da51bc60027c;
its166-line independent review19fcb2af6d9f1ef804931a29c2298fc12bb1dda6,
SHA256d61068fb4bb7fc55f21af976bb2103b0922697ff931568aba2f11960b962b505.
The proof here is direct elementary algebra, not an external theorem transfer.

## Objects, phases and the correct gauge convention

Label the cycle j=0,1,2,3, modulo4. Each complement edge j--(j+1) has
the SAME weight a>0; the two diagonals have complement weight0. Define

    z†Lz=sum_j a |z_j-exp(i theta_j)z_(j+1)|^2.

Thus L_jj=2a and L_(j,j+1)=-a exp(i theta_j), including the closing edge.
The flux is Phi=sum_j theta_j modulo2pi. It is FOUR times the canonical
forward edge phase, not that phase itself. Choose Phi_0 in[-pi,pi] and
psi=Phi_0/4 in[-pi/4,pi/4], so4psi=Phi modulo2pi.

Set chi_0=0,chi_(j+1)=chi_j+psi-theta_j for j=0,1,2 and
D=diag(exp(i chi_j)). The transformed forward phase is
theta_j-chi_j+chi_(j+1)=psi. On the closing edge it is Phi-3psi=psi modulo2pi.
Consequently D†LD=L(psi), the uniform-phase cycle. Different flux lifts by
2pi give gauge-equivalent descriptions; no eigenvector branch is fitted.

Let phi=|psi|. Reflection R:j->-j gives R†L(psi)R=L(-psi).
Equivalently L(-phi)=overline(L(phi)). This sign removal needs reflection
or complex conjugation in general; a diagonal gauge ALONE cannot change a
generic flux Phi into-Phi. No incorrect pure-gauge identification is made.

## Fourier order, ground shift and normalization

Use EXACTLY F_jq=(-i)^(jq)/2, q=0,1,2,3. For the nonnegative edge phase
phi in[0,pi/4], its q-th column satisfies

    L(phi)F_q=[2a-a exp(i phi)exp(-i pi q/2)
                  -a exp(-i phi)exp(i pi q/2)]F_q,
    lambda_q=2a[1-cos(phi-pi q/2)].                       (1)

Write c=cos(phi),s=sin(phi), with c>=s>=0. In FOURIER order this is

    (lambda_0,lambda_1,lambda_2,lambda_3)
      =2a(1-c,1-s,1+c,1+s).

The numerical order is lambda_0<=lambda_1<=lambda_3<=lambda_2, not the
Fourier order. The minimum is lambda_0 and the width is4ac. Therefore the
P101 normalization is

    Lambda=max(1,4ac), H=[L(phi)-lambda_0 I]/Lambda,
    spectrum_F(H)=(0,2a(c-s),4ac,2a(c+s))/Lambda.         (2)

All eigenvalues of H lie in[0,1]. The key identity is the EXACT additive relation
lambda_2-lambda_0=(lambda_1-lambda_0)+(lambda_3-lambda_0).
For any finite strength beta>=0 set

    x=exp[-beta a(c-s)/Lambda],
    y=exp[-beta a(c+s)/Lambda].

Then in the canonical nonnegative-flux representation

    exp(-beta H/2)=F diag(1,x,xy,y)F†, 0<y<=x<=1.        (3)

The closure obeys0<=y<=x<=1. The product is
xy=exp[-2beta ac/Lambda]. For beta>0 it equals exp(-beta/2) iff the width
branch Lambda=4ac applies; at beta=0 both are1. When4ac<1, Lambda=1 and
the special-strength formula is false for beta>0.
For phi<pi/4 and beta>0, y=x^r with r=(c+s)/(c-s)>=1. This is a
fixed-flux curve, not the entire square at one fixed optical compiler.
At a=1/2,phi=pi/6, Lambda=sqrt(3), r=2+sqrt(3), reproducing P101 exactly.

## Counts and decoder labels are not changed silently

For the diagonal gauge, functional calculus gives T'=D†TD and E'=D†ED,
E=sqrt(I-T^2). Hence U'=[[T',E'],[E',-T']]
=diag(D†,D†) U diag(D,D). With the declared input|11110000>, input phases
give one global phase and output phases give one phase per Fock occupation.
Every normalized FULL8-port count probability is unchanged at the SAME
physical port labels. Thus signal counts, total loss, thresholds and the
two P101 uniform-tie decoders are unchanged; no vertex mask is permuted.
For D, the same fact follows directly from unchanged single-particle intensities.

Reflection alone DOES permute ports. If used, graph/port labels and tie
priorities must be transported by R. There is also a direct same-label
argument avoiding that bookkeeping: for negative psi, T(psi)=overline(T(phi))
and its principal E and U are also conjugates. All fixed-CF Fock amplitudes
are conjugated, so probabilities coincide at each SAME8-port occupation.
The D intensity law coincides as well. Thus arbitrary initial edge phases
are count-equivalent to(3), with no data relabeling or decoder optimization.
This is the fixed real Fock-input setting, not an assertion about arbitrary
phase-coherent input superpositions. Species/internal-state changes are not used.

Gauge equivalence of count laws does NOT preserve the embedding of REAL
spin vectors in P101's energy identity. That identity used the original
cos(theta_ij)=-1/2 convention and is not generalized to arbitrary flux here.
Nonnegative spectral factors in(3) also do not imply an entrywise nonnegative T.

## Endpoints and degeneracy

At beta=0, x=y=1 and T=I for every flux. At phi=0, x=y and the ground is
simple for a>0; the two middle excited eigenvalues coincide. At phi=pi/4,
lambda_0=lambda_1 and lambda_2=lambda_3, so the ground has rank2:

    x=1, y=exp[-sqrt(2) beta a/Lambda], spectrum_F(T)=(1,1,y,y).

For fixed a>0,phi<pi/4 and beta->infinity, canonical T approaches the uniform-bright
rank-one projector F_0F_0†. At phi=pi/4 it instead approaches the rank-two
projector F diag(1,1,0,0)F†, the algebraic corner(x,y)=(1,0).
The simple-ground rank-one surrogate must NOT be applied to that endpoint.
The strong-filter and phi->pi/4 limits do not commute; a small positive gap
does not supply a uniform finite-strength rank-one approximation.

If a=0, L=0,Lambda=1,H=0,T=I for ALL beta. Flux then has no observable
edge meaning; the ground is fourfold. Treat it separately, not as a bright
rank-one limit. Ground subtraction/normalization define an ideal compiler;
they do not restore transmission lost in an actual device.

## Precisely conditional square-certificate transfer

For the P101 nonnegative graph convention restrict0<a<=1:
w_j,j+1=1-a and w_02=w_13=1. The adjacent-pair partitions cost4-2a and
the opposite-pair partition costs4-4a. For every balanced partition Z,

    C_a(Z)=2a C_(1/2)(Z)+(4-8a).                        (4)

Here C_(1/2) is P101's graph with costs3 and2 on the SAME vertex labels.
The graph is connected for0<a<1; at a=1 it is two disjoint unit-weight
diagonals. The optical reduction holds for any a>0, but a>1 would create
negative graph weights and is outside this graph/cost scope. At a=0 all
cuts cost4 and their mean contrast is identically0.

IF an independently valid certificate proves, for one specified P101
decoder, delta_(1/2)(x,y)=E_B C_(1/2)-E_D C_(1/2)>=0 throughout[0,1]^2,
THEN(3), labelled-count invariance and normalization give

    delta_a(beta,Phi)=2a delta_(1/2)(x(beta,phi),y(beta,phi))>=0. (5)

The same decoder, four-CF source, canonical vacuum dilation, full raw-event
denominator and same optical parameter for D are essential. The conclusion
is a mean comparison to that allowed D member. It gives no equality of B/D
laws, tail/hitting/best-of-run domination, matched total cost, actual loss
certificate, other graph transfer or arbitrary state-dependent compilation.
The square certificate is a premise, NOT established by P115, P107 grid
values or P112's certificate obstruction. No P114 sign is promoted here.

Only this file was written. No import/AST, scripted scientific calculation,
symbolic engine, RNG, graph draw, native/test/runner/QPU, manuscript edit,
push or other source/contract/raw-data change occurred.
