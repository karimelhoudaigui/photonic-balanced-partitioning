# Continuous conditional-phase marginal: exact-fixture qualification

The coordinator-supplied DP dictionary is implemented in the PURE stdlib module
`research/P47_conditional_phase_marginal.py`, frozen before execution at
`427d984e2bd5a8ef376f9297376e619a5344c8b3`. Its SHA256 is
`263cfe954645f4a5de6edb5beedcaa4b8766d1a364d46f45d150639977c6efb0`.
No module source changed after qualification. This is an algorithmic control
component, not a positive optimization result, independently replicated physics
experiment, QPU gate, or novelty claim.

The exact input model is Bernoulli(p) active set A, l=|A|, followed by l particles
in a shared independently CONTINUOUS-phase field. Independent (l+1)-th roots
give the SAME averaged multinomial law: each count probability is degree l
in phases and degree l in conjugates, so each exponent difference has absolute
value at most l. Only zero differences survive averaging either continuous
phases or roots of order l+1. This is NOT the old four-root control at l>=4.

The DP is the positive coefficient array

    D[l,r]=[y^l t^r] product_a ((1-p)+p y sum_h q_a^h t^h/(h!)^2).

The binomial-shift PGF has c0=1 and, for r>0,

    c_r=sum_(l=r)^N (l)_r*r!*D[l,r]/l^r.

There is no division by l=0. PMF inversion is alternating, computed in
Decimal80 with strict small arithmetic-error thresholds. Input row-sum
normalization <=1e-12 and tiny PMF corrections are explicitly returned. It
does not provide an interval certificate for floating unitary input data.

Qualification was authorized in the sole numerical slot and executed once:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python -m pytest -q \
  tests/test_p47_conditional_phase_marginal.py \
  --junitxml=research/P47_conditional_phase_qualification/run_001/data/junit.xml
```

The bounded Mathbox runner enforced CPU30/wall50/thread1/log4MiB and exactly
three input artifacts from the frozen contract. Source was clean and every
before/after hash matched. Its v2 manifest is
`research/P47_conditional_phase_qualification/run_001/manifest.json`.
Status **completed**, exit0, observed wall0.513359s. The manifest validator
passed against this worktree. The slot was explicitly released afterwards.

Result: **24 tests PASS in0.23s**. The independent reference uses Fraction
arithmetic, all Bernoulli active subsets, all l+1-root phase tuples, exact
cyclotomic norms for roots of orders2/3/4, and exact binomial output laws.
It includes uniform N0..3, a nonuniform rational-amplitude row, pointmass rows,
p0/1, l0, and invalid-input/tiny-normalization cases. Thus it does not merely
reimplement the same two-index Decimal DP. Agreement is within1e-60 on these
fixtures, with normalization and first moment p checked.

These are AUTHOR-executed small-reference tests, not fresh-agent code review.
They do not certify N13/17 performance. A separate deterministic synthetic-row
resource/precision contract is being frozen before those evaluations; no DEV
graph, held-out graph, Perceval call or photon sample entered this qualification.
The P46/P47 four-root sampler and its empirical tables remain unchanged unless
a new explicitly frozen continuous/l+1 model is integrated by the coordinator.
