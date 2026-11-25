# P67: exact graph covariance extends the P66 dark-sector obstruction

25-Nov-2026. STATIC derivation and independent review of the coordinator's
proposed extension; no code, import, test, graph draw or numerical experiment.
Base: `eae1ddabb215c9dfda05ea9bdcc286a6698ba0ad`.
The P66 audit in `theory/P66_independent_bright_dark_audit.md` defines the
family, source, target, acceptance and resource conventions used here.
No other P66 author's proof or verdict was read.

**Verdict: proved as written below.** Exact deterministic graph-only
permutation covariance forces the same separate dark occupation invariants,
even for optical matrices that are not Cayley transforms or graph polynomials.
This is a restricted worst-case obstruction, not an all-optics impossibility
or a novelty claim. The positive optimization objective remains open.

## 1. Objects and scope

Use four size-L cliques A1,A2,B1,B2, L>=2, heavy weight M>0, matching weight
h>0 between A1,A2 and B1,B2, and M(L-1)>Lh. Include either no edges between
CA=A1 union A2 and CB=B1 union B2, or every such edge with weight
0<w<h/L as in the connected P66 extension. These are explicit graph families.

Let F map a weighted adjacency matrix to a one-particle unitary. Assume
EXACT deterministic graph-only permutation covariance:

    F(P*A*P^T)=P*F(A)*P^T

for every vertex permutation P. There is no selected source S or vertex
marking among the arguments. The map can otherwise use arbitrary graph
analysis, spectral operations or computation. For every automorphism P of
the fixed graph, U=F(A) therefore commutes with P.

A history-dependent controller may choose among functions F_theta, provided
EACH realized function obeys this exact graph-only covariance. Merely having
a distribution of optical matrices that is covariant in law is a weaker
property and does not suffice. Current-state features, independently labeled
random marks and history-dependent marked subsets are outside this claim.

## 2. Independent transitive automorphism subgroups

Label the L matching pairs in CA. Simultaneously permuting their labels in
A1 and A2 preserves every edge and weight. Swapping A1 and A2 also preserves
them. These transformations generate a subgroup GA transitive on all 2L
vertices of CA. It acts as the identity on CB. Such transformations remain
automorphisms after adding the uniform complete cross-block edges of weight
w. A corresponding independent subgroup GB acts transitively only on CB.
Thus the graph automorphism group contains GA times GB.

The fixed vectors of GA on CA are exactly the uniform line spanned by bA.
Indeed, transitivity forces each invariant vector's coordinates to agree;
the converse is immediate. Let R_A be the average of the permutation
matrices in GA, acting on the entire N-dimensional one-particle space.
Averaging over a finite group is the orthogonal projector onto its invariant
vectors: it is self-adjoint because inversion permutes the group, idempotent
because each product occurs equally often, and its image is pointwise fixed.
Consequently

    R_A=|bA><bA| direct-sum I_CB,
    I-R_A=projector onto DA inside CA.

Since U commutes with every element of GA, it commutes with their average
and hence with this dark projector. The same argument applies independently
to GB and DB. This proves that U preserves DA and DB separately. Its only
cross-block coupling acts between the two uniform bright lines.

Equivalently, its CA,CB block is z*|bA><bB|: left invariance under GA forces
constant columns, and right invariance under GB forces constant rows. The
group-average proof also establishes preservation of the dark complements
inside the diagonal blocks, which a cross-block rank argument alone would
not establish.

## 3. Transfer of the P66 probability and chain bounds

The passive Fock lift Gamma(U) commutes with both dark photon-number
operators. For a bad whole-clique source, the source support N_DA<=L and
the target support N_DB=0 give the two-projector identity from the P66 audit.
The source projector weight is a_L=L!/(2L)^L. The full-CA target projector
weight is bounded by

    b_L=min(1,((L+1)/2)*((L+1)/(2L))^L).

Thus the probability of either better feasible target is at most
p_L=min(1,2*a_L*b_L), uniformly over these graph-only covariant unitaries.
The original and connected families have the same four bad whole-clique
sources, the same two better targets and uphill gap lower bound
2M(L-1)-2Lh, so the zero-temperature and properly scoped finite-temperature
hazard bounds transfer unchanged. Collision attempts remain paid self-loops.
The proof says nothing about full random initialization, arbitrary graphs,
stateful quantum memory, a different decoder or measured wall-clock costs.

## 4. Why covariance in law is insufficient: an exact counterexample

There is a graph-only random passive permutation procedure with a relabeling-
covariant LAW and raw good-target probability exactly one half from any
fixed bad whole-clique source. It is given to delimit the theorem, not as an
optimization benefit: its construction uses the easily found graph solution.

1. Choose R uniformly from the four bad whole-clique subsets.
2. Choose T uniformly from the two good whole-block subsets CA,CB.
3. Choose uniformly a bijection R to T and independently R-complement to
   T-complement. Apply the resulting passive permutation optical matrix.

The collections of bad and good subsets are defined by the weighted graph,
without vertex labels. Uniform choices and uniform bijections are carried
to the corresponding choices by every graph relabeling, so conjugating the
random matrix gives exactly the procedure's law on the relabeled graph.
Individual matrices need not commute with the graph automorphisms.

Fix S in the four bad subsets. If R=S or R=S-complement, its image is T or
T-complement and is good. This occurs with probability 2/4. For either other
R, S intersects R and R-complement in L vertices each. Its image has L
vertices in each of T and T-complement and therefore is neither good target.
Every output is collision-free; the success probability is exactly 1/2.

In contrast a_2=1/8 and

    a_(L+1)/a_L=(1/2)*(L/(L+1))^L<1/2,

so 2*a_L*b_L<=1/4 for every L>=2. The covariant-in-law procedure therefore
violates a proposed extension of the P66 numerical bound to this larger
class. There is no quantum advantage: a classical routine used the same
graph structure to build a permutation sending a randomly selected bad
partition to a known good partition.

## 5. Consequence for proposed scalar graph features

Any exact graph-only covariant scalar feature vector must be fixed by every
automorphism. The family is vertex-transitive: GA,GB act within their blocks,
and exchanging the two identical blocks is another automorphism. Hence all
entries of every such scalar feature agree. Weighted degree is one example;
substituting another automorphism-invariant scalar feature cannot break this
obstruction on this family. A noncovariant tie-break, random marks or current-
state data changes the hypothesis and requires separate scientific controls.

Review provenance: independent rederivation from the exact candidate, not a
numerical certification. All group averaging, support and covariance-in-law
counterexample steps were checked symbolically. No empirical claim or
manuscript update is made. Stronger current-dependent covariance is a separate
proposed P68 extension and is not assumed established by this file.
