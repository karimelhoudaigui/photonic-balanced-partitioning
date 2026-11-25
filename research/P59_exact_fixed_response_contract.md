# P59 exact response: source and execution contract

25-Nov-2026. IMPLEMENTATION ONLY. No module has been imported, no test or
calibration has been executed. ROOT must review the final source/closure and
grant a numerical slot. Qualification and main are SEPARATE authorizations.
The mathematical question and all parameters were fixed in9f5b7ea before code.

## Claim and finite assertion

For the one fixed N6 full-CF source/device/decoder, reconstruct the exact
occupation probability and decoded-edge spectra for ALL phases, then report
ALL15 derivatives at the ONE center0. This is a finite symbolic calculation,
not a graph benchmark, physical replication or proof of algorithmic benefit.

Conventions are in `P59_N6_FIXED_RESPONSE_CARD.md` and its theory companion.
U=Q/(5sqrt6), GramQ*=150I, integers in Z[xi],xi²=xi-1. The numerator source
is obtained by multiplying the SIX ACTUAL columns, with commuting occupation
monomials and integer coefficients. Final records include all462 occupations
and all three phase coefficients, including all exact zeros. Dropping a zero
term during intermediate multiplication does not discard a final occupation.
The squared Fock amplitude MULTIPLIES by prod(n!) and divides by150^6.

All probability/edge/class spectra are represented by(u,alpha,beta), where
F2=alpha+beta*xi is the coefficient of exp(2i phi). Consequently

    f(phi)=u+(2alpha+beta)cos(2phi)-sqrt3*beta*sin(2phi),
    r=f'(0)/sqrt3=-2beta,
    B=4*(|2alpha+beta|+2|beta|).

Every spectrum exports u,F2,cos2,sin2/sqrt3,r,center value and B exactly.
Proof numbers are canonical integer/rational JSON, never floats. Observed
CPU/wall clock readings are decimal STRINGS in metadata, outside the proof.

## Exact validation and independent guards

- Matrix: every entry is one integer Z[xi] monomial. Reconstruct the formal
  Laurent column Gram150I and compare the COMPLETE q matrix to the fixed one.
- Creation: source degree1 identically0,236 parity-allowed/226 structural
  zeros, c0 only even-sector>=2 and c2 only<=4. All-phase mass1.
- Hand fixture: independently enumerate the720 six-input permanent monomials
  for n=(4,2,0,0,0,0), then DIVIDE coefficients by4!2!. Compare integer-Q
  c0=(-35050,1000),c2=(175,-1000),r_n=-124/421875. This does not aggregate a
  decoded response. The fixture was independently derived before code.
- Six COMPLETE marginal PMFs,7 bins each: compare with exact q-only PGF
  coefficients. All42 bin phase harmonics must vanish; no clipping/reweighting.
- ALL83 joint factorial moments of orders1..3: compare constant and harmonic
  parts with the q-only P1/P2/P3 formula of P56. Repeated indices included.
  The formula is transcribed in ordered-index form; the qualification checks
  identity-source moments and the known two-photon HOM law independently.
- Decoder: enumerate ALL20 triples for EVERY occupation; maximize observed
  count sum and average uniformly over ALL winners. No rejection, favorable
  partition or complement quotient before averaging. Required tie support
  is{1,2,3,4,6,10,20},LCM60. Per-state crossing incident sum3,total9.
- Aggregate all15 edges and ten unoriented classes (canonical side contains0)
  DIRECTLY from those uniform ties. Independently check the10x10 cut-crossing
  Gram with diagonal9/off5, and for every coefficient of every class verify
  pi_class=(sum_edges_crossing_class f_e-5)/4. Its slope obeys the same /4
  identity without the constant. All-phase class mass1, six incident sums3
  and total edge mean9 are checked as exact spectra.

The main calls no archived production module. Independent precode proof
b7341f9/59dc56e is a convention/fixture dependency, not a newly executed
independent replication. No LP, phase scan, graph, seed, API or QPU is used.

## Small qualification, then single full main

`tests/test_p59_exact_fixed_response.py` contains16 SMALL synthetic items.
It NEVER calls `calibrate`, `main`, or six-photon `creation_coefficients`.
Only the single-occupation720-term permanent is evaluated for six photons.
The only full source multiplication is the THREE-output two-photon HOM
fixture. Other guards cover arithmetic, integer rejection, Gram/q/phase sign,
decoder ties, class Gram/inversion, moment targets and exact serialization.
No graph, count draw or actual462-response aggregation occurs in qualification.

After a separately reviewed qualification receipt, one separately authorized
main may create `experiments/P59_fixed_response/run_001/data` (fresh path;
the parent runner creates run_001, the child creates its data subdirectory).
The source/parameters/precision/caps do not change between these two commands.
No retry, second center, rotation flip, precision escalation or replacement
parameter is authorized by either PASS or failure.

## Closure, resources and immutable outputs

Both JSON contracts list the same13 exact source/convention inputs, including
themselves, tests, pinned P56 lemma, independent precode proof, AGENTS.md and
dependency pins. Imported scientific project dependencies: NONE; stdlib only.
Pinned interpreter Python3.11.15; qualification also uses pytest8.4.2.

CPU20s/wall30s/thread1/logs4MiB/scientific output4MiB;64MiB planned logical
scientific workspace, NOT a Darwin RSS or affinity guarantee. No runtime
calibration. Before outcomes, the source multiplication is bounded by at most
3*C(t+5,5) occupation/phase keys at stage t<=6 and six transitions per key.
For a very conservative arithmetic bound, entry coefficient L1<=11 and ring
products cost at most2 in L1. The total coefficient L1 is at most32*66^6<2^42;
probability numerators before rational reduction are below2^96. No int64 cast.
Coverage is exactly462 states,42bins,83moments,
15edge responses and10class responses, all checked explicitly. The logical
workspace estimate counts at most1386 final coefficient pairs,462 raw records
with25 rational decoder weights each,125 invariant records, two JSON buffers
and gzip. This stays comfortably inside the declared64MiB logical budget;
it is an a priori estimate, not a measured hardware-memory result.

Main results are THREE files: `raw.json.gz` (all zero/source/kernel/spectrum
rows plus42PMFs/83moments), `summary.json` (all15/10 responses and status),
and `failure.json` (null on success). Check the4MiB scientific budget BOTH
before and after gzip; mtime0 makes gzip deterministic. The runner writes
stdout/stderr/v2 manifest separately and caps logs. On an ordinary exception,
save the FIRST error type/message/traceback in failure.json and re-raise.
If killed by the external resource bound, partial files/logs/manifest remain;
missing declared results do not change resource inconclusiveness into success.

## Frozen interpretation

1. Failed invariant: IMPLEMENTATION_OR_CONSTRUCTION_FAILURE, no mean-channel
   conclusion. Preserve first evidence; do not patch then claim the first run.
2. Any r_e!=0: NONZERO_FIXED_CENTER_EDGE_RESPONSE; actual decoded mean phase
   channel at constant q/low moments, but no six-particle/classical advantage.
3. All r_e0, some cos2!=0: ZERO_CENTER_SLOPE_WITH_FINITE_PHASE_MEAN_CHANNEL;
   the center0 gradient rule fails. Do not declare phase blindness or rescan.
4. Both response types zero: ALL_DECODED_EDGE_MEANS_PHASE_INVARIANT for this
   family/decoder. No universal optical obstruction or sampling/tail claim.

For graph weights A_e>=0, the previously fixed rule is phi=-h/M with
h=sqrt3 sum A_e r_e,M=sum A_e B_e. If h!=0 its CONDITIONAL mean gain is at
least h²/(2M); if M0 choose0. No graph or phase is evaluated in this main.
Calibration, storage, phase precision and all later physical/classical costs
remain paid. N6 has only10 complementary cuts, trivially classically searched.
No favorable edge/graph, C*, known partition or novelty/held-out/hardware/paper
claim can be inferred. Full-count phase/sphere and independently optimized
species/classical controls are necessary before any future algorithm test.
