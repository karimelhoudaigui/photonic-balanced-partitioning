# P42 independent physical reconstruction and finite replication receipt

## Outcome and provenance

**Finite numerical assertion passed at tolerance 1e-10**, not a universal or
interval-certified numerical proof. The single run has Mathbox manifest v2
status `completed`, exit 0, repository dirty=false, and freeze commit
`c4a178d7c9786d4e32d4c02b24dbed0abf2f7c87`. Base was
`525e2549907a478623df7c0e49190c423e5e8291`, worktree
`/Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication`, branch
`research/p42-replication`. The complete 42-case population and all four eta
values were committed with the code and contract BEFORE the first execution.
There was exactly one physical calculation, run_001; no failed run was replaced.

Independence boundary: this reviewer sent a first-quantization derivation to
the coordinator BEFORE reading the two P42 author proofs. The proof files were
then read and audited, before numerical code was designed. Their contents are
therefore NOT author-blind numerical inputs. However, neither the primary
`P42_loss_spectrum_probe.py`, its imports nor primary raw data was read, imported
or copied before the code freeze or execution. They remain unread at this
receipt. This code imports only standard library and NumPy; it does not invoke
production physics/Gram/noise code. There is no claimed bytewise reproduction
of primary raw results or comparison against primary samples.

This reviewer previously authored the project's noise/P40 components and
reviewed P33/P37. This new calculation does not silently become an independent
third-party validation of those authored components: none is imported here.

## Exact proof targets and independently reconstructed normalization

The following source hashes were read during the earlier proof audit and
rechecked in the isolated base checkout:

| Proof file | SHA256 |
|---|---|
| `theory/P42_threshold_loss_obstruction.md` | `01f98f59e975e783bfbb95bf2003fab435732797141bdb5196222dbd460aac4d` |
| `theory/P42_general_fock_loss_extension.md` | `c2bae66e8a69d194b3224741093afb84cdab0cbc4341a3e0674db561421736d0` |

The independent derivation first normalizes the ordered spatial state rho_N to
trace1 after tracing internal degrees. Its support consists of ordered words
with histogram s. Bosonic permutation invariance makes their diagonal masses
equal to1/d_s, d_s=N!/prod(s_i!). Tracing N-r particles gives a block at t of
trace d_t*d_(s-t)/d_s=prod binom(s_i,t_i)/binom(N,r). Multiplication by the
binomial probability of r survivors yields the unnormalized block trace
lambda_t=prod binom(s_i,t_i)*eta^r*(1-eta)^(N-r). Vacuum and all lost sectors
remain in the full distribution.

With arbitrary internals, lambda_t is a BLOCK TRACE, not necessarily an
eigenvalue. Its normalized block sigma_t has support Pi_t and sigma_t<=Pi_t.
For any rank-R output projector P, after the same U on every block,
x_t=Tr(P sigma_t) satisfies0<=x_t<=1 and sum x_t<=Tr(P sum Pi_t)<=R.
Consequently the probability is bounded by the R largest block traces, without
assuming that indistinguishability always increases probabilities. Counting
ordered surjections gives R=k!*Stirling2(r,k); symmetric compositions give
R=binom(r-1,k-1) only for the fully indiscernible spatial state. For PNR total
k only r=k contributes; for empty support only vacuum contributes.

**Analytic proof-review verdict on the above two hashes: proved as written
for their central caps and adaptive consequence**, with their physical reading
of uniform loss as internal-blind and identical photons as fully indiscernible.
The text's L=ceil(nQ/nC), nC>0, and separate nQ=0 case repair the missing
L>=1 condition found in the earlier claim card. The earlier L=1/6 diagnostic
refutes that unrestricted card, not these files. No cap applies to a
renormalized postselection law without accounting for its denominator/cost.
The cost and shared-front-end assumptions remain assumptions of the corollary.
The numerical experiment does not test adaptive best-cut search or hardware
costs and is not the proof of this analytic verdict.

## Implementation checks and complete finite coverage

The source amplitude is the normalized sum of all N! products of one-particle
spatial/internal vectors, including repeated factors for bunched sources.
The maximum source vector contains16^4 complex128 entries,1MiB. For each r,
amplitude matricization traces every internal factor and every lost spatial
factor by AA*. The program then applies U tensorpower r to the reduced density.
No global boson/distinguishable interpolation, permanent surrogate, probability
clipping, postselection normalization or primary probability implementation is
used. Complex internal amplitudes and their actual Gram matrices are saved.

All 42 source/unitary/internal cases were retained, giving 168 all-sector laws
and 2880 support/encoding checks. The configurations span vacuum, one photon,
distinct inputs and several bunched patterns; all details and two fresh seeds
2026112471/2026112472 are in `experiments/P42_replication/cases.json`.
Every possible output support is checked twice, threshold versus PNR exactly
its size. Input block traces come directly from the reduced density; ranks
come directly from ordered-word enumeration. Indexed-loss subset enumeration
and the product-binomial formula are cross-checked separately. Fully identical
and opaque internal cases are distinguished when selecting projector ranks.

Observed maxima, retained without rounding them to exact zero:

| Check | Observed residual |
|---|---:|
| Source normalization | 5.551115123125783e-16 |
| Source bosonic symmetry | 1.3877787807814457e-17 |
| Input-block trace normalization | 9.992007221626409e-16 |
| Coherence between different input occupations | 0 |
| Unitarity | 6.661338147750939e-16 |
| Output-sector trace | 1.4432899320127035e-15 |
| Loss-mixture normalization | 1.2212453270876722e-15 |
| All-photons-detected eta^N | 1.2212453270876722e-15 |
| HOM versus internal overlap | 3.3306690738754696e-16 |

The most negative probability cap margin was -1.1102230246251565e-16 for both
applicable rank models. Reduced densities retained a minimum numerical
eigenvalue of -4.1572301896365023e-16; this is a floating residual, not an exact
positive-semidefinite certificate. No output occupation probability was
negative in this run. All declared finite invariants pass 1e-10.

The predeclared bunched scope falsifier C037 is preserved:
four photons from one mode, balanced first two outputs, eta 0.1, gives
P(two clicks)=0.027087499999999994. The known-model prediction evaluates to
0.027087500000000264 and the cap 0.01 valid for DISTINCT input photons is
violated. This supports the need for the general-source extension; it does
not refute that extension. No N8 DFT/internal-species calculation was run:
that falsifier remains outside this finite validation. No unresolved run or
filtered case is omitted.

## Real execution, closure, budgets and immutable outputs

The actual runner command was exactly the command frozen in
`research/P42_replication_contract.md`:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication --contract research/P42_replication_contract.json --input research/P42_replication_contract.md --input research/P42_replication_contract.json --input experiments/P42_replication/cases.json --input experiments/P42_replication/ordered_replication.py --output experiments/P42_replication/run_001 --result experiments/P42_replication/run_001/laws.jsonl --result experiments/P42_replication/run_001/states_and_sectors.json --result experiments/P42_replication/run_001/summary.json --timeout 90 --max-output-bytes 33554432 --max-cpu-seconds 60 --max-threads 1 -- /private/tmp/pbp-clean-venv-20261124/bin/python experiments/P42_replication/ordered_replication.py --cases experiments/P42_replication/cases.json --output experiments/P42_replication/run_001
```

The input closure is exactly FOUR files: human contract, JSON contract, cases,
and executed code. The contract execution_artifacts list exactly matches the
runner's four --input paths. Their observed SHA256 before/after values agree.
NumPy2.4.6 and Python3.11.15 are the only non-system computation dependencies;
their versions are recorded. The installed runner SHA256 was recorded in the
frozen contract. The runner records no missing or invalid result.

The child reports CPU 0.36767 seconds and timed calculation wall 0.412158125
seconds; the runner measures launch-to-exit wall 0.721225 seconds. The child's
timing begins after NumPy import, while the enforced 60-second CPU limit covers
the entire child. Maximum RSS on this Darwin host was 43,810,816 bytes. Each
array is far below 64 MiB; largest source array 1,048,576 bytes. Total six output
files including logs and manifest occupy 983,225 bytes, below 32 MiB. One
sequential child ran under all six numerical thread variables set to 1. Darwin
has no supported sched_setaffinity here, so max_cores is truthfully null; no
hard CPU-affinity guarantee is claimed. Limits remain CPU60/wall90/threads1.

| Artifact | SHA256 |
|---|---|
| Frozen code | `2fe58ca0afe40e6847f83379a4474fd1b0f807beea1a944f823abc454dcb8aef` |
| Frozen cases | `298097eb997432c7b4e26056a71a2d45de67b6fca3303032213c79ee580a3c2e` |
| `run_001/laws.jsonl` | `658193e97b57d3869a92d3be8c53b4cf127a967c53e482e06c1f1c959826c61e` |
| `run_001/states_and_sectors.json` | `fe6819bcc9b7d8cd39706156c23dfd9c58174031d63e431c7cdd8b94174c4f6a` |
| `run_001/summary.json` | `0852350fbbe215e2e26efbb220a724a4881826f8d80ee5ab52ed0c38bdc74df1` |
| `run_001/manifest.json` | `a2172f769887317d61f742dc8d30b0f3422b6b07a9c5a568021f579d71138d72` |

Manifest validation was actually executed and returned a valid completed
evidence record:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py experiments/P42_replication/run_001/manifest.json --root .
```

A separate read-only stdlib receipt check confirmed exactly 168 distinct
(case_id,eta) rows matching the frozen Cartesian population, 2880 support checks,
all output sizes and SHA256 hashes above. No further physical run occurred.
The immutable run_001 directory must not be overwritten; future authorized
reproductions must use a fresh output path and matching result paths.

## Source overlap and limitations

The analytic ingredients are established:
[Ivan--Sabapathy--Simon, arXiv:1012.4266v1](https://arxiv.org/pdf/1012.4266v1),
section IV equations (4.6)/(4.19), gives Fock pure-loss binomial weights;
[Oszmaniec--Brod, arXiv:1801.06166v1](https://arxiv.org/pdf/1801.06166v1),
section II.C equation (9) and figure 5, gives the particle-trace loss model and
commutation with passive optics; [Marcus--Moyls, 1957](https://doi.org/10.4153/CJM-1957-038-6),
section 2, discusses Fan's maximum principle. These primary
passages were read in the preceding analytic audit. The internal-state
translation and adaptive composition require their own hypotheses, checked
above; those sources are not claimed to state this exact search corollary.
No exhaustive novelty search was conducted here.

Remaining limitations: finite small cases and floating arithmetic; sampled QR
unitaries rather than exhaustive unitary coverage; product pure internal input
vectors rather than arbitrary correlated internal states; the general proof,
not these cases, carries that broader quantifier. No hardware model parameter,
cost guarantee, calibration, advantage or global impossibility result follows.
No QPU, network processor, paid model or paper modification was involved.
