# P35 component review at d402374

**Primary verdict: correct only after the stated restriction to finite integral resource limits.** The core rank-one/rank-two vacuum DP and the threshold-QUBO formula are proved as written under the distinct-single-photon and exact-frame hypotheses. No mathematical or numerical discrepancy was found. The reviewed implementation accepts NaN resource limits, defeating its guards; this does not invalidate the archived P35 results, which used the integer defaults and an external bounded runner.

Reviewed base: `d402374b21a812de1d1b5658fac37d294a20a035`. Component SHA256: `3a780d09389d80fe5156a86a062c56210378d0ee64ed97d0f1faa994faa5b515`. All executions used this isolated worktree's source. The coordinator subsequently reported a resource-validation fix in the principal checkout; that different implementation is **not** covered by the evidence below. The old source and receipts are deliberately unchanged.

Independence: this reviewer proposed the original P35 API and scientific route before a quota interruption. The coordinator wrote the actual component, tests and experiment examined here. I did not author those files, but knew the route and prior derivation and read the author's report. This supplies a separate implementation review and an independent arithmetic code path; it is not a blind external review or independent discovery of the method. Mathbox proof-audit and computation-audit guided the review. No source, shared status, manuscript, hardware, credential or model-service change was made.

## Normalized claim and dependency graph

For any exactly represented Gaussian-rational m-by-N frame W with orthonormal columns, 0<=N<=m, representing one indistinguishable photon in each of N distinct occupied inputs, the class returns the unconditioned threshold means E[x_i], E[x_i x_j] and E[x^T Q x] for real symmetric rational Q. Output collisions remain included. Its low-level function evaluates the associated formal polynomial for at most two selected rows even without a physical frame. Subject to sufficient finite integer resource caps, evaluation terminates by exact integer/Fraction arithmetic, without Fock-law enumeration in the marginal routine.

The dependency graph is:

- The distinct-input creation state has norm one; projection onto no photons in selected outputs A replaces each column by its complementary projection.
- The projected product state's squared norm is the permanent of the projected-column Gram matrix, `I - V^dagger V`, where V=W[A,:]. This follows by explicitly pairing each annihilator with a creator. It is a permanent, not the squared modulus of that permanent.
- Expanding the identity contribution leaves principal subpermanents of `V^dagger V` with subset signs. Resolving each Gram factor by its selected-output label gives the polynomial and factorial extraction below.
- The integer recurrence evaluates that polynomial exactly, including off-diagonal multidegrees.
- Threshold inclusion-exclusion and `x_i^2=x_i` yield the returned moments and symmetric-Q energy.

These are internal algebraic implications, not empirical deductions from 12 circuits. Attribution to the known marginal algorithm remains as documented in `research/phase3_lowrank_sources.md`; this review does not reauthenticate that external literature record or claim novelty.

## Independent invariant and extraction check

Let D be the LCM of every real and imaginary entry denominator of V, and put `z_aj=D V_aj` in the Gaussian integers. At stage j, the dictionary entry for `(p,q)` is exactly the Gaussian-integer numerator

`D^(2j) * [x^p y^q] product_(ell=1..j) (1 - (sum_a conjugate(V_aell) x_a)(sum_b V_bell y_b))`.

The initial constant is one. Carrying an old coefficient into the new denominator multiplies it by D^2. A transition subtracts `conjugate(z_aj) z_bj` times the old coefficient and increments p_a and q_b. In the code, this kernel has real part `ar*br + ai*bi` and imaginary part `ar*bi - ai*br`. Subtracting its product with `(cr,ci)` gives precisely `(old_r-real*cr+imag*ci, old_i-real*ci-imag*cr)`. The signs and conjugation are correct.

Every state has equal total degrees `|p|=|q|<=j`. Only exactly zero coefficients are pruned. Off-diagonal p!=q states must survive because later transitions can reach p=q; they do survive here. A fresh dictionary avoids overwriting an old stage. The final denominator is D^(2N), consistent for every degree because the carries supplied all missing denominator factors.

For a selected subset of inputs, the two assignments of output labels contribute to a principal Gram permanent exactly when their label multiplicities match. With multiplicity vector p, there are `product_a p_a!` label-preserving bijections. Consequently the answer is `sum_p (product_a p_a!) f_(p,p)`. This explains both factorials in code and why no global N!, output square, or distinguishable-particle product may replace the extraction. Hermitian Gram permanents are real; the exact imaginary-part check is appropriate.

The HOM control uses the exactly rational complex unitary with rows `(a,b)` and `(b,a)`, `a=(1+i)/2`, `b=(1-i)/2`. Single-mode vacuum is exactly 1/2, and joint two-mode vacuum is zero. Omitting the degree-two factorial gives the familiar wrong single-mode value 1/4. Dropping off-diagonal polynomial states gives the wrong joint value 1/2. The reviewed code returns the correct values. Vacuum and empty selected-output sets return one; the unary control gives `1-|3/5|^2=16/25`.

## Threshold, source and input semantics

`click_means` uses `1-p0(i)`. Distinct pair entries use `1-p0(i)-p0(j)+p0(i,j)`, while diagonal entries equal the means. For symmetric Q, the implemented energy is `sum_i Qii E[x_i] + 2 sum_(i<j) Qij E[x_i x_j]`; the factor two is correct and non-symmetric Q is rejected. No constant offset is part of the `x^T Q x` API. No success/feasibility normalization or optimum label appears.

Exact orthonormality checks both real and imaginary Gram components, not just column norms. Thus duplicated occupied columns are rejected in physical mode. A frame models distinct occupied input modes, not a list permitting repeated input photons. Its N=m case is within scope and is present in the original exact controls. A physical orthonormal frame can be completed to a lossless unitary; arbitrary formal selected rows do not by themselves establish that physical interpretation.

`encode_binary_frame` converts the supplied binary64 entries to exact rationals separately. With frame validation disabled, the code labels the result `FORMAL_POLYNOMIAL_ONLY_UNVALIDATED_FRAME`; it need not be a probability. This is correct. The adversarial input `[[2]]` is rejected by exact physical validation but returns vacuum -3 and click mean 4 in formal mode, with no clipping. Neither formal exactness nor a small floating orthogonality residual certifies an unknown physical matrix, relative error, calibration uncertainty or the theory note's sufficient-precision hypothesis. This component implements no interval certificate, loss model, partial distinguishability or full-output sampler.

## Finite verification and provenance

The committed review script is `experiments/P35_component_review/audit.py`, with contract `contract.json` declared before execution. Its reference uses complex numbers as separate pairs of Fraction values, independently implemented addition/multiplication/conjugation, and the Ryser subset permanent of the N-by-N matrix `I-V^dagger V`. It does **not** reuse GaussianRational arithmetic operators or the DP recurrence in that reference. Ryser is deliberately an exponential small reference, not the proposed scalable baseline.

The script reads all 12 existing raw records, seeds 20261122–20261133, without generating circuits or running the original P35 campaign. It checks every one-/two-output vacuum marginal, giving **190 exact comparisons**, maximum difference **0/1**. It then checks all saved means, pair moments and QUBO expectations against those independent values. For the six exactly physical rational frames it additionally sums the archived exact Fock probabilities and verifies normalization and all vacuum events. The other six remain explicitly formal binary inputs. Dimensions are m=4,6,8, N=2,3,4, with full-law size at most 330. No conclusion about tested larger N follows.

Three deterministic formal complex-row controls also agree exactly with the independent Gram permanent: rank-one value `84989/158760`, rank-two value `21855250843/70013160000`, and the same rank-two value after reversing the input columns. HOM, vacuum, unary, nonphysical-frame and invalid-limit probes are retained in the same receipt. These are small algebraic controls, not new physical circuit trials.

The saved Perceval laws were checked for unique complete basis size, photon count, nonnegativity and normalization; their reported moments and energy remain consistent with the independently verified exact/formal values. This review did **not** make fresh Perceval calls. The original experiment did so for all 12 circuits, with six exact Fock comparisons. Its archived maxima remain click/pair error `5.551115123125783e-16` and QUBO error `7.105427357601002e-15`; finite floating agreement does not turn the six QR encodings into exact physical unitaries.

The existing targeted test file passes **7 tests in 0.70 s**, run after the coordinator confirmed the shared full suite had finished. Only this file was run here. The independent exact check took 0.192 s internally, 0.289 s including runner overhead. Both new runs have wall cap 60 s, per-process CPU cap 30 s and conventional one-thread caps, below the requested small-check budget. They created no physical shots. The review run completed successfully while explicitly reporting `EXACT_CHECKS_PASS_WITH_RESOURCE_GUARD_DEFECT` rather than hiding the defect.

The original v2 manifest and both review v2 manifests were validated with current hashes in this worktree; validation outputs and commands are retained in `experiments/P35_component_review/validation_receipt.json`. All pinned inputs were unchanged. The review script loads only the audited stdlib module directly from this worktree to avoid an unrecorded dependency on the principal checkout. The pytest run puts this worktree's src on PYTHONPATH. No dependency was added or installed.

## Findings and cost audit

| Obligation | Verdict | Evidence or limit |
|---|---|---|
| Common-denominator invariant, complex signs | Passed | Direct algebra above; independent exact Gram/Ryser comparisons |
| Factorial extraction and normalization | Passed | Multiplicity bijection count; HOM1/2 and joint vacuum0 |
| Off-diagonal p,q retention | Passed | Full dictionary keys; cancellation-sensitive HOM and complex controls |
| Threshold/QUBO conventions | Passed | Inclusion-exclusion, symmetric factor two, independent full quadratic sum |
| Exact physical versus binary/formal semantics | Passed | Exact complex Gram validation and explicit formal labels; no clipping |
| Current archived results | Verified in stated finite range | 190 exact marginals; all 12 records, six physical exact frames, seven tests |
| Resource guards on arbitrary public arguments | Failed | NaN bypass reproduced at lines88,110,114; discussed below |
| Full integer-operation or hardware cost | Not established | Counters are logical DP work only, correctly limited by author report |
| External source authentication/novelty | Out of scope | Existing source note; known baseline, no novelty claim |
| Growing-size performance and optimizer quality | Out of scope | No scaling benchmark, optimizer, finite-shot or device comparison |

**Confirmed defect, reviewed old source:** `vacuum_probability([[Fraction(1,2),Fraction(1,2)]], max_states=float('nan'))` returns 5/8, visiting three states, instead of rejecting the invalid cap. The corresponding `max_transitions=NaN` call likewise completes with three transitions. Comparisons with NaN are false both at initial validation and at the guard. Finite integral positive state limits and nonnegative transition limits avoid this flaw; defaults and all archived runs satisfy that restriction. This is a public resource-validation defect, not a counterexample to the marginal formula. The coordinator was notified immediately. The recommended repair is to reject booleans, non-integral values and out-of-range integers at both entry points. The current receipt records the old defect and must not be rewritten after repair.

The dense state bound is `S_r(j)=sum_(s=0..j) binom(s+r-1,r-1)^2`; rank-one visits are at most `T1=N(N+1)/2`, and rank-two visits at most `T2=N(N+1)^2(N+2)/12`. Nonzero-kernel pruning can reduce actual work. The recorded `state_visits`, `transitions` and `peak_states` respect these bounds for all archived cases and are reproduced exactly by the independent review calls. N=4 rank-two peak is 55 states. The largest archived reported integer bit size is 505 (309 among exactly physical rational cases).

These fields do not count all primitive integer operations: carries, LCM/GCD/denominator preparation, complex-kernel preparation, factorial extraction, exact Gram validation, Fraction reduction, QUBO aggregation and bookkeeping remain additional. The bit statistic scans stage coefficients and the final numerator/denominator, not every multiply/add temporary. Peak states describe one following dictionary, not combined live dictionaries or bytes. The class performs exact physical validation using O(mN^2) Gaussian-rational products; the DP itself does not form an N-by-N Gram matrix. The reviewed implementation computes factorials during extraction instead of precomputing their table; this does not invalidate the polynomial bound but belongs in honest measured cost.

The theory's fixed-rank polynomial arithmetic/bit-computability conclusion is supported. Total marginal arithmetic is O(mN^2+sN^4) for s needed output pairs, plus validation/input/QUBO costs; workspace is polynomial and caches add O(m^2) values. No unit-cost physical arithmetic model, numerical stability theorem for ordinary float64, speed advantage or large-size practicality follows. Source construction, variational-unitary access, optimization and finite-shot information remain separate obligations.

The first contract literally asked for real rational orthogonal four-mode controls. The recorded exact cases are instead Gaussian-rational complex unitary frames; these are genuinely orthonormal physical frames and test the stronger conjugation path, but they should be described by that executed domain. The report already does so. This review did not silently add a real-frame trial or exceed the declared original 12 circuits.

## Remaining action and strongest safe statement

Keep P35 as the known exact ideal threshold-mean baseline. Its core math and preserved finite data pass this review, with the old API restricted to valid integer caps. Review the separately committed guard repair before advertising arbitrary-argument guard validation. No scientific campaign rerun is needed to establish the old data's correctness; any post-fix check must have a new receipt and source hash.

The executable routine gives exact unconditioned threshold-QUBO means for exactly supplied orthonormal Gaussian-rational distinct-input frames, subject to its resource guards. For encoded binary approximations, it gives exact values of the encoded formal polynomial. Neither statement supplies a full sampler, feasibility-conditioned objective, optimizer guarantee, modal candidate, quantum advantage or hardware gate.
