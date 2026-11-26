# P83: accepted phase-gauge reduction and a signed-source falsifier

ROOT read the complete338-line source and294-line exact-source audit,
reconstructed the phase equations, hafnian invariance and both log-PGF
coefficient calculations. No correction was needed. This identifies a
boundary of the positive-loop construction, not quantum hardness or a
positive graph optimization mechanism.

Source `theory/P83_GAUGE_AND_FRUSTRATION_BOUNDARY.md`, original
d1749a1778f1107c3887f76b0c58cb715c4b94ec, SHA256
ec6a88bc87e236ca3f9ab38cccc2a447c3bb1a1b6f38e675a5b8a5dae7da9b06.
Review `theory/P83_EXACT_HASH_REVIEW.md`, original
48939d60d1b37cf654386627a6226b2c19c47d09, SHA256
3313e1a878e8ebb29eef56d48d23e9a45e57a9b7a2cfc7c4d175a4d4e7e4443e.
ROOT supplied the initial gauge/signed-cycle candidates. The reviewer read
the source before reconstructing it; this is exact-source review, not blind
discovery. No experiment or source-preparation capability was assumed.

## Exact accepted claims

For a physical symmetric pair matrix Z=D B D, diagonal unitary D and
entrywise real nonnegative B=|Z|, the COMPLETE raw PNR law equals that
of B. This is congruence, not similarity. Norm and Gaussian normalization
are preserved; every repeated-label hafnian acquires only the common
occupation phase product_i d_i^(n_i). Vacuum/collisions/all sectors are
included. Vertex phases alone therefore do not escape P78/P80. The latter
requires rational B and its own finite-bit costs; arbitrary phase
recognition/encoding complexity is not free.

The gauge exists iff every EVEN CLOSED SUPPORT WALK has trivial
alternating edge phase. Repeated vertices/edges and loops are allowed.
A spanning-tree root/parity construction proves both directions; two odd
rooted walks must prescribe the same half phase. Simple even cycles
alone do not suffice: two triangles sharing one vertex can prescribe
incompatible root phases despite having no simple even cycle. Zero and
disconnected support, singleton loops and two-root ambiguities are covered.

For the signed four-cycle

    Z=t*[[0,1,0,-1],[1,0,1,0],[0,1,0,1],[-1,0,1,0]],
    0<t<1/sqrt(2),

Z²=2t²I, p_vac=(1-2t²)² and haf(Z)=0. The coefficient of1111 in log G
is exactly -2t⁴, independently found from eight oriented/rooted length4
walks and from the degree4 term F4-F2²/2. The standard PGF domain
|z_i|<=1 (or simply its analytic germ near zero) supplies convergence;
there is no claim for unrestricted z.

A positive compound-Poisson count law with nonzero vacuum mass has
nonnegative nonconstant log-PGF coefficients. Thus this physical source
has NO such representation, even with arbitrary nonnegative integer
count-vector jumps. This falsifies extending P78's positive-loop argument
to all signed matrices. It excludes neither other classical simulators
nor efficient fixed-dimension calculation, and gives no hardness result.
Gaugeability is not asserted necessary for every compound-Poisson law.

The four-mode interference statistic is a complete-event log coefficient
formed using the FULL vacuum denominator, not marginal or postselected
probabilities. Its estimation would charge all pulses and uncertainty.
Two CF photons per complementary color have only a single-edge hafnian,
so phase changes do not alter that conditional cut law; source acceptance
and normalization may change. Larger orders allow interference but no
cut benefit is proved. A graph-independent coincidence zero is not an
optimizer success. Hardware control of these pair-source phases remains
unverified; the actual finite-Fock passive escape task is separate P82.

No source import, AST, numerical computation, RNG, backend, QPU or paper/
change occurred for P83. Existing1187PASS code is unchanged. Novelty and
the positive optimizer objective remain OPEN.
