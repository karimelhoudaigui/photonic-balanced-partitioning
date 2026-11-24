# P42 exact-author-version independent proof audit

Reviewer: p41_adaptive. Reviewed author commit
`525e2549907a478623df7c0e49190c423e5e8291`, artifact
`theory/P42_threshold_loss_obstruction.md`, SHA256
`01f98f59e975e783bfbb95bf2003fab435732797141bdb5196222dbd460aac4d`.

**Primary verdict: proved as written**, with the full source/channel/readout,
prior-history, cost and exclusion clauses retained. The verdict does not
authenticate novelty, actual Lucy calibration, implementation or run output.

## Independent derivation provenance

The source card was supplied without the author argument. My initial spectral,
threshold and adaptive-search reconstruction was committed as bbeb0cd before
the author file was read. The photon-number nonmonotonicity counterexample and
a local text correction were committed as ed54866, still before comparison.
The independently found simpler eta<=1/5 bound was included in bbeb0cd and
communicated to the root before author525e254 was examined. The author note
attributes this improvement explicitly.

Shared P41/R3 project context is disclosed. I had no authorship role in the
root's initial P42 proof. The internal-species domain counterexample was
committed separately as6929fed. No mathematical computation or QPU call was
executed for this reconstruction or audit; source hashes were obtained as
metadata only.

## Quantified object and assumptions

There are m=2k graph modes, k>=2, and M>=max(m,N) physical modes. Each trial
starts with one internally IDENTICAL photon in each of N distinct inputs.
The loss is uniform independent passive survival eta, without access to its
current-trial lost-photon identities when choosing the passive U. Graph and
prior classical-history dependence are unrestricted. All physical output
modes are observed or required empty with their rejection charged.

The event is exactly k clicked graph modes S and no others. It includes all
occupations positive on S, including collisions and ell>k. Current-trial loss
feedback, hidden outside modes, fabricated clicks, classical completion and
arbitrary input resources are excluded by the note's scope. These exclusions
are mathematical hypotheses, not optional experimental conveniences.

## Dependency and obligation audit

### 1. Conditional source spectrum — PASS

Uniform loss can be moved before the passive unitary. Its environment states
for different lost subsets of distinct source modes are orthogonal. Hence
the unnormalized ell sector is eta^ell(1-eta)^(N-ell) times a rank
binom(N,ell) projector onto singly occupied input subsets. Passive Fock
evolution preserves that spectrum. The binomial multiplicity is already the
projector's trace and must not be multiplied in a second time.

This step remains valid with extra physical modes M because all extra outputs
are required vacuum. It would not be valid with an unobserved current-loss
record used for the same attempt's feed-forward. The author excludes access
to lost identities and coherent feed-forward in its final scope paragraph.

### 2. Threshold projector rank — PASS

For ell>=k, occupations positive on exactly the k modes of S are counted by
binom(ell-1,k-1). Outside S every physical mode is vacuum. Thus the accepted
projector has precisely this spatial Fock rank. The projector-overlap bound
Tr(PQ)<=min(rankP,rankQ) gives equation(1), including every survivor sector
and collisional occupation. This is a physical unconditioned probability bound.

For strict total=k PNR only ell=k remains. Rank1 gives the sharper
eta^k(1-eta)^(N-k) cap. Its asserted sharpness is correct: route a chosen k
source inputs to S and the others elsewhere by a permutation; exactly those
k survive with the stated probability. The general threshold rank cap is
not asserted attainable, appropriately.

### 3. Source-size maximization — PASS

The author takes max over all explicitly allowed N, not just Nmax. This is
essential: my precomparison example has
b_(5,3)=eta^3[1+eta(1-eta)] greater than
b_(6,3)=eta^3[1+3eta^2(1-eta)] when0<eta<1/3. A monotonicity shortcut from
the binomial survival-tail theorem would be wrong here.

### 4. Adaptive best-cost distribution — PASS

For any fixed target A of balanced graph subsets, every conditional optical
hit probability is at most |A|b. If L=ceil(nQ/nC)>=1 and LDb<=1, this is
at most p/L for p=|A|/D. Failure-history induction then gives

    Pr_Q(no hit) >= (1-p/L)^nQ
                   >= (1-p/L)^(L nC) >= (1-p)^nC.

The last inequality is integer Bernoulli; the previous one uses nQ<=LnC.
Taking every cost-sublevel target proves first-order stochastic domination
of best measured cost. No evaluation of p_B/q, transcript garbling, or coupling
between divergent adaptive histories is hidden here: the reference is uniform
and the same target cap holds at every history. This correctly avoids the
non-extension identified in the P41/R2 audit.

The empty/full target cases are harmless. nQ=0 is handled separately by the
author; nC=0 supplies no certificate. A common fixed frontend/incumbent can
be conditioned upon. Adding extra adaptive classical discoveries to the
optical event would change the object and is expressly excluded.

### 5. Costs, floors and classical queries — PASS in the stated model

nQ is an upper bound on charged fresh physical attempts; nC is a guaranteed
positive integer number of uniform feasible draws. Fixed or deterministic
upper-classical/lower-optical cost bounds give the stated floor counts.
Mean latencies do not suffice. Any binding graph-score cap must reduce nC,
as the author explicitly notes. More optical training costs cannot invalidate
an upper bound already granting those costs optimistically.

The blockwise remark is understood with enough classical draws to cover all
blocks, equivalently nQ<=LnC. It cannot be used to ignore the partial-budget
floors merely because a primitive-cost ratio is below an integer L.

### 6. Both analytic survival constants — PASS

The independent stronger bound drops the factor(1-eta)^(N-ell)<=1, keeps only
the positive-composition rank and extends its series. For0<=eta<1 this gives
b<=[eta/(1-eta)]^k. Thus eta<=1/5 implies

    D b <= binom(2k,k)/4^k < 1,

certifying equal counts. The exact finite L criterion and the treatment of
eta0 do not require logarithms or divisions by eta.

The earlier root bound is also valid, not a contradiction. For eta<1/2,
the positive series at r=eta/(1-eta) gives

    b <= (1-eta)^N [eta/(1-2eta)]^k
      <= [eta(1-eta)/(1-2eta)]^k.

The condition4eta(1-eta)/(1-2eta)<=1 is equivalent to
4eta^2-6eta+1>=0. In the stipulated domain it holds exactly up to
(3-sqrt5)/4, approximately.190983. This is weaker than1/5 but correct.
For strict PNR the author uses b<=eta^k, giving the separate sufficient
eta<=1/4. None of these constants is claimed to be a sharp hardware threshold.

## Domain counterchecks and interpretation

The source and detector restrictions cannot be removed by calling the ideal
case optimistic. The independently stored nonextensions are valid physical
counterexamples: bunched input, current-loss herald routing, or a partially
distinguishable internal-species model can violate the identical-source cap.
The author does NOT claim these models are covered. The companion general
source/internal-opacity extension is outside this audit and was not read.

The theorem does not ban arbitrary graph encodings, completion of shorter
strings, quantum memory, non-Fock resources or high-transmission proposals.
It also does not assert a runtime ratio from uncalibrated loss data. The
scope is nevertheless substantive: it bounds all fixed-readout adaptive
passive threshold controllers in its stated low-survival/cost regime, not
only a particular optimizer or graph ensemble.

One terminology recommendation, NONBLOCKING and not an instruction to edit
active experiment inputs: the header "low-loss regimes" would be clearer as
"low-survival" or "high-loss regimes", since eta denotes survival. Also the
absence of same-trial loss-identity feedback could be repeated upfront rather
than left to the final exclusion list. Neither changes the proof in its full
current scope.

## Final status

No proof gap or counterexample was found within the exact stated identical-
photon model. The independently reconstructed source spectrum, threshold
rank, finite-budget inequalities and improved eta1/5 constant agree with the
author's frozen note. The mathematical verdict is proved as written.
External attribution/novelty, the actual physical model of Lucy, observed
efficiency and calibrated cost bounds remain separate obligations. No finite
table, implementation, active experiment input or historical result was changed.
