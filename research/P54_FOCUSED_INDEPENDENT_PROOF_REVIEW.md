# P54 focused independent proof review

Verdict: **PROVED AS WRITTEN**, for its fixed finite graph, real sqrt(weight)
guide, full one-photon-per-mode input and ideal raw-count uniform-tie decoder.
This is an asymptotic local statement, not a finite-angle/hardware/total-cost
or general passive-optics obstruction.

Exact audited revision:
`4d6826d19fab2d84f4aa7ea80db3353193f5e7cf`, file
`theory/P54_full_input_small_hop_obstruction.md`, SHA256
`6363b35c0bd7987398ad066ee189be876894e0c8f514ef18b7716bf258531e55`.
I read all77 lines after freezing my independent derivation at
`43b35f9c36781cb921c5407df3fb47ab156b93ad`, SHA256
`dc53038f195039cf20959f4975d6e774dfd2274f390d58fe24e92a2bdc8d6e84`.
I had received the question and later narrower sqrt(w) scope, but not the
author proof before that freeze. Same-team review is disclosed; this is not
an external novelty or hardware validation. No executable calculation,
import, simulation, test, graph sample or raw-data consultation was used.

## Load-bearing implications checked

1. For U=exp(itH), the second-quantized generator is
   sum_ij H_ij a_i†a_j. A hop from an initially occupied j into an initially
   occupied i has factor sqrt2; with H_ij=sqrt(w_ij), each normalized Fock
   target therefore has probability2t²w_ij at leading order. Two directions
   per edge give total escape4t²W. The unchanged count's coefficient and
   retention of all other O(t4) patterns are correct.

2. Real H makes every Fock amplitude at -t the conjugate of that at t, hence
   probabilities are even. Fixed N supplies finite output support, so the
   O_G(t4) statements survive summation/decoding and expectation. These
   constants need not be uniform in N, and no such uniform bound is claimed.
   Fully distinguishable particles have one routing probability t²w per
   directed one-hop pattern at this order; their factor2 versus B factor4 is
   correct. Source-permutation count routings do not create extra order2 D
   terms.

3. At the unchanged count, all N entries tie and the decoder is uniform on
   balanced subsets. At a hop, the doubled site is included and empty site
   excluded, with K-1 remaining labels uniform. The orientation average gives
   P0 conditional on edge crossing. Its probability q=K/(N-1) is correct and
   positive. Equivalently
   1/[2 binom(N-2,K-1)]=1/[q binom(N,K)]. No collision-free conditioning or
   division by a postselection success probability enters.

4. Combining these laws gives the exact displayed leading density tilt.
   Its total mass correction is zero since E0 C=qW. Multiplying by C gives
   (4t²/q)[E0 C²-(E0 C)²], not a raw-count quadratic proxy. For positive
   variance the increase holds for all sufficiently small nonzero |t| for
   that fixed graph. Zero variance means C is constant on the complete
   finite feasible set. Complementing any balanced subset preserves its
   undirected cut exactly.

5. The stated rare-hop mixture is a genuine nonnegative classical law when
   4t²W<=1 and approximates B only to the given local order. W=0 is handled
   explicitly. The D family at sqrt2*t has the same leading tilt. Neither
   observation proves equal-cost performance, all-order simulation or absence
   of a useful collective finite-angle effect, and the proof does not assert
   those conclusions.

## Domain checks and attempted overextensions

The equality g_ij=|H_ij|²=w_ij is essential. In my independently frozen
generalization the response for an arbitrary guide is
(4t²/q) Cov_0(C_w,C_g). The exact N4 table there has negative covariance for
H=w weighted; it **does not refute this file**, whose guide is sqrt(w).
The file's final warning correctly separates these two choices. For
unweighted adjacency they coincide. Normalizing the guide by a fixed
positive scalar merely rescales t in the corresponding formula.

Raw count access matters: a threshold click detector would erase the
distinction between count2 and count1, so the forced-inclusion argument is
not automatically valid for that detector. Partial filling, losses, complex
guides, fields, PIT, fixed-priority ties and greedy/completion decoders are
outside the stated proof. No statement here rules them out. The title's weak
full-input scope and final exclusions make this boundary explicit enough;
there is no hidden generic impossibility inference to repair.

No missing implication or numerical obligation was found for the stated
asymptotic theorem. The separate manual weighted counterexample needs no
executable check to serve its algebraic role. This receipt changes no author
proof, code, raw file, manuscript or scientific-goal status. No novelty claim
is made or verified.
