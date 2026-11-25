# P48-B corrected freeze: exact-source static addendum

2026-11-25. Reviewed code commit
`5e06e8f5d846f16399eff95c77869014600720c9`, parent
`4a199f85a0a6f015c31ad96b83d8a66c73702659`. Primary script SHA256:
`b123bec4f67feb8ffc2255e0a56bc1181748a80bb716fe92328954a6f4d538ca`.
The inspected source/tests/contracts have an empty scoped working diff
from that commit. No computation, import, pytest or P48 graph generation
was performed during this addendum.

Primary verdict: **conditional on the named input of a successful targeted
52-case preflight at this exact execution closure**. The minimal correction
is statically coherent and discharges the previous deterministic-Gaussian
handling obligation. No further blocking mismatch was found. This is not
a claim that those tests have passed or a numerical/optimization result.
P48 remains DEV, with no positive, hardware or novelty conclusion.

The earlier verdict at 4a199f8 is preserved unchanged in
`research/P48_PHYSICS_STATIC_REVIEW_4a199f8.md`, review commit
`d1312729f0890c6f7a3e7d908a5be88350874ebf`, SHA256
`713ae4cff16eb267265b2ca35cd43d6bb7da49563e0f30136506a23e1652e087`.
That review identified a permitted floating-point amplification risk, not
an observed DEV failure. This later pass does not rewrite that provenance.

## Exact change and frozen data

Only five files change from the earlier freeze: script, integration tests,
MD contract and two runner contracts. Graph population, graph/role seeds,
marks, encoder/lambda settings, budgets, preparation candidates, coherent
helper, primary source and baselines are unchanged.

| File | SHA256 at corrected freeze |
|---|---|
| research/P48_spectral_pit_probe.py | b123bec4f67feb8ffc2255e0a56bc1181748a80bb716fe92328954a6f4d538ca |
| tests/test_p48_spectral_pit.py | c22a532b4b617c7d1bb6bbddca90247a1900635d7f3f4fc609d90fe0e33ee689 |
| research/P48_spectral_pit_spec.json | 7e1881ce23fe1690bafae4c8b7ee8a339da99ed670b727b816448ba0e77763e8 |
| research/P48_spectral_pit_contract.md | 350d11679eb8345e5a8c29efea1ef484ca1d7a252da120214f0449167b567094 |
| research/P48_spectral_pit_preflight_contract.json | 91ffc384c676c3820643403202646d833b9f262290d70ed1d4036c7ac6fc9e41 |
| research/P48_spectral_pit_execution_contract.json | 993636117d3f8c765fca225572c754d034b256383de51a288372e2ee16611031 |
| research/P48_coherent_marginals.py | a231a94578daf43993f62e393f1c58f90030a693ad2bf7722977ae65e181b2ac |
| tests/test_p48_coherent_marginals.py | 43fb78402527c607124ec58a44017bae53b1520c14296021e52910e95a14ff0c |

The authoritative root card remains bfdff40926ad395a14f64260513b6ef21a1257f5
with its preparation amendment. Main/preflight closure lists remain11/12
execution artifacts respectively; software and resource declarations are
unchanged. Actual versions, manifest input hashes before/after, clean source
and run status remain to be measured by the authorized runner.

## Structural correction checked

The corrected build_network identifies empty rows by zero nonzero entries
in q and occupied-deterministic rows by exactly ONE nonzero q entry with
that entry exactly1. It does not use mu1 alone or introduce a near-unit
tolerance. For a CF source those patterns have deterministic count0 or1;
their exact theoretical covariance rows are zero. Numerical covariance
calculation can still have small residuals, which remain recorded.

The mask is applied to SPATIAL ROWS of the Gaussian factor, the correct
coordinates to eliminate the leakage. Pre-mask row variances are saved
before mutation. The removed-factor L2 diagnostic equals the Frobenius
norm of all removed rows, sqrt(sum prevariance over the mask). Lists of
empty and occupied-deterministic rows plus these diagnostics are exported
by pack_network. Target covariance, factor covariance and variance residuals
remain distinct and visible.

After masking, factor rows and their effective variances are exactly zero
in numerical arithmetic. The existing make_field branch consequently keeps
the independent per-coordinate PIT-jitter uniform value instead of dividing
zero/small leakage by its own standard deviation. Nonempty stochastic rows
still use the actual remaining factor variance. This addresses the singular
normalization amplification identified in the old review without claiming
a relative or interval copula certificate near every variance boundary.

## New fixtures checked by reading, not execution

The mixed6-mode source V has columns e0,(e1+e2)/sqrt2,(e3+e4)/sqrt2, leaving
row5 empty. It includes both an occupied deterministic row and genuine
fluctuations. Its test monkeypatches the covariance eigensolver, injecting
1e-14 into a positive-eigenvalue eigenvector at rows0 and5. This models a
tiny admissible factor leakage; it is not a measured production LAPACK
error and does not touch any DEV graph. Assertions require nonzero pre-mask
variance, zero post-mask variance and raw value, a small remaining covariance
residual, and the exact independent seeded jitter at both deterministic rows.

The other new fixture uses the full four-mode Hadamard frame with q=1/4
in each row/column. mu=1 everywhere but the true B variance is
1+1-2*(4/16)=3/2. The fixture requires NO occupied-deterministic mask and
effective variances3/2. It prevents overmasking spread mu1 rows.

Together these target the specific missed structural case rather than
asserting a sampler law from a single draw. They add two integration cases:
26 integration plus26 helper cases are planned, all unchanged small/zero
fixtures with no DEV spec/main invocation. The new seed480086 is confined
to the integration fixture. No preflight data were produced by this review.

## Carried conclusions and execution boundary

The unchanged, previously inspected paths preserve subunit q, explicitly
record tiny row/PMF corrections, retain the specified occupied source ports
and vacuum completion, use correct covariance and analytic phase/sphere
tables, and credit every preparation/marginal/rounding discovery and cost
to the common frontend before gain. No source state is replaced by Cref.
All seven arms/five baselines, tuning costs, failures and incomplete-population
labels remain as reviewed. These are static findings, not performance evidence.

Commands actually used were read-only git-show/diff and shasum plus reading
the five-file correction. No code was edited in encoding and no numerical
slot was used. The reviewer is independent of the encoder author but had
authored earlier physics analyses; this limited review is not independent
revalidation of those prior proofs. The next step is solely the coordinator's
authorized targeted preflight under the frozen contracts, preserving its
first failure if any. No DEV success or goal completion is inferred here.
