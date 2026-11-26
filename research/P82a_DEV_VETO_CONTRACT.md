# P82a prospective K8/n16 first classical veto

26 November 2026. **CONTRACT ONLY; no implementation or execution is authorized by this file.** This is one prospective B-only development screen, followed first by fixed from-raw FAST controls. A surviving screen remains inconclusive for advantage. ROOT must review the implemented source/tests/bindings, authorize one tiny qualification, inspect its sealed result, then separately authorize one main. Zero failed retries or unregistered canaries.

Frozen parent design: P82 commit f7cb5d99fa35b6ab9e6ff60839f985d81ea87001, research/P82_HARDWARE_COMPATIBLE_ESCAPE_DESIGN.md, SHA-256 c008f60143a1c4b0e81dcec1ba7a07c28d89244b10d4d69695070d27b0916723. It is not modified.

## 1. Fixed population and scope

Use $n=16$ graph vertices/modes, $K=8$ photons, receiver dimension eight and $d=4$. This is the smallest even-K member with replacement distance four beyond the paid one/two/three-swap controls. K6 cannot supply that distinction. Complementation identifies raw costs at distances $r$ and $K-r$; it does not by itself equate stochastic quench endpoints.

Two NEW unplanted anchors, never replaced on an unfavorable outcome:

| Case ID | Topology recipe, pinned NetworkX 3.6.1 | Topology seed |
|---|---|---:|
| ER8201601 | gnp_random_graph(16, 0.4, seed), undirected, no connectivity filter | 8201601 |
| RR8201602 | random_regular_graph(4, 16, seed) | 8201602 |

For each topology, replace every edge by its canonical pair (min(u,v),max(u,v)), sort these pairs lexicographically, and draw one integer weight in 1..5 inclusive per pair using its independent PCG64 weights stream. Build an exact int64 symmetric adjacency with zero diagonal. Do not use P43.make_graph or an old DEV adjacency. Generator failure stops; no seed repair, graph selection, planted optimum or held-out data. Synthetic graph generation is timed separately as construction of the problem input, not B's optimization allowance. Each algorithm pays its own raw-input copy/validation.

Main performs **48 B raw attempts per anchor: three independent resets, sixteen steps each; 96 attempts and 768 modeled injected photons total** if complete. No parameter grid, SPSA or data-selected setting is present. Graph-dependent phase optimization is part of the paid algorithm, not uncharged training. All attempts, including $r=0,8$, identities, bunches and repaired outputs, remain in the result. Optional D/species experiments are NOT RUN by this program.

## 2. Fixed parameters, marks and seeds

Use rho=1, eta=1/2, TWO sequential phase-coordinate sweeps. The repeated source odds are $(1/2,5/6,7/6,3/2)$, hence the splitter probabilities are
  \[
  (1/3,5/11,7/13,3/5,\ 1/3,5/11,7/13,3/5).
  \]
These settings are fixed before graph generation; none is reselected after counts.
Graph cuts use exact integer arithmetic; compiler arrays use float64/complex128 and record their actual rounded values.

Root seed is **82026001**. Every role is a distinct tuple
  \[
  [\text{"P82a"},82026001,\mathrm{caseID},\mathrm{arm},
    \mathrm{chain},\mathrm{step},\mathrm{role},\mathrm{index}].
  \]
Encode it as compact ASCII JSON with separators comma/colon, no whitespace, in exactly this order; hash with SHA256. PCG64 seed is the first eight digest bytes interpreted little-endian. Native seed is 1 plus the first four digest bytes modulo $(2^{32}-1)$. No seed digest or RNG has been evaluated for this contract.

Main fixed B roles are case priority; reset start (chain0..2); and for each step0..15: portS, portT, phase_init, split, native, repair. Unused fields are -1 and index0. Weights use arm GEN, chain/step -1, role weights, index0. Each classical call uses one private stream with its uppercase mode as arm, chain/step -1, role control and index0, advancing only in its stated policy order. P50 receives that stream's seed and owns its RNG internally. Source must archive the literal tuples and actual derived seeds; check distinct main PCG role seeds and all 96 potential native seeds before any graph. A collision is first failure, not a rehash.

Each stream is an explicit Generator(PCG64(role_seed)); do not rely on NumPy globals. A native call explicitly sets/records its separate native seed. Perceval random_seed also resets Python/legacy NumPy globals; it must not affect any explicit Generator stream.

For each attempt, independently permute the sorted CURRENT S and T under portS/portT. First four S ports form I0, last four I1; first four T outputs are a-plus, last four a-minus. Draw four phase_init integers in 0..3, representing $(1,i,-1,-i)$. These fresh marks are carried through all physical/graph coordinates. They provide relabeling covariance in law, not additional independent graph evidence.

## 3. Exact algorithmic policy

Define the graph cut by summing weights across a balanced subset and its complement, once per edge. At case setup B draws one uniform vertex priority permutation. This same rank fixes all B ties and complement orientation throughout that case.

Canonical orientation of a subset is the member of $\{X,X^c\}$ containing the rank-zero vertex. Descent first canonicalizes, and canonicalizes each accepted state and its return value, using the exact identity C(X)=C(Xc). Thus with a fixed case rank, Q(X)=Q(Xc); no independent complement quench or free better-of-two is performed.

Each reset draws a uniform eight-subset WITH REPLACEMENT across resets, canonicalizes and scores it, then performs at most TWO complete best-one-swap scans. A scan evaluates all64 inside/outside swaps, in rank order. Each candidate receives an actual integer cut, record and paid-best credit; do not count a delta never evaluated as a score. Choose the lowest-cut strict improvement; ties use (rank(removed),rank(added)). Stop early on a completed scan with no improvement. A cap without a final no-improvement scan is not a certificate of local optimality.

The common proposal quench Q performs ONE such complete scan on the canonical decoded proposal. It returns the **BEST SCORED candidate including its input**, never merely the last tested candidate. Repeated subsets are scored again; no cross-attempt score cache is gifted. Every scored candidate, whether selected, rejected or only a neighbor, contributes to B's all-paid best. Chain/all-paid best ties retain the first actual discovery in event order; no new candidate is generated to break a tie.

For each of the sixteen steps:

1. Compile the P82 receiving W from current G,S and fresh marks. F4 has literal exact entries ±1/2 and ±i/2, not exp evaluated at multiples of pi. Build Q_rs and A=F4 diag(odds) F4-dagger, then J_rs=Q_rs|A_rs|². Initial phases are the four recorded roots. In sweeps0,1, update r=0,1,2,3 sequentially using H_r=sum_(s!=r) J_rs exp(i phi_s), in increasing s order; keep on exact floating complex zero, otherwise set atan2(Im H,Re H). The general compiler MUST branch analytically on exact eta=0: set A=rho*I, J=H=0 exactly and retain the initial roots; never feed a floating matrix-product residue into arg. That branch is required in qualification, not an added main arm or a post-outcome tolerance. No objective-cut oracle or optimal mask enters this compiler.
2. Draw the eight split coins in port order using independent uniform integers 0..denominator-1 compared to the stated rational numerators. This gives R; archive all eight integer draws. W is compiled BEFORE observing R. Never recompile from the lucky active subset.
3. Sample the full eight-mode receiving count conditional on sorted R-port indices. Restore kept counts to 1 outside R and0 inside R. Validate/retain the complete16 counts and their vertex mapping, including all zero entries.
4. Let B_y be the receiver support. Fill r-|B_y| uniformly from sorted T minus B_y using the repair stream's permutation prefix. If required size is zero or equals the entire remaining set, the set is deterministic and no repair RNG is invoked. Archive the seed and whether it was used. Score the decoded eight-subset, run Q, and record all its scores.
5. Replace current S by the canonical Q result only on STRICT improvement over current cut; on equality hold the old current. Update chain-best and all-paid best independently. No Metropolis/Gibbs claim, favorable seed selection or reset to the global paid best.

Each chain starts with its own scored reset and its own chain-best; duplicate starts remain. Final case result is minimum cut across ALL actually scored B candidates in all resets/steps; report raw proposal means, Q-best means, three own-chain gains and current/best distinctions separately. Normalized means use exact Fraction(cut,total_edge_weight), with the identically zero graph assigned normalized value0. A cut found by warmstart or quench is classical discovery, not an optical improvement. r=8 has the complement's raw cut; any subsequent Q improvement is also available from the canonical original input.

## 4. Physics engine: fixed choice and limits

Main uses **serial local Clifford2017Backend.sample()**, never samples(count), Processor, remote client or Naive full-law enumeration. Use immutable P43.make_optical_sampler(W, sorted_R_ports, "bosonic", native_seed) for r>=1. It constructs a NEW receiver factory each attempt, sets circuit then source, and returns a single serial sample. Any fallback flag is failure. There is no backend fallback or count retry.

For r=0 return the deterministic eight-mode zero receiver count without a native call. It still consumes one modeled full eight-photon source attempt and receives the same paid scoring/quench policy. Every r=1..8, including rare r=8, gets its registered native request. A malformed dimension, negative/noninteger count, total different from r, nonfinite compiler value or native exception is first failure; it is not a fabricated loss model or a resampled shot.

This factorization changes simulation workload only. It preserves
$P(R,y)=\prod_Rp_i\prod_{\neg R}(1-p_i)|per W[y,R]|^2/\prod y_a!$.
All eight photons, including those in the kept bank, are counted in modeled physical resources. The result is a seeded floating local-backend simulation, not exact rational sampling, physical replication or a certified TV approximation.
Main retains every zero component of each observed count vector; it does not enumerate unobserved occupations or claim to have certified their structural zeros.

Text-only inspection pins Perceval1.3.0/exqalibur1.4.2: Clifford's set_circuit delegates unitary, set_input_state delegates source, sample delegates one serial count; Naive deterministically computes a permanent amplitude divided by Fock factorials. Main deliberately avoids all receiving Fock tables. Current helper hashes are P43 b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777 and P50 6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86. Installed Clifford/Naive .py hashes are 8dad1b8f389f346bde1b902f21d74e1466eabb258aeb0e92f827ff745d27329b / aaa26604b0866eeba61aaca80e83afe4df689711f4ce3bf965db1da74314ef4d. No import or API call was used for this inspection.

## 5. Paid classical time: the primary gate's actual quantity

For each case define G_case as the SUM of measured, disjoint B **wall-time** spans for:

* private graph copy/validation/degree setup; own F4/profile/A cache construction; priority, reset seeds/RNG/start generation and all warmstart scores;
* every fresh mark, Q/J/phase/W compilation, angle handling and runtime matrix guard; split coins and source/routing request; the P43 factory pre-clock prefix;
* count validation/mapping, support/repair, raw scores, canonical orientation, Q scans, acceptance, current/chain/global-best updates and case algorithm finalization.

The case owns a new algorithm cache; none is shared free across anchors. There is no parameter-selection stage to omit. Recompute actual role-seed derivations inside the paid policy even if integrity metadata were precomputed separately.

Record factory_total_wall and its returned backend_setup_wall nested inside it; require 0<=backend_setup_wall<=factory_total_wall. Only the difference is paid prefix. Its CPU split is UNKNOWN/None, not inferred. Exclude the returned native/backend setup wall and the separately wrapped sample-call wall from G_case, recording both CPU and wall separately. r=0 has zero native spans. Native imports/configuration, synthetic graph generation and evidence serialization are separately timed and excluded. All still count toward the runner's total resources.

Every paid component has an owner and unique event ID, start/end clocks and duration; none overlaps another paid span. Reconstruct G_case exactly from that ledger, not from a nested residual. Record whole-run/case clocks, native simulation clocks and harness/IO separately. Numerical matrix guards used by the algorithm are paid. For this VETO ONLY optical preparation/routing/detection latency is assumed zero; no local sampling or import time is called a QPU clock.

## 6. Fixed from-raw modes and their individual allowances

Every mode receives the original raw graph, fixed public policy constants and its OWN seed, starts, priorities and setup. It receives no B incumbent, warmstart, port marks, phase cache, eigensystem or samples. Common warmstart/quench means the same recipe; each private arm recomputes and pays it. Future matched D arms may replay the registered reset recipe only with their own charged preparation.

For EVERY fixed mode separately, its full available CPU time is G_case seconds; do not divide by the number of modes. Measure the adapter's actual CPU before the solver boundary and give the solver max(0,G_case-adapter_CPU). Solver CPU begins before validation, copying, RNG or graph features. All actual control CPU/wall and overrun are retained.

Tier1 ALWAYS completes these four normal calls, in mode-major order:

* FAST_RANDOM on ER then RR, using immutable P50 initialization random;
* FAST_SPECTRAL on ER then RR, using immutable P50 initialization spectral.

Both have max_proposals=10000. P50 charges its own graph validation, preparation, complete64-delta first scan, annealing/descent/restarts and online snapshots. No B feature is passed. A normal guard return is preserved; a source exception is first failure.

After Tier1, if either ONE fixed FAST mode has a valid timely cached cut STRICTLY lower than B's all-paid best on EACH anchor, report DEV_REJECTED_FIXED_FAST. Other modes may not be chosen per graph. Do not run Tier2, D or species after this veto.

If no veto, but a FAST call lacks a timely complete first scan, has no timely candidate, or hits its work guard before its time allowance, report INCONCLUSIVE_FAST_ELIGIBILITY; Tier2 remains NOT_RUN. Otherwise Tier2 runs the following modes, each on ER then RR, each with its OWN WHOLE G_case allowance and10000 candidate/delta work guard:

| Mode | Fully specified policy until deadline/guard |
|---|---|
| RECIPIENT_FRONTIER | Own uniform start plus two-scan descent. Draw fresh portS and split R from the fixed profile. Enumerate all r-subsets of T in own-priority lexicographic order; score each X and pay Q on EACH. Credit every scored state. On complete frontier update current to its best Q endpoint only on strict improvement, then repeat. Partial frontier scores remain anytime evidence; do not call them a completed frontier dominance certificate. |
| PHASE_HYPERPLANE | Own start/descent. Recompute its own marks and two-sweep phase compiler. Draw theta uniformly in [0,2pi); choose a-plus iff cos(phi_r-theta)>0, with own rank breaking exact zeros. Remove four uniformly selected current vertices, score, Q, strict improvement update; repeat. No unbilled opposite hyperplane or phase portfolio. |
| CONTINUED_DESCENT | Own start; complete best-one-swap scans until no strict improvement, then own fresh uniform restart. Repeat, crediting all64 candidates per scan. This is the explicit zero-optics continued-search control. |
| MULTISWAP | Own uniform start plus two-scan descent. Cycle radii2,3,4; draw independent uniform removed/added subsets, score, Q and strict improvement update. After every12 completed kick proposals perform and pay an own uniform restart plus two-scan descent; repeat. |

All custom modes use their own fixed case priority, canonical complement orientation and BEST-scored Q. They check deadlines/remaining work before atomic scores and scans, cache each completed best mask BEFORE its timestamp, and never return a late overall best as an eligible prefix. Work guards count starts, actual cut queries and delta evaluations; they are guards, not equal-time score prices. Deadline-interrupted Q does not return a completed Q endpoint, though its fully scored timely candidates remain valid anytime discoveries.

A valid negative witness is an actual complete candidate snapshot with elapsed adapter+solver CPU<=G_case. Even a timely initialization can veto; a later work-guard stop cannot erase that cheaper observed witness. All four Tier1 calls must have returned normally and all96 B attempts must be complete before an accepted FAST veto. Absence of a winner under an early guard or late first scan is inconclusive. The same timely-witness rule applies to a single fixed Tier2 mode on BOTH anchors, producing DEV_REJECTED_FIXED_CLASSICAL; a first exception/resource failure takes precedence over any partial veto.

If no fixed-mode veto and any required control is ineligible, final status is INCONCLUSIVE_CONTROL_ELIGIBILITY. If all required calls are eligible and no veto, use STAGE1_REOPTIMIZED_D_SPECIES_REQUIRED. Neither status accepts a positive result. Reoptimized D/species, fresh seeds/relabels, held-outs and matched total physical costs require a separate future contract; they are not automatically launched.

## 7. Qualification: tiny, deterministic and before main

Qualification is a separate one-time execution AFTER source/test/card freeze and ROOT review. It draws NO graph, DEV start, PCG stream, native stochastic sample or RNG. Use hardcoded fixtures and scripted hooks only:

* Three deterministic Naive amplitude queries for the two-mode/two-photon HOM law, retaining20,11,02 including the zero.
* The K4 receiver/r2 PRE-QUENCH witness at phases0,pi/2,pi, with rho1/eta1/2 and a hardcoded one-edge receiving graph. Independent two-by-two Fraction/complex arithmetic reconstructs all six removed pairs, ten two-photon receiver occupations, repairs and the exact sector-mean difference -8/225 between phase difference0 and pi. This fixture uses its d2 probabilities1/3,3/5, repeated twice. Naive queries are only four-mode/two-photon amplitudes; no native eight-photon matrix/source is constructed.
* Enumerate the sixteen ordered D receiver draws and uniform repairs for a fixed removed pair; every one of the six receiver pairs has probability1/6 and every vertex inclusion1/2. Test r=0/full-complement deterministic branches without sampling.
* Verify the eta=0 analytic branch is exactly graph independent, with bit-exact zero J/H and unchanged phase IDs. For every 0<=h<=r<=K in a hardcoded small fixture, verify the Fraction identity binom(r,h)/[binom(K,h)*binom(K-h,r-h)]=1/binom(K,r). This proves that independent uniform receiver-port marks plus equivariant repair give a uniform decoded r-subset for every r when W is graph independent, regardless of its physical full-count law. It is the all-r B/D decoded-law null after marks; do not substitute a floating near-zero J test or a sampled approximation.
* Scripted counts/clocks verify all48-step/reset indexing, every scored-neighbor credit, fresh-current source refresh, Q best-vs-last and complement coupling, factory nested-prefix guards, native errors, timeline sums, adapter subtraction, late masks, same-mode/two-anchor veto, guards/output reserve and first-failure precedence. Full-size workflow fixtures use mocked compiler/samplers/scores; they do not compile a DEV optical matrix or evaluate a generated DEV graph.

All fixed native observations, including zeros/tiny values, must be archived in test properties BEFORE value assertions. Preserve earlier observations and actual repr on nonfinite/exception failure rather than JSON NaN. Naive absolute tolerance is2e-12,relative0; Fraction identities are exact. Runtime entrywise-max guards are max|W-dagger W-I|<=3e-12, max||W|²-1/8|<=3e-12 and max|V-dagger V-I|<=3e-12 for V=[C;iWD]; relative tolerance0. Fail rather than reorthogonalize. These guards do not certify a many-photon TV error or native implementation correctness. No stochastic Clifford canary is part of qualification.

## 8. Caps, evidence, input closure and authorization

Both prospective qualification and main use ONE worker, CPU60s, wall90s, environment threads1 and native maximum1. Set OMP/OPENBLAS/MKL/VECLIB/NUMEXPR/BLIS thread variables before scientific imports. Import exqalibur first, set Config.compute_max_thread_count=1, read back; import Perceval, read back again; verify after each case and at end. No samples(count), parallel pool or guessed native thread bound.

Logical workspace plan is at most256MiB, not an RSS guarantee. Main retains no full Fock table, only one active receiver, one control trace at a time and streamed records. Each control has at most10001 checkpoint records; two-byte little-bit membership masks suffice at n16. Trace/export limits do not expand the10000-work guard.

Scientific output cap is32MiB UNCOMPRESSED, no gzip/zip, with1MiB reserved for compact first-failure/summary records. Runner log cap4MiB. Guard each serialized append and final summary before writing; never duplicate complete traces in summaries. No timing benchmark was performed to justify these caps; resource failure is inconclusive, preserved, and never followed by a cap increase or retry.

Proposed main output is experiments/P82a_dev_veto/run_001/data with metadata.json, graphs.json, B_ER.jsonl, B_RR.jsonl, paid_ledger.jsonl, controls.jsonl, summary.json and failure.json. Control records carry mode/case IDs, compact masks, exact cuts, CPU/wall checkpoint times, guards and online eligible index; no late-prefix reconstruction. B records include all seeds/marks, compiler phases/J/H, requested R, native source/full counts, repair and every scored candidate, current/chain/global best, counts/photons and disjoint timers. Raw r-histograms include all nine bins even if zero. NOT_RUN controls receive explicit reason metadata, not fabricated empty successful traces.

First failure flushes completed events and the pending/failing payload, then stops without retry, with INCONCLUSIVE_FIRST_FAILURE. Resource/hard-kill manifest status is authoritative and means INCONCLUSIVE_RESOURCE_FAILURE; a partial B/control panel cannot become an accepted veto. Summary positive_accepted is ALWAYS false. Ties, no optical gain, zero macro moves and every unfavorable outcome remain possible and retained, never reasons to redraw a graph/seed. Every raw outcome is sealed before interpretation; no C*, optimum, mask, paper, credential, QPU or held-out artifact is read or written.

Implementation must later freeze research/P82a_split_scatter_veto.py, tests/test_p82a_split_scatter_veto.py, a literal JSON spec mirroring this card, and separate v2 qualification/main contracts. Their complete input lists must include this card/design, source/tests/spec, immutable P43/P50/API card, both runner contracts, AGENTS.md, pyproject.toml and requirements-research-lock.txt; pin the actual installed critical backend files, native extension/package versions and interpreter provenance. No completed binding is claimed while those files do not exist.

Use the persistent interpreter /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python and the installed Mathbox v2 runner in the reviewed worktree, with the source/spec/output argv frozen in those later contracts. Tests must use their executing interpreter rather than hardcode this Mac path into portable fixtures. No source override, backend switch, arm switch, hidden canary or automatic follow-on run is allowed. This document freezes the prospective decision rule only.
