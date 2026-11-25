# P53d — fixed witness against every classical phase (STATIC proposal)

Question: for the SAME B source at theta=pi/3 and saved witness
w=(X04-X15)/2, is g_G(phi)=E[b4(G),phi](w)-E[B,pi/3](w) strictly positive
for every real phi and every one of35 complementary groupings? B, decoder,
old graph and w remain fixed; no optimizer training or replacement graph.
This card introduces no code, imports, evaluated controls or polynomials.
P55's new mechanism keeps numerical priority.

## Exact scalar construction and resource check

For G containing r inputs from ports4..7, its four-photon creation
coefficients C[G,u](zeta) are REAL integer polynomials of degree<=3r,
zeta=exp(i*phi). Define Laurent probability numerators

    A[G,u,k] = prod(u_i!)*sum_h C[G,u,h]*C[G,u,h+k].

They are symmetric in k, with k=-3r..3r, and probability denominator8^4.
The complementary group has r'=4-r. Probability convolution therefore has
Laurent degree<=12, even in phi; its scalar mean has rational cos(k*phi)
coefficients for k0..12. No extra final-occupation Fock factor is introduced.

For total occupation n, sum the unchanged integer tie weights to obtain
s(n)=sum_t weight_t*(X04(t)-X15(t)), so |s|<=420 and E_tie(w|n)=s(n)/840.
Precompute only M[u,v]=s(u+v), size330x330. The Laurent scalar coefficients
are contractions A[G]^T M A[Gc], folded by k+l, with denominator840*8^8.
There is NO need to construct6435 occupation laws times25 Fourier entries.
Keep all35 groupings and zero coefficients; no favorable phase/group filter.

Cauchy bounds |A[u,k]|<=A[u,0], sum_u A[u,0]=4096, hence every column L1
<=4096. Verify those bounds using Python integers BEFORE int64 conversion.
Then |M A|<=1,720,320 and every bilinear entry<=7,046,430,720 in absolute
value, including partial sums. Folding at most13 terms and multiplying
offzero harmonics by2 stays below2^38. Both operands of each matrix product
must be int64; cast outputs to Python integers before Chebyshev/Fraction work.
Thus these matrix products are exact integer operations, not floating proofs.

Using symmetry of M, multiply M by the smaller Laurent bank first. The35
groupings have r0/1/2/3 multiplicities1/12/18/4. A conservative estimate is
39,502,650 integer multiply-adds, with <8MiB numerical arrays. Scalar rational
postprocessing is small. Propose CPU20s/wall30s/thread1/log4MiB/scientific4MiB,
planned64MiB scientific data, zero LPs; no hard Darwin memory guarantee.

## Frozen certificate ladder proposed for ROOT arbitration

Let f_G(phi)=a0+sum_(k=1)^12 ak*cos(k*phi), b=the SAME saved exact B mean.
First compute the exact triangle lower bound a0-sum|ak|-b. A positive bound
certifies a strict uniform gap; a negative bound proves nothing about a phase.

For an unresolved grouping, set t=cos(phi) and form the exact polynomial
g_G(t)=a0+sum ak*T_k(t)-b over Q, degree<=12. Try degree12 Bernstein controls
on the WHOLE [-1,1]. If unresolved, use degree24 on exactly EIGHT fixed
intervals [t_j,t_(j+1)], t_j=-1+j/4, j0..7. No adaptive split, new degree,
root finder, phase optimization or extra stage. Exact affine substitution
and Bernstein-to-power reconstruction must recover the original polynomial.

All controls positive give a strict lower bound; all nonnegative give only a
weak nonnegative certificate if their minimum is zero. Every interval and
all35 groupings must be covered, retaining failures. A negative INTERIOR
Bernstein control is only inconclusive. A negative endpoint value at one of
the PREDECLARED t_j is an actual exact falsifier, phi=arccos(t_j), without
changing the B phase; an exact endpoint zero falsifies strictness only.
Never identify a Bernstein control with an optimal classical phase.

Outcomes: STRICT_UNIFORM_GAP, NONNEGATIVE_WITHOUT_STRICT_BOUND, an explicit
negative/zero registered endpoint witness, or INCONCLUSIVE. A failed finite
certificate is not phase nonmembership or evidence of optimizer benefit.
Any accepted statement concerns this fixed N8 witness/architecture against
phase-retuned b4 ONLY; other controls and feasible graph search remain open.

Only after ROOT approval: freeze source/spec/tests/contracts, qualified exact
references for the scalar contraction and polynomial transforms, independent
static review, one bounded qualification, then separately authorized main.
Archive all35 harmonic polynomials, raw group spectra, tie scalar, bounds and
Bernstein controls. Preserve P53/P53b/P53c and any failure. No QPU, paper or
positive-optimizer claim follows, even from a verified uniform certificate.
