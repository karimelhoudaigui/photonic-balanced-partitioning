# P93: low-rank initializer surrogate and raw-observation stability

26 November 2026. **Verdict: the proposed decomposition and conditional
stability bound are proved below.** No small residual on actual graphs,
efficient classical full-Fock sampler, optimization obstruction or advantage
is established. The frozen P90a compiler and experiment remain unchanged.

## 1. Exact objects and algebraic decomposition

Fix `K>=1`, a real symmetric weighted graph and a current balanced S,T.
Use the paired rank-sorted orders of the P90a card at `14d8dbdd`, SHA-256
`dfdcabfd93cf1a1e0d06fb370ad295123c1726247857820acab9f5d08d04c660`.
Let `u=ell_T`, `v=ell_S` be real K-vectors, and let the real K-by-K block
B have entries `B[a,i]=w_(s_i,t_a)`: target rows, source columns.
Here B denotes a graph block, not a probability law. With `1` the real
all-ones column, the P90 matrix and Hermitian initializer are

    M = u1^T - 1v^T + 2B,
    H = (M+M^T)/2 + i(M-M^T)/2.

Set `z=(u-v)+i(u+v)`. Direct expansion gives exactly

    H = H0+E,
    H0 = (z1^T + 1z^dagger)/2,
    E  = (1+i)B + (1-i)B^T.

Both summands are Hermitian. The range of H0 lies in the complex span
of z and 1, so `rank(H0)<=2`. This can drop to one or zero. The spectral
norm obeys

    ||E||op <= sqrt(2)||B||op + sqrt(2)||B^T||op
             = 2sqrt(2)||B||op.

No symmetry of B was used: the two label sets have distinct meanings,
with their coordinate pairing explicitly fixed before these operations.

## 2. Shared normalization and one-particle comparison

Keep the original normalization and angle exactly:

    d=max(1,||H||op),  V=exp(-iH/d),  V0=exp(-iH0/d).

In particular V0 does not use its own separately chosen normalizer.
All matrices here describe exact mathematical unitaries; rounding and
any numerical certificate would require separate implementation review.

Differentiating `exp[-i(1-s)H/d] exp[-is H0/d]` and integrating yields

    V-V0 = -i integral_0^1 exp[-i(1-s)H/d] (E/d)
                              exp[-is H0/d] ds.

The two exponential factors are unitary, so

    ||V-V0||op <= ||E||op/d.

Let delta be any nonnegative certified upper bound for that distance;
`min(2,||E||op/d)` is one such choice, since two unitaries differ by
operator norm at most two; the graph-block envelope above is also valid.

H0 vanishes on its kernel, hence V0 is identity there. Therefore
`ker(H0) subset ker(V0-I)`, proving `rank(V0-I)<=rank(H0)<=2`.
This receiving-coordinate rank does not bound photon number or eliminate many-boson interference.

## 3. Full raw law with the same pre-R port transport

Use a known normalized collision-free K-photon source, K vacuum inputs,
the same uniform splitter probability one half, and the same physical
source/target orders sigma,tau in both models. Condition on their common
pre-R marks; averaging these later only contracts TV. Transport V and V0 by
those identical row/column permutations to W and W0. Then
`||W-W0||op<=delta`. Both are compiled before the transferred set R.

The kept-bank observations determine R. For every R, in physical port
coordinates, its marginal probability is exactly `2^-K` in both models.
The conditional receiver input is the normalized indistinguishable-boson
Fock state `|1_R>` of `r=|R|` photons. All collisions and output counts
are measured; the kept bank plus receiving bank always contains K photons.

On the symmetric r-particle space the passive lift Gamma_r(W) is the
restriction of `W^tensor r`. Tensor telescoping gives

    ||Gamma_r(W)-Gamma_r(W0)||op <= r delta.

Indeed the tensor difference is a sum of r terms, each containing one
`W-W0` and otherwise unitary factors. Restricting to the symmetric space
cannot increase its norm. This does not replace bosons by independent
photons; it is an operator bound on their normalized common Fock space.

For normalized pure states psi,phi, their trace distance satisfies
`D^2=1-|<psi,phi>|^2 <= ||psi-phi||^2`. The inequality follows because
the difference of the right and left sides is `|1-<psi,phi>|^2`.
Complete PNR measurement contracts that distance. Consequently, for
the two conditional receiver count laws,

    TV(P_R,Q_R) <= min(1,r delta).

At r=0 both conditional states and observations are vacuum, with error
zero. Global phases do not create a problem: if the two states differ
only by a phase, their PNR laws agree although this norm envelope may
be loose. The bound is one-sided, never an inferred TV lower bound.

Mixing the SAME R probabilities gives the complete joint raw-count bound

    TV(P_raw,Q_raw)
      = sum_(R) 2^-K TV(P_R,Q_R)
      <= E_(r~Bin(K,1/2)) min(1,r delta)
      <= min(1,K delta/2).

The equality uses observed R in the joint alphabet; the last bound combines one and delta times E[r].
No accepted-sector denominator or discarded attempt occurs. The source
cost remains K injected photons per raw attempt, not the mean K/2 transferred
photons. The K=0 vacuum source is separately trivial.

## 4. Common postprocessing and adaptive observation histories

Any SAME classical randomized decoder/quench, with the same graph,
current state, raw-count inputs and common coins, contracts the last TV
bound. It must not acquire different private V/V0 information and then
be called an identical kernel. No claim concerns a conditioned accepted
law, source-label selection after R or changed repair rule.

For a measured/reset protocol with at most T raw attempts, assume the
same observation-driven policy and fresh source model at every matching
history h. Suppose its conditional distance certificate is delta_h;
write `epsilon_h=min(1,K delta_h/2)`. Coupling the next observations
until their first mismatch proves

    TV(P_observation_transcript,Q_observation_transcript)
       <= min(1, sum_(j=1..T) E_P epsilon_(h_j)).

The first-mismatch probability at j is at most
`E[1_(histories still match)*epsilon_(h_j)]<=E_P epsilon_(h_j)`.
Uniform certificates give the corresponding T-times bound. Identical
count-driven stopping may be padded with stop symbols. Hidden coherent
memory, differing controller policies, runtime stopping and internal
matrix/implementation tags are not in this observation-only transcript.
In particular recording V versus V0 as distinct deterministic diagnostic
objects does not inherit a small-TV claim from raw PNR closeness.

## 5. Scope and research disposition

No premise here says H0 dominates E: H0 can vanish while B does not,
and cancellation in H may make the shared denominator unhelpful. The
envelope may simply be one. No actual graph, ratio or matrix was tested.
Even when it is small, V0 is a structured photonic surrogate; efficient
sampling of its entire many-photon law was not established. Its full
physical kept/receiver frame still has cross-bank block `iW0/sqrt(2)`
of rank K. This is not the P69 cross-rank theorem on different blocks.

This result neither rejects P90a before trial nor changes centering,
angle one, normalization, source, card, seeds or controls. No alternative
variant, benchmark or sampler is allocated. Positive optimization,
matched total resource comparisons, novelty and hardware claims remain open.

Provenance: bounded hand derivation of ROOT's candidate using the fixed P90 definitions, not independent discovery.
No new scientific source-code read, import, AST, seed evaluation, RNG,
graph generation, programmatic matrix/probability calculation, experiment,
native call, B outcome, QPU or manuscript action was performed. Only this new
theory note and isolated file/hash/Git operations accompany the proof.
