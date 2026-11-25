# P61 static device/protocol review and pre-data amendments

This reviews the communicated PROPOSAL, not an implementation or an executed
card. No code, imports, graph, sample or numerical computation. Construction
and normalization are valid. However the proposed phase has EXACT three-mode
support, and the separately frozen frontier theorem supplies a stronger
classical best-of-trials comparator under the proposed uniform independent
embedding. **Do not implement/run this pilot before ROOT's proof review or
a refutation/change of those assumptions.** No global positive-goal closure,
universal matched-time no-go or novelty conclusion is asserted.

## 1. Exact unitary, intensities and low moments

Put N18=3d, d6, rows r=da+i and columns s=db+j. With normalized Fourier
matrices, the proposed device is

    U(phi)=V (F3 tensor I_d) D(phi) (I3 tensor F_d),

where D phases the SINGLE intermediate mode(b1,i1), and V rotates outputs
0,d by[[3,-4],[4,3]]/5. The stated scalar entries before V are exactly
omega3^(ab) omega6^(ij) exp(i phi 1_(b1,i1))/sqrt(18).
All factors are unitary. Equivalently, column orthogonality follows by
summing omega3 over a first for unequal b; when b agrees the phase cancels
and the omega6 sum supplies the remaining orthogonality. No flatness or
nondegenerate eigenbasis is needed.

The two mixed rows have i0, so neither carries the variable phase. In the
common unnormalized Q convention, U=Q/sqrt(450), their intensities are

    row0: six entries1/450, twelve entries37/450,
    row6: six entries49/450, twelve entries13/450,
    other16 rows: all entries25/450=1/18.

For a fixed input block b these follow from3-4omega3^b and4+3omega3^b.
Every row and column sums to one. q is exactly phi independent; D's entire
labelled-photon count law is therefore phi independent for each fixed V.
For full1^18 identical input the B means are one, full single-mode PGFs
are sum_h h!e_h(q_row)t^h, and all joint factorial moments through total
degree3 are q-only by the square/full-CF theorem. None of this proves a
nonzero decoded mean response.

D's independently tuned gamma grid is genuinely stronger than D at B's V:
rows0,d have intensities[1-2cs cos(2pi b/3)]/18 and
[1+2cs cos(2pi b/3)]/18, c=cos(gamma),s=sin(gamma). The declared seven
gammas include B's atan(4/3), and phase is redundant for D. Four training
draws per gamma give28, followed by16 fresh draws at its own selected gamma.

## 2. Charge support is six, although polynomial degree is six

Only the six input columns in block b1 can contribute a phase factor.
The phase-arm photon number L immediately after its full-CF Fourier6 has
PGF sum_h h!*binomial(6,h)*(t/6)^h. Its exact ordinary PMF is

    P(L=0..6)=(155,84,45,20,15,0,5)/324.

For example P(L5)=5!*6/6^5-6*6!/6^6=0. The amplitude support is therefore
charges{0,1,2,3,4,6}; the coefficient of charge5 vanishes IDENTICALLY, not
only after a decoder. Fixed subsequent unitaries preserve these zero/norm
sector identities. Seven equally spaced phases integrate all probability
harmonics through degree6 exactly. P60 gives p_phi<=6 q_phaseavg, sharper
than the loose degree factor7, but q_phaseavg is still generally quantum.

The complete18-photon/18-mode Fock space has binomial(35,17)=4537567650
occupations. That makes the P59-style complete table impractical here; it
does not prove hardness of other samplers or of graph optimization. There
are only binomial(18,9)=48620 feasible subsets, with any exact-optimum
diagnostic kept out of training and fairly budgeted/quarantined if used.

## 3. The knob acts on only three measured modes

Let L0=V(F3 tensor I6), t=(b1,i1). Then

    U(phi) U(0)* = L0 D(phi) L0*
                 = I+(exp(i phi)-1) v v*,
    v=L0|t>,   support(v)=A0={1,7,13},
    v_on_A0=(1,omega3,omega3^2)/sqrt(3).

V acts only in i0, so it leaves this vector untouched. Thus the relative
unitary is LOCAL on A0 and the complete JOINT count law of the other fifteen
modes is exactly phi independent. This is stronger than q/low-moment
invariance and holds even though those modes can be entangled with A0.
Their quantum law need not be classically simulable conditional on a fixed
embedding; locality alone does not supply such a simulator.

The total photon number T in A0 has mean3, variance5. Before the tritters
it is the sum of three independent L variables from the PMF above; subsequent
operations preserve T. It is not capped at three photons, but its mean does
not grow in the extension3d. Under common inactive counts and fresh common
uniform tie priorities, two phase-dependent top9 outputs differ by at most
three exchanges. For each inactive count/order realization, at most eight
balanced frontier completions cover all possible phase-dependent outputs.

The independent reconstruction
`theory/P61_uniform_embedding_frontier_independent_reconstruction.md`
(f301920) proves the stronger conclusion: averaging over a UNIFORM embedding
fixed per graph and independent of G, a PURELY CLASSICAL algorithm drawing
fresh uniform active labels/complement order and scoring all eight frontier
candidates stochastically dominates best-of-T optical decoded costs. The
proof handles fixed-P correlations by Jensen; it does not replace them by
an iid assumption. For fixed P only the quantum-fixed-phase-plus-eight-
completion envelope is immediate, not pure classical domination. Both
comparisons must pay their eight scores and do not imply equal wall time.

The first discriminator is therefore this paid classical frontier envelope,
not another larger-Fock mean signal. Growing the Fock count with fixed active
support does not escape it. An actual escape needs a changed premise, such
as growing active support, a paid graph-informed outside law/mapping or a
different non-topK decoder; it cannot be claimed by a new favorable seed.

## 4. If a revised pilot survives that obstruction, freeze these amendments

- Retain the proposed STAGEDVETO: run all88 B observations and four fixed
  from-raw FAST calls first. A single fixed random OR spectral FAST algorithm
  dominating B's paid best on BOTH graphs rejects the DEV. Optional controls
  then have zero executed draws and explicit NOT_EXECUTED_STAGE_VETO status,
  never PASS. Missing/late FAST snapshots cannot open follow-up. No free
  best-of-two portfolio is used for the fixed-algorithm veto.
- Train each model independently PER GRAPH using all28 normalized-cut
  observations and exact Fraction losses/canonical ties, then16 fresh
  observations. Credit all44 cuts to that model's incumbent. This is not
  P55's one global policy or its photon-neutrality DP. Top9 uses the full
  ranking and uniform boundary ties, including all-zero/variable-total
  product outcomes. Fix whether required D/phase mean vetoes use equal-graph
  mean normalization or per-graph means BEFORE data; follow-up still requires
  strict per-graph improvement over every control and eligible FAST result.
- Compile B's seven graph-BLIND matrices/Gram checks once, allocate their
  actually observed cost once (e.g. half to each graph). Do not duplicate
  this overhead to inflate B's comparator allowance. Charge each immutable
  factory RNG/validation prefix: exclude only its returned optical backend
  WALL, and keep CPU splits unknown. No optional preparation/scoring funds
  B-only FAST. Zero optical latency is an envelope favorable to B, not a
  hardware time model. Reuse only the audited P55 metadata/cost pattern.
- The mandatory P60 control is the bosonic uniform seven-root mixture,
  sampled by one random reference phase per attempt. It is not the coherent
  random-input-phase model. A fresh arm would change the original528-draw
  maximum and must be declared prospectively; do not silently obtain it by
  pooling selected-phase fresh data. The pure classical frontier is an even
  stronger relevant control under the current embedding assumptions.
- At least one at-most-four species grouping should be j-ALIGNED: six
  groups{j,6+j,12+j}, j0..5. Each is a three-photon phase-carrying kernel.
  For fixed j the matrix restriction differs from j0 only by output phases
  omega6^(ij), which V's i0 rotation preserves. Thus the six group kernels
  are IDENTICAL and form a cheap explicit classical control after convolution.
  Random/contiguous four-photon groupings can miss this natural explanation.
  Specify the second fixed <=4 grouping and every group size/seed before
  outcomes; do not force six3-groups into an old helper hardcoded to chunks4.
- The B-marginal product control needs only three exact18-rational q types.
  Compute their19-bin PGFs using Fraction, optionally integer CDF/alias
  weights over450^18. An exact integer sampler avoids Decimal cancellation
  entirely in this small precomputation. Do not condition its independent
  total M back to18; M<=324, including zero, remains part of the null.
- Spherical coherent counts followed by uniform top9 have EXACT uniform
  feasible decoded law for a full-square unitary. Sampling a uniform9-subset
  is a legitimate classical shortcut if labelled as such, not a claim that
  photon counts/collisions were observed. The continuous-phase model instead
  requires full Multinomial(18,|Uz|^2), not the old CF weighted-subset routine.
- Mapping marks, input species roles, special q-row identities and tie
  priorities must be carried under relabeling. A single graph-independent
  random embedding must not be selected for its observed performance.
  Freeze graph generators6101801/02, sorted-edge weights1..5, all namespaces
  and ALL possible training/fresh role seeds before any draw. No C* or
  favorable edge/source/partition enters the phase selection.

All these controls are prospective protocol requirements, not executed
experiments or an implementation request. Under the current theorem's
assumptions no new P61 pilot is authorized or scientifically needed merely
to rediscover a local phase correlation. The larger positive objective,
including any matched total-cost advantage from a different mechanism,
remains OPEN. No paper, hardware preparation or QPU follows this note.
