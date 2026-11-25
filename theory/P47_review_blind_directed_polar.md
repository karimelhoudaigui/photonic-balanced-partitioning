# P47 — independent card-first reconstruction of the directed guide

Adaptive lane, shared broad context. Read only the P47 blind claim card in
the physics worktree before this reconstruction, not its companion proof or
encoding code. No numerical work or optimization result is asserted. The
classical proxy and the elementary Fourier argument are not claimed novel.

Let b>=2, D real inside-by-outside swap costs, Z=I-11*/b, R=ZDZ,
sigma=||R||op>0, C=R/sigma, and F the positive-sign unitary Fourier matrix.
Write G=C odot F, c=max|C_ij|, nu=||G||op, h=max(c,nu), epsilon=1/(4h).
When R=0, use Y=F without dividing by zero. Otherwise M=F-epsilon G and
Y=polar(M). Let s_C(W)=sum_ij C_ij|W_ij|^2, with real Frobenius inner product.

## Tangent and finite step

The tangent space at F consists of FK for K*=-K. Its orthogonal projection of
G is Pi=F skew(F*G)=G-F sym(F*G). Differentiating the polar map at F gives
Y'(0)=-Pi. Therefore

    d/d epsilon s_C(polar(F-epsilon G)) at0 = -2||Pi||F^2.

Since epsilon*nu<=1/4, s_min(M)>=1-epsilon*nu>=3/4. In particular the polar
factor is unique. It globally minimizes the Frobenius distance to M among
unitaries. Comparing that distance with F gives, with E=Y-F,

    ||E+epsilon G||F^2 <= ||epsilon G||F^2,
    2 Re<G,E> <= -||E||F^2/epsilon.

The quadratic objective expands EXACTLY as

    s_C(Y)-s_C(F)=2 Re<G,E>+sum_ij C_ij|E_ij|^2
                <=-(1/epsilon-c)||E||F^2
                <=-3||E||F^2/(4epsilon).

This allows signed C; no entrywise positivity assumption was used. Centering
changes s_D by a constant on doubly stochastic |W|^2, because every removed
row/column additive term is summed against row/column sums1. Consequently
s_D(Y)-s_D(F)=sigma*(s_C(Y)-s_C(F)). This is a FINITE cost-proxy descent bound.

## Stationarity and prime strictness

Put B=F*G. If Y=F, then F*M=I-epsilon B is Hermitian positive, hence B is
Hermitian and Pi=0. Conversely, if Pi=0 then B is Hermitian; the bound
epsilon||B||<=1/4 makes I-epsilon B positive, so Y=F. Thus the specified
safe step is stationary exactly when its tangent projection vanishes.

For Fourier F, define h_t(j)=b^(-1) sum_i C_ij exp(2pi i i t/b). Then

    B_ab=h_(b-a)(b),
    B=B* iff h_t(j)=h_t(j-t) for every j,t mod b.

If b is prime and t!=0, repeated addition of t visits ALL column indices.
Thus h_t is constant. Row-centering of C makes sum_j h_t(j)=0, so that
constant is zero. Column-centering gives h_0(j)=0. Fourier inversion now
gives C=0. Therefore NONZERO real doubly centered C has Pi!=0 and Y!=F at
PRIME b; the finite bound is strictly negative. This is why b13/17 removes
the composite Fourier stationary obstruction, not a proof of useful graph cuts.

An optional quantitative check follows from

    ||Pi||F^2=(1/4)sum_t sum_j |h_t(j)-h_t(j-t)|^2.

For prime b, each nonzero shift on the zero-mean subspace has smallest
singular value2 sin(pi/b), and Parseval gives

    ||Pi||F^2 >= sin^2(pi/b)*||G||F^2.

This lower bound can shrink with b; it supplies no extensive optimization
response or many-photon advantage.

## Size and spectral angle bounds

Since ||C||op=1 and F is flat,

    ||G||F^2=||C||F^2/b<=1.

A FIXED quarter-step, not the adaptive epsilon, has
||Y-F||F<=2*(1/4)*||G||F<=1/2 by triangle inequality and polar optimality.
The adaptive step removes this dimension-independent Frobenius bound, but
strictness alone provides no growing-response lower bound.

For the adaptive step let Q=F*Y and H=(M*M)^(1/2). Then F*M=QH and
||QH-I||op<=1/4. If Qv=exp(i theta)v with ||v||=1, its normality gives
v*QH v=exp(i theta)*(v*Hv), with v*Hv>0. Thus this positive-radius point
lies within1/4 of1, implying cos(theta)>0 and |sin(theta)|<=1/4. Hence

    ||Y-F||op <= sqrt(2-2sqrt(15/16)).

This argument does not assume M normal. It is an upper angle bound. At b13
it also excludes zero entries because1/sqrt(13) exceeds that constant; the
same simple inference FAILS at b17. In neither case does it prove extensive
interference, useful decoded partitions, or hardware performance.

## Exact composite graph stall from the card

Let b4, v=(1,-1,1,-1), within-side edges17/16 and cross edges1+v_i v_j/8.
The old-side anchor cut is16. All degrees are115/16; its linear cut gradients
are13/16 on old vertices and-13/16 on new vertices. Therefore

    D_ij=3/8+v_i v_j/4,
    R=C=vv*/4, sigma=1, nu=c=1/4, epsilon=1.

All single swaps increase the cut by either1/8 or5/8, so this is a strict
one-swap local minimum. The partition{0,2,4,6} has cut

    2*(4*17/16)+8*(7/8)=31/2 <16.

Nevertheless G=(diag(v)F diag(v))/4 and B=F*G is Hermitian: it is1/4
times the shift-by2 permutation followed by diag(v), which commute. Thus
I-B is positive and Y=F EXACTLY, not just within a numerical tolerance.
Nonzero centered C is insufficient at composite b. This is a counterexample
to unqualified strictness, not a counterexample to prime strictness.

## Hungarian control and the optimization gap

P=|W|^2 is doubly stochastic. A linear routing objective has a permutation
optimum, so the Hungarian assignment on C (or D, differing only by a constant)
matches or improves ANY unistochastic proxy value. It uses information already
computed classically and must receive its full preprocessing/search credit.
B and D share every one-particle transition intensity of the SAME W. A lower
s_D cannot itself be an interference-dependent B optimization result.

For simultaneous removed set A and added set B matched in pairs(a_r,b_r),
the ACTUAL cut change equals

    sum_r D_(a_r,b_r)
      -2 sum_(r<s)(A_(a_r,a_s)+A_(b_r,b_s))
      +2 sum_(r!=s) A_(a_r,b_s).

Those interaction terms are absent from the routing proxy. Transferring ALL
old vertices to ALL new vertices always gives the complementary partition and
the SAME cut, whatever negative centered assignment cost is achieved. In the
explicit graph, Hungarian centered cost is-1 and actual full-complement cut
remains16. Proxy descent is therefore not a cut-improvement theorem.

The only accepted consequence here is a genuinely cost-directed classical
guide, strictly moving away from prime F when C!=0. The common nonlinear PIT
decoder, independently optimized D/phase/other fields, strong feasible search,
fresh labels/seeds/graphs, total costs, replication and physical validation
remain unproved obligations. No numerical or hardware experiment follows from
this analytic review alone.
