# P38b/c: constrained effect search did not settle the lemma

All four declared cells are retained. Initial search:2076 objective calls,
2.183s, every solver at its25-iteration cap. The explicitly frozen refinement
resumed the recorded best points with120 iterations and a smaller difference
step:8714 additional calls,6.019s. Total10790 queries, including infeasible and
finite-difference trials. Both v2 manifests validate, status completed.

No numeric candidate or exact counterexample to D_pinched<=delta was found.
Maximum near-feasible excess was -0.0201018. This is not a global margin,
proof, or convergence certificate. All solvers still report failure: three
refinements hit120 iterations and the fourth stopped after65 with a positive
directional derivative for line search. These statuses are not hidden behind
the successful process exit.

Every refinement winner was rationalized and repaired toward the strict
diagonal reference. Exact Hermitian principal-minor/dominance tests and sum I
pass, and exact Rayleigh lower witnesses are retained. Their actual deltas
are near0.2/0.6, not asserted equal to the target after numerical differences
and repair. The four approximate lower values are0.175991,0.179898,0.443452,
0.443452. A lower value below delta does not prove an upper bound by delta.
The data certify feasible lower witnesses, not the conjecture.

This search used the compact effect domain supplied by the complex-k3 cone
lemma. No explicit optical circuit was constructed from those optimizer points,
no Fock law or Perceval call was added, and physical shots remain0. The
separate36-frame P38 experiment has actual full-law/Perceval checks.

The dual boundary note theory/phase3_pinching_dual_boundary.md supplies an
exact method obstruction: at delta0 finite dual witnesses cannot attain the
needed zero cost, although the infimum and true distance are0. Handle that
case directly or use a limit. The scalar curved-envelope counterexample in
P39 is a different, explicitly post-hoc question; it does not turn these
failed searches into a refutation of the linear lemma.

Decision: INCONCLUSIVE on the universal bound. Preserve the traces under
experiments/P38_effect_search/. An unchanged SLSQP rerun is not justified;
the next step needs a different boundary-aware algorithm or analytic witness.
