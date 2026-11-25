# Independent audit: passive all-CF cost-phase obstruction

2026-11-25. Target ROOT commit
`336a9f877fdb641ffca6c875184a77404cf08f72`, file
`theory/P50_passive_hard_core_cost_phase_obstruction.md`, SHA256
`f819dfac91d6f4544a50e08f23752637df0203edfc773edee2a9eff280cc0523`.
The exact Git bytes were read and hashed. No numerical run, model import,
source modification, graph experiment or hardware call was performed.

**Verdict: proved as written under its exact stated model.** The proof does
not exclude approximate leakage, fixed-input circuits, other encodings,
ancilla/heralded operations, finite isolated phase aliases or P50's all-count
decoder. It supplies no optimizer advantage/no-go or hardware conclusion.
I previously wrote a related cost-phase-route note; this audit is independent
of this proof's author within the same team, not an external or blind review.

## Reconstructed characterization and endpoints

For a normalized CF basis state |A>, the two annihilations must hit distinct
occupied inputs. Each unordered pair occurs twice; both annihilation square
roots are1. Thus

    a_i(out)^2 |A> = 2 sum_(a<b in A) U_ia U_ib |A\{a,b}>,
    ||a_i(out)^2 |A>||^2 = 4 sum_(a<b in A) |U_ia U_ib|^2.

Distinct removed pairs leave distinct residual occupations, so there are no
cross terms. The norm is exactly E[n_i(n_i-1)], including its factor4.
Zero leakage forces it to vanish for each row and each input basis state.
For every pair a,b there exists an r-subset containing it when2<=r<=N.
Every row therefore has at most one nonzero entry. Square unitarity fixes
its modulus to1 and places exactly one such entry in each column. Conversely
a monomial spatial unitary permutes CF occupations with product mode phases.
Checking basis states suffices, by linearity, for the entire subspace.

At r=N there is only one CF basis state, but it contains ALL pairs, so the
argument still forces a monomial U. At r=1 no pair is available and every U
is collision-free, exactly the stated exception. Vacuum is outside the
claimed domain and would also give no restriction. Complex conjugation or
the equivalent input/output convention changes no modulus or factor here.

## Fixed input is strictly weaker

For one fixed occupied input set A, the calculation only separates columns
indexed by A. A concrete nonmonomial example is

    U = [[c,0,s],[0,1,0],[-s,0,c]], c^2+s^2=1, cs!=0,
    A={0,1}.

The occupied columns have disjoint row supports {0,2} and {1}; there can be
no collision, although U is nonmonomial. With disjoint occupied supports,
each nonzero output has a unique source assignment. Its permanent has at
most one nonzero term, so B and D full occupation probabilities coincide.
This validates the proof's narrower fixed-input statement, not a stronger
monomial assertion for an arbitrary experimental source.

## Continuous oracle, permutation and global phase

A continuous path of monomial unitaries has locally fixed permutation:
nonzero entries have modulus1 and cannot move continuously between positions.
For N=2K, K>=2, a permutation inducing the identity on EVERY K-subset must
itself be the identity: choose a K-subset containing i but not its distinct
image. Thus an oracle equal to identity at0 up to encoded global phase has
no hidden nontrivial permutation there; a fixed relabeling convention causes
no loophole. The local generator has diagonal one-mode coefficients only.

If Gamma(U(t)) agrees with exp(-it C) up to a subspace-global phase, the
latter phase can be read from any fixed nonzero diagonal entry and chosen
differentiably near0. Differentiation then gives real c,h_i with

    C(S)=c+sum_(i in S) h_i.

Complement invariance C(S)=C(S^c), |S|=|S^c|=K, forces every K-subset sum
of h to equal half the total. Comparing T union{i} with T union{j}, with
|T|=K-1 and i,j outside T, gives h_i=h_j. The cost is constant on the slice.
No assumption of favorable graph weights or a known optimum enters this step.
Differentiability/continuity over an interval is essential to the statement.

## Finite-angle alias is a real exception

For integer weights and the usual loop-free cut convention,
C(S)=sum_(i in S)degree_i-2 sum_(i<j in S)w_ij. At t=pi the second term is
invisible modulo2pi, so a passive diagonal phase implements the cost phase.
This need NOT be merely a constant phase. On four vertices with the sole
unit edge(0,1), balanced cuts have cost0 or1, and

    U=diag(-1,-1,1,1)

implements exp(-i pi C(S)) on every size2 subset, with both signs occurring.
It is not a family implementing exp(-it C) near0. The target explicitly
retains this exception and makes no universal finite-angle exclusion.

## Encoding and physical scope

The passive no-leakage assumption concerns the WHOLE CF subspace of the
specified N modes. Permanently inactive external vacuum ports change that
quantifier; they must not be silently imported as the same model. Occupied
ancillas, conditioned operations, species labels and loss are excluded.
Dual rail is a proper code subspace: independent within-pair beam splitters
can preserve one photon per pair without being monomial on all spatial modes.
This observation does not itself provide an entangling oracle for dual rail.

Similarly a projected hard-core generator PHP can have hopping terms while
the full bosonic generator leaks. In general exp(-it PHP) is not
P exp(-it H)P. A final successful projection or repeated nondestructive
checks require their own map, failure probabilities, ancillas and resource
accounting; they do not establish the deterministic hypothesis here.

The mathematical obstruction and its fixed-input/alias exceptions are sound.
Its elementary algebra is not a novelty assessment. No conclusion is drawn
about arbitrary collision-retaining photon proposals, the finite-strength
interaction route, performance against classical methods or a device.
