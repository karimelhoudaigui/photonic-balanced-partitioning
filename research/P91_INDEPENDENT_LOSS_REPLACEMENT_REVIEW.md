# P91 independent exact-source proof audit

26 November 2026. **Primary verdict: proved as written**, under the stated
known-CF-source, passive-vacuum, certified spectral-loss and measured/reset
observation-history hypotheses. This does not establish a calibrated Lucy
claim, finite-bit simulator, measured cost advantage or optimizer obstruction.

## Claim card and reviewed revision

For a known collision-free k-photon input in distinct occupied modes A,
let T be a finite passive transmission contraction with vacuum environment.
For a certified `||T||op^2<=eta`, `0<=eta<=1`, and integer `s>=0`, P91
constructs a normalized whole-attempt replacement Q of the complete raw PNR
law P with

    TV(P,Q) <= Pr[Bin(k,eta)>s]
            <= min(1,binom(k,s+1)*eta^(s+1))  when s<k.

The last bound is zero for `s>=k`. A common decoder contracts TV. A fresh-shot
adaptive observation protocol has transcript error bounded by the sum of the
true-process expected conditional tails over a bounded number of attempts.

Exact source: `theory/P91_INDEPENDENT_LOSS_SECTOR_REPLACEMENT.md`, 220 lines,
commit `bca4f2aa90421c5bf5fc3bbf6777326fee6a581a`, in
`.local/p81-exact-review`, SHA-256
`51466d154b781b0eb97622133a608f65a172abeb0c8ad5f486a615688cab5e53`.
All 220 lines were read. No P62 independent note or draft was opened, and
its author was not contacted. This report leaves the primary proof unchanged.

## Dependency graph and obligation matrix

The proof chain is: contraction certificate -> uniform input-loss channel
factorization -> exact CF survivor mixture -> exact finite small-sector law
plus normalized high-sector fallback -> one-step coupling -> common Markov
postprocessing and first-divergence transcript coupling.

All load-bearing leaves are internal finite-dimensional linear algebra,
Fock normalization, combinatorics or the explicit physical/model hypotheses.
No numerical experiment, external simulation theorem or device datum is needed.

| Obligation | Status | Check |
|---|---|---|
| Whole-channel factorization, not just mean matching | Passed | Source system columns and environment Gram agree |
| CF survivor mixture and binomial weights | Passed | Distinct lost subsets have orthogonal environment occupations |
| Low-sector probability normalization/collisions/losses | Passed | Finite dilation Fock law, including output factorials, is marginalized |
| Normalized fallback and full raw TV | Passed | High branch is retained once, with coupling error at most its mass |
| Factorial-moment tail bound | Passed | `1_(L>s)<=binom(L,s+1)` and surviving-subset counting |
| Adaptive expectation under P | Passed | First mismatch is bounded along the true observation history |
| Vacuum/eta0/eta1/s>=k boundaries | Passed | Direct cases avoid division and preserve exact normalization |
| Public mean as a spectral certificate | Failed implication, correctly rejected | A single intensity .48 has 24-mode mean .02 |
| Actual hardware/finite-bit/CPU applicability | Out of scope | Required certificates and implementation costs are not supplied |

## Decisive algebra checks

For `eta>0`, `T'=T/sqrt(eta)` is a contraction. An isometry with system
columns T' and environment columns E' exists because
`E'^dagger E'=I-T'^dagger T'` is positive semidefinite. After uniform loss,
the source-input columns of the complete environment are

    E_comp = [sqrt(1-eta) I ; sqrt(eta) E'],
    E_comp^dagger E_comp = I-T^dagger T.

Together with the same system block T, this determines the same reduced
passive-vacuum channel. Equal environment Grams give an isometry between
the corresponding column spans; padding unused vacuum modes extends it to
an environment-only unitary. Its Fock lift cannot change a partial trace.
The argument works for rectangular T and rank-deficient defect matrices.
It proves equality for the channel, not only its one-particle transmission.

Uniform loss applied to the product of distinct occupied creation operators
gives mutually orthogonal lost-label records. Tracing them yields the mixture
of `|1_J><1_J|` with weight `eta^|J|*(1-eta)^(k-|J|)`. Thus L is binomial
and J is uniform at fixed L; the surviving bosons remain indistinguishable.
A fixed occupied-input restriction is valid because other source inputs
are vacuum, but that restricted norm still needs its own certificate.

At `l<=s`, a finite passive dilation has `binom(M+l-1,l)` output occupations.
The repeated-row permanent formula, with Fock factorials, retains collisions
and all environmental occupations. Summing out the latter gives the exact
raw system law in the stated ideal arithmetic model. Fixed s bounds only
the photon-sector enumeration order; it does not waive setup or arithmetic.

Using common L,J, true and replacement laws agree on `L<=s`. A high-sector
fallback is sampled once rather than rejecting/resampling the attempt.
Consequently mismatch probability, hence TV, is at most beta with no extra
factor two. If a fresh flag is used, the alphabet is augmented and TV equals
beta; mapping that flag to a raw fallback contracts it. The source explicitly
distinguishes this from filtering accepted photon counts.

For `L~Bin(k,eta)`, counting surviving `(s+1)`-subsets gives
`E binom(L,s+1)=binom(k,s+1)*eta^(s+1)`. The integer binomial coefficient
dominates the high-sector indicator. No normalization by accepted events or
detected photons enters this inequality. `eta=0` is exact vacuum; `eta=1`
has the direct binomial law; `k=0` and `s>=k` have no replacement error.

## Adaptive coupling and its precise information scope

Let the current matching observed history be H. Use common classical
controller coins and maximally couple the two next observation kernels.
Their mismatch chance is at most `beta(H)`. The probability of a first
mismatch at step j is at most

    E[1_(histories matched so far) beta(H_j)]
       <= E_P beta(H_j),

since the P marginal follows the true process even after a mismatch.
Summing gives equation (3), clipped at one. Common count-driven stops are
padded with identical stop symbols after termination. No smoothness of the
controller's matrix-selection map is needed: matched observations select
the same conditional model before the first mismatch.

The transcript here comprises the common raw observations and classical
controller outputs/coins. It does not add the simulator's latent survivor
labels, an environment purification, execution time or implementation traces
as though both physical models observed them. Fresh measured/reset sources
and no hidden coherent memory are essential. Uncoupled wall-time stopping,
postselection or rare-event conditioning cannot inherit the unchanged bound.
A lossless-only decoder also needs a declared common all-loss-event policy;
the theorem does not silently supply one.

## Hand arithmetic, external scope and remaining obligations

The two hypothetical 96-attempt bounds are correct:
`binom(12,4)=495`, so `96*495/50^4=47520/6250000=0.0076032`;
`binom(8,4)=70`, giving `6720/6250000=0.0010752`.
These are conservative factorial-moment bounds, not exact binomial tails,
measurements or claims that Lucy has the required spectral certificate.

The diagonal contraction with one nonzero intensity `.48` and 23 zeros
has trace-intensity mean `.48/24=.02`, while its spectral intensity is `.48`.
It is a physically admissible passive-loss counterexample to inferring a
2% norm bound from that scalar average, not a model of actual Lucy hardware.
The public CEA statements and their version are externally documented in
the primary note; this reviewer did not independently reaccess that page.
They are non-load-bearing context, not an admitted norm certificate.

There is no remaining gap in the stated conditional replacement theorem.
Applying it requires a suitable uniform spectral/occupied-span certificate
for the actual allowed histories, known source and channel, and separately
qualified numerical/finite-bit and resource accounting. A cheap ideal low
sector does not prove an end-to-end speedup or classical optimization
dominance. Exact prior overlap and novelty remain unassessed.

Provenance: separate reviewer of the frozen proof, aware of ROOT's candidate
and requested checks; not independent discovery. Only source/instruction text
reads, hashes, hand algebra and isolated review/Git operations were used.
No B outcome, seed, generated graph, import, AST, test, RNG, programmatic
probability or matrix calculation, native call, experiment, QPU or paper edit
was used. The positive research objective remains open.
