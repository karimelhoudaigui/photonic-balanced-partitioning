# P113 independent mean/certificate source review

26 November 2026. Reviewer `/root/p66_dark_audit` authored P107 and did not
author P113. This is a non-author audit of P113's distinct implementation;
it is not an independent authorship of the P107 reference mathematics.
I remained blind to every P107 raw payload and certificate outcome.
No import, AST, collection, test, scientific evaluation, RNG, native call,
runner, validator, QPU operation, manuscript edit or push occurred.

## Identity, coverage and verdict

Read all381 lines at exact commit
`7267e6a4ce544772cf8f5018988e142940c9586e` as frozen Git blobs:

| File under research/ | Lines | SHA256 |
|---|---:|---|
| P113_independent_mean_certificate.py | 278 | af1056d49ba5df8472fb0cecaa97b2ab29f1da0600cb698350186423451848a3 |
| P113_POPULATION.md | 74 | ad76b00020a4d106970b8b5e335b913ad348f357009f63efe3703e1d4724e528 |
| P113_contract_TEMPLATE.json | 29 | edcc42add85efd7a9b505c503abdffc5c0fbf726af0bc7ceaf14b95606aaf0bf |

Also read all102 lines of the frozen decoder-identity dependency at
`98c76e34`, SHA256
`9dca56e56c724b67493199f637094dfa59f17e2d12b1d01d93493735fbded9f9`.
The earlier P107 source/schema identities are those I froze at `6d9c16c`.

Verdict: **STATIC PASS for the declared mean/certificate comparison, subject
to the explicit ROOT seal-binding gate below; audited, not executed.**
I found no blocking mathematical or nominal-population defect. Neither this
review nor the passive TEMPLATE authorizes execution or establishes a match.

## Algebra and independence

The transfer's first row is exactly
`((1+x)(1+y),1−xy+i(x−y),(1−x)(1−y),1−xy−i(x−y))/4`.
The circulant indexing `(j−i) mod4` matches `F diag(1,x,xy,y) F†`
under the stated output-row/input-column convention. Real/imaginary
polynomials are separate exact Fraction dictionaries. Algebraic functions
construct fresh dictionaries; shared row entries are never mutated.

Ryser uses `sum(nonempty J) (−1)^(n−|J|) product_i sum_(j in J) M_ij`.
For n>0 the empty-subset term vanishes; n=0 is handled separately as1.
Sizes never exceed4 and bidegrees never exceed(8,8). This is a different
permanent algorithm from P107's permutation sum. The five literal hands
cover the empty permanent, complex cancellation, 3-4-5 rotation including
the repeated-output factorial, an affine linear box, and the top basis.
They are meaningful checks but have not been executed by this reviewer.

For an allowed pair A, the event is no signal counts outside A; dump
photons remain unrestricted. Its Gram is `I−T†Q_(A^c)T`. Source void_pair
forms precisely this matrix, using per for B and diagonal product for D.
This is a whole raw event, with no survival or collision conditioning.
For qA/qO the four repeated output rows are respectively `(2,0,1,1)` and
`(2,1,0,1)`. Source record_probability divides both the squared complex
permanent and intensity permanent by the single output divisor2!, which
is the correct CF-input B/D normalization. Those records have total4;
their probabilities are unconditioned full-survival probabilities.

I rederived the decoder reduction. Write `w_ij=C_ij−cbar`; complement
symmetry gives each row sum0. The threshold mean differs from cbar only
for exactly two clicks. Inclusion-exclusion for that click set cancels
all singleton/vacuum terms in the w-weighted sum, leaving pair voids.
For this cycle cbar=8/3, adjacent cuts3 and opposite cuts2. Four adjacent
and two opposite unordered pairs give `meanT=8/3+(4/3)(VA−VO)`.

For total counts≤4 the only PNR/threshold disagreement is2110: doubled
i, empty l. Its correction is `(cbar−C_il)/2`. Eight ordered adjacent
and four opposite pairs therefore give `(4/3)(qO−qA)`. Rotations plus
reflection identify the two directed adjacent types: reflection conjugates
the Hermitian circulant T and its canonical vacuum dilation; the filled
four-mode CF source is invariant, so both B and D probabilities agree.
These are special cycle/decoder identities, not arbitrary-graph formulas.
The source's means have the correct constants, signs and factors.

The independent Bernstein routine first expands each power on the affine
box, then uses `t^r=sum_u binom(u,r)/binom(8,r) B_(u,8)(t)`.
The tensor product and lower-corner/width substitutions are correct.
This differs structurally from P107's direct combined transform. For each
decoder all1+4+16 boxes and all81 coefficients are retained; a complete
level of nonnegative coefficients is sufficient for the square. A negative
Bernstein coefficient alone supplies no counterexample. All25 grid pairs
are checked, and a grid-negative result is restricted to the square claim.

## Population, comparison and outcomes

The324 component rows are4 components×81 powers. Two means give162 rows,
and42 boxes give3402 independent Bernstein rows. The source computes and
archives those quantities before parsing the reference records. Endpoint
and x/y identities are exact additional guards, not fitted simplifications.
It does not reconstruct the entire70-state law or use that law as an oracle
for its own mean calculation; its limited independence is stated correctly.

The reference parser requires all9612 producer rows with every expected
kind count,5670 distinct occupation/power coefficient metadata entries,
full162/3402 mean/Bernstein key domains,25 normalized complete grids and42
box statuses. Coefficient pairs are checked for integer components, internal
B/moment/difference consistency and zero imaginary parts. The formal
normalization record, source provenance and successful summary/null failure
are also required. These checks do not independently prove each full-count
coefficient, fixture, endpoint or grid probability; those are reference
consistency gates, not newly recomputed evidence.

The exact comparisons number162+3402+50+42+2=3658: means, Bernstein,
grid means, box flags and complete certificate dictionaries. Actual and
reference values, zeros, negatives and mismatches are emitted. A mismatch
does not stop the remaining comparisons. Independent whole-level/grid signs
produce the expected certificate before comparison; it is accepted only
when all comparisons pass. COMPARE_FAILED is a complete mismatch outcome,
not an optimizer result; malformed/resource/incomplete cases are INCONCLUSIVE.
The planned7555 output records follow the declared arithmetic exactly:
1+5+1+324+162+3402+1+1+3658. No extra case or favorable box is selected.

## Binding, caps and remaining conditions

Authorization requires ROOT_AUTHORIZED/run_authorized=true, original seal
ID and exact reference paths, unique descriptor closure, six descriptor
copies, actual SHA256/byte sizes, regular nonsymlink inputs and the source
hash agreeing with its own descriptor. Extra inputs are restricted to frozen
research Markdown reviews. There is no producer import, RNG, native backend,
external package installation or adaptive precision/parameter selection.

Important explicit boundary: P113 does not itself compare the six files with
their Git blobs, parse the opaque manifest, or validate its v2 completion/
before-and-after provenance. The matching seal string and SHA descriptors
alone do not prove that relationship. The population card deliberately
assigns it to ROOT: before binding, ROOT must verify the original six sealed
blobs, upstream completed v2 provenance and the actual current descriptors.
An active binding is acceptable only after that separate metadata gate.
This review has not performed that gate or opened any of those six files.

The parser is not a hostile-input validator: JSON duplicate members and
some numeric metadata coercions are not rejected as strictly as in P110.
For authenticated original P107 bytes this does not change the assertion;
it must not be generalized to arbitrary replacement JSON as equivalent.

The source enforces CPU30 and per-file FSIZE4MiB before mathematical work;
its writer enforces aggregate4MiB and64KiB reserve, with exclusive fresh data
creation and flushed prefix records. The runner must separately enforce
wall60, combined logs4MiB, fresh whole parent, exact declared result/input
paths and before/after input hashes. There is no hard RSS or measured-runtime
claim. A hard interruption can omit final files and cannot be called PASS.
All independent/source/native/reference costs remain real; no setup-free
optimization inference follows from a mean identity or agreement.

ROOT must read this frozen review and close the metadata gate before any
separate run authorization. No tests or execution are authorized here.
All earlier validated results and negative evidence remain unchanged.
