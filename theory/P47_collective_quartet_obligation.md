# Collective quartets after P47: an exact cancellation and a distinct open discriminator

Analytic route note, 2026-11-25, physics owner. No code, numerical run or
experiment is proposed as executed. The first cancellation and composite
phase-family formulas were sent to the coordinator before receiving its
aggregate P47 DEV result. The coordinator subsequently communicated a
possible finite DEV separation; no P47 raw has been read for this note.
Nothing here evaluates that outcome or changes its frozen experiment.

## 1. What the full hollow map cannot encode through raw second moments

Take K distinct CF inputs in the old block, empty new block and

    U=[[sqrt(1-p)I,-i sqrt(p)W],[-i sqrt(p)W*,sqrt(1-p)I]],

with W a K-by-K unitary. For occupied-input frame V=U[:,old], write
q_ia=|V_ia|^2, mu_i=sum_a q_ia and P=VV*. Directly expanding creation and
annihilation operators for distinct single-photon inputs gives, for i!=j,

    E_D[n_i n_j]=mu_i mu_j-sum_a q_ia q_ja,
    E_B[n_i n_j]-E_D[n_i n_j]=|P_ij|^2-sum_a q_ia q_ja. (1)

Here P=[[ (1-p)I, i sqrt(p(1-p))W ],
        [ -i sqrt(p(1-p))W*, pI ]]. Therefore the B-minus-D difference is

    0, for old/old or old/new distinct modes;
    -p^2 sum_a |W_ai|^2|W_aj|^2, for distinct new i,j.    (2)

First moments and same-mode second moments also depend only on intensities:
E_B[(n_i)_2]=2[mu_i^2-sum_a q_ia^2], and D is half of that expression.
Thus every UNCONDITIONAL raw quadratic occupation mean is invariant under
any change of W that preserves its entry intensities. For the polynomial
extension of a graph cut, J_num(n)=d^T n-n^T A n with A_ii=0, this includes
its B/D mean difference. This polynomial can be negative on bunched counts;
it is not itself a feasible binary partition objective there.

This does not imply any impossibility for threshold bits, PIT, completion,
hinge gain max(0,Cref-cut), success events, best-of-attempts or adaptive
search. Those functions are nonlinear in more than these moments. In
particular it does NOT refute or explain away P47's completed DEV data.

## 2. Genuine phase-sensitive two-transfer routes, and their classical cover

Fix two old indices a<b as exactly the transferred subset. Its raw mask
probability is p^2(1-p)^(K-2). For distinct new targets i<j, define

    Q_abij=W_ai W_bj conj(W_aj W_bi).

The raw B-minus-D probability of that CF target, INCLUDING the mask factor,
is exactly

    2p^2(1-p)^(K-2) Re(Q_abij).                         (3)

Positive Re(Q) enhances this route and negative Re(Q) suppresses it. If a
route is improving this can have a useful LOCAL sign; unitarity constrains
the compensating other routes and does not guarantee a useful aggregate.

The actual two-swap cut has the collective correction

    J(S0-a-b+i+j)-J(S0)
      =D_ai+D_bj+2(A_aj+A_bi-A_ab-A_ij).                (4)

It is independent of which matching of the same two removed/added sets is
used. Equation (4) shows the missed quadratic interaction; minimizing the
assignment proxy is not minimizing the actual cut.

Even (4) does not immediately make a useful phase guide. If all transferred
pairs are sampled uniformly, then the mean actual cut over exactly two
transfers, with collisions replaced by the same fixed feasible fallback,
is invariant under intensity-preserving W changes. To see this, the old
pair is uniform and the averaged new input pair occupation correlation is
the same for every distinct input pair. All output first/second moments
and old-marker/new-count correlations then depend only on intensities by
the same expansion as (1). These determine the quadratic cut polynomial.
On a collision into i, the probability for each old pair is
2|W_ai W_bi|^2 for B and |W_ai W_bi|^2 for D, also intensity-only. Replacing
that sector by the fixed fallback subtracts/adds phase-invariant terms.

Equivalently, row/column orthogonality cancels the quartets when the true
quadratic weights in (4) are fully summed. A claim of a nonzero mean
phase benefit from that sum would need to identify where this argument's
hypotheses were changed. It cannot silently select a favorable old pair.

There can still be phase-dependent improving MASS or tail gain. However,
explicitly targeting only two-swap events admits a polynomial exact classical
control: enumerate O(K^4) old/target pairs, compute their 2-by-2 permanents,
include all collision/fallback mass, and sample that finite kernel. If the
graph costs of all these routes are evaluated to design the guide, every
discovered improving candidate is credited to the common classical frontend.
Its minimum cannot then be called an optical discovery. At fixed p>0 the
probability of exactly two transfers also becomes exponentially small in K;
taking p~1/K instead returns to O(1)-photon proposals. Neither is the sought
growing collective mechanism.

## 3. A phase-only family that isolates a higher-order copula obligation

Unlike prime Fourier matrices, composite flat Hadamard families can have
non-gauge internal phases. Let K=2n, F_n the normalized Fourier matrix,
D_phi=diag(exp(i phi_alpha)) and

    W_phi=(1/sqrt(2))[[F_n,D_phi F_n],[F_n,-D_phi F_n]].  (5)

This is unitary and every intensity equals 1/(2n), for every phi. It is a
known block-Hadamard construction, not a novelty assertion. The hollow map
using (5) has identical one-mode count PMFs, exact marginal PIT tables,
distinguishable joint count law and Gaussian-B-covariance control for all
phi. Source masks remain Binomial(K,p) with mean Kp; no spectator is added.
The output BOTH-block joint bosonic law can nevertheless change.

Indeed, with old a=(r,alpha), b=(r',beta), new i=(s,gamma), j=(s',delta),
where r,r',s,s' are 0/1, the quartet is

    Q_abij=((-1)^((r-r')(s-s'))/(4n^2))
      *exp(i[(s-s')(phi_alpha-phi_beta)
               +(2pi/n)(alpha-beta)(gamma-delta)]).    (6)

Thus opposite-new-block routes have a controllable interference sign,
while D and the calibrated scalar marginals stay fixed. At n=2, taking
r=r'=0, alpha=0,beta=1, s=0,s'=1, gamma=delta=0 gives
Re(Q)=cos(phi_0-phi_1)/16. Equation (3) switches from enhancement to
suppression as that phase difference changes from 0 to pi. This is a
physical discriminator, not a proof of a favorable graph effect.

A weighted quartet phase fit is polynomially evaluable O(K^4); (6) reduces
it to a classical phase-synchronization/XY objective in exp(i phi_alpha)
after summing coefficients. Spectral rounding/local optimization and all
graph-cost evaluations are shared polynomial classical work; global
optimization of the resulting nonconvex phase objective is not claimed
polynomial. If the weights are merely the actual quadratic cut averaged
as in section 2, their apparent benefit cancels. Selecting nonlinear
improvement weights by exhaustive two-swap scoring falls under its exact
classical cover.

The genuine remaining hypothesis would be: an optimum-blind, charged
phase rule at growing n changes the large-transfer B copula so that the
SAME fixed completion decoder gains over the PHASE-INVARIANT D/Gaussian
arms and over phase-sensitive small-species/coherent-field and nonlocal
classical controls. No such rule with a demonstrated useful sign has yet
been proved here. No pilot is justified by the quartet sign alone. For
large-transfer kernels this note proves neither an efficient exact
classical replacement nor hardness or useful search performance.

## 4. A rectangular isometry removes a different cancellation

The coordinator suggested K ancillary source modes and 2K vertex modes.
For an isometry V: C^K -> C^(2K), set P=VV* and

    H=[[0,V*],[V,0]],
    exp(-itH)=[[cos(t)I,-i sin(t)V*],
              [-i sin(t)V,I+(cos(t)-1)P]].             (7)

This identity follows by splitting vertex space into range(V) and its
orthogonal complement. It is a passive unitary on 3K modes. Distinct photons
start in the ancillary K modes; the vertex count is Binomial(K,p),
p=sin^2(t). ALL ancillary outputs and transfer sectors are retained, with
no herald conditioning or claim of free source preparation. Ignoring
ancillary outputs is an ordinary partial observation, not a no-loss event.

For distinct vertex i,j, (1) now becomes

    E_B[n_i n_j]-E_D[n_i n_j]
       =p^2(|P_ij|^2-sum_a |V_ia|^2|V_ja|^2).          (8)

P is a nontrivial rank-K projector on the 2K vertices, so the full-W
cancellation in (2) need not hold. This is a genuine change of architecture.
Its sign for an arbitrary graph is not automatic. First/two-mode means
and their programmable objectives remain classically evaluable; a gain in
those means is not an optimization advantage. A specific graph-dependent
isometry, a justified nonlinear search discriminator and its charged
classical controls remain missing. This note does not invent them from
the mere availability of a projector.

## 5. A genuine interaction phase is a different resource model

A desired exp(-i gamma sum_ij J_ij n_i n_j) is not obtained by inserting
single-mode phases into a passive one-particle matrix. For example a
two-mode passive map that fixes |10> and |01> up to phases maps |11> to
the SUM of those phases; it cannot add an independent controlled phase.
A diagonal cost phase immediately followed by occupation measurement also
leaves every probability unchanged; a noncommuting mixing step is needed.

Measurement-induced gates with ancillas are a different, legitimate route,
not a free extension of (5). The primary KLM
[source](https://arxiv.org/abs/quant-ph/0006088) distinguishes reliable
feedback-assisted computation from nondeterministic operation. The official
[Perceval v1.1 catalog](https://perceval.quandela.net/docs/v1.1/reference/components/catalog.html)
documents heralded CZ/CNOT and postprocessed gates with herald modes and
postselection; that documentation was read, but the attempted v1.3 catalog
URL was inaccessible and installed API/hardware support was not tested.
No success probability is assumed here. A gate-level proposal must account
for ancilla photons, full failed heralds, detection, feedforward and preparation.
Naively composing independent constant-success heralded gates can multiply
their success probabilities; efficient LOQC constructions are not refuted
by that observation. No such resource-complete construction is supplied by
this note, so this is not currently a cheap implementation of graph quartets.

No numerical evidence, QPU compatibility, novelty or advantage follows from
these analyses. The exact cancellation is narrow; the useful nonlinear
collective mechanism and its scalable classical discriminator remain open.
