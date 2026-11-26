# P87: sharp first-order passive oracle obstruction accepted

ROOT read all168+308 source lines and the complete344-line exact-source
audit. The finite bound, infimum/limit argument and operator variant are
accepted without correction. This is a precise oracle obstruction, not a
proof against all photonic graph-optimization mechanisms.

| Artifact | Original commit | SHA256 |
| --- | --- | --- |
| `theory/P87_FIRST_ORDER_PASSIVE_COST_PHASE.md` | 643686079fb50c16f7d23b0a7f7b7214f0a4516c | f4934640c71362f76c179d57435974d0c6959c0ea18b867c87d84a943bdac3cc |
| `research/P87_independent_first_order_optimality.md` | 17ba1d4568621870cf18d6766d79e6714654b5ac | c23638c0345a0c5c1fdcc35d59228367303cebec3d58a830a9b3a7d894b132cb |
| `theory/P87_EXACT_HASH_REVIEW.md` | b77c8c02dbe4e68c9c33db5c7ae44a48cdac4f29 | 22cfcb7f1a8d9915987075ad5cdf20a2ab0bd1eb14053ccc8041b24ea38e69ad |

ROOT supplied the candidate route before the independent reconstruction.
The reviewer wrote its entire standalone source audit before reading that
reconstruction, recording the intermediate hash. These are independent agent
contexts sharing a candidate/model/supervisor, not independent discovery,
an external referee report or novelty clearance.

## Accepted theorem and mechanism

Fix even N>=4, a complement-symmetric real balanced cost C, N photons on
2N dual rails, and the lossless passive no-ancilla/no-herald model of P81.
Let delta(U,gamma) be the worst balanced-basis STATE-VECTOR error relative
to the cost phase, fitted with ONE common global phase. Optimize over ALL
passive U, without a continuity or generator assumption. For cost range R,

    lim_(gamma->0,gamma!=0) inf_U delta(U,gamma)/|gamma| = R/2.

Identity optics attains that same first-order coefficient. The optimized
operator norm from the balanced subspace INTO the full N-photon space
has the same limit. Extrema only analyze the metric; identity uses no
optimum/mask and no graph-dependent setting. The fitted global phase is
an unobservable reference, not an optimization resource.

P81/P86 first show that small oracle error forces physical U's entire
off-diagonal Frobenius mass to be O_N(delta). A principal CF-to-itself
permanent has no nonidentity term with just ONE moved label. Its deviation
from the product of physical diagonal entries is therefore O_N(delta²).
Complementary code inputs use all2N physical rails once in their combined
diagonal products. This yields the sharper invariant

    |sin(gamma*(C(S)-C(T)))| <= 2delta+2E*delta²

in the small-error branch. The explicit conservative E=(N!-1)d² and
the other branch yield a uniform finite lower bound; identity's centered
phase upper bound2sin(|gamma|R/4) matches its leading coefficient.

N and C are FIXED: E can grow factorially, so this is no dimension-uniform
or practical error-threshold theorem. It does not show finite-angle identity
optimality, rule out periodic aliases, or lower-bound basis-PNR/fidelity
errors. Extra resources, selected inputs and P82's state-dependent
collision-repair sampler change the task. No cumulative algorithmic error
claim follows just by summing one-step bounds. Novelty remains OPEN.

No numerical experiment/import/RNG/backend was needed. The1187PASS
executable tree is unchanged; paper/main/QPU stay frozen. The positive
optimum-blind optimizer objective remains OPEN.
