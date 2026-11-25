# P66 scoped route note: restricted warm-start obstruction

Author freeze: 2026-11-25, branch `research/p66-dark-barrier`, base
`3e708637639b8664d0f81bb8947ce05fed0e0a4c`. The self-contained evidence is
`theory/P66_bright_dark_barrier_obstruction.md`. This note records an
internal mathematical route, with no novelty assertion and no numerical
or QPU authorization. The separate peer derivation was not read before
this freeze.

The four-clique construction yields an explicit obstruction when a raw
collision-counted passive proposal chain starts in one of four prescribed
whole-clique states. Both the disconnected family and its connected
constant-cross-weight extension have only two improving balanced subsets.
Component/block dark occupations are invariant under every specified
Cayley or scalar-spectral unitary. A normalized source projection and a
proved target bright-number factorial-moment bound give

    r_L = 2 [L!/(2L)^L]
              min(1, (L+1)/2 * ((L+1)/(2L))^L),
    log r_L = -L log(4e) + O(log L).

For a zero-temperature chain with an arbitrary history controller choosing
among the allowed unitaries, improvement by T raw attempts has probability
at most min(1,T r_L). Collisions remain self-loops and consume attempts.
At finite deterministic beta_j, add the escape term sum_j exp(-beta_j g),
where g=2M(L-1)-2Lh>0. History-random beta requires the expectations stated
in the proof. No independence between proposal successes is assumed.

Two extensions are proved separately. Complete cross-block edges with
0<w<h/L preserve the invariant spaces and graph gap. The graph is then
connected; its targets have cost 4wL^2, not zero. Also, any deterministic
exact graph-only permutation-equivariant one-particle unitary must commute
with independent transitive within-block automorphism groups and hence
with the same dark projectors. Covariance in law or joint covariance in
the graph and current subset does not suffice for this corollary.

The present route closes only this engineered warm-start, low-temperature
mechanism as a candidate for an optimization advantage on this family.
A classical routine finds the four heavy cliques and evaluates six unions
to return an optimum in O(V^2+E) arithmetic. The construction is deliberately
favorable to this comparator, rather than a hard-instance or all-graphs
claim. It is not the registered P65 graph distribution. Integer rescaling
of the connected example can also leave P65's weight range.

This does not establish difficulty for uniform balanced starts: most such
starts are outside the four-state trap. Nor does it rule out the actual
P65 anneal. For fixed M,h the schedule beta_j=(N/W)2^(j/2), at fixed j,
has beta_j*g of constant order as L grows, so the thermal term need not
be small. A change to an encoding using the current subset, realized
symmetry breaking, different input sources, extra modes or a different
measurement/decoder would change the theorem premises and need separate
analysis. No such route is claimed successful or implemented here.

No scientific imports, tests, numerical computations, graph generation,
random seeds/draws, native backend calls, experiments, or raw-data edits
were performed for this proof-only checkpoint. Code test requirements
remain applicable before any later merge containing executable changes;
there are none in this checkpoint.
