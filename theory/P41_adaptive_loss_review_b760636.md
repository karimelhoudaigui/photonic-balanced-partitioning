# Exact-version audit of the P41 loss/oracle entropy proof

Reviewer p41_adaptive. Initial reconstruction was frozen in commit fd479d8
BEFORE reading the author proof. Audited author revision:
`b76063645d41d8002041d9c0f6cb2022f0cff06f`, file
`theory/P41_obstruction_loss_entropy.md`.

## Verdict

**Correct only after a stated restriction:** in sectionD's real-log/minimizer
calculation use0<eta<1/alpha. Treat eta=0 separately by a=0 and immediate
classical domination when nC>=1. Equivalently, supply explicit extended-real
endpoint conventions and the limiting minimizer. The nondegenerate finite
and entropy arguments are correct. This is a minor endpoint clarification,
not a counterexample to the underlying survival statement.

The primitive-cost calculation is proved in the mathematical model of fixed
costs (or guaranteed upper/lower cost bounds). Observed average wall times do
not by themselves make exact floor counts guaranteed. The author's conditions
about actually establishing costs/calibration must remain binding before an
empirical hardware conclusion is asserted.

## Dependency and obligation check

1. Necessary event: success entails >=k true photons detected from the same
   fresh preparation. Under conditional independent uniform survival the
   Bin(Nmax,eta) cap holds at EVERY history, independent of the interferometer,
   optimizer, graph or photon statistics. PASS under stated hypotheses.
2. Failure-history induction gives1-(1-a)^nQ without assuming independent
   success events. Arbitrary source choices N<=Nmax and early stopping respect
   the cap. PASS.
3. Complement symmetry gives at least two oriented minimizers. Uniform feasible
   proposals score and retain their best candidate without needing C* or g.
   Their success is at least1-(1-2/binom(2k,k))^nC. PASS.
4. For nC>=1 and nQ>=1, L=ceil(nQ/nC) and La<=p0 imply
   (1-p0)^nC<=(1-a)^(LnC)<=(1-a)^nQ by integer Bernoulli and monotonicity.
   The author handles nQ=0 and nC=0 separately. PASS.
5. The exact logarithmic count comparison is valid on0<=a<1; a=1 and
   zero counts need their ordinary separate limiting treatment. PASS for the
   nondegenerate use in which the sufficient certificate can hold.
6. Exponential Markov with positive t and Nmax<=alpha k yields
   a<=exp(-tk)(1-eta+eta exp(t))^(alpha k). Its stated finite minimizer is
   correct for alpha>1,0<eta<1/alpha. alpha=1 is the infinite-t limit giving
   eta^k. The missing eta=0 branch is the restriction in the verdict.
7. binom(2k,k)<4^k gives the ratio envelope .5 exp[-k(I-log4)]. The
   alpha1 quarter boundary is correctly handled separately: at eta=1/4,
   delta=0 but2a<p0 remains strict. PASS.
8. At alpha2, I=-log[4eta(1-eta)], so the strict entropy condition gives
   eta<(2-sqrt3)/4 within eta<1/2. PASS.

The proofs need no unverified external mathematical theorem beyond the
elementary inequalities explicitly reconstructed. The author's separate
source report is NOT an independent novelty assessment by this reviewer.

## Finite costs and scope checks

The author expressly distinguishes aligned budgets from arbitrary floors.
This matters even when the primitive-cost ratio is an integer: cC/cQ=2
does not force nQ<=2nC at every partial budget. The declared condition uses
actual nQ,nC and is safe. The rate-only counterexample in the initial review
shows why it cannot be replaced by cC a<=cQ p0.

If nC>=1 and costs are fixed, the statement about polynomial cost ratios also
has a direct justification: floor(B/cC)>=B/(2cC), hence
L<=ceil(2cC/cQ). A polynomial primitive ratio therefore gives polynomialL,
eventually below2exp(kdelta) when delta>0. Without nC>=1, no such comparison
is available, and the author does not claim one.

The following exclusions in the author statement are necessary and correct:

- Fixed/common frontend: discoveries made there are outside the optical-stage
  success event. The theorem does not bound the whole adaptive hybrid method.
- Genuine fresh attempts: nonempty provider shots condition away vacuum,
  and cannot be substituted for nQ without denominator/cost accounting.
- Independent loss: marginal transmission alone permits correlated all-or-none
  survival, whose tail can be eta rather than a binomial small-loss tail.
- Photon-per-selected-vertex encoding: decoders requiring fewer than k true
  detections, survivor accumulation, free retries and correction change the
  premise. They are not universally ruled out.
- Measured resource costs: source preparation, training, actual graph scores,
  classical setup and integer budget counts are not free or interchangeable.

The current statement is therefore a graph-universal regime obstruction for
its declared sampling stage. It is not a full-distribution simulation theorem,
an ideal-eta1 obstruction, a global photonic-optimization impossibility, or
experimental evidence about Lucy. The author's scope paragraphs accurately
retain these differences. No model calibration was independently established.

## Independence and remaining action

The initial proof reconstruction and counter-readings are in
`theory/P41_adaptive_loss_review_initial.md`, commit fd479d8. Only afterward
was author b760636 read and compared. Shared project context and the parent's
claim card were available, but no author derivation or verdict was supplied
before reconstruction. No numerical experiment or QPU call was executed.

Resolve the eta=0/domain and fixed-cost wording in a new author revision,
then audit the exact diff and pin its hash. No unchanged simulation campaign
is needed for these analytic clarifications. Originality of the composition
and actual hardware assumptions remain separate obligations.
