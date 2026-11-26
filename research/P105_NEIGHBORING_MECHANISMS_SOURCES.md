# P105: neighboring sources translated into small photonic mechanisms

26-Nov-2026; parent `ccb2b032cd7a0c660b6474d1e8452cba99218478`.
**Four transfers, no positive optimizer result or numerical allocation.**
This portfolio targets 4–8 TOTAL orthogonal optical modes and 2–4 TOTAL
input photons, counting internal labels, copies, helpers and their failures.
Each proposed transfer below is distinguished from what its primary proves.

## Existing records and acquisition boundary

Read the full P103 transfer map, SHA256
`8046fad38f0f592105f8b5c76ad3c3ce839c36b94ac60a351f639973c30818ae`,
and the relevant P74 herald-resource record, SHA256
`0b4b4bbca399ab8c80d4b5f152b7eff1f3c8b50c344e3a2d2ab8ba5966cea12b`.
Mukai's single-walker and Bardenet/Fanuel/Feller's DPP/QR statements remain
existing records; they are not rediscovered or promoted to photon theorems.
Anand/JSV/Sinkhorn is ROOT's separate route and is not duplicated here.
The literature-check workflow used primary versioned arXiv, published academic
scans and PMC copies of original articles. Selected definitions/formulas,
algorithm/resource paragraphs and stated limitations were extracted, not
whole-paper proofs. No new external cache/PDF was retained; retained SHA:NONE.

## Primary source cards

S1. Harrison/Smilansky/Winn, *Quantum graphs where back-scattering is
prohibited*, [0708.0839v1](https://arxiv.org/html/0708.0839v1),6-Aug-2007,
Definition1.1/Proposition3.2/section1: unitary coins with zero diagonal and
equal off-diagonal moduli; directed-bond evolution has 2|E| states and its
CLASSICAL counterpart is |U|^2. The spectral claims are not cut-quality claims.

S2. Alon/Benjamini/Lubetzky/Sodin, *Non-backtracking random walks mix faster*,
[math/0610550v1](https://arxiv.org/html/math/0610550v1),18-Oct-2006,
Theorem1.1/Remark2.6: regular graphs with nontrivial absolute eigenvalue
lambda<d have rate psi(lambda/(2sqrt(d-1)))/sqrt(d-1), psi(u)=1 below1,
u+sqrt(u^2-1) above1. Complete graphs can mix SLOWER without backtracking.
Thus neither a tiny dense graph nor a graph optimizer inherits a speedup.

S3. Karypis/Kumar, *A fast and high quality multilevel scheme for partitioning
irregular graphs*, SIAM J.Sci.Comput.20,359–392(1998),
[published scan](https://people.eecs.berkeley.edu/~jordan/sail/readings/karypis-kumar.pdf),
section3, pp.363–365: summed coarse edge weights preserve the cut of a
block-constant lifted partition; vertex masses must also be summed. Heavy-edge
matching/refinement is an effective tested heuristic, not a universal optimum
or a guarantee that the best original partition respects the contractions.

S4. Okamoto/O'Brien/Hofmann/Takeuchi, *Realization of a Knill-Laflamme-Milburn
controlled-NOT photonic quantum circuit combining effective optical nonlinearities*,
PNAS108,10067–10071(2011), DOI10.1073/pnas.1018839108,
[primary text](https://pmc.ncbi.nlm.nih.gov/articles/PMC3121828/), NS-gate section:
the ideal heralded sign on |2> succeeds with probability1/4; two NS modules
give the stated CNOT profile1/16. The actual characterization used fourfold
THRESHOLD coincidences instead of the required herald PNR/loss discrimination;
its Results also disclose background subtraction. It is not a raw-device
feed-forward/PNR certificate for our account.

S5. Matthews et al., *Observing fermionic statistics with photons in arbitrary
processes*, Sci.Rep.3,1539(27-Mar-2013), DOI10.1038/srep01539,
[primary text](https://pmc.ncbi.nlm.nih.gov/articles/PMC3609020/), Results,
equations4–8/Methods: entangled particles pass through identical copies of A;
relative phase pi gives antisymmetric/determinant statistics. The prepared-
source ideal construction needs no further output selection, but the reported
experiment uses postselected polarization entanglement. It requires an actual
entangled source/copy structure, not ordinary product-CF photons.

## A — zero-return phase coin: a local primitive, not a free global walk

1. **Graph structure?** Use directed-arc memory on a sparse residual move graph;
   input port means previous arc. S1's no reflection then means no immediate
   edge reversal. On VERTEX modes a zero diagonal merely prohibits staying put.
2. **Why B?** A four-port zero-diagonal unitary from S1 accepts two CF inputs.
   The exchange term 2Re(C_ac C_bd conjugate(C_ad C_bc)) can alter joint
   move pairs while leaving single-photon intensities fixed. First missing
   bridge: a nonzero useful cost/hitting statistic AFTER decoder and mark average.
3. **Reoptimized D?** Optimize D's coin, phases, times, memory and decoder
   independently; include exact two-particle pair laws and groups2/3. S2 already
   motivates a strong classical no-backtracking control; single-walker gain is free of B.
4. **Classical information?** Arc ordering, residual selection, boundary fields,
   previous edge and phase compiler are public/paid for every control. No optimum-
   chosen port map or favorable label sample may be hidden in the optical source.
5. **Hardware?** A4-port coin is compatible with an ideal passive4-mode block;
   the full coherent walk costs2|E| modes plus repetition/delay resources. A simple
   regular degree>=3 graph already needs at least12 directed modes. With4–8,
   use only a local block/classical outer memory; no large coherent-walk claim.
6. **Falsifier?** Keep all conflicts/collisions/losses paid. Reject the optimizer
   interpretation if a classical arc/pair sampler with the same information or
   independently optimized D matches it. A suppression coincidence is insufficient.

## B — coarse restriction plus exact boundary residual

1. **Graph structure?** Pay S3's hierarchy; freeze exterior, r=2K in {4,6,8}
   unit/equal-mass blocks and K occupied ports. The residual is
   C_R(x)=const+sum_i h_i x_i+sum_(i<j in R)w_ij(x_i+x_j-2x_ix_j),
   h_i=sum_(j outside R)w_ij(1-2x_j).
2. **Why B?** Current-port CF input, passive U_R and CF K-subset output give
   simultaneous swaps. A permanent/cost-quality bridge remains UNKNOWN.
3. **Reoptimized D?** Optimize D on the identical residual; pay the complete
   2^r frontier alongside FAST.
4. **Classical information?** Share/pay contractions, selection, fields,
   lifting/refinement; no optimum masks.
5. **Hardware?** Photon cardinality is not weighted balance; unequal masses
   require a proved decoder and paid rejects.
6. **Falsifier?** A paid-frontier win stops. Restricted optimum is not global
   optimum or hardness evidence.

## C — measured ancillas: genuine interaction, presently a hardware gate

1. **Graph structure?** Encode edge phase exp(i phi n_i n_j). A fixed sign is
   not arbitrary weighted phi; balance-preserving mixing is a separate gate.
2. **Why B?** The conditional |2> sign supplies genuine measurement-induced
   interaction, outside deterministic passive code preservation.
3. **Reoptimized D?** Reoptimize allowed D/heralded circuits; include exact
   tiny logical search, not merely gate-fidelity comparisons.
4. **Classical information?** Share graph phases; pay helpers, preparation,
   failures, detector records and corrections.
5. **Hardware?** Two data photons plus two helpers in an eight-mode two-NS layout carry only
   TWO dual-rail qubits. Cached P74's stronger profile/veto remains intact.
6. **Falsifier?** Require every branch's Kraus/feasibility accounting before
   retries. Coincidence-postselected fidelity does not certify raw operation.

## D — antisymmetric-input repulsion: a strong control, not bosonic advantage

1. **Graph structure?** V†V=I gives q(Y)=|det V[Y,:]|^2. Repulsion need not
   lower cut(Y,Y^c).
2. **Why B?** None: entangled labeled copies supply the minus sign, not
   product-boson exchange. A distinguishable-copy entangled control shares it.
3. **Reoptimized D?** Optimize D independently and retain P103's exact
   classical DPP sampler, which reproduces the target law.
4. **Classical information?** Share/pay kernel/QR, weights, source and scoring;
   no preparation/gate gift.
5. **Hardware?** Two copies of four spatial modes cost eight orthogonal modes.
   This construction uses Nm modes; N>=3,m>=N exceeds eight, not a universal bound.
6. **Falsifier?** Product-CF inputs, mismatched copies or unpaid postselection
   invalidate the map. Repulsion alone cannot beat its same-law control.

## Exact continuation: number-resolved loss holding, not intrinsic washout

P100's frozen washout result concerns ALL failures flipping sigma. For its
known-K source and common uniform loss after U, a different controller can
HOLD (x,sigma) when observed total N<K, and execute the original lossless
lift rule on N=K, including collision/rejection/same-class flips. Then
all-K survival is independent of (x,sigma), and conditional on it the law
is lossless. Therefore

    L_eta=(1-q)I+q L_1, q=eta^K.

This internal deduction preserves Pi and the full embedded sign/destination
law of L_1; waiting/attempt counts multiply by1/q. All lost attempts still
cost K source photons. It needs total-number discrimination and a raw-attempt
denominator, not coherent within-shot feed-forward. Threshold click counts
cannot generally separate loss from bunching. D and classical controls receive
the identical holding improvement. This corrects no P100 byte and proves no
advantage, source efficiency or current Lucy capability.

## Ranking unknowns and the next gate

| Route | Present role | First unresolved bridge |
|---|---|---|
| PNR loss-hold continuation | Exact shared control, highest priority capability question | Raw PNR/attempt visibility, not quantum advantage |
| A local phase coin | Most concrete extra passive primitive | Useful averaged graph statistic beyond D/pair/classical memory |
| B coarse residual | Engineering context and mandatory exact classical frontier | Any optical benefit after identical reduction costs |
| C heralded interaction | Genuine changed resource model | Available ancillas/detectors/corrections and raw cost/feasibility |
| D entangled determinant | Same-law classical/entanglement control | Source/copy certification; no unique B reason |

The ordering is qualitative, not a predicted probability/runtime score. None
authorizes DEV. A future card must freeze source, all-output decoder, graph-
only compiler, relabel/heldout law, independently optimized controls and paid
caps BEFORE execution. Never use C*, known masks or a free best-of-portfolio.
Current PNR, entangled inputs and within-shot feed-forward remain unverified;
P103's simulator/roadmap references are not account capability evidence.
Discovery used six bounded English author/title/mechanism queries, then exact
primary passages. A nonexistent HSWv2 and inaccessible publisher/old author
URLs were replaced by actual v1/PMC texts. No source absence implies novelty.
No imports/AST/code/scientific execution/RNG/graph/native/test/runner/raw-data/
QPU/manuscript/push/checkout/delegation occurred. Only this portfolio was added.
