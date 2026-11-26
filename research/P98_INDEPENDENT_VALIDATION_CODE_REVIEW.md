# P98 exact hierarchy checker: independent static code review

26 November 2026. **Verdict: no material checker-logic blocker found; the active v2 contract MUST add mathematics.inputs, absent from the TEMPLATE. NOT EXECUTED.** This supports preparing the separate ROOT binding and its review, not authorizing a run. The program cannot accept an early successful pair as a complete PASS. The full pipeline still requires actual sealed inputs, a schema-complete active contract, the bounded runner and post-run inspection of its status and raw prefix.

## Exact source and review provenance

Read all three files,235 lines, at freeze `afefa4cb8074e8681b5f7eed17532b67a828f216`, parent proof `8a01023fcf55d06c4f421fe98d72154d4e39ff44`:

| File | Lines | SHA256 |
|---|---:|---|
| `research/P98_hierarchy_validation.py` |179|`52070f1a2ce7a92e9d32c299638aacdbae7037f6f2b95685a2697c2b56bd77ef`|
| `research/P98_hierarchy_contract_TEMPLATE.json` |27|`dd1bafbc6ccbba296143106bd2ce0077a42c91365f485e1d8f4d5f1d934f8fa1`|
| `research/P98_HIERARCHY_VALIDATION_POPULATION.md` |29|`d2a1ef81fadb4af8c103374c1962967858b12ace33e939bcec8fd9852b46519d`|

The mathematical comparison uses the exact160-line P98 proof, SHA256 `918d721f33a691351aa0ab2b4618f3fde0101341de87b719d2ecdfea23038c8d`, and my committed mathematical review `77811d2a950d6ca51805a9786bcf5d96b353d939`. This is a non-author source review with manual reconstruction, not a test result or independent numerical replication. No import, AST, collection, test, RNG, scientific arithmetic in software, native call, runner, QPU, paper, push, checkout or delegation occurred. Only this review is written in the clean reviewer tree based at77811d2; the five P96 code/test/contracts/population files remain unchanged.

## Population independently reconstructed

The13 P96 cases comprise one K0, one K1, one K2, five K3 and five K4 cases. Hence the all-degree pair count is `1+2+3+5·4+5·5=51`. Their dense raw support counts are167. Grouping coefficient counts by K gives `1+4+18+192+550=765`. R16 adds17 count states and17 degrees, hence289 coefficient rows. Totals are14 sources,184 moments/raw states,68 case-degree pairs and1054 coefficient rows.

| Population | Case-degree pairs | Dense coefficient rows | Moment comparisons |
|---|---:|---:|---:|
|13 sealed P96 laws |51|765|167|
| R16 closed law |17|289|17|
| Total |68|1054|184|

These counts include every zero-probability state and every coefficient with |n|>s for the particular pair being checked, whose q value must be zero. ALL degrees are tested regardless of the degree selected for a target error. The `support` set check enforces ALL occupations of total0..K. Duplicate states, incorrect dimensionality and total-loss mismatches are rejected; negative P or nonunit total P is rejected. Full support matters: omitting P=0 states would invalidate the signed L1 comparison. The case order and input/source dimensions are not selected from results.

## Moment and permanent paths

`moments(p)` computes the multivariate binomial moments directly from the whole supplied law. For K≤4, `from_transfer` separately enumerates distinct occupied-input subsets, expands a small permanent by permutations, squares its exact real value and divides by exactly one product r_j!. This agrees with proof(D) for these REAL rational cases. Repeated output rows are kept, so the bunching factorial is tested. It does not claim validation for arbitrary complex T.

The registered moments have degree≤K≤4 on this path. In addition, `permanent` rejects more than4 rows BEFORE constructing its permutation iterator. R16 takes the OTHER branch at every moment, using `d!binom(16,d)/64^d`; it never reaches the permanent helper, including at d16. Computing factorial16 as an integer is not enumerating16! permutations. No native backend, dilation, scientific package, stochastic primitive or16-photon full-mode state space is constructed.

R16 uses the registered scalar PGF `Σ_d d!binom(16,d)(z−1)^d/64^d`. Its17 coefficients are expanded exactly, and its moments are checked against the corresponding closed formula. This checks the high-degree transformation and repair on that known law; it is not an independent16-photon Born-law reference. P96 supplies the separately sealed small physical laws, without repeating their native validation.

## Hierarchy gates, negatives and degree choices

`coefficients(a,s)` implements the binomial change of basis with sign `(−1)^(|r|−|n|)` and only r≥n, |r|≤s. All computations stay in integers/Fraction; no negative exponent or floating shortcut enters that sum. The independent literal pointmass N3 at s2 gives `(1,−3,3,0)` and signed half-L1=4, checking both the sign and displaced low-sector masses.

Each pair computes α from ALL negative coefficients and repairs by `q^+/(1+α)`. This is the proven positive-part operation from the P98 proof and review, not clipping a noisy physical probability or silently normalizing a selected optical sector. Coefficient records retain the ORIGINAL signed q, repaired weight and P. Pair records retain α, signed half-L1, V expectation and each successive bound BEFORE their rejection gate.

The gate checks exact normalization of q and its repair and the chain

    repaired_TV≤signed_halfL1=E V_s(N)
      ≤2^s E binom(N,s+1)≤2^s(s+1)!e_(s+1)(c)≤2^sµ^(s+1).

The last expression equals the theorem's geometric bound without introducing a floating formula at µ0. `elementary(c)` allocates the extra zero coefficient e_(K+1), so the sK gate is defined, and `q==p` is explicitly required there. The V formula is evaluated only when N>s, preventing invalid negative-upper binomials. The repair's nonnegativity follows directly from exact max and α≥0; its normalization and nonexpansion are checked, with no extra factor2.

For R16 let `a_j=j!binom(16,j)/64^j`. Then

    q_s(s−1)=a_(s−1)[1−s(17−s)/64].

Thus q6(5)=−a5/32 and q8(7)=−a7/8 are strictly negative. The code's predeclared assertions test both and α>0. These are not post-hoc selected negative cells. ALL17 degrees are retained regardless of the chosen degree.

For µ1/4, degree8 has the certificate1/1024≤1/1000; degree7 gives1/512>1/1000. `choose` uses exact rational products and therefore needs no logarithmic rounding. µ0 chooses0; ε≥µ chooses0; ε0 chooses K except vacuum. The µ1/2 cases and physical X4 with µ1 select full K for ε1/1000, invoking explicit exactness rather than a false decaying geometric certificate. X4 is outside P96's nonnegative-q2 hypothesis but inside the general signed-hierarchy algebra; retaining and repairing its signed coefficients does not erase that earlier negative result.

## Binding, paths and immutable inputs

The TEMPLATE is passive and unbound. Its8 static paths match the source's STATIC tuple; all8 were confirmed tracked in the producer checkout. ROOT must integrate those actual frozen bytes before binding in ROOT. The source additionally requires all six specifically named producer archive paths as a subset of the descriptors: manifest, stdout, stderr and data/records/summary/failure. Extra provenance files are allowed.

The active binding lists unique descriptor paths, excludes its own descriptor/selfhash, and has an execution_artifacts list equal to descriptors plus binding itself. Therefore the minimum closure is15 files:8 static,6 producer and1 active binding. Every descriptor is checked for canonical relative path, nonsymlink ancestors, regular-file status, byte size and SHA256; the running source hash is checked separately. `input_records` is forced to the fixed P96 archive path. Descriptor values must match the actual files; placeholders or missing symbolic input files fail these checks.

**Required metadata correction before authorization:** the TEMPLATE mathematics object omits inputs. Reading the installed computation-audit `validate_manifest.py` confirms REQUIRED_MATH includes inputs and its validation requires an array (lines29–36,137–141,159). `run_experiment.py` checks only a mathematics object at launch; its final validate call precedes writing manifest.json. Copying the TEMPLATE verbatim could therefore permit the computation and then REFUSE to write a valid v2 manifest. ROOT must add an explicit mathematics.inputs array in the SEPARATE active contract/binding, alongside the actual execution_artifacts closure. This does not require altering the frozen checker or TEMPLATE. No validator or runner was executed to discover this omission.

The original seal field is checked as40 lowercase hexadecimal characters. The script does NOT authenticate that commit's Git blobs or producer manifest contents; the TEMPLATE explicitly assigns that verification to ROOT BEFORE authorization. Similarly, the actual literal matrices come from those bound P96 records, rather than a second matrix whitelist in this checker. ROOT's original-seal/blob verification must establish that they are the registered archive. The six files are hash-bound, but only exact_case_start/exact_raw payloads are parsed; P96 native payloads are not reinterpreted or rerun.

The lexical kind filter matches the frozen P96 writer's JSON formatting, which emits the expected spaces after colons. Its scope is that fixed archive, not arbitrary JSON reformatting. The source writes only the fresh P98 child directory and never opens a producer or qualified P96 code file for writing. An active binding has not been constructed or authorized by this review.

## Prefix failures, resources and interpretation

Literal, producer, case/moment and degree work is enclosed in the scientific try block after output creation. Each emitted record is flushed. Pair entry appends attempted BEFORE computation; finished is appended only AFTER all gates. A failure reports its phase/traceback and exits nonzero. FAILED_PAIR is attempted minus finished; NOT_RUN is the full fixed plan minus attempted. A failure during moment preparation legitimately leaves that case's degree pairs NOT_RUN. There is no fallback PASS or automatic retry.

Final PASS additionally requires finished to equal the ENTIRE ordered plan, plan length68 and coefficient_rows1054. Thus neither a successful literal nor the first selected/positive pair can conceal later failures. The184 moment comparisons are implied by the dense-support loops in every case; their rows must still be counted during post-run inspection. On complete success failure.json is JSON null; it is not an unrecorded failed check.

Profile/binding/path checks occur before the scientific try/output creation. Their failure can yield no three-file scientific receipt: the bounded runner's nonzero status/stderr/manifest must then be preserved and interpreted. A hard kill or incomplete receipt is resource/provenance inconclusiveness, not a counterexample to the hierarchy theorem. A source FAILED status also must not automatically be translated into a mathematical refutation without its phase and exception.

The source sets CPU30 and per-file FSIZE4MiB before scientific work. It enforces aggregate scientific bytes with a64KiB final reserve; the fresh runner must enforce wall60 and separate log4MiB and supply all six thread variables1. No extra worker, scientific import, hard RSS or affinity guarantee is implied. Output freshness plus the prior safe-input checks exclude existing-input overwrite. Final summary/failure writes are inside that newly created child only. Parent/runner integrity and actual post-run v2 hashes remain required.

**Remaining obligations:** complete mathematics.inputs in the active v2 metadata, ROOT's actual seal/blob and binding audit, explicit bounded-run authorization, then seal the new raw directory BEFORE reading outcomes and inspect every count/status/hash. No material numerical/algebraic checker blocker was found by static reading, but syntax/import/runtime success has NOT been tested. A future finite PASS would validate this deterministic construction in this range; it would not execute the categorical sampler, establish throughput or novelty, demonstrate graph optimization advantage, or open a QPU/paper gate. No change to the P96 package or existing scientific results is made here.
