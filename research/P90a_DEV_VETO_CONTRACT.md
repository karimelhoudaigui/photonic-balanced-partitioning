# P90a prospective ideal K12/n24 DEV veto card

26 November 2026. **CARD ONLY: no implementation, qualification or main authorized.**
This is a changed source-bound nonflat mechanism, not a P82 rerun or a positive
claim. Broad Fock/cost-feedback and graph-exponential frameworks have prior art.
P90 source: c52afab, SHA b3c0b04c486f3368a0cbbc7e2030d8225d015f182cbfb00e0a9b63e0a0b2f173.
Exact math review:1412c9a, SHA ad2a473b7b37da806b7e327e07ca6273278dbbffd0f6cf5d271a99865589f4d5.
Literature note:3de2a0b, SHA fa1c2be4a2b148450653207befe4cd4647dfef10f1147b0d1b03ce978a94e831.
Those records remain unchanged. This card is prospective and knows P82's early
FAST-guard outcome; it is not a blind extension of that pilot.

## 1. Fixed population, hypotheses and limits

Use n24,K12; minimize C(X)=sum_(u in X,v outside X)w_uv for |X|=12. Trial input:
12 single-photon source modes and12 vacuum receivers; lossless passive evolution,
full24-entry PNR records and uniform collision completion. ROOT's public CEA
context(up to12 photons/24 fibres) is motivation only; no account/connectivity/PNR
or calibration is bound. P91's mean2% gives no norm bound; no loss decoder is defined.
This ideal first veto does not qualify Lucy/TGCC or authorize QPU access.

| Fresh unplanted case | Pinned NetworkX3.6.1 recipe |
|---|---|
| ER9002401 | gnp_random_graph(24,0.4,seed=9002401), no filter |
| RR9002402 | random_regular_graph(4,24,seed=9002402), no filter |

Canonicalize edges to sorted(min,max) pairs; own GEN/weights PCG64 supplies one
integer1..5 inclusive per edge. Never inspect an old adjacency, redraw, condition
on connectivity/quality or consult a known optimum/mask. Exactly3 resets×16 steps
per anchor:96 B attempts and1152 modeled injected photons if complete.
No seed digest, graph, probability, calibration or timing run was evaluated here.
Fix p=1/2, exponent scale t=1, warmstart2 scans, proposal Q1 scan; no grid/training.

Each separate qualification/main slot has CPU60s/WALL90s, one worker, env/native1,
log4MiB, scientific32MiB UNCOMPRESSED with1MiB final reserve, zero automatic retries.
Logical workspace plan≤256MiB on the ROOT-specified M2/8GB class is not an RSS or
runtime guarantee. No calibration supports these caps. Any resource failure is
inconclusive and preserved; neither grants nor caps are resized after outcomes.

## 2. Seeds, coordinates and the actual changed compiler

Root seed90026001. Literal role tuple:
`["P90a",90026001,caseID,arm,chain,step,role,index]`, unused fields -1, index0.
Compact ASCII JSON(comma/colon separators), SHA256; PCG64 seed=first8 bytes LE;
native seed=1+first4 bytes LE modulo(2^32-1). No digest is evaluated at authoring.
GEN uses weights; B uses case priority, reset_start(chain0..2), and per-step
portS,portT,split,native,repair. FAST_RANDOM/FAST_SPECTRAL each use one own control
role with chain/step -1. Archive tuples/seeds/unused repair roles. Check all
potential PCG seeds and96 native seeds for collisions before graphs; fail, no rehash.
Each actual algorithm rederives/charges its roles and uses private explicit PCG64
Generators, unaffected by Perceval's separate native/global seed bridge.

B owns one uniform case vertex priority/rank. Canonical X is X or X-complement
containing its rank-zero vertex; use it at resets, accepted states and Q returns.
Given CURRENT S and T=S-complement, let s_i,t_a be their rank-sorted orders.
Compute exact ell_v=degree_v-2sum_(u in S)w_vu and
`M[a,i]=ell_(t_a)-ell_(s_i)+2w_(s_i,t_a)`.
Materialize EVERY144 feasible canonical swap mask and integer cut C(S)+M[a,i],
in i-major/a-minor order, with all-paid/own-chain-best credit before continuing.
An inside×outside delta array must be TRANSPOSED to this T-row/S-column M.
These candidates do not update CURRENT S; only the later strict Q rule does.

Set `H=(M+M.T)/2+1j*(M-M.T)/2`, `d=max(1,max(abs(eigvalsh(H))))`,
`V=expm(-1j*H/d)` using pinned NumPy2.4.6/SciPy1.17.1. Archive M,H,eigenvalues,d,V
and actual rounded values. H is Hermitian; no favorable objective or optimum
chooses an angle. V need not be nonflat/nonmonomial on every graph; retain nulls.
Only after V is compiled draw independent uniform physical source/receiver
orders sigma,tau, then transport `W[a,i]=V[index_T(tau[a]),index_S(sigma[i])]`.
There is no extra sigma-dependence or recompilation after observing R.
Check finite values, max|V†V-I|/|W†W-I| and occupied-frame Gram for
`F_occ=[I;1j*W]/sqrt(2)`≤3e-12 absolute/relative0; fail, no reorthogonalization.
Flatness is NOT a main guard. Record a paid nonflatness/IPR diagnostic.
Draw12 independent uniform integer coins0/1 in port order; coin0 transfers.
Thus R is uniform conditional on r, but Y depends on the actual labeled columns
V[:,R]. This is source/receiver coupling, not classical steering of marginal R.

## 3. Source, repair, search and candidate accounting

Each reset draws an own uniform12-subset with replacement across resets,
canonicalizes/scores and runs at most2 complete144-neighbor best-swap scans.
Strict improvement only; ties use(removed rank,added rank); stop on a full
no-improvement scan. A cap without that scan is not a local-minimum certificate.
For r≥1 use a NEW immutable P43.make_optical_sampler(W,sorted_R_ports,"bosonic",
native_seed), one serial sample(), never samples(count), Processor or fallback.
For r0 use the deterministic zero receiver vector without native call; still
charge12 full-source photons. All r0..12, collisions, identities and zeros stay.
Restore kept bank(1 outside R,0 inside); require receiver12/full24 nonnegative
integer counts, sums r/12 and the explicit vertex map. Malformation stops, no loss fill.
Decode receiver support, then uniformly fill r-support_size from sorted unused T
using its repair permutation prefix; invoke no repair RNG for empty/all fill.
Score canonical proposal X, Q does ONE complete144-scan and returns BEST SCORED
including X. CURRENT updates only if C(Q(X))<C(CURRENT), equality holds old state.
Track current, own-chain scored best, endpoint best and global all-paid best
separately; all compiler/warmstart/Q scores count, ties keep first actual event.

All144 cut/mask entries in each M/Q batch must actually exist before its end
clock. Vectorized exact integer deltas+base cut and compact canonical uint32 mask
arrays are allowed; duplicates/repeated evaluations are retained. Batch best and
all-paid updates are prepared before clock; no invented per-candidate timestamps.
Audit JSON-dict construction/serialization occurs AFTER that clock, using only
those arrays; no new scored cut/mask may create a witness. Independent later
scalar checks validate rather than repair/select a better candidate. This
implementation obligation requires independent source review before execution.
Full compiler features/candidates are exposed in raw records and to the design
of classical controls; none is free setup or a claimed optical discovery.

## 4. Exact grant and four independent from-raw controls

Per case G is the sum of disjoint B paid WALL spans: own raw copy/check/degrees,
priority/reset/RNG/warmstarts, every144-M batch/H/eigen/expm/guard/transport/split,
factory residual below, count checks/repair/raw/Q scores/current/bests/finalization.
Graph generation(problem input), imports/native simulation and audit JSON/I/O are
separately timed/excluded from G but included in global caps. Optical latency is
assumed ZERO only for this favorable-B negative-first proxy, not measured QPU time.
Observe factory outer CPU/WALL; identify its P43 REPORTED_DURATION(setup WALL,
CPU/endpoints null, helper hash). Paid DURATION_DIFF=outerWALL-reportedWALL has
both refs/null endpoints/unknown CPU; require0≤reported≤outer, no clip/doublepay.
Record serial sample CPU/WALL separately. No complete B CPU is inferred from G.

Always run FAST_RANDOM/ER,RR then FAST_SPECTRAL/ER,RR with immutable P50
solve_from_raw, each receiving its OWN WHOLE G, own raw setup/start/priority/seed;
no B incumbent, priority, M, cache or optical samples are gifted. The algorithm/
features remain public; future identical-feature baselines recompute/pay them.
Measure direct adapter CPU/WALL; helper CPU budget=max(0,G-direct_adapter_CPU).
Archive typed observed outer/direct records and P50 REPORTED_DURATION CPU/WALL
with null endpoints/hash. Delta=outer-direct-helper_compute in EACH clock is
finite/nonnegative without clip. Select only LAST chronological preclock cached
cut+mask satisfying direct_adapter+Delta+checkpoint≤G on BOTH CPU and WALL.
Preserve direct diagnostic results, late snapshots and exact first-scan timing;
never reconstruct a late best or treat CPU-only flags as a WALL certificate.

P82's known10k early guards motivate a prospective work guard1,000,000 here,
not a rescue of P82 or a timing extrapolation. Text inspection of P50 shows n24
epochs192/chunks32/scans144. Pair cheap restart/perturb checkpoints with the next
144-scan except at termination; initialization/setup/final partial events give
trace count≤floor(work/32)+4≤31,254. Assert40,000 exported-checkpoint cap; never trim.
Six Python lists/packed masks plus export arrays get a64MiB logical workspace
allowance, one control resident; native-private allocations/RSS are not certified.
Raw traces use compact column arrays, stage codes and3-byte little masks, no
per-checkpoint repeated dicts or summary duplication; an80-byte/checkpoint plan
gives≤3.2MB per cap-sized trace. Enforce total32MiB rather than assuming this plan.

## 5. Fixed decision, qualification, evidence and later gates

Exceptions/output failure: INCONCLUSIVE_FIRST_FAILURE; resource/hard limits:
INCONCLUSIVE_RESOURCE_FAILURE. Retain prefix/null/NOT_RUN. For all96 B+4 normal
FAST returns, a call is adequate only with a dual-timely candidate/complete first
scan and no early work/trace guard. Any inadequate required call makes the panel
INCONCLUSIVE_BASELINE_ELIGIBILITY, regardless of appealing partial results.
If all four are adequate and B fails C_B<C_FAST in ANY named mode/anchor,
return NO_POSITIVE_SIGNAL. This refutes a necessary gate, not a universal REJECT
or a free per-graph portfolio. Only strict C_B<C_FAST for EACH mode on BOTH
anchors yields FOLLOWUP_REQUIRED. positive_accepted is ALWAYS false.

Mandatory qualification after source/card review: tiny independent cuts/144-mock
batches, H/unitarity/transport, all-r count/repair/current/clock/failure fixtures;
flat F4[a,j]=i^(a*j)/2(i imaginary) r2 inclusion/uniform-R null; toy(6): V=H2⊕I2,
H2=[[1,1],[1,-1]]/sqrt(2), sole edge s2--t2, p.5: B-minus-D=-5/192 and
B-minus-group2=0 on all16 R(including013)/fills; group2 advantage gate MUST fail.
Exactly254 planned deterministic Naive queries:3 HOM +6R×10outputs(flat K4/r2)
+191 nonempty toy points(4×4+6×10+4×20+1×35); vacuum exact, no native call.
Max4 receiving modes/4 photons; archive all observations/zeros/errors BEFORE
assertions, abs2e-12/rel0. No real K12/native stochastic/DEV/RNG or role-hash canary;
full96 workflow uses mocked compiler/scorer/factory/RNG/clocks. One reviewed batch,
no automatic retry; main is a separately authorized slot with a predata checker.

Freeze implementation/tests/literal spec/qual+main v2 contracts and full input
closure(above P90 records/card, AGENTS/deps/lock, immutable P43 b0507d36/P50 6def5c0f
+API card, installed critical sources/native/package/interpreter pins) before
any import/AST/collection/test. Set env/native1 before scientific imports and
read back after imports/cases/end; persistent CLI interpreter, portable fixtures.
Main raw metadata/graphs/B_ER/B_RR/paid_ledger/controls/summary/failure live under
experiments/P90a_dev_veto/run_001/data; append-exclusive, guarded/pre-sized final
reserve, seal raw BEFORE interpretation, then separate receipt/independent audit.
Record13-bin r histograms, all counts/marks/rounding, raw/Q means, accepted steps,
compiler-only discoveries and all-paid curves. Questions are useful coordinated
raw moves and strict first-gate performance, never significance/advantage from96.
Later mandatory: reoptimized D; species≤3/exact low-r; intensity/routing/bunch/repair;
compiler-only/full-feature high-order feasible/frontier; projection-DPP |det V[Y,R]|²,
with own reoptimized V/parameters and paid setup/QR/leverage(exact sampler needs review);
fresh relabel/seeds/heldouts/replication. None is implemented or automatically run.
