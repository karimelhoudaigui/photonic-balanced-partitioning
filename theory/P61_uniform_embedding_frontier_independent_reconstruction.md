# P61: independent reconstruction of the uniform-embedding frontier theorem

**Verdict: proved under the conditions below.** The claim is mapping-averaged
stochastic domination of best observed cost, at up to2^s paid classical
scores per trial. It is not a fixed-embedding, wall-time, or all-architecture
no-go. This text was derived and frozen BEFORE reading ROOT's separate
proof. ROOT supplied the hypothesis and proposed conclusion; the proof,
edge cases and counterexamples here were independently reconstructed.
No code, import, graph draw or numerical computation was used. No novelty
or positive scientific result is claimed.

## Conditions and precise conclusion

Fix a graph/objective C on K-subsets of N LABELLED vertices before drawing
an embedding. Optical mode labels and an active mode set A0, |A0|=s, are
fixed. Draw P uniformly from ALL N! mode-to-vertex bijections, independently
of the graph. This SAME P is used for every optical attempt.

Each attempt has a fresh source and a fresh private uniform tie priority.
In mode coordinates the joint inactive count vector Y on O0=A0^c has a
fixed law mu, independent of P, the current phase and prior measurement
history. It may depend on shared data held fixed in this theorem, provided
that conditioning on those data leaves P uniform and mu independent of P.
Phases may be chosen by ANY policy using graph, P and earlier outcomes.
The conditional active-count distribution may be arbitrary and history
dependent; the inactive marginal assumption is what matters.

The decoder chooses a uniform K-subset among ALL maximum-captured-count
subsets, without postselection on attempts. The returned optical best is
the minimum C over at most T decoded attempts, where T is a fixed cap.
All training attempts included in that returned best count toward T.
No additional P-dependent classically scored candidate outside these
decoded subsets is silently added to this definition.

Classical comparator, on EACH of T trials:

1. Draw a fresh uniform s-subset A of vertex labels.
2. Draw a fresh uniform order of its complement O.
3. For every B subset A with0<=K-|B|<=N-s, form
   S_B=B union the first K-|B| labels of O.
4. Score every such S_B and retain the best across all trials.

There are at most2^s scores per trial (exactly2^s when s<=K<=N-s).
For every real threshold c,

    Pr(classical_best_T <= c) >= E_P Pr(optical_best_T <= c | P).    (1)

Probabilities on the right include optical/tie/policy coins. The statement
holds for any fixed objective C, not just a quadratic graph cut.

## Step 1: conditional frontier contains every decoded outcome

A private uniform random total priority order implements uniform boundary
ties exactly. Fix P, inactive counts Y and the priority order. Order the
inactive vertices by descending(count,priority), obtaining pi_O. The
restriction of any global topK outcome to inactive vertices is a PREFIX
of pi_O. If its chosen active set is B, that prefix has length K-|B|.
Therefore the decoded subset belongs to the frontier family in step3,
whatever the active counts or the chosen phase.

Let F(P,Y,priority) be the minimum objective on this family. Pointwise,

    F(P,Y,priority) <= C(decoded subset).                         (2)

This also proves at most s exchanges between two topK outputs coupled at
the same inactive counts/priorities. The frontier permits completions
that may not be physically reachable; this only strengthens the comparator.

## Step 2: conditional iid frontier bounds adaptive optical policies

For a threshold c define r_P(c)=Pr_mu,priority[F(P,Y,priority)<=c | P].
Fresh inactive vectors/priorities are iid conditional on fixed P. Changing
phase according to past outcomes does not alter that law. Consequently the
T frontier values are iid conditional on P even when optical outputs are
not. By(2), or by bounding each conditional optical hit probability,

    Pr(optical_best_T > c | P) >= (1-r_P(c))^T.                    (3)

Adaptive stopping at or before T is allowed: padding to T can only improve
the optical best. Conditioning on successful shots rather than counting
physical attempts would change the budget/law and is not this assertion.

## Step 3: uniform embedding eliminates the inactive sampler in one trial

Fix ANY mode-coordinate inactive order produced by Y and tie priorities.
For independent uniform P, its image is a uniformly ordered complement
of a uniformly chosen active label set P(A0). Internal order inside A is
irrelevant because the frontier enumerates all its subsets. This law does
not depend on which mode order Y generated. Hence

    rbar(c)=E_P r_P(c)

is EXACTLY the single-trial hit probability of the purely classical
comparator. No inactive quantum sample or conditional-state computation
is needed by that comparator. This step requires independence of mu and P;
it is not obtained merely from independence of phase and the inactive law.

## Step 4: fixed P correlations are handled by Jensen, not ignored

For integer T>=1, x -> (1-x)^T is convex on[0,1]. Averaging(3) yields

    Pr(optical_best_T > c)
      >= E_P (1-r_P(c))^T
      >= (1-E_P r_P(c))^T
      = Pr(classical_best_T > c).

This proves(1). At T0 both return no sampled candidate; at T1 the Jensen
step is equality, while frontier containment may be strict. In particular,
the proof does NOT pretend that quantum fixed-P trials are unconditionally
iid. Their common latent embedding produces a mixture of iid frontiers;
fresh classical embeddings improve best-of-T diversification in this sense.

## Scope failures and auxiliary candidates

There is no pointwise guarantee for a particular fixed embedding. A full-CF
passive example makes this clear: take N18, nine independent HOM pairs and
top9 decoding. Every output picks exactly one vertex from each pair. Let
the graph be K18 with these nine matching edges deleted. Every quantum
output has the minimum cut81-9=72 at that fixed matching embedding. The
fresh classical s3 frontier has positive probability of putting BOTH ends
of a missing matching edge among its common first six inactive vertices;
then every completion cuts at most eight missing edges and costs at least73.
Thus its one-trial success at cost72 is below1. Mapping averaging is
essential; this is not a counterexample to(1).

If mu depends on P through a graph-informed encoder, or P itself is chosen
from the graph/selected after trials, step3 fails. If inactive trials are
negatively correlated rather than fresh iid conditional on P, step2 fails.
A nonuniform, graph-informed or non-topK decoder needs its own analysis.
Uniform embedding is a distributional assumption, not a guarantee for one
chosen deterministic seed or a favorably selected mapping.

Extra classical candidates require care. A deterministic graph-only
frontend incumbent, or a random one independent of P/source coins, can be
granted equally to both algorithms by conditioning on that common data.
An arbitrary P-dependent frontend cannot simply be inserted and declared
covered. For example, in an abstract latent mixture r_P in{0,1}, let a
frontend hit whenever r_P=0 and fail whenever r_P=1. Optical+frontend then
always hits, while the SAME frontend plus a fresh mixed trial can fail.
The weighted Jensen expression is no longer the one above. Either restrict
the theorem to optical decoded candidates, prove independence of the
common frontend, or supply an additional classical comparison argument.

## Paid computational cost

For s<=K<=N-s, all frontier candidates share the first K-s inactive labels.
Only the s active labels and next s inactive labels are variable. One base
cut and external fields of this2s-vertex core permit all2^s scores using
O(Ns+2^s*s^2) arithmetic plus base-cut/order work; every operation is paid.
For s3 this is a six-vertex core and at most eight feasible scores. No
optimum, conditional optical likelihood or permanent is queried.

The theorem compares trials with up to2^s classical scores against one
optical decoded score. It does not establish equal wall time, equal energy,
identical candidate-score counts or a universal classical-cost veto. Any
constant-factor timing comparison must charge preprocessing, randomness,
sorting, scoring, source preparation, training and all physical attempts.
To escape this specific envelope one must change its assumptions: growing
active support, a paid graph-informed outside law/mapping, or a genuinely
different decoder. Larger Fock cardinality alone changes none of the proof.
