# P60: phase-average envelope, sharp pair factor, and its actual scope

Status: **proved with explicit hypotheses**. The Cauchy envelope and
conditional rejection construction below are valid. A fixed-budget
'c baseline shots dominate one target shot' inference is refuted. For the
stated finite P59 calibration, a table-based classical replacement is a
mandatory control, subject to verifying and paying its actual table and
precision costs. This note is not a universal classical no-go or a positive
optimization result. Novelty is OPEN; the proof is elementary and no
literature-priority assertion is made.

Static derivation only: no code, imports, graph, numerical experiment,
random draw, source-table evaluation or QPU call. New isolated worktree
.local/p60-physics, branch research/p60-physics. P59's future source code
and its actual calibration table have not been reviewed in this note.

## 1. Complete-law polynomial envelope

Let n range over the complete orthogonal measurement outcomes, including
collisions, vacuum, loss/failure flags and every other retained event.
Suppose its amplitude is

    A_n(z)=sum_(j=0)^R a_nj z^j,       z=exp(i theta),

and sum_n |A_n(exp(i theta))|^2=1 at all physical phases. The coefficients
must be fixed as theta changes. A fixed stochastic decoder K(S|n) has
nonnegative weights and sum_S K(S|n)=1. In the proposed protocol it is
graph independent; mathematically the proof only requires the SAME kernel
at every phase, conditional on any shared graph/history information.
Write p_theta(S)=sum_n K(S|n)|A_n(exp(i theta))|^2.

Choose any fixed phase origin gamma and the R+1 equally spaced phases
theta_l=gamma+2*pi*l/(R+1). Discrete character orthogonality gives

    q(S) = (1/(R+1)) sum_l p_theta_l(S)
         = sum_n K(S|n) sum_j |a_nj|^2.

Indeed every nonzero difference j-k has absolute value at most R and is
not a multiple of R+1. Pointwise Cauchy then gives

    |sum_j a_nj exp(i*j*theta)|^2 <= (R+1) sum_j |a_nj|^2,
    p_theta(S) <= (R+1) q(S).                              (1)

Summing over any event E gives the same domination for event probabilities.
The probability Fourier degree is at most R, rather than2R: its frequency
indices are the differences j-k. A removable monomial factor or finite
Laurent interval can be treated using its exponent width. More generally,
if only T charge coefficients are present, Cauchy's factor is T, provided
the chosen averaging measure actually cancels every cross-frequency of
those charges. T arbitrary roots do not automatically do that for an
arbitrary lacunary charge set.

Vector-valued coefficients in an unobserved environment obey the same
Hilbert-space Cauchy proof. Thus a common phase-independent trace-preserving
channel after this family is allowed, with all its outcomes retained.
It does not follow that an arbitrary noisy preparation preserves the same
charge support or that a calibrated hardware source meets these hypotheses.

Operationally q is sampled by choosing one fixed reference phase uniformly
and making ONE circuit attempt, using the same decoder and denominators.
For degree bound R=2, phases0,2*pi/3,4*pi/3 give the valid factor3 control.
These phase choices are graph blind; the encoded circuit and hence q may
still depend on the graph. In particular **q is still a quantum sampler**
unless an additional classical construction is supplied. Dephasing one
bounded charge removes only coherences between its sectors, not arbitrary
many-photon interference within a sector. A phase-independent bosonic
family is an immediate limiting example where q=p has no new simulation
guarantee from (1).

## 2. P59 isolated-pair refinement: two charges, not three

For an isolated perfectly indistinguishable occupied pair at an exactly
balanced splitter, the HOM state has only the |2,0> and |0,2> occupations.
Apply the variable phase to one of these modes BEFORE subsequent mixing
with spectators. The two branches acquire charges0 and2. Any fixed later
passive network and fixed other input photons preserve amplitude linearity:

    A_n(phi)=C0_n+C2_n exp(2i phi).

There is no charge1 term. Consequently

    q(n)=(p_0(n)+p_(pi/2)(n))/2=|C0_n|^2+|C2_n|^2,
    p_phi(n)<=2q(n),        p_phi(S)<=2q(S).                (2)

This is sharp as a general two-charge statement. It is the preferred
prospective phase-average control for that exact source family; the
three-phase/factor3 version remains valid but looser. Unequal splitting,
nonidentical internal states, an overlapping earlier source mixer, or a
phase arm containing other photons can invalidate this two-charge proof.
One must inspect the actual source and charge support; 'two photons' or
'one variable phase' alone is not sufficient.

## 3. What (1) and (2) do NOT imply about a shot budget

Even for iid observations, p(E)<=c q(E) does NOT imply

    1-(1-q(E))^c >= p(E),

nor domination of T target shots by cT baseline shots. A physical pair-MZI
example has p_phi(E)=cos^2(phi-pi/4), where E is its CF return. The fixed
offset is part of the circuit. At target phi=pi/4, p(E)=1. Both reference
phases0 and pi/2 have success1/2, so q(E)=1/2. Two iid q attempts hit with
probability3/4<1. Even one attempt at EACH reference phase has the same3/4
hit probability, so deterministic root allocation does not rescue it.
Appending untouched spectator photons does not alter this counterexample.

More generally, when p(E)=c q(E)>0 and c>1, Bernoulli's strict inequality
gives (1-q(E))^c>1-c q(E), hence the proposed implication has the wrong
direction. A union bound only yields P_p(hit in T)<=c*T*q(E), whose right
side is not the actual q hit probability. For fixed iid event laws, the
expected hitting-time inequality E_q[tau]<=c E_p[tau] is valid when q(E)>0;
it is a different statement and still assumes comparable proposal costs.
No such simple claim is transferred automatically to distinct adaptive
histories or graph-dependent proposal mechanisms.

## 4. Exact rejection replacement, with its missing algorithmic hypotheses

Suppose q has an actual classical sampler and p_theta(S)/q(S) is computable.
For q(S)=0, domination guarantees p_theta(S)=0; never form0/0. Draw S~q and
accept it with probability p_theta(S)/(c q(S)). Its total acceptance
probability is1/c and its accepted law is exactly p_theta. Therefore the
expected number of q proposals is c, geometrically distributed, NOT a
deterministic c-shot budget. All candidate generation, likelihood evaluation,
randomness, rejection and decoder costs belong in the comparison.

The likelihood requirement matters: p_theta can involve hard permanents.
An envelope does not provide their values, a classical q sampler or a cheap
implementation. For an adaptive target policy, the same rejection can
reproduce its transition at each current history if those requirements
hold conditionally there. History changes only on acceptance. Expected
proposal count for T simulated target steps is cT; fixed-budget trajectory
or hitting domination still does not follow. Any history-dependent table
rebuild or phase selection is paid.

## 5. The finite N6 P59 table makes that control concrete, conditionally

For the stated ideal six-photon/six-mode calibration there are
binomial(11,6)=462 complete Fock occupations. If the already proposed
C0,C2 table is fixed before graphs and q has the stated exact rational
weights, it can be precomputed/stored and sampled by integer cumulative
weights or an exact rational alias table. This is a finite, practical
classical control; its rationality, source alignment and actual code still
need to be verified rather than inferred from Cauchy alone.

For a stored row, set h_n=conjugate(C0_n)*C2_n. Then

    p_phi(n)/q(n)=1+2 Re[h_n exp(2i phi)]/q(n),
    acceptance=1/2+Re[h_n exp(2i phi)]/q(n).

The bounds0<=acceptance<=1 follow from2|h_n|<=q(n). After a table lookup and
one phase's cosine/sine preparation, the per-proposal likelihood uses a
constant number of arithmetic operations, without a new permanent. Expected
proposal count is exactly2 under the ideal normalized law. Sampling n first
and then applying the SAME stochastic decoder also reproduces its complete
decoded law, including collisions, ties and adaptive history. It is not
necessary to compute a summed decoded likelihood if n itself is retained.

Charge all coefficient/q/alias preprocessing, storage, random bits, phase
selection, trig/précision and decoder work. Arithmetic-operation O(1) is not
constant bit complexity. Exact rejection requires exact algebraic
probabilities or a suitable real-probability oracle/refinement procedure;
ordinary rounded cosine/acceptance values give an approximate sampler.
There is no unconditional polynomial-time claim for arbitrary exact-real
inputs or near-boundary numerical comparisons. A fixed finite phase grid
may make exact arithmetic easier, but its actual conventions must be shown.

The462-state count is for the stated ideal fixed-total law, not automatically
an all-loss-sectors or calibrated internal-noise table. For growing photon
and mode counts, the complete coefficient table can be exponential; nothing
here supplies a scalable classical construction. Conversely, for this
small pretabulated calibration it would be misleading to compare only to
generic D/b4/phase controls and omit the exact-law classical replacement.

Accordingly P59's required controls are the fixed two-phase bosonic mixture
and, when its finite table is established, the paid table/rejection
classical replacement. Neither control is by itself a matched-cost theorem,
an unknown-optimum discovery, a novelty claim or completion of the positive
scientific objective. Source/caller audits and any numerical evaluation
remain separate tasks, requiring their own freezes and authorization.

### Raw P59 coefficient convention (normalization clarification)

The 'stored row' formulas above use normalized Fock amplitudes C0_n,C2_n.
They must not be applied to raw creation-polynomial coefficients without
their common Fock/source normalization. Under the supplied P59 convention,
write f_n=prod_i n_i!, D=150^6 and raw coefficients c0_n,c2_n. Then

    C0_n=sqrt(f_n)/150^3 * c0_n,
    C2_n=sqrt(f_n)/150^3 * c2_n,
    q_n=f_n (|c0_n|^2+|c2_n|^2)/D,
    H_n=f_n c2_n conjugate(c0_n)/D,
    p_phi(n)=q_n+2 Re[H_n exp(2i phi)].

Consequently the common f_n/D cancels in the likelihood ratio. At a
positive-q row the rejection acceptance is

    1/2 + Re[c2_n conjugate(c0_n) exp(2i phi)]
                / (|c0_n|^2+|c2_n|^2).

The q alias/cumulative table itself must STILL include f_n/D; cancellation
only applies to the row's ratio. A zero denominator means q_n=p_phi(n)=0
and is never sampled by an exact q sampler. These are algebraic conversion
identities for the stated raw convention; the separate P59 source audit
must verify that its actual coefficient construction has that convention.
