# P37 proof self-review

Verdict: **proved as written**, for Haar-mean source selection and fixed-lambda
boundary scaling. This review is by the proof author, not an independent audit.
Target: theory/phase3_loss_source_selection.md at1d65279;
SHA256 fda5160d1d4eb232f67eae09cfcfabf3024822ea1e0720ef639267374a642807.

Dependency graph: known Haar law and commuting loss -> binomial mixture;
exact h/g ratios -> signs; coupling/size bias -> signed expectations;
one-crossing lemma -> unique roots; increasing probability ratio -> root order;
ordered adjacent differences -> global maxima. Fixed loss-count moments and
tails -> boundary expansion; two fixed-lambda sign evaluations -> root limits.
No finite computation supplies a proof leaf.

| Obligation | Result | Detail |
|---|---|---|
| Domain | passed | even m>=8, k=m/2, k<=N<=m, distinct single inputs, uniform independent loss, all attempts |
| External law | passed | P32 primary Lemma1/Eq6, twirl and loss derivation |
| Exceptional zero h values | passed | l=k-1 handled directly; no ratio through zero |
| Adjacent signs | passed | attempt zero at m-2; photon sign switch between m-4 and m-3 |
| Size bias | passed | l*C(N,l)/N=C(N-1,l-1); eta and eta² factors correct |
| Unique root | passed | divide by first negative power, then strictly decreasing between opposite limits |
| Root order | passed | increasing binomial likelihood ratio, plus a negative new final term |
| Global optimum | passed | earlier choices strictly dominated; candidate sequence unimodal |
| Endpoints | passed | extra attempt tie at eta=1 restored; zero-success eta=0 excluded |
| Boundary scaling | passed | fixed moments bound Taylor errors; peak-normalized tails negligible |
| Fixed loss/fixed device | out of scope | no fixed-loss rate or E_U[N/p_U] conclusion |
| Fresh review/novelty | not addressed | quota-blocked reviewers; no novelty certificate |

The size-biased lost count has N-1 trials, not N, but still mean lambda+O(1/m).
Peak-weight relative errors C(1+s+T)^2/m contribute only O(m^-2) because fixed
third moments are bounded. Tail differences divided by their own peak are
bounded: no uncontrolled inverse small h(l). The root sandwich evaluates
fixed lambda on either side of1,2,3, not an unproved expansion at varying roots.

All1610 finite values and36 brackets pass a separate Polya/de Casteljau
implementation. Remaining obligation: fresh reconstruction of the sign/root
and asymptotic steps, then exact prior-art comparison. Neither numerical
agreement nor self-review establishes originality or optimization benefit.

Proofreading scope: the new proof and this audit, using proofread-math
self-review mode. Routine edits: none. Mathematical-token changes: none.
No unresolved notation or cross-reference issue found in that scope.
