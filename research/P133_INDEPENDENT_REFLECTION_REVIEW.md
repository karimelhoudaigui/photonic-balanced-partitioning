# P133 — independent rational-reflection proof audit

Reviewed 2026-11-26; all93 lines of `research/P133_RATIONAL_RECEIVER_REFLECTION.md`.
Exact source commit: `f09300740aa2fe59fba83c400ae9b71740ecb484`.
SHA256: `56720652d4dbf7c2053ff5599fcfa1bbb1f88e632a3256ee8b9ece5c9735c98d`.
The Git-pinned text was read in full; the current ROOT file had zero diff and matching SHA.
Reviewer is not P133's author; ROOT supplied the candidate. No separate author verdict was read.
P109/P126 source contracts were read only to delimit their screen hypotheses, not to re-audit their entire proofs.
Reviewer authored P129; this is not a new independent review of that dependency.
No script/import/AST/test/RNG/raw-data/native/experiment or external priority search occurred.

**Primary verdict: proved as written for the rational construction, Gram identities, graph full-rank property and non-gauge-positive witness.**
The screen applications have the restrictions below; the useful four-source optimizer bridge remains OPEN.
There is no identified physical counterexample and no accepted advantage or new passive-instrument class.

## 1. Projector, occupied columns and full-attempt law

For arbitrary F in Q(i)^(r-by-k), H=F†F is positive semidefinite.
Thus I+H is positive definite, Q=(I+H)^(-1) exists in Q(i), Q†=Q and HQ=QH=I-Q.
For V=[F;-I], V†V=I+H, so

    P†=P,  P²=VQ(I+H)QV†=P,  U†U=(I-2P)²=I.

Block multiplication gives exactly (1). In particular the LAST k columns are
`[2FQ; I-2Q]=[T;-D]`, because `(I-H)Q=2Q-I=D`.
Preparing the first k columns instead would be a different experiment.
The intended input occupies modes r,...,r+k-1 in zero-based indexing, with every other input vacuum.

Since D is Hermitian and commutes with H,Q,

    T†T=4HQ²,  D†D=(I-H)²Q²,
    T†T+D†D=[4H+(I-H)²]Q²=(I+H)²Q²=I.

These also hold for rank-deficient or zero F; the -I block keeps V full column rank.
An F singular value s gives signal singular value 2s/(1+s²)<=1, with equality iff s=1.
Neither large s nor a full-rank F certifies strong signal transmission.
For all normalized full-U output occupations, unitary Fock evolution has total probability1.
With known CF input, receiver-CF Y probabilities are precisely `|per(T_Y)|²` and `per(|T_Y|²)`.
Every other full record maps to the same hold atom; its mass is `1-sum_Y p(Y)`.
There is no collision/loss conditioning or factorial missing from these CF formulas.
The ten-mode/four-photon and sixteen-mode/four-photon counts, with15 and495 CF targets, are correct.

Rational Gaussian elimination or fraction-free inversion has polynomial bit cost in the fully encoded input.
Clearing denominators and bounding determinant/minor bit lengths provides the ordinary finite-bit justification.
This eliminates the inverse square root in the algebraic target; it does not make mesh synthesis, physical precision, calibration or setup free.
Also `exp(-i*pi*P)=I-2P` shows that this remains a static passive reflection, with no feedback/nonlinear instrument.

## 2. Graph family and the hand witness

Assume distinct prototype vertices, r>=k, rational nonnegative graph weights and the stated beta/kappa range.
The strict +1 in W gives |d_j|/W<1, hence every prototype diagonal entry of A0 is strictly >1/2.
The prototype block is A0+iB0 with B0 real symmetric. For nonzero x, x†B0x is real and

    Re[x†(A0+iB0)x]=x†A0x >= min_diag(A0)||x||² > ||x||²/2.

Cauchy implies `||(A0+iB0)x|| >= min_diag(A0)||x||`.
Adding the remaining receiver rows cannot decrease this norm; F therefore has smallest singular value >1/2.
This full-rank argument does not replace the earlier rank-free projector proof or imply a useful cut bias.
At beta=kappa=0, H=I, Q=I/2, T is the prototype injection, and D=0.
The known deterministic receiver candidate must be credited to classical controls, as the source states.
Fresh boundary fields still require their full graph work, unless an explicitly paid/shared cache supplies them.

For F=[[1,i],[i,1]], direct multiplication gives H=2I, T=(2/3)F and D=-I/3.
The rectangle product is `(2/3)^4*(-i)^2=-16/81`.
Input/output diagonal phases cancel from a rectangle product; entrywise nonnegative matrices give nonnegative products.
Thus this T is not gauge positive. This is not a proof of non-gauge-real chirality: this two-by-two example is gauge equivalent to a signed real Hadamard matrix.

On the supplied four-vertex graph, S0 is empty, d1=d2=1+1/2+1/2=2 and W=1+2+1=4.
Taking beta=0,kappa=4 therefore realizes exactly that F with rational data.
Its permanent vanishes, while the D coincidence is `2*(4/9)^2=32/81`.
However the only receiver set {1,2} is S^c, so both it and S={3,4} have cut2.
Accordingly this witness has zero feasible improvement utility for BOTH arms.
It proves a compiler/gauge/count contrast, not a favorable or unfavorable graph-utility contrast.

## 3. Existing screens, without enlarging their hypotheses

**P99:** a reflection at projector phase pi is not automatically its dense real symmetric weak-time family.
The prescribed coupling floor, small-time threshold, source/complement orientation and available doubled time must all hold.
Here graph features also depend on the current residual. Complex entries alone do not establish a universal escape;
a special admissible subfamily still needs the P99 control.

**P109:** Cauchy gives `|per M|²<=k! per(|M|²)` for each full-k occupation matrix, with its output factorial retained.
An admissible cT with c^(2k)>=k! therefore dominates raw receiver-CF probabilities under the common CF/hold contract.
This implies fixed-incumbent retained-improvement and independent best-of-T order, not arbitrary adaptive chains or matched wall cost.
The ratio of the signal singular values for aF and F is `a(1+s²)/(1+a²s²)`, generally dependent on s.
Thus scaling F is not automatically the required common cT control; neither is removing fixed device loss.

**P126:** its exact contract is fixed-few-loss signal sectors with the rest aggregated as FAIL.
P133's CF/hold observation can use its r0=0 full-survival/FAIL view followed by common collision holding.
It does not replace a fully resolved signal-plus-dump PNR law, quantum state or arbitrary all-loss observation.
Its counting primitives require a supplied NONNEGATIVE RATIONAL matrix after the phase gauges, with their verified finite-bit interface.
If “rational gauge positive” means only T in Q(i) and existence of a positive gauge, that is insufficient by itself:
for example T=[(1+i)/2] has positive-gauge magnitude1/sqrt(2), which is not rational.
One needs an explicit rational positive representation or a separately controlled approximation/extension.
This is a screen-input qualification, not a counterexample to the reflection or to physical gauge invariance.

**P129:** the rational T removes its matrix-encoding obstacle, but the stated certificate still needs ||T||²<=eta<1.
If an F singular value is1 then signal norm1 is possible, so no strict-eta certificate exists.
The separately justified eta=1 endpoint uses L=K and fixed-sector error `1-k!/k^k`; it does not rewrite P129's strict header.
Where the norm-certified structural bound is large it supplies no sharp practical veto; complex signs supply no exemption where it is informative.
The frozen P131 implementation is bounded K<=7/M<=8; its unexecuted prospective qualifier covers K<=4, not every P133 dimension.

For k4, the proper source-species partitions number7 with two blocks,6 with three, and1 fully distinct:14 total, including D.
Each requires independent parameter optimization and its own paid setup/grant; a free best portfolio would be a different comparison.
The mandatory exact-law/FAST/pair/beam/frontier controls remain useful practical tests even though no asymptotic runtime ordering follows.
The first unclosed bridge is a useful four-source raw CF/hold statistic after compilation, all attempts, all scored candidates and these controls are charged.
No new population, implementation, experiment, hardware certificate, priority claim or positive optimizer verdict follows from this review.
