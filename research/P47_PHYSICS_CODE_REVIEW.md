# P47 frozen-code physics and comparison review

2026-11-25. Reviewed encoding commit
`695b5d2f49c5bb90d070a38c31abc0a697fbedd4`, parent
`fa3740c574f3ff580b8c2c691a05ce959b02116f`, in the read-only worktree
`.local/p41-worktrees/encoding`. The script SHA256 matches the requested
`fac164f64a3ba15a061c56547be58f5c540486852c9016ccc70a129637ca53b1`.
The inspected files match that commit (scoped git diff was empty).

Primary verdict: **conditional on the named input of a successful targeted
preflight at this exact code/input closure**. Static reconstruction finds
the intended orientation, finite-step map, physical marginals and declared
DEV comparison consistent. This is not a claim that the code/tests have
executed or that its outputs pass. No blocking algebraic mismatch was found
in the frozen path. P47 remains DEV and has no accepted positive result.

The reviewer derived the two prior P47 mathematical notes and is therefore
not an independent third-party validator of those proofs. This is an
implementation review independent of the encoding author, with explicit
shared theory provenance and the usual same-team/model limitations. No
P47 raw/result was available to or consulted by this review. The P46
contract's stated prior outcomes were read as context, not revalidated.

## 1. Exact inputs and inspected scope

All paths in this table are relative to the encoding worktree at the
reviewed commit. Hashes were obtained by `shasum -a 256`, without executing
any Python, simulator, test or experiment.

| File | SHA256 |
|---|---|
| research/P47_directed_pit_probe.py | fac164f64a3ba15a061c56547be58f5c540486852c9016ccc70a129637ca53b1 |
| research/P47_directed_pit_contract.md | 1cd68efe7640d0cc07a1e4d12af8a833d0a4bc4eb4181a33d49056c4cb27d381 |
| research/P47_directed_pit_spec.json | 11656d15ba526ca6b432cb8dc93f2d0c171039ece691b6bb3e8ff84bde1f7834 |
| research/P47_directed_pit_execution_contract.json | b22633d6463665dc6a4b4a8ee771730ff54fa1f990e547ccc8227d22a60699ef |
| research/P47_directed_pit_preflight_contract.json | e139b28e62655ab022830007dc6bdb681f25797389d77a1345b04c0f6968b8df |
| tests/test_p47_directed_pit.py | c7a10ec931187479519dd37666a276ed3e7c9eeec5c205b711ffe9cf73c9cff7 |
| research/P43_global_gain_probe.py | b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777 |
| research/P45_adaptive_probe.py | bb00ca61e45794ecea2333e0aa1864edfaec43128c1efa98dd8384c3d6889f92 |
| research/P46_bulk_pit_probe.py | 721cc9f3ee6ba1d604ae29130fb25d092a21bcc756e8d4b4a42e6238d47c315c |

The P47 script, contract, spec, both runner contracts and tests were read;
the P46-to-P47 script diff was read completely. Relevant imported helper
bodies were inspected: graph/cut/seed construction, local optical samplers,
anchor preparation, feasible searches, greedy completion and collective KL.
The software versions in the runner contracts are declarations, not version
measurements made by this review. Runner implementation, all dependencies,
complete repository tests and statistical correctness of the installed
Clifford sampler are outside this static pass.

The self-authored mathematics reread was
`theory/P47_cost_directed_polar_step.md` at
`9e1d9f900f1c768c399259a8b3fffffe01b43c62` (SHA256
`ea397213b671b36df9796769c015064fa525cfeede93eb4e7cc9534b16d61598`)
and `theory/P47_prime_Fourier_stationarity_review.md` at
`f492da8e84a975be2833caa7f2a9b6b394dc5783` (SHA256
`c583b40c6e625135157e4d7257b38274a1f71c6aa1fee495df5f45c9a353a298`).

## 2. New mechanism and orientation

The diff changes the old polar perturbation F+i*zeta*C to the ambient
step F-epsilon*(C odot F), adds the directed diagnostics, changes the
declared dimension/seed/grid namespaces and preserves the existing PIT,
sampler, decoder and baseline logic. There is no covert new decoder or
postselection in this change.

In script lines 329-344, Delta has inside rows and outside columns, and
each entry is checked against an actual scored single-swap cut. For these
integer-weight production cases the imported integer-returning cut helper
is appropriate; this is not a general arbitrary-real-weight cut evaluator.
Lines 35-42 put W in the top-right and W* in the bottom-left block. Thus

    U_(outside j, inside i)=-i sqrt(p) conj(W_ij),
    |U_(outside j,inside i)|^2/p=|W_ij|^2.

The inside-by-outside proxy therefore requires NO additional transpose.
The unit test at lines 193-212 explicitly reads the physical transfer block
and transposes that block back into the proxy's layout. That transpose in
the test is correct; it is not a missing transpose in the guide.

## 3. Directed polar map and prime qualification

Script lines 45-74 implement C=J Delta J/||J Delta J||op, G=C odot F,
h=max(||G||op,maxabs C), epsilon=1/(4h) for guided1 and h>0, followed by
the SVD polar factor. It is the AMBIENT step used by the finite theorem,
not polar(F-epsilon Pi_F(G)). The proxy, distance, tangent and finite bound
have the correct signs and factors in normalized-C units. To convert a
proxy difference to original Delta units requires multiplication by the
saved centered_delta_norm; the unit test does so.

The exact argument is short: nearest-unitary projection yields
2 epsilon <G,Y-F> <= -||Y-F||F^2; quadratic expansion of s_C yields

    s_C(Y)-s_C(F)<=-(1/epsilon-maxabs C)||Y-F||F^2.

Also epsilon||G||op<=1/4, so the exact polar input has minimum singular
value at least 3/4. The code records and checks the corresponding numerical
quantities (lines 64-73). Its tangent is G-F sym(F*G), not twice that value;
the mathematical first derivative of s_C is -2||tangent||F^2.

At prime K=13/17, exact REAL doubly centered nonzero C has nonzero tangent,
by the previously reconstructed Fourier shift argument. Safe polar stepping
then gives strict exact proxy descent. This is established Fourier-defect
structure, not a new unistochastic/optimization theorem. The following
qualifications are material and already declared in the frozen contract:

- Norm<=1e-12 is treated as C=0, including truly nonzero weak signals.
  The prime strictness statement does not apply to that declared branch.
- Floating point centering, norm, Fourier and SVD calculations are not exact
  objects. The tolerances 2e-12/3e-11 are checks, not interval certificates;
  a sufficiently tiny exact improvement can fall below their resolution.
- For guided0 the mathematical output is F; the SVD may change its last
  bits. No exact bitwise equality is promised.
- K4 nonzero stall and the zero-signal fixture remain in the tests. Choosing
  prime dimensions prospectively avoids this particular kernel; it does
  not show extensive response, actual graph-cut descent or a B/D separation.

The new prime test uses an explicit centered rank-one table with Frobenius
norm one after normalization, so its bound sin^2(pi/K)/K has the right
normalization. It does not test every prime signal; the universal implication
comes from the proof, not those two test inputs.

## 4. Physical source, count laws and PIT controls

The declared path is ideal eta=1, K distinct single-photon inputs and K
vacuum modes, passive U, all occupation outcomes retained. No CF retry or
CF conditioning appears. The imported B sampler uses local
Clifford2017Backend objects with a fixed source state. D draws each labeled
input independently. species4 sums independent bosonic groups using the
same predeclared grouping for sampling and marginal tables; it is an
orthogonal-species model, not arbitrary partial distinguishability.

For a mode with occupied-input intensities q_a, the B generating function
is sum_r r! e_r(q)(z-1)^r, since its rth factorial moment is (r!)^2 e_r(q).
D removes r!. The coefficient inversion at lines 122-142 matches these
expressions. Independent species convolve their generating functions.
Old modes have exactly one possible contributing input, hence an exact
Bernoulli(1-p) marginal; their analytic replacement is valid for all three
particle models. Decimal80 operates on FLOAT input probabilities and the
final PMFs clip tiny negatives/renormalize: this is numerical arithmetic,
not an exact or relative-error certificate.

The B covariance diag(mu)+|VV*|^2-2PP^T has the correct CF-source form.
Gaussian sampling uses the actual covariance factor's variance after
eigenvalue clipping. Phi of each standardized nondegenerate coordinate
is marginally uniform; zero variance receives independent uniform jitter.
This controls marginal calibration, not the entire B PIT copula.

For exact marginal tables, randomized PIT F(n-1)+xi P(n) is marginally
uniform. Separate per-mode/shot jitters are used. The conditional-phase
control keeps the exact Bernoulli transferred subset and emits a multinomial
from its normalized coherent field. Its calibration samples the GLOBAL,
unconditional count law rather than conditioning the CDF on that subset.
The empirical CDF is not exact: per-mode DKW and finite-alphabet TV bounds
are logged separately and no joint-copula certification is claimed. The
declared failure probability uses 16*17 as a conservative union-count upper
bound on the 240 new-mode calibration histograms. All models use the same
top-q and greedy completion rule, priority, q=ceil(K/2), and lambda grid.

## 5. Shared guides, discoveries, tuning and budgets

The source is the charged capped best-swap anchor S0, with a certification
flag distinct from reaching the scan cap. It remains fixed for all optical
draws. All K^2 swaps, zero/pure-greedy decoders and per-network/model/lambda
counterfactual vacuum-mid-PIT candidates are scored before the shared Cref
is chosen. Those discoveries are available to every arm. All network,
marginal and phase-calibration preprocessing time is recorded as common
work; it is not omitted from a standalone-method budget by this review.

Six field arms get the same four network settings, two decoder lambdas,
two trials and four draws per graph. Each model independently selects its
setting by pooled DEV gain; all trials/settings remain in raw. There is
no held-out acceptance. Scanning eight settings is tuning effort, not eight
free candidates from a single selected circuit. This selection cannot
support a positive result without subsequent independent evaluation.

Static arithmetic confirms 256 decoded proposals per arm. With q=7 at
K13, the completion counts 19+18+17+16+15+14 partial marginals plus one
final cut: 100 score units/proposal. At K17/q9 the count is
25+24+23+22+21+20+19+18+1=173. Thus 32 proposals per graph/trial correspond
to 3200/5536 baseline query units. Each B/D/species arm injects 3840
SIMULATED photons in total, with no loss rejection. The 65536 conditional-
phase calibration draws are extra common CLASSICAL work, not optical shots.

Anneal, spectral+swap, collective KL and block matching each independently
receive the full query budget. Matching consumes the same Delta and samples
Bernoulli transfer sizes at p=.25/.5, then solves a rectangular assignment
and scores the actual multi-swap cut. There is no implication that a sum
of single-swap costs equals that cut. Shared guide preprocessing is
classical and assignment already globally minimizes the routing proxy.
Observed baseline prefixes are capped by BOTH score budget and measured
online model time. Such simulator timings do not constitute hardware
latency comparisons; cold imports and recording overhead are acknowledged.
Taking a best-of-four classical portfolio would require charging its
combined work, not silently treating it as one baseline.

One minor accounting distinction should stay explicit in reporting:
the ledgers count charged proposal/score INFORMATION units, not a literal
instrumented count of every call to cut(). Known initial/source cuts are
recomputed in prepare and baseline initialization without being counted
again. This supplies no uncredited new candidate or optimum information,
but “exact number of all objective-function invocations” would overstate
what these ledgers measure. Timing includes those repeated computations.

## 6. Checks pending, interpretation and provenance

The 13 parametrized test cases were READ, not run. They cover finite K3
Fock/labeled enumeration, small species, marginal/transfer/covariance
identities, carried-order labeling, Gaussian variance, PIT moments,
conditional-phase calibration, decoder accounting, matching, local sampler
acceptance, prime proxy orientation/descent and the exact composite/zero
fixtures. One accepted local sample is a smoke check, not a statistical
sampler certificate. The synthetic prime table need not be a production
graph: its job is the algebra/orientation check. The separate positive-
weight composite graph is a realizable counterexample to universal strictness.

No static finding here substitutes for the targeted preflight at the exact
closure, preservation of its first failure, or the full integration suite.
Only after the authorized single-slot preflight passes can the bounded DEV
run be assessed. A completed runner is not a positive physics verdict. Any
signal must surpass independently tuned D, species, Gaussian, IID, phase
and honestly budgeted classical searches; tiny samples/calibration ambiguity
remain inconclusive. There is no QPU, novelty or quantum-advantage verdict.

Commands actually executed for this review were read-only `git show`,
`git rev-parse`, scoped `git diff 695b5d2 -- ...`, `git diff --no-index`
between P46/P47 scripts, `rg`, `cat`, `nl -ba`/`sed` for the listed sources,
and `shasum -a 256`. Review-file scope/whitespace and hashes were checked
before its isolated commit. No Python, pytest, physical simulation, source
modification, raw inspection, QPU call or numerical experiment occurred.
