# Phase-control quartic response: independent factor check

2026-11-25. ROOT supplied the candidate factor; the derivation below was
reconstructed without reading an author proof. No project import, simulation,
MC draw, graph or hardware call. **The factor is correct under the stated
fixed-N phase-control model.** No novelty, decoded N8 scaling or optimizer
advantage follows. The P51 proof is reused with authorship disclosed.

## Generating function and balanced multigraph count

Let U be a square complex Hadamard unitary of size N, and take N counted
particles in the classical phase control: x_a are iid unit phases and,
conditional on x, n~Multinomial(N,|Ux|^2/N). This is a FIXED-N multinomial
model, not unconditioned Poisson laser counting. With A=U*diag(t)U,

    G_phase(1+t)=sum_(h=0)^N binom(N,h) E[(x* A x)^h]/N^h.         (1)

Here * is adjoint. Flatness gives A=mI+B, diag(B)=0, m=T1/N, with
Tj=sum_i t_i^j. Write Y=x* B x, so x* A x=T1+Y. Averaging phases keeps
exactly directed multigraphs whose in/out degrees balance at every vertex.

Use the SAME conventions as P51: w_ab=A_ab A_ba, W1=sum_(a<b)w_ab,
W2=sum_(a<b)w_ab^2, M2=sum of products for meeting distinct edge pairs,
D2=sum for disjoint edge pairs, and Cj sums oriented simple j-cycles on each
unordered vertex set. Then

    E[Y]=0, E[Y^2]=2W1, E[Y^3]=6C3,
    E[Y^4]=6W2+24M2+24D2+24C4.                                 (2)

The coefficients count ordered factors: a repeated two-cycle has two copies
of each directed edge, giving4!/(2!2!)=6; two distinct two-cycles, whether
meeting or disjoint, have four distinct directed edges, giving24. A simple
oriented four-cycle also has24. These exhaust balanced loop-free four-edge
multigraphs. For three edges, each oriented triangle has3!=6, NOT merely the
three cyclic starts in a trace. Thus the cycle-normalization distinction is
load-bearing here.

P51 gives M2+D2=(W1^2-W2)/2, R=T2/N-m^2, and

    C4=T4/4-Nm^4/4-3m^2 W1-3m C3-N R^2/2+W2/2.

Substitution into(2) yields

    E[Y^4]=6W2+12W1^2+6T4-6Nm^4-72m^2 W1-72m C3-12N R^2.       (3)

For Hadamards every term except W2 is invariant. The lower phase moments
are also invariant; expanding(T1+Y)^h adds only invariant terms for h<=4.
Consequently

    Delta P4_phase = 6 binom(N,4)/N^4 * Delta W2
                   = cN Delta P4_B,
    cN=(N)_4/(4N^4),  c4=3/128,  c8=105/1024.                  (4)

P4 denotes the homogeneous TOTAL-degree-four shifted-PGF part. The factor
1/4 is genuine. Treating only the all-single input component of the phase-
averaged multinomial source would give the larger wrong factor: its other
input occupations also contribute and cancel part of the phase response.

## Full-law conclusion for H4 ONLY

At N4 both generating functions have degree at most4. All theta-dependent
terms below degree4 vanish, so(4) upgrades to the complete signed-law identity

    p_phase(phi)-p_phase(psi)=(3/128)[p_B(phi)-p_B(psi)].           (5)

It does NOT say that either phase law equals(3/128) times B, nor that their
lower invariant moments equal B's moments. At N8 degrees5 through8 remain;
(4) provides no analogous full-law, TV, top4 or crossing-mean scaling.

Why is the phase top2 baseline uniform at real Walsh H4? Index Walsh rows
and columns by F2^2. Any affine row relabeling becomes a permutation of input
columns with signs, preserving the iid unit-phase input measure. The affine
group AGL(2,2) has24 elements and equals S4. The full count law is therefore
exchangeable; top2 with uniform ties is uniform on the six pairs.

Apply the SAME fixed uniform-tie decoder to(5), and use the previous H4 B
mixture with u=sin^2(phi). Exactly,

    p_phase,top2(phi)=(1-3u/512)U6+(3u/512)UX.                   (6)

The B coefficient is u/4, but both decoded laws have the already recorded
O(1) classical mixture sampler. A larger B/phase response is not an optimizer
advantage; the classical sampler simply chooses the required coin weight.
No finite bucket, fixed-priority beta0 rule or free postselection is included.

## P52 quartic witness and a Walsh8 mean null

For U8(theta) in the card, use t_top=(a,b,0,0), t_bottom=-t_top. Then m=0,
W1=a^2+b^2, R=(a^2+b^2)/4, T4=2(a^4+b^4), and

    W2=(a^2+b^2)^2/16+a^2 b^2 cos^2(theta)/4.

Equation(3) gives
[a^2 b^2]E[Y^4]=51/4+(3/2)cos^2(theta). Since binom(8,4)=70, for
K_j=(n_j-n_(j+4))^2-n_j-n_(j+4),

    E_phase[K0 K1]=1785/2048+(105/1024)cos^2(theta),
    E_B[K0 K1]=1/2+cos^2(theta).                                (7)

This is an exact algebraic prediction, NOT a new posthoc MC target or claim
covered by the392-indicator confidence bound. K0K1 is not an[0,1] indicator.
The constants differ; only the ANGULAR quartic contrast has factor c8.

At theta0, U8 is Walsh8. Affine output relabelings AGL(3,2) again correspond
to input monomials, so both full B and the phase law have this symmetry.
This group is two-transitive; uniform-tie top4 preserves the symmetry. Every
edge-crossing mean is therefore the same number c. Balanced subsets obey
sum_(j!=i)c_ij=4, so c=4/7 for ALL28 edges at theta0. However AGL(3,2) is
not S8 and is not transitive on four-subsets: affine planes and nonplanes are
distinct orbits. Thus uniform70 is NOT inferred for the full ranked law.

This last fact is a pre-data equality/null, not proof of useful global
interference. At other angles, fourth-order response, decoded response and
separation from every regrouped b4/phase/orbit mixture remain distinct arrows.
No numerical work, circuit cost, significance or scaling conclusion is hidden
in(4)–(7).
