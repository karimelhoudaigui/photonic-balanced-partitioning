# P58: falsify a stronger interpretation of the fixed mean witness

Frozen prospective question, 25-Nov-2026. Owner ROOT on
research/p45-positive-discovery, base35f7ab1. This is a diagnostic route
alongside the new P56/P57 algorithm designs, not the optimizer objective.
No source calculation or control evaluation has occurred for this card.

P53c verifies separation from all4+4 species groupings at the SAME phase
pi/3. P53d's all-phase extension concerns4+4 only. Neither establishes
whether fewer than eight mutually identical photons can reproduce the old
signed mean. The next cheapest falsifier is ALL127 unordered nontrivial
two-species partitions at the SAME already fixed angle. No new graph,
angle, witness, classical optimizer, physical draw or held-out panel.

Use the original eight-mode matrix and all eight input photons. Let
xi=exp(i*pi/3), xi²=xi-1. For output row r and input column j, the
unnormalized entry is

    q[r,j]=W[r mod4,j mod4] * xi**(r mod4 if j>=4 else0)
           * (-1 if r>=4 and j>=4 else1),

where W is the unnormalized Sylvester4 sign matrix, U=q/sqrt(8).
Independently multiply linear forms for each nonempty input group G:
P_G(x)=prod_(j in G) sum_r q[r,j] x_r, in Z[xi]. If its occupation
coefficient is a+b*xi, its exact weight is
(a²+a*b+b²)*prod_r n_r!, with common probability denominator8**|G|.
Keep every occupation, including exact zero weights. Each group's total
weight must equal8**|G|; verify the Gram identity exactly before calculation.
This code must import no P52/P53/P53c/P53d production helper.

For each output occupation n of total8, enumerate all70 balanced subsets
and retain those maximizing captured photon count. Uniform ties define
s(n)=420*(Pr(cross04|n)-Pr(cross15|n)), an integer. Compute it independently
of previous stored tie matrices. Thus the witness mean is E[s]/840.
For G and its complement, convolve their exact weights using base9
occupation keys; no digit can exceed8 so addition has no carries. Normalize
all means by840*8**8. Enumerate all partitions with smaller side size1,2,3
and all size4 groups containing input0:8+28+56+35=127 controls.

Also reconstruct the full eight-photon mean from the same independent ring
construction. It must equal the already certified -767/327680; a mismatch
is an error to preserve, never a replacement of that target. All four-photon
source laws are retained too, but this does not borrow their source code.

Decision: if any exact control mean <= the bosonic mean, report
STRONGER_SAME_PHASE_SPECIES_INTERPRETATION_REFUTED, retaining every group.
If all127 are strictly larger, report SAME_PHASE_ALL_BIPARTITIONS_SEPARATED
with the exact smallest gap and all minimizers. The second outcome concerns
this one observable/circuit/angle; it implies separation from all finer
distinguishability partitions at THIS angle only when explicitly proving
their mean is in the convex hull of these bipartition controls. Do NOT assume
such monotonicity or convexity: arbitrary finer partitions remain untested.
In particular this screen alone must not be called a genuine order8 witness.
No mean gap implies optimization advantage, novelty, a cost gain, independent
replication, new graph performance or hardware feasibility. The graph remains
posthoc and trivially searchable classically.

Before one execution, freeze source, integrated independent toy guards,
input closure, command and resource contract and obtain same-team static
review. Guards must include ring-root identities, exact two-photon HOM,
distinguishable convolution, a nontrivial tie average and base9 no-carry.
CPU20/wall30/thread1/output8MiB, planned logical workspace64MiB; no claim
of hard RSS/affinity control. One fresh bounded run, first failure retained,
no automatic retry or wider phase search. Save every group weight law,
all6435 tie scalars, all127 means, the full-B reconstruction and summary.
No code, test or graph calculation is authorized by this card alone.
