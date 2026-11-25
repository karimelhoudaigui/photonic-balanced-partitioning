# P53d exact fixed-functional all-b4-phase code audit

Normalized claim: for the ONE frozen N8 bosonic point at theta=pi/3, the SAME
saved w=(X04-X15)/2 and its saved normalized graph, construct and check exact
lower bounds for every real phase of each of35 complementary4+4 species
groupings in the same U8 architecture. A strict result is conditional on an
actually completed exact certificate; no particular sign/result is assumed.

Primary verdict: **conditional on named inputs** (the pinned P53/P53b/P53c
physical proof data and successful authorized execution). Implementation
review outcome: **PASS STATIC — AUDITED, NOT EXECUTED**. No load-bearing
algebra, normalization, integer-range or classification blocker was found.
One nonblocking output-field naming issue is recorded below.

Exact revision: `9284f7d7ad197efb29ea45b606723191e4b89248`.
Primary309 lines, SHA256
`6507b8b50f9f5bac30bad40b0272b0452f18f60015d2693faefa19b3e75db8d4`.
Tests22 functions/235 lines, SHA256
`aabe4ba2fe28e8cc7f155a076e0096d7b3450340f7655baa445ee7fec46d9965`.
Cards b2f3fe9/e0440e8 and the explicit4+4 title/scope at9284f7d were read.

## Dependency graph and provenance

- Internal definition: real H4 signs and
  U8(phi)=1/sqrt(2)[[W,D(phi)W],[W,-D(phi)W]], U[out,input]. Four distinct
  input photons per species; species probabilities convolve, not amplitudes.
- Internal definitions: complete compositions(8,4), compositions(8,8), exact
  uniform top4 ties, fixed edge order and the frozen functional w.
- Computation leaves: previously sealed P53 source/endpoint library,
  P53b canonical rational w/graph, and P53c exact pi/3 control means.
- New computation leaf:70 symbolic group spectra,330x330 scalar M,35 integer
  contractions,105 exact anchors and the fixed rational certificate ladder.
- Internal elementary implications: Cauchy/Parseval column bounds, Fock
  normalization, Laurent-to-cosine conversion, Chebyshev substitution,
  Bernstein partition of unity and exact affine inverse reconstruction.

I read the primary, all22 tests, both contracts/spec and the relevant exact
provider bodies. Metadata-only inspection used `git show` bytes at the exact
revision, AST/JSON parsing and SHA256. All17 main and18 preflight inputs exist;
the full project import closure is pinned: P53d, P53c, P53b, P53_exact,
P52_collective and P43. No project module was imported, test run, gzip proof
payload decoded, matrix product/polynomial evaluated or new control built.

All eight source/data hash checks matched the constants at this revision:

| Input | SHA256 |
| --- | --- |
| P53c source | `737d6743f184661c4352d93c40410679bec5b5e739aa2cd964a63b919eaa53e2` |
| P53b source | `66ed6abdb1005c961d9bb54fe70008241ef37fe56d8d548e48173d5e9c01c908` |
| P53 exact source | `aedbc561c900bcbed8f9eff3bbfa7d2fd47bd640502966d132898ea68f261692` |
| P52 provider source | `56a71f048973cae7d4922d9da7d3952943c52f5a11597fc46bbb1a2bab84d242` |
| P53c certificate.gz | `408140f0a1a3865e374256d2a1e797961adcf6742cd8b1d234c2c7b4b2cbc065` |
| P53b certificate.gz | `bd9874399ffed241b045f09a5a4f155d7d60263e7314a55e1bfd2358c9022dbe` |
| P53 source.gz | `2a593abba088327ccb8b54f5f14bab6f8edcf5fc42128de6c31f394bf454d7a0` |
| P53 library.gz | `cb210de13928e365b8983c2a17b882623a346975b522293fd549b6980871963b` |

Hashes authenticate identity, not the physical correctness of old calculations.
Historical LP floating fields may be parsed in P53b/c checkpoints, but only
canonical integer numerator/positive-denominator pairs enter proof fields.
No LP, numerical permanent or floating reconstruction is called by P53d.

## Obligation matrix

| Obligation | Static result |
| --- | --- |
| Group polynomial phases/signs and full support | PASS within fixed architecture |
| Per-species Fock factor and probability convolution | PASS |
| Tie functional/840 and scalar denominator840*8^8 | PASS |
| Python L1 bounds before int64; every partial sum | PASS |
| All35 groupings/70 spectra/105 anchors | PASS iterator and symmetry reduction |
| Chebyshev/Bernstein/affine original-power identity | PASS exact rational formulas |
| Strict, weak, negative-node and unresolved decisions | PASS reachable main domain |
| Old graph normalization and uniform-control inclusion | PASS conditional on pinned checkpoint |
| Actual normalization/anchor assertions and output bounds | PENDING authorized execution |
| Physical replication/full-law/optimization/hardware | OUT OF SCOPE |

## Decisive mathematical checks

For a four-input group with r inputs in ports4..7, the creation coefficient
C_n(z) has integer coefficients and degree<=3r, z=exp(i phi). Each matrix
entry has magnitude1/sqrt(8); four creation factors contribute8^-2. Thus the
normalized amplitude is sqrt(prod n_i!)*C_n(z)/8^2 and the probability is
prod n_i!*|C_n(z)|^2/4096. `group_spectrum` implements exactly its real
autocorrelation Laurent coefficients. The assignment-count bound24/prod n!
and every harmonic mass are checked using Python integers. Pruning algebraic
zero dictionary entries does not drop any330 final occupations/phase columns.
All-bunched output has one monomial and central probability numerator24,
consistent with the independent assignment fixtures.

The species are distinguishable ACROSS the groups, so their normalized
probabilities multiply/convolve. There is NO extra factorial of the final
summed occupation. `make_tie_matrix` contracts the decoded observable directly.
For the frozen weights w, s(n)=sum(weight420*(X04-X15)) gives s/840 and
|s|<=420. Independently, an occupation with four photons in0 and four in4
forces both0/4 into top4 and chooses two of the other six modes: X15 has
mean8/15, hence s=-224 and w-mean=-4/15. The test's signs/scale are correct.
All-one and single-bunch occupations give s=0 by symmetry.

For each fixed Laurent column k, extend C_n,j by zero. Weighted Cauchy bounds
sum_n |prod n!*sum_j C_n,j*C_n,j+k| by the geometric mean of the two shifted
total squared-coefficient sums. Each is4096, from the zero-harmonic Parseval
mass. Therefore EACH column L1<=4096, not the sum of all columns. Both banks
are checked as rectangular Python-int arrays with odd width<=25 BEFORE casts.
M is checked as symmetric int64 with entries bounded420; its construction
checked the Python entries before conversion as well.

Every partial M@B sum is bounded420*4096=1,720,320. Every partial A.T@(M@B)
sum is bounded420*4096^2=7,046,430,720, far below signed int64. Swapping banks
when needed is legitimate because M is symmetric. Widths2dA+1 and2dB+1
with dA+dB<=12 give at most13 pairs on a folded harmonic. Folding uses Python
integers; its bound is13*420*4096^2. Cosine doubling is at most
2*13*420*4096^2<2^38. No post-hoc overflow detector is being mistaken for an
overflow proof: these absolute bounds protect EVERY intermediate partial sum.

The complementary reduction is exact species exchange: exactly one of G,Gc
contains input0. The multiplicities of r0/1/2/3 for that first group are
1/12/18/4, totaling35. Both members' spectra come from all70 groups.
Three anchors per grouping use exact cos(k phi) cycles at0/pi2/pi3 and
known positions j,j+35,j+71 in the pinned libraries. Their labels and the
fixed B/w are checked, so the105 checks are not fresh physical replication.

`cosine_to_power` constructs T_k(2x-1) for x=(1+cos phi)/2, including all13
harmonics. Affine substitution p(L+(R-L)u) is exact over Q. The inverse
q((x-L)/(R-L)) uses endpoints -L/(R-L),(1-L)/(R-L), whose difference is
positive, and reconstructs the original padded power vector exactly.
Bernstein controls reconstruct local AND original power coefficients.
Nonnegative basis functions summing to one justify only their actual minimum
control bound, over the entire global interval or ALL eight fixed subintervals.

Negative values at the nine registered nodes are genuine physical-phase
counterexamples to the claimed margin. A negative interior Bernstein CONTROL
is not such a value and stays inconclusive. Zero bounds are never strict;
an actual zero node falsifies strictness without proving nonnegativity at
unresolved phases. The positive-polynomial/negative-control fixture tests this
distinction. Generic `aggregate` assumes35 valid decisions and positive graph
scale; MAIN enforces35 and checkpoint verification enforces positive scale and
a strictly positive old uniform gap. No broader generic API claim is used.

## Residual issue, scope and next gate

NONBLOCKING metadata naming: `shorter_bank_multiplied_first` actually stores
the local `swapped` Boolean. M is multiplied by the shorter bank in BOTH
orientations; false means no swap was needed, not that the optimization failed.
The test currently confirms that swap flag. Interpret/rename this field as a
swap indicator; it is not a mathematical failure or evidence of float work.

If a completed exact STRICT result is obtained, the strongest safe conclusion
is a uniform lower bound for this ONE linear functional/old normalized graph
against all35 b4(4+4) curves and the included uniform control. Convex mixtures
inherit this linear-mean bound. It does not prove a full-law/tail simulation
separation, optimized phase minima, order8 indistinguishability,7+1/6+2/5+3
cases, all classical output models, classical-search benefit or hardware value.
The graph/w were already fixed posthoc witnesses, not optimum-blind training.

Next narrow gate: independently reviewed22 synthetic qualifications, then the
separately authorized main with all35 records and exact evidence replay before
accepting any actual bound. No sign is predicted here and no new computation
is requested by this audit. P55 remains a separate optimization question.

Provenance: independent static implementation review by the encoding agent,
which authored neither P53d nor its tests. Earlier P53 algebraic reviews were
shared context, so this is not a blind reconstruction of every historical
provider or an independent physical/code reimplementation. Only this new
review file is written; author source/tests/raw artifacts remain unchanged.
