# Independent proof audit of P31: fixed-input penalty washout

**Primary verdict: proved as written**, under the explicitly stated hypotheses. No incorrect factor, missing inequality, invalid normalization, or scope-breaking step was found in P3.1, the Fock/copy consequences, the conditional decoder reduction, or the counterexamples. This is a correctness verdict for the restricted mathematical result, not a novelty, optimization-performance, or QPU-readiness verdict.

Exact proof reviewed: `theory/phase3_penalty_washout.md` at commit `b58246fdcb8efaf66d5dbb13faa6849590d1b847`, SHA256 `59f2879c830cd42b8c8f647df947e5c27d7262fecfbe6e60358151270806034b`. The theory worktree's current file was checked against that Git object's bytes and has the same hash. Review date: 2026-11-21. Reviewer worktree: `.qwen/worktrees/phase3-literature`, based on `1680234067000c0f4d8121fe328176fb2edc8c16`.

The reviewer is a different agent from the proof's author and reconstructed the implications before accepting the author's computation report. The reviewer had previously implemented the static optical component; that familiarity is disclosed rather than presented as a blind implementation review. The additional calculation below imports no project optical/simulation code. This review and agreement between agents are not formal proof certificates.

## Claim card

Quantified objects: fixed even `m>=4`, fixed symmetric zero-diagonal nonnegative weights with at least one zero off-diagonal pair, target `k=m/2`, canonical symmetric penalty QUBO, fixed integer `R>=1`, variant `v in {1,2}`, and a fixed permutation of every unordered mode pair. The strict normalization regime is `m*lambda>d_++w_+`. For the displayed `R>=2` constant, additionally `w_+/D<=1/2`, where `D=m*lambda-d_-`.

Conclusions: exact normalized coefficients; operator-norm bounds (4) and (5); fixed-parameter upper convergence rates; the symmetric `N`-photon norm lift; measured total variation and necessary independent-copy budgets for a common pure input; and the stated classical candidate-pool reduction only with the required gaps, unrestricted prefix branch and `lambda>W`.

The theorem does not quantify over graph-dependent changing sources, adaptive retuning, penalty-dependent layouts, arbitrary QUBO gauges, uncharged postselection, or the complete hybrid optimizer. For an inter-graph comparison the inputs and subsequent channels must be common as stated. Its big-O constants are allowed to depend on the fixed graph, size, layout and repetition count.

## Dependency graph and obligation matrix

The proof has the following internal chain:

`penalty expansion -> exact min/max -> normalized couplings -> scalar gate differences -> finite unitary-product telescoping -> symmetric-tensor lift -> common-input vector overlap -> pure-state trace distance -> measured/copy bounds`.

The decoder statement is a separate branch:

`raw Fock TV -> marginal/event errors -> strict-gap stability -> one feasible kth prefix + stable modal pattern -> infeasible-energy separation -> at most two fixed feasible candidates`.

The counterexamples independently delimit which hypotheses cannot be removed. External sources fix the competitor's implementation, not an unproved mathematical leaf of the norm or fidelity argument.

| Obligation | Verdict | Decisive check |
|---|---|---|
| Symmetric QUBO coefficients and additive constant | Passed | Off-diagonal terms occur twice in `x.T Q x`. |
| Minimum, maximum and positivity of `D` | Passed | Strict diagonal/off-diagonal separation plus the zero-weight pair. |
| Literal Rx half-angle and doubled variant | Passed | Checked archive definition and existing authenticated gate convention. |
| Equation (6), exact gate norm | Passed | Eigenvalues of `exp(i delta_beta X/2)` give `2 abs(sin(delta_beta/4))`. |
| `R=1` bound and constant `v/4` | Passed | Exact complementary-arcsine identity, then the gate factor one half. |
| `R>=2` derivative constant and `R` repetitions | Passed | Denominator bounded separately on `[1/2,1]`; telescoping counts each pair `R` times. |
| Noncommuting ordered products | Passed | Telescoping only uses unitarity, not commutation. |
| `N`-photon symmetrization and factorials | Passed | Normalized symmetric embedding is an isometry; restriction cannot increase norm. |
| `F>=1-e^2` | Passed | The real-overlap lower bound is nonnegative in the explicitly used range `e<=1`. |
| Pure-state trace distance and halved TV convention | Passed | Two-dimensional span gives `sqrt(1-F)`. |
| Independent-copy `sqrt(t)` factor | Passed | Fidelity tensorization and Bernoulli's inequality, with the large-`e` cap handled separately. |
| Necessary copy bound and zero-bound exception | Passed | The implication is necessary only; `N=0` and `B=0` are separately excluded/handled. |
| Common channels versus postselection | Passed | Trace-preserving common channels contract; conditioning needs its denominator. |
| Decoder branch and kth-prefix support | Passed | Authenticated `graph_val=0` returns every nonempty prefix, including size `k`. |
| Modal statistic matches the archive | Passed | A modal raw Fock outcome is selected and only then thresholded. |
| Two-candidate reduction under gaps | Passed, conditional | Boundary gap fixes the kth set; modal gap fixes one Fock outcome; `lambda>W` excludes every infeasible candidate. |
| Counterexample to automatic marginal gaps | Passed | Commuting matching generators give a permutation-invariant limiting circuit. |
| Rotating-eigenvector counterexample | Passed | Distinct finite eigenvalues, nonconvergent projectors and a degenerate limiting unitary. |
| Claims about full-solver failure or novelty | Out of scope | Neither follows from the mathematical result. |

## Independent reconstruction of each constant

### 1. Penalty and exact global normalization

For binary variables,

`cut_w(x)=sum_i d_i*x_i - 2*sum_(i<j) w_ij*x_i*x_j`,

and the penalty contributes diagonal `lambda*(1-2k)` and pair coefficient `2*lambda`, together with `lambda*k^2`. With `2k=m`, equation (1) follows exactly.

The strict regime gives

`max(diagonal)=d_+-(m-1)*lambda < lambda-w_+ = min(off-diagonal)`.

A zero-weight pair makes the largest off-diagonal coefficient `lambda`. The smallest diagonal is `d_--(m-1)*lambda`; subtracting it gives the denominator `D=m*lambda-d_->0`. Therefore the off-diagonal numerator is `D-w_ij` and the diagonal numerator is `d_i-d_-`, proving (3). In fact the regime also implies `D>w_+`, so every square root in the `R=1` bound is inside its required domain. Empty weights are permitted and give the exact limiting circuit already at finite penalty.

This derivation depends on the canonical QUBO including its diagonal. Removing the diagonal, changing a QUBO gauge, or normalizing off-diagonals alone would be a different map; the proof does not silently cover those choices.

### 2. Gate norm and endpoint bound

On the affected pair, `G(beta)=exp(i beta X/2)`. The eigenvalues of `G(beta')^dagger G(beta)` are `exp(plus/minus i*(beta-beta')/2)`. Consequently its difference from identity has norm `2 abs(sin((beta-beta')/4))`, including when embedded into additional unchanged modes. The upper bound `abs(beta-beta')/2` is correct.

At `R=1`, for `z=w_ij/D`, the complementary-angle identity gives

`g_1(1)-g_1(1-z) = (1/2) arcsin(sqrt(z))`.

Multiplying by `v`, then by the gate Lipschitz factor one half, gives a per-pair difference at most `(v/4)*arcsin(sqrt(w_ij/D))`. There is one pass, so summing gives (4). The square-root term in the stated angle expansion has the correct coefficient `-v/2`; its next term is of order `D^-3/2` with fixed positive weight.

For `R>=2`, differentiation gives exactly

`g_R'(a)=1/[4R sqrt(a) sqrt(1-a/R^2)]`.

On `[1/2,1]`, `sqrt(a)>=sqrt(1/2)` and `sqrt(1-a/R^2)>=sqrt(1-R^-2)`, giving the stated conservative `L_R`. The extra hypothesis places all normalized off-diagonal couplings in this interval. A coupling difference is `w_ij/D`; multiplying by `v`, the one-half gate factor and the number `R` of occurrences gives `v*R*L_R*W/(2D)`. No factor of two or repetition is missing in (5).

For a product of unitaries, insert one changed factor at a time. Every unchanged prefix and suffix has norm one. This justifies summing the gate errors in any fixed chronological order; no assumption that all gates commute is present. Since `D=m*lambda-d_-` is asymptotic to `m*lambda` with fixed graph and size, the stated half-power and first-power upper rates follow. Cancellations can make the true distance smaller.

### 3. Symmetric-sector lift

The normalized occupation basis identifies the `N`-photon space with `Sym^N(C^m)` isometrically. Passive linear optics acts there as the restriction of `U^(tensor N)`. This identification includes the input and output occupation factorial normalizations; it is not an unnormalized monomial representation.

Expanding the tensor-product difference replaces one factor at a time, giving `N` terms, each with norm at most `||U-V||` because the remaining factors are unitary. Both tensor products preserve the symmetric subspace. Restriction therefore yields (7) without a dimension or factorial multiplier. Applying it to the same unit vector gives a vector distance at most `e=N*B_lambda`. The vacuum representation is constant as separately noted.

### 4. Fidelity, TV and independent copies

For normalized vectors `psi,phi`, `||psi-phi||^2=2-2 Re<psi,phi>`. Thus the real overlap is at least `1-e^2/2`. When `e<=1` this lower bound is nonnegative, so squaring is legitimate:

`F=abs(<psi,phi>)^2 >= (1-e^2/2)^2 = 1-e^2+e^4/4 >= 1-e^2`.

The proof uses **squared** fidelity. The trace distance of the associated pure states is `sqrt(1-F)`, with no extra factor of two because trace distance is already halved. For a common POVM, every outcome-event probability difference is bounded by trace distance; hence measured TV cannot exceed it. This proves (8); for `e>1`, its cap at one is sufficient.

For `t` independently prepared copies, the squared overlap is `F^t`. Joint measurements do not change the pure-state trace-distance upper bound `sqrt(1-F^t)`. For `e<=1`, Bernoulli's inequality gives `1-(1-e^2)^t<=t*e^2`. For `e>1`, the capped result is trivial for any positive integer number of copies. Equation (9) therefore holds throughout the declared range.

If a measurement has TV at least `c`, then `c<=sqrt(t)*N*B_lambda`, which implies (10) when `N>=1` and `B_lambda>0`. If `B_lambda=0`, the states are identical and no positive discrimination distance can be obtained; the note handles that case explicitly. The big-O upper bound on distance supplies the **necessary** big-Omega copy cost, without asserting attainability. In particular, perfect separation at finite copies is not promised by this inequality.

A common completely positive trace-preserving channel can be absorbed before the final measurement. A postselection normalization cannot be absorbed in that way for free. For two graphs the triangle inequality requires the same limiting unitary, photon sector, input and channel; the text specifies those common objects and does not transfer the bound to independently graph-aware maps.

## Decoder corollary: no hidden universal gap assumption

The original archive's `get_sorted_indices` is descending `argsort`, and `solution_guesses3(...,graph_val=0)` returns every prefix of lengths one through `m`. These functions were read from the authenticated archive, not inferred from a generic decoder name. The coloring and assignment branches filter candidates and are correctly excluded.

A raw Fock TV error `epsilon` changes any fixed click marginal and any individual Fock-event probability by at most `epsilon`. If the reference kth and next marginal differ by `g>2epsilon`, no outside mode can enter the top-`k` set; internal ties within that set do not matter. Similarly `h>2epsilon` preserves a unique modal Fock outcome. Thresholding that fixed mode gives the same modal binary candidate. The proof does not confuse this with the mode of the coarsened threshold distribution.

Every infeasible binary string has integer cardinality mismatch at least one, nonnegative cut and therefore `E_lambda>=lambda`. Every feasible cut is at most `W`. Under `lambda>W`, the feasible kth prefix beats all infeasible candidates strictly, including the size-`m` prefix and any infeasible modal threshold. The final winner is selected among that fixed kth set and the fixed modal threshold if it is balanced. Thus the cardinality of the remaining feasible pool is at most two, as asserted. Neither the global optimum nor graph-independent final selection follows.

The paragraph about a graph-aware decoder being a common channel is also appropriately qualified. A common single-sample stochastic map contracts. The actual distribution-level ranking/argmax operation is not itself a linear single-sample channel; the following gap argument is its separate justification. There is no invalid direct application of data processing to the discontinuous ideal ranking operation.

## Counterexamples checked analytically

For the ordered matchings `(01,23),(02,13),(03,12)`, each matching generator `P_i` is an involution. Their products form the Klein four group; in particular they commute, and their sum is `J-I`. The two disjoint gates in a matching give `exp(i beta P_i/2)`. Hence an `R`-pass equal-angle circuit is

`exp(i R beta (J-I)/2) = exp(-i R beta/2) [I + (exp(2i R beta)-1)J/4]`.

This confirms every factor in (11). The matrix commutes with all mode permutations. Its bosonic lift sends the permutation-invariant source `|1111>` to a permutation-invariant output law, forcing equal click marginals. Therefore `g=0` exactly. The text correctly claims failure of an automatic-gap premise, rather than claiming that every perturbed decoder has a nonconvergent output.

In the rotating-eigenvector example, at every finite `t>=1` the two eigenvalues `exp(plus/minus i/t)` are distinct. The first spectral projector is the rotated rank-one projector. Along `t=2*pi*n` it is the original projector, while along `t=2*pi*n+pi/4` it is a different fixed projector. Meanwhile the unitary distance to identity is exactly `2*sin(1/(2t))<=1/t`. This is a valid counterexample to unqualified spectral-anchor convergence and does not challenge the static finite-product theorem.

Common unitary evolution preserves the inner product of two source states. Orthogonal graph-selected inputs, or different photon-number sectors, therefore invalidate a blanket extension to arbitrary changing source selectors. Likewise different graph-aware classical output maps can produce different outputs from identical raw distributions. The threshold detector need not distinguish every orthogonal pair; the note explicitly avoids that stronger claim.

Finally, off-diagonal-only normalization of `lambda-w_ij` is `(w_+-w_ij)/(w_+-w_-)` when the denominator is positive, so its penalty cancellation is exact. The note correctly requires a separate convention for a constant off-diagonal range and does not infer task-quality improvement merely from avoiding washout.

## Executed small independent falsification attempt

No large P31 run was repeated. A new standalone calculation used SciPy matrix exponentials of embedded pair generators and explicit permanent sums over all permutations for every input/output occupation. It imports **no project simulator, creation recurrence, component or competitor program**.

The script checked seven domain-valid configurations on four modes: a weighted-regular cycle, an irregular weighted path explicitly within the mathematical extension, and the empty graph; penalties `1.2`, `2`, `100` as appropriate; `R=1,2,10`; both variants; lexicographic, reversed and matching orders. The nonempty matrices meet the exact normalization regime and, when used, the extra derivative regime. For each configuration it constructed full `N=2` and `N=3` Fock operators, not only a single output state: **14 operator cases and 3500 input/output matrix entries**.

For each case it tested raw representation unitarity, the full operator lift against `N*||U-U_infty||`, the displayed `N*B_lambda` bound, a fresh normalized complex superposition input, fidelity and PNR TV. It checked the independent-copy bound at `t=1,2,7`, **42 checks**; twelve nonzero copy bounds were below the trivial cap, and the empty-graph zero-distance cases were retained. It also checked the matching-generator identities exactly using integer matrices.

Seed: `813260521`, NumPy `default_rng`/PCG64. Maximum raw Fock-operator unitarity residual: `6.217248937900877e-15`. No bound violation was found at the declared `1e-11`/`1e-10` floating tolerances. This is finite falsification evidence, not the proof of a universal claim.

Executed command from the literature worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 \
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python \
/private/tmp/phase3_washout_independent_check.py
```

Preserved script SHA256: `c0136ef4a39c7f6b1a226ae06ac9495d97f5f92d8eccd0884b1cc5cac0bc2f27`.
Preserved receipt: `/private/tmp/phase3_washout_independent_receipt.json`, SHA256 `1634df7b6cf66432684d4a11c5bcfc1320c2d0bfd5156e00a61a849363418f46`. The receipt records the exact proof Git object and hash; no result is substituted for the analytic reconstruction above. Runtime was approximately 0.065 seconds for the calculation, process exit zero. The temporary script and receipt can be copied into a coordinator-owned evidence area if durable retention is desired; no third project file was written by this review.

The existing P31 `run_001` manifest was also checked read-only with the Mathbox v2 validator against its theory-worktree root. Result: `valid evidence record (run status: completed)`. The author's 972 matrix, 36 Fock and 36 gap checks were inspected as supporting evidence, not rerun or treated as proof.

## Residual limits, tests and disposition

No unresolved mathematical implication was found within the exact stated theorem. Physical support is still ideal simulation; changing source preparation, graph-aware processing, finite-sample ranking, hardware acceptance and actual optimization resources remain separate research obligations. This review makes no claim about novelty; the companion `research/phase3_washout_novelty.md` is the distinct source-overlap audit.

The strongest safe conclusion is the restricted static-unitary washout bound, its common-input independent-copy consequence and the explicitly conditional decoder candidate-pool reduction. The gap-free decoder, spectral-anchor and arbitrary hybrid extensions are correctly excluded or refuted. No full-solver lower bound, quantum advantage, or hardware gate follows.

Before committing these two reports, the existing suite in the isolated literature worktree was executed:

```sh
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/private/tmp/pasqal-matplotlib \
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -m pytest tests/ -q
```

Result: **150 passed in 2.24 seconds**. No proof, source, test, raw P31 data, shared research state, manuscript or QPU file was modified. This is an independent proof-review artifact tied to the exact reviewed revision, not a change to that revision.
