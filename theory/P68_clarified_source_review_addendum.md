# P68 review addendum: clarified graph-barrier wording

Primary verdict: **proved as written**, unchanged from the independent
review `P68_independent_current_covariance_review.md` at commit
`0c7fa52dd8eb3883011c2d8bae90e049062c3066`.

This addendum reviews only the exact source delta in commit
`5904e6f287c4c3737e15d452f74ba9a798c8c5ed`, read with
`git show --format=fuller --no-ext-diff 5904e6f -- research/P68_current_covariance_rank_two_audit.md`.
The current source SHA256, independently checked with `shasum -a 256`, is
`8a4bd9cfd751f1e8fd3d55bf2a6325d90fa10f52ed49882c5b2a588ef8e78235`.
The earlier audited source SHA256 was
`0c587b01c3a37bac5b0ff94fb03546d451babb69695a35ff1d702af8e78f264b`.

The sole hunk replaces the ambiguous phrase “every other balanced subset”
by an explicit decomposition: G={CA,CB} are the only strict improvements
from B; every balanced subset outside B union G is uphill by at least g;
the other members of B have equal cost. This is exactly the graph
classification reconstructed in section 1 of the prior review. It changes
no numerical constant, formula, hypothesis, acceptance rule, probability
bound or proof step. The new wording resolves the only local prose issue
reported there. The original source and review remain preserved in history.

The prior mathematical verdict and all its scope limitations therefore
apply to this clarified current source hash. No new route, claim of
stationarity, or result for generic starts is added. The delta and this
addendum received mathematical proofreading. No imports, tests, scientific
computations, seeds/draws, backend calls or QPU calls were performed.

Independent reviewer, 2026-11-25, `research/p66-dark-barrier`.
