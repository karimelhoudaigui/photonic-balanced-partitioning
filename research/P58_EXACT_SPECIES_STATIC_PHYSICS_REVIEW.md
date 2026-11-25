# P58 exact two-species diagnostic: static physics review

**STATIC PASS for the proposed bounded computation.** No blocking physical,
normalization, indexing or finite-coverage error was found. This review is
not execution authorization or an executed result. No import, test, matrix
evaluation, source recurrence, convolution or graph calculation was run.

Exact reviewed revision: `54ff30df4f1925c5ea960201dd90f62acd39b075`.
The complete source, card and execution contract were read, including the
port-order correction from b27ff0c. SHA256 from read-only git objects:

| File | SHA256 |
| --- | --- |
| `research/P58_same_phase_species.py` | `9b7c5e8e0b7bdf8dd5580a754f1305bfc79abf58d05bd7fada39aa32ee026b96` |
| `research/P58_SAME_PHASE_ALL_SPECIES_CARD.md` | `444ab38d58476e48987b71a0c63471279112a3dd308507698fbfed430fc57d4b` |
| `research/P58_same_phase_execution_contract.json` | `a872d40c39d39c6cd9132c516dcb95c8584eb16ee0b0ac8fba50a35b6364637f` |

## Matrix, internal species and Fock normalization

The explicit W4 rows now match the original input-port order. Substituting
the standard bit-dot row order only permuted two input columns, preserving
the full-B law and the unlabelled set of all127 controls, but not individual
group labels. Correcting it before evaluation is necessary for exact label
provenance; the final matrix does so.

Entries are in Z[xi], xi=exp(i*pi/3), xi^2=xi-1. Multiplication
(ac-bd,ad+bc+bd), conjugation(a+b,-b), and norm a^2+ab+b^2 are correct.
The six explicit roots and the sign/block formula give the stated fixed
U=q/sqrt(8). The exact column-Gram check q* q=8I is sufficient for this
square matrix's unitarity; no floating normalization is introduced.

For a group of k distinct single-photon input columns, the polynomial
coefficient C_n of prod_j sum_r q_rj x_r equals per(q[n,G])/prod_r n_r!.
The normalized Fock probability is therefore

    |C_n|^2 prod_r n_r! / 8^k.

The source recurrence and weight formula implement this identity, including
bunching and exact zeros. There is no input factorial because all occupied
inputs contain one photon. Every occupation has a key even after its
coefficient cancels to zero: the recurrence retains zero-valued terms.
The sum-of-weights check8^k is an appropriate invariant for every group.

Two internally distinguishable species have independent spatial Fock laws
whose occupations add. The weight convolution v*w needs NO final output
factorial: the factorials have already normalized each species' law. The
product denominator is8^k*8^(8-k)=8^8. The code does not replace an actual
Gram/internal-species calculation by a global B/D mixture.

## Complete states, ties and decision

Manual state-count reconstruction, by group size1 through8:

| k | binomial(8,k) binomial(k+7,7) |
| --- | ---: |
| 1 | 64 |
| 2 | 1008 |
| 3 | 6720 |
| 4 | 23100 |
| 5 | 44352 |
| 6 | 48048 |
| 7 | 27456 |
| 8 | 6435 |

Their sum is exactly157183 stored group occupations across255 nonempty
groups. The all-eight output space is binomial(15,7)=6435. Base9 encodes
the full eight-mode occupations without carry: both species together have
total8, hence every added digit is at most8. The target scalar lookup
therefore covers every convolution term, including zeros and collisions.

For each occupation, the code exhausts all70 balanced subsets and averages
the two edge-crossing indicators over ALL maximizing subsets. Its scalar
is420*(Pr(cross04)-Pr(cross15)). Dividing its expectation by840 correctly
implements w=(X04-X15)/2. For the nontrivial guard(3,2,1,1,1,0,0,0), the
three maximizers include0,1 and two of2,3,4. The signed values are0,-1,-1,
so the scaled mean is-280, not-210. The HOM/D toy weights also have the
correct denominators4 and bunching factors.

The unordered control count is8+28+56+35=127: all1+7,2+6,3+5 partitions,
and precisely one representative of each4+4 partition by requiring input0
in its size-four group. The streamed convolution has exactly11083116 pairs:
219648+1729728+5322240+3811500. This count is a manual iterator audit, not a
timing measurement. No all-finer-partition population is being implied.

The independently reconstructed full-B mean is checked against the fixed
-767/327680 before control conclusions. A mismatch raises and is preserved,
instead of adjusting the target. The minimum exact control gap >0 gives
separation from these127 controls; equality or a negative gap refutes that
stronger interpretation. All controls and minimizers remain in the output.
The output's genuine_order8_witness and positive_optimizer flags stay false.
The card correctly excludes finer partitions without a convexity theorem,
phase optimization, general distinguishability monotonicity and advantage.

## Execution boundaries and disclosure

Source/card/contract/pyproject/lockfile form the planned five-input closure.
There is no production helper import, archived numerical target input,
floating-point physics, RNG or LP. The only float is elapsed wall time.
Fresh output creation precedes computation; any caught failure is saved
and reraised, without retry. Partial source-law/tie archives may exist after
a later failure and must be retained, not reported as a completed decision.

The declared CPU20/wall30/threadenv1/output8MiB and planned64MiB logical
workspace are consistent with the finite iterator sizes. The157183 figure
counts stored mathematical states, not Python heap bytes: dictionary/list,
JSON encoding and interpreter overhead remain a resource-projection risk.
No hard RSS/affinity guarantee or measured runtime is supplied by this review.
The runner, actual complete output size and result status must be inspected
after any separately authorized run.

I previously reconstructed/reviewed related P53b/c physics and the fixed
mean witness. That same-team history is disclosed; this is adversarial static
review of a new source implementation, not a fresh independent physical
replication or novelty check. The graph is posthoc and small enough for
trivial feasible search. Nothing here demonstrates a useful optimization
gap, an unknown optimum, hardware capability or a QPU result.
