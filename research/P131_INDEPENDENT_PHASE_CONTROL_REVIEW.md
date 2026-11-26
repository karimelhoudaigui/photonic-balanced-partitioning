# P131 independent finite-phase control/code review

2026-11-26. Non-author STATIC audit; no import/AST/test/RNG or scientific run.
Frozen package `21caef25c294e0b5ec8447fcd286314c20b3b13d` was read FULL:

| File in research/ | Lines | SHA256 |
|---|---:|---|
| P131_phase_multinomial.py |232| bdf3e490e90330b67c7ca8089068abf5be5674ea71daff3dd5ea436b30e5042f |
| P131_phase_multinomial_validation.py |604| 5009194e358d3013d33ac47d3bff2ec31abb24a92d82961d91bcae88b6b07ff9 |
| P131_PHASE_MULTINOMIAL_POPULATION.md |120| bbc77a334bf7127e660e81ea4e5021fefcb9c3a50d013ed6eee5ee4c6b50cccc |
| P131_phase_multinomial_contract_TEMPLATE.json |27| fabbaf20fcd92d14ea8f9ac089cd534efec2db7a9f220ace1eb6712ccd05385b |

All 983 lines and all four Git-blob SHA256 values were checked, against
the FULL 190-line P129 proof `6bee40d85ea941818959e4641cabffa009bbf480`,
SHA256 `515d2c2ac9b2e4763d17d591691ff8aa71e004fd77400b0d8364e2d5092870b8`.
Review parent: `5527fa8695101b712a1902031cd78b0efddec093`.

**STATIC PASS: no blocking algorithmic, normalization or schema gap found.**
One nonblocking final-rehash diagnostic limitation is stated below. This
verdict is not execution qualification, an observed TV, a runtime assertion
or permission to launch. ROOT must separately bind and authorize these bytes.

## 1. Production kernel, contraction and finite roots

The production scope is m>=1 and 0<=K<=7, not generic-M code. Matrix parsing
uses exact Gaussian-rational pairs; binary floats and bool rational entries
are rejected. K>=8 raises UnsupportedScope before any callback is consulted.
The Hermitian residual eta I-T^dagger T is formed correctly. Positive-pivot
Schur updates use the unchanged pivot row/column; a zero residual diagonal
must have zero remaining row/column. This exact PSD test handles rank
deficiency and eta=1 without numerical tolerance, clipping or eigenvalues.
build_model uses eta=1 for validity; a sharper eta is an EXTERNAL error
certificate, not a parameter secretly inferred from output intensity means.

M is the smallest power of two STRICTLY greater than K. For K=1,2/3,4..7
it is respectively 2,4,8; K=0 has its own vacuum/zero-bit branch. Thus the
finite twirl kills every off-diagonal exponent difference of magnitude <=K.
With scale S, isqrt(floor(S^2/2)) equals floor(S/sqrt(2)); the displayed
integer residuals certify a<=1/sqrt(2)<a+1/S. Axes are exact, diagonal roots
have error squared <2/S^2 and norm squared 2a^2<=1. Choosing 2/S<=delta
therefore implies the required error <=delta=epsilon/(4K). No precision
search based on results occurs. This inward construction differs from
P129's generic construction but satisfies its SAME two load-bearing bounds.

The denominator D is the smallest power of two >=2Km/epsilon. Signal
weights floor(D|(T zhat)_j|^2/K) and the final loss residual sum to D.
Contraction and inward roots prove the loss is nonnegative; it is not clipped.
The CDF uses ticket<cumulative, correctly skipping zero-weight intervals.
Exactly K phase blocks precede K categorical blocks, sharing ONE phase vector
across all trials. Even zero T consumes all these blocks. K=0 consumes none.
Malformed callback returns are rejected with their observed representation.
Fairness and independence are assumptions on the explicit provider, not
consequences of integer-range checking. The qualifier supplies no RNG.

The mathematical errors are the P129 ones: per-context phase perturbation
categorical TV <=2delta, hence <=epsilon/2 for K trials. Floor rounding
moves all lost signal mass to the loss category, giving categorical TV
<m/D and K-fold error <=epsilon/2. Counts never exceed K. This phase-shared
particle-separable law is generally DIFFERENT from independently labeled D.

## 2. Independent repeated-input oracle: both factorials are necessary

The validator's Gaussian-rational class and sparse-polynomial subset DP are
separate from production tuple arithmetic and direct matrix-vector weights.
It forms M(z)=I-T^dagger T+T^dagger diag(z)T in SOURCE-mode coordinates.
For occupation a, it repeats BOTH row and column indices of THIS matrix,
including the repeated identity entries, then computes per(M[a,a])/a!.
It does not substitute a new K-by-K identity after repeating Gram indices.
The DP masks labeled column COPIES, correctly counting identical columns.

That first a!=product_i a_i! normalizes a Fock input. The separate mixture
weight K!/(K^K a!) is the diagonal probability of the phase-twirled condensate.
Its factorial is not removable merely because the first divisor is present.
The doubled-input hand with a=(2,0),T=(1/2,0) gives
(3/4+z/4)^2, coefficients 9/16,3/8,1/16, as registered. Summing the
normalized PGFs with their multinomial weights computes the ideal surrogate.
This is not an optical preparation of that surrogate at no source cost.

Independently, every ordered phase context contributes the integer
multinomial K!/(n! loss!) product_j h_j^n_j h_loss^loss. Dividing by
M^K D^K after summing gives exactly the finite callback law under fair blocks.
The K=0 empty permanent/empty occupation gives vacuum with mass one. All
final signal bins are dense; canonical sparse zero removal inside a PGF
does not remove zero output bins, losses or collisions from the final record.

## 3. Counts, certificates and original-reference interpretation

I independently counted the 15 cases: K multiplicities are 1,1,1,5,7 for
K=0,1,2,3,4. Thus phase contexts are 1+2+16+5*64+7*4096=29011;
input PGFs are 1+1+3+5*10+7*35=300. P96 contributes 167 output bins and
the two complex cases contribute 140, total307. The twelve hand groups are
vacuum+4 unary boundaries+2 H2 boundaries+1 doubled PGF+3 rejections+1 bool.
Their fixed CDF tickets agree with the actual unary/H2 weights and bit widths.

All 13 P96 literal matrices match the frozen schema source. X4 remains a
physical trace-one endpoint, not a fabricated negative probability matrix.
For these real Grams, min(trace,maximum absolute row sum) is a valid spectral
upper bound and the exact PSD check separately confirms it. G4's first row
agrees with F diag(1,1/2,1/8,1/4)F^dagger using the stated negative-i Fourier
order; its spectral intensity norm is one. G4atten=T/4 has bound 1/16.
Fourier orthogonality and the literal reconstruction are checked explicitly.

The exact binomial expression for tau and the birthday bound are implemented
with intensity eta, not amplitude. K=0/1 and eta=0 have their proper zeros.
For eta=1, the separate endpoint argument uses R=T and L=K, giving distance
1-K!/K^K. This valid diagnostic extension is disclosed; it does not edit
P129's strict eta<1 header or imply an informative small bound at eta=1.
Ideal row means equal sum_i|T_ji|^2; finite means are only approximately
equal, with a range-K error bound. No rounded-mean equality is invented.

P96 physical p references and all 70*81 P107 B/B_moment coefficients are
required completely; no favorable numerator is selected. P107 is evaluated
at x=1/2,y=1/4. The attenuated reference uses exact TERMINAL binomial thinning
of every source signal count at intensity1/16, including preexisting vacuum.
It is not conditioning on survival or applying a count kernel through a
subsequent coherent mixer. Original files remain immutable and are not run.

## 4. Authority, evidence and boundaries

Before reference payload parsing, the code requires the distinct ROOT binding,
exact argv/caps, complete unique static+12-reference closure, actual source
hashes, interpreter pin, -B and six thread settings one. All paths are regular
and checked for symlinks; the output is a fresh exclusive child. Both reference
groups are checked against their ORIGINAL Git blobs, SHA256 and byte sizes.
ROOT additionally confirmed only metadata, without transmitting outcomes:
both original v2 manifests have the expected claim IDs, one producer source
with matching sha256/sha256_after, five payload/log outputs and three declared
results. This confirms the legacy parser's exact interface assumptions.

Input PGFs, phase weights, bins, means and comparison operands are emitted
before scientific checks. Scientific failures accumulate through later
registered observations and yield SCIENTIFIC_COMPARISON_FAILURE. Infrastructure
exceptions stop with a prefix/partial-case/NOT_RUN ledger. A processed case is
not thereby a passed case; final counters and failure status decide acceptance.
Missing finals after a resource kill remain inconclusive, never PASS.

Nonblocking diagnostic caveat: final input/external rehash comparisons do not
save the newly observed drifting hash before raising. They DO reject drift,
and initial observations/expected hashes/prefix survive; ROOT confirms the
outer runner separately records before/after hashes. Do not claim this
source alone archives the final observed mismatch value. No false-PASS path
was identified, and no source change/retest is required by this static review.

CPU120/wall180, logs4MiB, science8MiB and separate64KiB finals with128KiB
reserve are prospective limits. Logical256MiB is a plan, not hard RSS.
The 32-transition K4 DP bound and fixed context loops are finite work counts,
not measured runtime guarantees. Root sealing, full manifest/exit/artifact
inspection and a separate launch authorization remain mandatory.
No generic-M implementation, finite-case proof of the general theorem,
verified RNG provider, optimizer gain, matched-cost result, native/QPU
capability or novelty follows. Only this review was written; no P130/frozen
source/raw/manuscript modification or scientific execution occurred.
