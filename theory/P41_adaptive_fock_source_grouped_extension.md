# Grouped domination extends to bunched Fock sources

Author: p41_adaptive. New derivation candidate, independent audit PENDING.
This is an extension of the grouped-output construction, not a revision of
the frozen encoding lane's statement or its finite probe. No numerical run
was executed for this note. Novelty is unassessed; generalized permanent
estimators and occupation-dependent transition bounds are known ingredients.

## Definitions and exact statement

Let source occupations s_1,...,s_r be positive integers with total N. Let
V:C^r->C^m be a contraction. Inject the pure Fock state with s_j identical
photons in occupied input j. Let G_1,...,G_N be disjoint nonempty observed
output groups. A useful tuple x selects exactly one photon per group.

Write V_x[s] for the N-by-N matrix whose rows are x and whose column j is
repeated s_j times. The unconditioned useful probability is

    p_s(x)=|per(V_x[s])|^2 / product_j s_j!.

There is an always-feasible classical proposal with O(mr) arithmetic per draw
and probabilities satisfying

    q_s(x) >= R_s p_s(x),
    R_s = product_j s_j^(s_j)/s_j! >= 1.                       (1)

Consequently the total physical useful probability obeys the sharp bound

    P_useful <= 1/R_s = product_j s_j!/s_j^(s_j).               (2)

The claim concerns fixed grouped readout, given V and s, with full attempts
charged. It does not cover arbitrary non-Fock coherent input superpositions,
general herald-pattern unions, all-CF decoding or full adaptive optimization.

## Proof and sampler

Draw r independent integers q_j uniformly from0,...,N, set
theta_j=2pi q_j/(N+1), and z_j=sqrt(s_j) exp(i theta_j).
Thus ||z||^2=N. Compute alpha=Vz.
For each group draw x_g independently with weights |alpha_i|^2, normalized
inside that group; use a fixed group element when its intensity is zero.

The disjoint group intensities a_g satisfy sum_g a_g<=N. There are N groups,
so product_g a_g<=1. As in the single-occupation construction,

    q_s(x|z) >= product_g |alpha_(x_g)|^2 = |F_x(theta)|^2.

Expand F_x=product_g sum_j V_(x_g,j) sqrt(s_j) exp(i theta_j).
Its coefficient at occupation s is

    c_s = per(V_x[s]) product_j s_j^(s_j/2) / product_j s_j!.

The divisor product s_j! counts permutations of repeated columns. Uniform
(N+1)-th roots distinguish every exponent0,...,N, so discrete Fourier
orthogonality extracts this coefficient exactly:

    E_theta[exp(-i sum_j s_j theta_j) F_x(theta)]=c_s.

Since the prefactor has modulus one, Cauchy-Schwarz gives E|F_x|^2>=|c_s|^2.
Combining the inequalities proves(1), because

    |c_s|^2 = p_s(x) product_j s_j^(s_j)/s_j!.

The integer inequality s^s>=s! proves R_s>=1. Summing(1) over useful x and
using sum_x q_s(x)=1 proves(2). No high-dimensional enumeration is part of
the sampler; exact phase probabilities are finite. Its exact-arithmetic
complexity and finite-precision caveats must remain separate.

The corresponding separable-state cover also extends. Let chi(theta) be the
product vector with group factors sum_(i in Gg) alpha_i |i>, and Sigma its
mean outer product. Its trace is at most one. Fourier extraction above gives
the vector coefficient sqrt(R_s) T, where T is the unnormalized physical
useful state. The covariance inequality therefore gives

    Sigma >= R_s |T><T|.

For useful probability p=||T||^2>0 and normalized state phi=T/sqrt(p), define
1+R_ent(phi) as minimum trace of a separable PSD operator dominating
|phi><phi|. Dividing the cover by R_s p proves

    R_s p [1+R_ent(phi)] <= 1.

This uses the stated cover definition; identifying a named external robustness
measure or asserting novelty of this extension requires a separate source audit.

## Sharpness and interpretation

Partition the N output groups into blocks of sizes s_1,...,s_r. Give source
column j amplitude1/sqrt(s_j) in one designated mode of each group of block j
and zero elsewhere. These columns have disjoint supports and are orthonormal.
For each input's s_j photons, uniform splitting gives probability s_j!/s_j^s_j
of exactly one photon in every assigned group. Different input blocks are
independent, so the product in(2) is attained. The isometry can be completed
to a unitary and additional empty modes can be appended inside every group.

Thus simply injecting bunched Fock states does not escape the grouped-readout
countercontrol; it also imposes a sharp useful-event penalty. This is a
feasibility statement, not an optimization advantage or broad passive-optics
impossibility. As for the single-occupation theorem, graph scoring, constructing
V, source preparation and total resource costs remain charged. Per-history
pointwise dominance alone does not imply an efficient dominating simulation of
an arbitrary adaptive training policy.
