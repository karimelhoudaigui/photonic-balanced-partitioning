# P74 exact-hash independent author-proof review

Primary verdict: **proved as written**, for the stated no-recovery profile
and its actual conditional-success/gate-count hypotheses. The catalog
distinction, concrete reentry example, Knill success and leakage fractions,
proposal-count dominance and resource qualifications pass the targeted
checks below. No source correction is requested. Auxiliary geometric-mean
and retry formulas are read on their nonempty, positive-success domains,
as made explicit in the endpoint check.

## Exact artifact, coverage and independence

Reviewed all 379 lines of
`.local/p66-dark-audit/research/P74_heralded_graph_cost_resource_screen.md`,
SHA256
`0b4b4bbca399ab8c80d4b5f152b7eff1f3c8b50c344e3a2d2ab8ba5966cea12b`.
The source is a frozen uncommitted artifact in a worktree with an unavailable
index. This review is attached to its bytes; no source commit is invented.
It covers all ten sections, including weighted phases, both catalog
profiles, protected flags, the asymptotic ceiling and hypothetical recovery.

Before reading that source, the reviewer froze an independent 330-line
proof in commit `3a3016c449ef4e82a51b2af5b76e2cd0bd77ce6b`, file
`theory/P74_independent_heralded_cost_screen.md`, SHA256
`77fa4c62038d3882259d4e8efb7e6cc791732ced2203ea130ff4fc1f0bf2e9ae`.
That hash remains unchanged. This subsequent comparison is not blind:
the author's disposition was visible, but is not evidence for itself.
The concrete local gate profile and recovery calculations were checked
directly, not inferred from the generic independent proof.

Review date: 2026-11-25. Worktree `.local/p66-dark-barrier`, starting at
the independent P74 checkpoint. Only this file is written. No imports,
AST evaluation, backend, circuit construction, numerical amplitude,
scientific calculation, test, random draw or QPU call was run. Inspection
used local source text, hashes, one primary paper and hand algebra. Other
active test/experiment workers were not accessed.

## Weighted graph phase and what can change its gate count

With n_i=(I-Z_i)/2, the cut term A_ij(n_i+n_j-2n_i n_j) gives

    C=sum_i d_i n_i-2 sum_{i<j}A_ij n_i n_j,
    exp(-i gamma C)=product_i exp(-i gamma d_i n_i)
                     product_{i<j}exp(+i 2gamma A_ij n_i n_j).

The signs and edge angle 2gamma A_ij are correct. Expanding
n_i n_j=(I-Z_i-Z_j+Z_i Z_j)/4 verifies the displayed local phases.
Conjugating target Z by CNOT gives Z_i Z_j, so the source's
CNOT Rz_target(-phi/2) CNOT produces exp(+i phi Z_i Z_j/4).
This is one two-entangler realization, not an optimal synthesis bound.
A fixed pi-CZ cannot be substituted for arbitrary weighted angles.

The Dicke input has equal magnitudes on all balanced strings. A diagonal
cost phase leaves its measurement law uniform; a noncommuting mechanism
is essential. Preparing that input or implementing a logical balanced
mixer is a real source/interaction obligation. A physical inter-qubit
beam splitter is not thereby a deterministic code-preserving logical XY
gate. No native availability is assumed.

For the stipulated implementation with a counted capped-success primitive
on every edge of a connected nontrivial interaction graph, g>=N-1 is
valid. The source correctly refuses to turn this into a compiler lower
bound. Its complete uniform-weight graph example is a valid exception:
the balanced cut is constant, so its cost phase can be global on the
feasible space. Actual angles, cancellations and joint compilation may
change the real g.

## Local bundle identity and protected composition

All SIX installed-file SHA256 values in source section 2 were independently
recomputed and match exactly. The read-only package paths were under
`.venv/lib/python3.11/site-packages/perceval/components/`. Relevant
definitions inspected were:

| File | Definitions checked |
|---|---|
| `core_catalog/heralded_cz.py` | six modes, helper inputs/outputs one on modes 4 and 5, ideal circuit convention |
| `core_catalog/postprocessed_cz.py` | vacuum heralds on modes 4 and 5 plus a separate data-pair postselection predicate |
| `unitary_components.py` | BS.H template, reflectivity-angle conversion, PERM input-to-output convention |
| `experiment.py` | copied heralded subexperiments, composition permutations, herald input/output registration, connectible mode type |
| `_mode_connector.py` | old-herald skipping, new herald append positions and connection checks |
| `component_catalog.py` | processor wrapper delegates to the experiment definition |

The heralded and postprocessed instruments are genuinely different.
`add_herald` defaults to the specified photon count at both input and
output. The heralded-CZ builder adds two one-photon flags and no extra
logical postselection predicate. The postprocessed builder adds two
vacuum flags AND a one-photon-per-data-pair condition.

In ordinary Experiment composition, old HERALD outputs are not connectible
as PHOTONIC data; new ancillary modes are appended and herald-bearing
subexperiments copied. Symmetric input/output herald layouts use routing
and its inverse. This supports the source's protected-flag model for that
standard composition path, not arbitrary raw Circuit manipulation or
cleared metadata. No multi-gate circuit was built or run, and floating
catalog parameter/engine errors were not qualified.

At the abstract level, each flag projector Pi commutes with later operations
and with other dedicated flag projectors. Moving Pi through those later
operations gives

    (P_g...P_1) U_g...U_1
       =P_g U_g P_(g-1) U_(g-1)...P_1 U_1.

Thus final reading of protected separate flags is equivalent to virtual
intermediate success projections. It does not need fast readout for this
probability identity. Correct logical operation still needs its success
Kraus profile. The statement does not apply to projectors on reused data
modes, nor establish a hardware memory/feedforward capability.

## Concrete postprocessed 1/9 and failure reentry

The local BS.H and permutation definitions give the author's data submatrix
by hand. With a=1/sqrt(3), b=sqrt(2/3), its middle block is

    B=[-a b; b a],      a^2+b^2=1.

The other two data entries are a. The four valid logical diagonal
two-photon amplitudes are a^2,a^2,b^2-a^2,-a^2, respectively: exactly
(1/3)diag(1,1,1,-1). This validates the one-block postselected fraction
1/9, not a nondestructive intermediate success monitor.

For input photons in rails 1 and 2, the complete middle-block output is

    (1/3)|1,1> -(2/3)|2,0> +(2/3)|0,2>.

The sqrt(2) occupation normalization is included: the bunched amplitudes
are sqrt(2)(-a)b and sqrt(2)ba. No amplitude from these input columns
enters the vacuum ancillary outputs. Thus ancilla-vacuum heralds alone
accept these leaked data occupations as well as the logical component.

Since B^2=I, two identical raw blocks on the same data rails return that
input exactly, even with separate vacuum ancillary checks. The final
logical success probability on this input is ONE, not 1/81. The omitted
term is Pcode K2(I-Pcode)K1 Pcode. This fully verifies the specific
counterexample, including the ancilla qualification. It does not claim
correct logical two-gate action on every input, an advantage, or that
Experiment's safety checks permit the unsafe composition.

## One authenticated primary profile and the nonunitary failure

The single external work checked was E. Knill,
*A Note on Linear Optics Gates by Post-Selection*,
[arXiv:quant-ph/0110144v2](https://arxiv.org/pdf/quant-ph/0110144v2).
The PDF version banner and
[versioned primary HTML](https://arxiv.org/html/quant-ph/0110144v2)
identify 25 October 2001; later rendering dates are not revision dates.
Section III, equations (2)–(8), imposes equal logical success amplitudes
and zero accepted leakage. Equation (11) and its following paragraph
supply the two-helper pi-phase profile with success 2/27. This verifies
the ideal scalar Kraus profile on the code, not universal optimality.

For the failure calculation, the local ideal BS/swap convention reproduces
the displayed active matrix with output rows and input columns. Its
helper-input to active-signal-output block is

    [ sqrt(2)/3   2/3 ],
    [ -2/3       sqrt(2)/3 ].

Both input and output occupations here are singly occupied, so their
permanent amplitude is 2/9-4/9=-2/9 and probability 4/81. Active signal
00 means those two signal modes are empty; the inactive logical rails
still carry two spectator photons. The helper-00 outcome therefore leaves
four data photons. A passive unitary on the data cannot restore a
two-photon logical pair. Consequently not all failures of this profile
have the known code-unitary form assumed by the abstract retry escape.
This conclusion follows from the verified branch, without executing a
catalog matrix or inferring native device behavior.

## Uniform conditional cap and best-of-T screen

For the ideal Knill success branch K^dagger K=(2/27)I. Linearity makes
that effect independent of arbitrary logical input or entanglement with
the rest of the register. More generally the proof only needs the stated
uniform conditional cap h on valid successful prefixes. With no failure
recovery, each valid candidate requires at least g such passes. Conditional
expectation gives P(all passes)<=h^g, without independent gates or shots.
Preparation failure and final feasibility checks can only reduce the raw
mass. Thus q(S)<=h^g and sum q(S)<=h^g with failed records retained.

If D_N h^g<=1, q(S)<=1/D_N pointwise. On every mathematical cost sublevel
E_b this implies a conditional hit probability at most |E_b|/D_N after
every adaptive optical history. Iterating survival gives at most
1-(1-|E_b|/D_N)^T hits by T raw attempts, the iid uniform feasible value.
With the same incumbent, thresholds at/above its cost are already met by
both procedures; lower thresholds give the claimed best-cost CDF ordering.
At T=0 both return that incumbent. No favorable optimum mask or computed
sublevel cardinality is supplied to a training procedure by this analysis.
Independent classical solutions must be shared/accounted; the screen
concerns credited optical candidates, not uncounted external improvements.

The recurrence for binom(2m,m)/4^m is correct and proves
D_N<=2^(N-1), strictly for N>=4. Together with the stipulated g>=N-1
and h<=1/2 this proves the connected edgewise application. The author
starts at N>=4; it need not claim the N=2 equality case covered in the
reviewer's broader independent theorem.

Endpoint annotation: the main raw-count statement extends to g=0 with
the empty product one, giving no gate-failure screen since D_N>1, and
to h=0,g>=1 with no successful proposals. Source sections 8–9's expressions
dividing by g or h, or using log(1-h) in a retry denominator, concern
g>=1 and 0<h<1. The actual nontrivial Knill profile satisfies these
domains. They should not be evaluated as 0/0 at an empty circuit or
zero-success gate; those cases use the preceding elementary limits.

## Resource counts, threshold scaling and hypothetical recovery

Two ancilla photons per reached Knill gadget follow from its explicit
herald inputs. Always launching all g gadgets gives 2g ancilla photons
before logical-source/preparation costs. Actual detection and on-demand
injection can instead use, conditional on a valid starting register,

    2 sum_{j=1}^g h^(j-1)=2(1-h^g)/(1-h).

Equality here is for the ideal constant-h branch. With only an upper
cap, the same expression is an upper envelope for reached-stage ancillas,
not an exact expenditure. The source states the ideal condition. Neither
abort savings nor full-g charging may be assigned without the actual
preparation policy. The fresh register, initial Dicke source, mixer,
failed preparations, compilation and scores remain paid. Proposal-count
CDF dominance does not automatically imply equal CPU, photon or wall-time
dominance.

The total usable-yield screen Y<=1/D_N is sufficient regardless of the
conditional distribution; Y>1/D_N only escapes this scalar certificate.
The source explicitly makes no sufficiency claim for optimizer benefit.
For g>=1 the product/geometric-mean threshold is algebraically correct.
The central-binomial bounds 2^N/(N+1)<=D_N<=2^N justify the stated limits
for g asymptotic to cN and of order N^2. Zero phases and joint compilation
must use their actual g. The example D_4=6 is an exact analytic threshold,
not a measured circuit result.

For the hypothetical code-preserving recovery instrument the two success/
failure effects sum to I. Applying V^dagger after failure restores the
unknown logical state before retry. Fresh lossless retries therefore have

    h_R=1-(1-h)^R,
    E[trials to success or cap]=sum_{j=0}^{R-1}(1-h)^j=h_R/h.

For g>=1 and 0<h<1, the stated R ceiling makes each gate failure at most
1/(2g); Bernoulli's inequality gives h_R^g>=1/2. This is a consistent
abstract escape from the all-first-try model. It is neither a passive
optical construction nor justified for every failure of the Knill gate,
as the four-data-photon branch demonstrates. Recovery, resources,
memory/feedforward, high-success helpers, weak-phase profiles or jointly
compiled blocks retain the OPEN status assigned by the author.

## Closure and checks

| Obligation | Result |
|---|---|
| Full source hash and independent 330-line pre-read proof | Passed; prior proof unchanged |
| Cost signs, weighted angles and mixer requirement | Passed |
| Six listed local-bundle hashes and relevant code paths | Passed by text inspection only |
| Protected deferred flags and raw-code postselection distinction | Passed |
| Postprocessed 1/9 and concrete two-block p=1 reentry | Passed by exact hand algebra |
| Ideal primary 2/27 success and 4/81 code-leaking failure | Verified in the stated convention |
| Conditional cap, failed-record normalization and adaptive CDFs | Passed at equal guaranteed raw counts |
| Edge-count premise, phase/compiler exceptions and incumbent | Passed with stated scope |
| Ancilla prefixes, threshold scaling and hypothetical retries | Passed on their indicated domains |
| Actual numerical circuit qualification, equal-clock advantage, Lucy features | Not established |
| All-QAOA no-go, novelty or a positive optimizer | Not claimed |

No load-bearing gap was found in the scoped source result. The strongest
safe disposition remains its own: close the simple low-success no-recovery
edgewise count profile; retain the encoding and screen; leave mechanisms
that genuinely change the gate/resource assumptions open. No experiment,
hardware circuit or P75 action is authorized by this audit.

Exact source/local hashes, text reads, the one primary edition and hand
derivations are the evidence here. The local files were never imported,
parsed as AST, executed or changed; no compiled circuit was generated.
Git whitespace checks accompany this review's commit. Final mathematical
proofreading covered signs, basis/flag conventions, success versus raw
mass, CDF direction, retry domains and resource qualifiers. No scientific
execution was performed.
