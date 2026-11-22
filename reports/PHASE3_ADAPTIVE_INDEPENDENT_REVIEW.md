# P34 independent proof review: adaptive replacement

## Original verdict, retained

**Primary verdict on e201f1c: correct only after a stated restriction.** The
deterministic error bounds e_t must lie in [0,1] before forming the product.
The literal original statement does not impose this condition and admits the
counterexample below. With that restriction, the transcript, success-event,
history-sensitive E_B, stopping and classical-cost conclusions follow under
the contract. No quantum advantage or new coupling theorem follows.

Original target commit: `e201f1c337cb780225bdcdd0a806cfd7d20d2fe2`.
Original proof SHA256:
`0f19135853b61494210067a4d10a5f6bcec1c40172797cc939f7117dd01453ef`.
The exact original file in this isolated sparse worktree was not edited.

The later correction at `b3b0219c81fa5cfb1c6807b57ff24361bde936cc` has a
separate addendum at the end. Its acceptance does not replace this first verdict.

## Claim card and independent reconstruction

Fix a graph, an identical classical randomized policy and a deterministic
maximum T on all physical attempts, including training. Each attempt prepares
fresh distinct singly occupied input orbitals, applies the selected passive
lossless interferometer and measures its complete output occupation. State,
random bits and actions can be included in the history. At the **same** history
h, the two eligible kernels are b_t(.|h) and d_t(.|h), where d_t scatters the
photons independently through the same occupied columns. The reference policy
uses its own preceding outcomes; it is not supplied the bosonic trajectory.

Assume pointwise TV(b_t,d_t)<=epsilon_t(h), 0<=epsilon_t(h)<=1. Uniform
e_t in [0,1] give transcript TV at most 1-product_t(1-e_t), hence at most
sum_t e_t. Alternatively it is at most min(1,sum_t E_B epsilon_t(H_(t-1))).
An identical final decoder or discovery-before-exhaustion event inherits the
absolute probability bound. No statement about accepted-shot budgets, ratios
of rare probabilities, or an unbounded stopping time is being audited as true.

The reviewer `/root/physics` did not author this proof. It was read raw and
the coupling was reconstructed from its marginals; the author's status was
not used as evidence. The reviewer previously audited the density dependency,
whose exact unchanged source hash here is
`7b2bee10ab5a738dfdcd16d657409be5eebdf7745b19a0bba91aace62a13e61c`.
That is a shared dependency, not a second independent review of density.
No production source, proof, manuscript, model service or QPU was touched.

## Smallest counterexample to the unrestricted product

Take T=2, m=k=1, V=(1) at both attempts, with a deterministic policy and no
stopping. Both output laws are the same point mass, so every epsilon_t=0 and
transcript TV=0. Deterministic e_1=e_2=3 dominate these epsilons, as allowed by
the original literal wording. Its product right side is

    1-(1-3)(1-3) = -3.

Thus the displayed inequality would require 0<=-3. This is a valid physical
instance and does not rely on numerical precision, nonorthogonal frames or a
failed density hypothesis. T=1 does not give this defect. The minimum repair
is e_t in [0,1]; a supplied nonnegative upper bound larger than one can be
replaced by min(1,e_t), which still dominates epsilon_t.

## Dependency graph and obligation matrix

The arrows are: normalized per-attempt Fock laws -> common-history local TV
bound -> local maximal coupling -> first-mismatch hazard or dominated prefix
submeasure -> transcript TV -> common postprocessing/success event. Fresh
inputs and absence of quantum memory are the physical bridge to the stated
classical kernels. The density theorem supplies an optional sufficient local
epsilon; it is not needed for the abstract coupling implication. The primary
source below supplies local coupling, not the whole adaptive photonic claim.

| Obligation | Original status | Reason |
|---|---|---|
| Deterministic e_t range | Failed | Physical counterexample above |
| Local maximal coupling with correct marginals | Passed | Explicit overlap and residual construction |
| Adaptive product bound once e_t in [0,1] | Passed | Conditional hazard, without independence assumption |
| E_B variant | Passed | Equal-prefix submeasure dominated by the full B marginal |
| Classical actions and random policy bits | Passed | Shared randomness until mismatch; state included in history |
| Stopping and absorption | Passed | Common stopping decision before mismatch; no new error after stopping |
| Success event at equal maximum attempts | Passed | Event difference bounded by transcript TV |
| Density dictionary and total-error condition | Passed | Exact local bounds, all positive rows, uniform error control |
| Classical sampler cost from supplied V | Passed in stated arithmetic model | No frame-building or exact-expectation oracle made free |
| Finite numerical density values as rigorous epsilons | Excluded | Proof explicitly requires separate numerical/error budget |
| Hardware advantage, wall-clock speedup, rare-event ratio | Out of scope | Not established by the theorem |

### Coupling and adaptive product, reconstructed

At a common history h put r_t(x|h)=min(b_t(x|h),d_t(x|h)). Its mass is
1-eta_t(h), where eta_t=TV(b_t,d_t). With that probability choose the same
outcome from normalized r_t. Otherwise choose outcomes from the two residual
laws. Their supports are disjoint. The mixture has exactly the b and d
marginals, and conditional mismatch probability eta_t. At eta=0 match always;
at eta=1 use the residual laws only. There is no division-by-zero obligation at
these endpoints. The construction is a proof device, not a computational demand
on the distinguishable simulator.

Let tau be the first differing outcome or action. Couple the policy's random
bits identically before tau. Equality of the complete state then implies the
same selected frame, action and stop decision. Thus

    Pr(tau>t) >= (1-e_t) Pr(tau>t-1).

All factors are nonnegative precisely when the missing restriction is imposed.
Multiplication gives Pr(tau>T)>=product_t(1-e_t). After the first mismatch
any marginal-preserving joint evolution is allowed. Complete transcripts
differ only if a mismatch occurred, so their TV is at most Pr(tau<=T).
No independence of the mismatch events or of the selected frames is used.
The union bound gives the sum version. For T=0 both transcripts are the shared
initial state; the empty product and sum give zero error as required.

### Why the B-expectation is legitimate

Let nu_(t-1)(A)=Pr(H^B_(t-1) in A, tau>=t) under this joint law. It is a
subprobability measure and nu_(t-1)(A)<=Pr_B(H_(t-1) in A) for every A.
The probability of first mismatch at time t is

    integral eta_t(h) nu_(t-1)(dh)
      <= integral epsilon_t(h) nu_(t-1)(dh)
      <= E_B epsilon_t(H_(t-1)).

Summing the disjoint first-mismatch events and capping by one proves the
claimed variant. The B-prefix law here is unconditioned. Replacing it by a
law conditional on survival, by arbitrary visited-history averages, or by
expectations under a different policy would require another argument. None of
those substitutions is present in the target. This proof also explains why
rare high-error histories cannot simply be omitted.

### Stopping and success events

A stopping time bounded by T is represented by an absorbing symbol. While the
histories agree, their stop decisions agree. Both subsequent conditional laws
are then the same point mass; their local TV is zero. A final decoder, possibly
randomized with identical conditional law, is common postprocessing, so an
event has probability difference at most transcript TV. Discovery before T,
the padded stopping time itself and output partition are all such functions.
An event defined by different criteria in the two runs is not common
postprocessing. The theorem compares the same deterministic physical-attempt
cap; stopping may of course give different realized numbers of attempts after
the histories diverge. Conditioning on collision-free acceptance or success
is not covered by this absolute unconditioned statement.

### Density substitution, access to V and cost

At every eligible history the supplied frame must satisfy the exact density
theorem's hypotheses. The density floor covers every positive row, and the
refinement requires M<c^2/2 before using the lower quadratic root. Fixed c
justifies the sharper leading term; it is not uniform over vanishing c.
For the coarse sequence condition set r=max_(t,h) M_t(h)/c_t(h). If Tr->0
with T>=1, then r->0 and the coarse envelope g(r)=r+O(r^(3/2)) tends to zero
uniformly in m,k. Thus T g(r)->0, as asserted. This does not certify a
uniform hypothesis merely from sampled frames.

Given V, each occupied column defines a normalized categorical law q_ia.
Sampling one output per column and forgetting labels exactly realizes d_t.
A linear scan uses O(m) arithmetic per draw, hence O(mk) per attempt; alias
preparation uses O(mk), with O(k) subsequent draws for a reused frame. These
are arithmetic/random-sampling-model costs, not bit-complexity or measured
runtime bounds for exact real numbers. Computation or storage of V, policy
optimization, scoring, preprocessing after a frame change, and numerical
sampling error remain additional costs. In particular, hardware that supplies
an unknown V does not automatically supply its classical description. The
proof explicitly says "Given V" and charges frame construction; there is no
unconditional efficient simulation claim for an inaccessible frame oracle.
Fresh state preparation and full measurement matter: a quantum-memory policy
cannot be represented by these kernels without a new physical argument.

## Primary-source check

The existing authorized read-only cache was used, not an unverified web
snippet: Levin and Peres, *Markov Chains and Mixing Times*, second edition,
with contributions by Wilmer, author-hosted [PDF](https://pages.uoregon.edu/dlevin/MARKOV/mcmt2e.pdf).
Checked locally on 2026-11-22. The file identifies itself as the second edition;
its exact bytes are pinned below rather than assuming a dated website version.

| Cached artifact | SHA256 |
|---|---|
| `mcmt2e.pdf` | `9ef39f9467d9647ff3f5e8747b9ce24b7a90d13be2f8156fbd827b95b661a772` |
| PDFKit extraction `mcmt2e.txt` | `92cae05daaa965e8f4551f99d7a7d880fb693c5bb1a5e9f662017ee0fdf800e0` |

Source metadata, title page, definition (4.1), Proposition 4.2 and the complete
proof of Proposition 4.7 / Remark 4.8 were read, including the residual mixture.
Section 4.1, printed pp.47-48, identifies event-supremum TV with half the L1
distance. Section 4.2, printed pp.50-52 (PDF pages66-68), proves the minimum
coupling mismatch identity and attainment by matching the pointwise common
mass. Its distributions are on a finite state space; each photonic outcome
space here is finite. No stationarity, reversibility, irreducibility or Markov
mixing-time assumption is needed for this proposition. Augmenting by history
does not make those unrelated assumptions necessary.

Notation translation is mu=b_t(.|h), nu=d_t(.|h), with the same halved-TV
convention. **Source implication: verified** for each local coupling. The
adaptive product and E_B result are a **formal corollary not stated** in this
extracted proposition, and were checked separately above. Cache hashes prove
identity, not correctness; the content check is the separate extraction and
translation just described. No broad novelty search or fresh HTTP retrieval
was performed. The author-hosted metadata provenance is inherited from the
existing cache; the report does not claim a newly authenticated network fetch.

## Independent finite checks and reproducibility

The retained code reconstructs all ten complete two-photon Fock probabilities
of a four-mode rational-rotation family directly from amplitudes, with exact
`Fraction` arithmetic. It enumerates a three-attempt adaptive policy: a fair
classical policy bit is included in the transcript; later mixing depends on
whether the preceding outcome collided; outcome (0,0) triggers absorption.
All random branches are enumerated, so no Monte Carlo seed or favorable sample
selection occurs. This gives 1,640 padded transcripts.

It constructs the equal-prefix measure using min(b,d), checks domination by B,
both transcript bounds, and a stopping-success event. Results:

- Exact transcript TV approximately 0.11425517644357416.
- Exact sum of B-expected local TV errors approximately 0.14768785703557155.
- Both product and expectation inequalities pass as rational comparisons.
- The initial-only control has zero first-attempt error but two-step TV
  7200/28561>0; an initial circuit alone cannot certify the adaptive policy.
- The missing-range counterexample is preserved with actual TV0 and RHS-3.

These local epsilon values are exact one-step TVs, not the production density
function's floats. The check tests the abstract adaptive implication and
physical interpretation; it is not a universal proof or a full evaluation of
all density certificates. The run uses under 0.1 CPU seconds per invocation;
total audit calculations are below the authorized 60-second CPU cap. A
provenance-only script adjustment declared output paths and regenerated the
same exact laws; the final manifest validates against the unchanged proof and
script. No production tests needed rerunning for this report-only change.

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python experiments/P34_independent_review/check.py
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py experiments/P34_independent_review/manifest.json --root .
```

Final manifest status: completed; validation passed. Python 3.11.15, standard
library exact arithmetic. Full rational transcripts are retained separately.

| Output | SHA256 |
|---|---|
| `check.py` | `5fa30ae63a2a30c0916d5e422fec60f3cd71f327bbc77213ca52966334788d75` |
| `receipt.json` | `ec8ac930aaec9530de57c5c29a47ebf4dc520a288e4ce18bd8de05101049a558` |
| `transcripts.json` | `b45db3993bae5d9fd40ef3a14a2eed90ba623d95d5c042d195249314155ce9e4` |
| `manifest.json` | `a24630e2296e073e8d2d1f6c0a5d5d146db74bffe5211c93e0fbc18410970141` |

## Separate correction addendum

After the missing e_t range was reported, the coordinator supplied commit
`b3b0219c81fa5cfb1c6807b57ff24361bde936cc`. The reviewer independently read
the complete corrected proof and its diff against e201f1c using Git objects;
the worktree's original proof was not replaced. Corrected proof SHA256:
`00d92f5551e30d167ef46ddb231a11c49a256bfcb3bb97e76bdf6fdf51985279`.

The only mathematical change explicitly restricts e_t to [0,1], clips supplied
nonnegative majorants before the product, and records the original T2/e3
counterexample. This suffices: clipping preserves domination because epsilon
is at most one, and every hazard factor used above is now nonnegative.
**Verdict on this corrected revision: proved as written**, under its stated
fresh-input, common-policy, finite-attempt and exact-local-bound contract.
This is a separate revision verdict, not a favorable rewrite of the initial
review. The unchanged exact finite experiment remains attached to e201f1c;
the corrected proof verdict rests on the reconstruction and diff, not on
silently relabeling an earlier computational manifest.
