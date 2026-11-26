# P145 — Non-author driver review before any DEV invocation

P66, 27-Nov-2026. Manual code review only: no import, AST, compilation,
collection, fixture, graph, numerical evaluation, native call or DEV execution.
P66 authored the kernel/tests, not ROOT's driver; this is a driver/API audit,
not independent physical replication or an uninvolved audit of the kernel.

Original target FULL168 lines: ROOT commit
dd41d63b3e92c653d68760e08aa1fe6f8511684b,
research/P145_run_declared_screen.py, SHA256
589d471a7073d435e11c93103400538f1eb3d830bf2bcb098bcd36704c4c1ec5.
Also FULL204 lines and full original-to-revised delta read at ROOT's supplied
pre-data working-tree revision SHA256
311dc813fedd7224e8d3dc6377e4a26e343d2a65a46ecac2ef9e0578c767c594.
Then FULL207-line final driver and FULL49-line hand tests read at ROOT commit
d14e1ea, driver SHA256
2f13709967ddbadae635d38bba55b934f89bbce45bb14042b658197520010b83,
tests/test_p145_screen_driver.py SHA256
940ce6fe5c6adcd903f8befbf7eb501de2405cc8b5ba54f1fd0c882295cdfba0.
Earlier revisions are preserved. ROOT owns the driver freeze.
Kernel target: 1f1b0500e0d6e676f8ec24dec278210b64ec8b80, 183 lines,
SHA6af77fadb703120130545779abba5c87618c1331c657e55dab66a95cb75c42bb.
Native finite-value guard is a separate PREQUAL test-only correction at
7ba7142f06534f001c9549608268644bf25b283b; tests119 lines,
SHA585c8ebb58a07eeed6c479ed89ed85596e17f3c495d0af9b87c697ec686397bb.
No test pass is asserted by these source identities.

## API and mathematical flow

All called kernel names and return schemas match the frozen kernel. Integer
20-gain dictionaries have exactly the required three-support keys. The first
three block vertices are always current, the last three always exterior;
source=(0,1,2), retained=current minus those first three, and gain(source)=0.
The local Hamiltonian is alpha*A+beta*diag(h), with SCALE=1. The driver performs
no further normalization: the active contract must state that literal scale.
This is a real symmetric six-mode floating exponential, not a new gate class.

Boundary fields include ALL vertices outside the block, using fixed range24.
For a support Y, local cut is sum_(i in Y)(sum_j Aij+h_i)-2sum_(i<j in Y)Aij
plus a constant. Subtracting the incumbent expression proves the implemented
whole-cut identity. No optimum cost, optimal mask, or isolated-six-mode trap
enters compilation. N24 and the public marks are fixed before optical scores.

Descent charges one initial query and 144 per full neighborhood. It refuses
a round that would exceed20,000 queries, so budget exhaustion is not a local
certificate. The cap is PER GRAPH. Counts are1+144r with r<=138, hence at most
19,873 descent queries and40 validation cuts per graph,39,826 overall. Reuse of previously computed incumbent costs is
explicit. Ties follow transported marks; improvements are strict.

The public block ignores scores. The near-barrier rule greedily takes three
disjoint low-delta pairs from the ALREADY paid final neighborhood, with public
ties. Sorting their vertices by marks fixes source/receiver order. Identical
public/near blocks are retained as duplicated rule contexts, not independent
graph evidence. A query-cap graph is retained and skipped, not replaced; the
other predeclared graph may continue, with overall INCONCLUSIVE status.

Each of five arms gets its OWN maximum over20 parameter settings. Four null
settings remain, and the kernel makes t=0 exactly identity. I3 is calculated
and labeled at ONE circuit, never from subtraction of differently selected
maxima. Eta1 results define the envelopes; eta.8 raw results are retained and
the eta^3 score identity is checked for every arm. This is the same comparison
under prescribed uniform loss, not a second claimed independently trained run.

All20 feasible costs are disclosed and credited to every arm. The exact-law
mirror preserves the complete20-CF+FAIL proposal utility with no survival
conditioning. Its assertion is an expected-utility identity, not a measured
sampling/wall-clock benchmark or executed adaptive chain. An improving block,
positive three-cycle contribution and strict proper-group survivor are distinct
diagnostics; none overrides the fully paid classical frontier or mirror.
optimizer_advantage remains false throughout.

## Pre-data corrections and residual recording obligations

The original168-line driver kept all data in RAM until finally, losing the
scientific prefix on a hard kill; ordinary failure also dropped graph metadata.
It lacked an explicit160-context guard. Both issues were reported BEFORE DEV.
The204-line revision streams and flushes graph setup, completed scans, blocks,
unitaries and completed optical contexts; failed summaries now retain graphs.
It checks four blocks/160 unique contexts/40 per graph-rule pair before PASS.
The completed stream is160*5*84=67,200 raw occupation probabilities, zeros
included. Failure or query exhaustion cannot become a successful prefix.

Both subsequent recording-order concerns are FIXED in the final207 lines:
candidate_check retains actual cost/formula operands BEFORE assertion, and
matrix_context retains U/parameters BEFORE P33. These change no population.
A hard kill inside a scan
can still leave an unfinished batch unrecorded; actual post-prefix query count
then must be treated as unknown, never reconstructed as an observed count.

The source enforces a7MiB combined JSONL cap plus1MiB combined final reserve,
and refuses optimized Python. CPU60/wall90, startup thread environment1,
fresh output parent, declared results, full dependency hashes, package/runtime
pins, zero retries and raw-before-reading sealing remain ROOT runner/contract
obligations. The guard is a byte cap, not a proved byte/runtime prediction.
No hard RSS/affinity or successful-run guarantee follows from this review.

The49-line tests independently check all20 cut differences on one HAND24 graph
and both public/paid rules under transported labels. Manual boundary fields
are exactly[0,0,-2,0,6,0]; v->(7v+5) mod24 is a bijection. No DEV generator or
optical evaluation enters these two tests. This is a hand algebra/covariance
check, not empirical fresh-graph relabel robustness or an optimizer comparison.

Verdict at SHA2f137099: STATIC ACCEPT; no unresolved mathematical, API or nominal
recording blocker found. This is not execution authority. Separate qualification
is planned as8 core plus2 driver tests; ROOT requires all56 native points and
zero skips, with the finite-value guard independently reviewed. Actual package,
environment and runner bindings remain required BEFORE the prospective DEV
screen. No result, novelty, hardware readiness, optimizer benefit or QPU gate
is established here.
