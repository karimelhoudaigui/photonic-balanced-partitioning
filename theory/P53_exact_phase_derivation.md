# P53 exact phase algebra — reconstructed before implementation

ROOT card `87abe69b21692e7fc0d48306ebc28517e59849a2` read in full. This is a
post-P52 follow-up motivated by its four numerical fits, not a prediction of
those outcomes or a positive optimizer. No P53 code/import/integer computation,
NPZ read, graph, sample or certificate has been used for this derivation.

Put A_j=X_j+X_(j+4), B_j=X_j-X_(j+4). The product of the four unnormalized
Walsh linear forms is, by pairing factors and expanding,

    F(v)=sum_j v_j^4-2 sum_(j<k) v_j^2 v_k^2+8 v0 v1 v2 v3.

Substituting v_j=exp(i*j*theta)B_j leaves only EVEN theta exponents:

    F_theta(B)=sum_j exp(i*4j*theta)B_j^4
        -2 sum_(j<k)exp(i*2(j+k)*theta)B_j^2 B_k^2
        +8 exp(i*6theta) B0 B1 B2 B3.

Thus C(X,z)=F(A)F_theta(B), z=exp(i2theta), has real INTEGER coefficients
c[n,h], h0..6. Each quartic factor has90 monomials in8 output variables:
4*5 from bunches,6*9 from pairs and16 from all-one pair totals. At most8100
monomial products suffice; no8! permanent enumeration is required.

Each U entry has denominator sqrt8. For CF input8 the wave polynomial is
C/8^4. In NORMALIZED output Fock states its amplitude is

    sqrt(prod_i n_i!)*sum_h c[n,h]z^h / 8^4.

The output factorial MULTIPLIES the squared monomial coefficient. Define
a[n,0]=n!*sum_h c[n,h]^2 and a[n,d]=2*n!*sum_h c[n,h]c[n,h+d]. Then

    P_n(theta)=(a[n,0]+sum_(d=1)^6 a[n,d]cos(2dtheta))/8^8.

Normalization must be verified as the EXACT identity sum_n a[n,0]=8^8,
sum_n a[n,d]=0 for d>0, retaining all6435 occupations including zero arrays.
The expression is nonnegative on the unit circle by its squared-amplitude
construction; this is not inferred by testing four angles.

For a fixed occupation, the number of source assignments bounds
sum_h |c[n,h]| <= 8!/prod n_i!, so |c[n,h]|<=40320. The quartic-factor
coefficient L1 norms are384 each, giving a global C coefficient L1<=147456.
Integer source arrays are small, but downstream Chebyshev/Bernstein transforms
must use Python arbitrary integers/Fractions; degree12 denominators and
intermediate cancellations must not be put through int64 or floating rounding.

## Exact ties, controls and Bernstein sufficiency

Let h be the number strictly above the fourth-count threshold and t the
number tied. If threshold0, t=8-h, h1..3, so denominators are35,15,5.
If threshold>=1, t+2h<=8 and h<=3. The possible binomial denominators are a
subset of {1,2,3,4,5,6,10,15,20,35,70}. All divide420;20,35 and6 are attained,
so420 is also the exact overall LCM. Do NOT include impossible C(8,3)=56 ties.

Consequently exact70-rank and28-edge cosine/power coefficients share
D=420*8^8. For b4 at theta0/pi2, each4-photon source polynomial has Gaussian-
integer coefficients. Its probability numerator is n!*(Re(c)^2+Im(c)^2),
denominator8^4. Convolving these PROBABILITIES needs no extra final-output
factorial and has denominator8^8. Tie integration gives the same D. Uniform70
and crossing4/7 also have denominators dividing D. All35 groupings per endpoint
are required, making a fixed71-vertex library with exact rational coordinates.

Set x=(1+cos2theta)/2. Exact Chebyshev recurrence for T_d(2x-1) yields rational
polynomials degree<=6. For p(x)=sum_k a_k x^k, degree-d Bernstein controls are

    beta_j=sum_(k<=j) a_k * C(j,k)/C(d,k),   d>=6.

LCM_k C(6,k)=60; LCM_k C(12,k)=27720. Degree12 elevation uses only exact
convex combinations of degree6 controls. If every beta_j has exact convex
weights lambda_j over the fixed library, then
Lambda_c(x)=sum_j C(d,j)x^j(1-x)^(d-j)lambda_jc proves the mean identity
for EVERY real theta. Verify the resulting POWER polynomial independently.

This condition is sufficient, not necessary. If a nonconstant curve touches
a supporting face at an interior x0, all Bernstein basis weights there are
positive. Controls inside the hull would force every control into that face,
hence the whole curve into it, a contradiction. Finite degree12 cannot promise
success. Failure of these controls, support exactification or a numerical LP
is inconclusive about membership of the curve itself.

Every edge vector obeys8 independent incident-sum constraints (=4), leaving
affine dimension<=20. An exact convex witness therefore admits support<=21
(remove affine dependencies until a coefficient becomes zero). Floating LP
weights select a support ONLY. Exact rational linear solving, signs, sum1
and all28 identities must then verify, without rationalizing source/target
coefficients from P52 floats. Row relabeling transports a valid identity;
other encodings, losses, tail/best-of-shot laws and adaptive histories do not
follow from this mean-only result. No physical/runtime/novelty claim follows.
