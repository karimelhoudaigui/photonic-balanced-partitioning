# P86: an error floor for approximate passive balanced-cut phases

Candidate theorem derived by ROOT. Independent before-source reconstruction
is requested separately; this document alone does not mark it accepted.
It extends the exact P84 obstruction to a specified phase-sensitive error
metric, using the already accepted quantitative P81 theorem. No numerical
calculation, backend or manuscript modification supports the universal proof.

## 1. Exact objects and proposed statement

Let N>=4 be even. There are N photons on2N physical rails, one photon
per logical input pair in each code basis state |S>, |S|=N/2. U is a
single fixed lossless passive unitary on these same rails. There are no
ancillary modes/photons, heralds, filters, losses or discarded outcomes.
The real cost C satisfies C(S)=C(S^c); an undirected weighted graph cut
is the intended instance. Define the normalized, phase-sensitive error

    delta(U,gamma)
      = min_(chi in R/(2piZ)) max_(|S|=N/2)
          ||Gamma_N(U)|S> - exp(i chi-i gamma C(S))|S>||_2.

Only ONE common chi is minimized. Allowing an independent phase for each
S would erase the intended oracle and invalidate this metric. The minimum
exists because the circle is compact and the maximum is over a finite
set of continuous functions. No continuity of U as a function of gamma
is assumed, and U can depend arbitrarily on the known graph and angle.

Put

    C_N=4N(N-1)^2/(N-2),
    b_N=1+N*sqrt(C_N).

For EVERY two balanced sets S,T the proposed bound is

    delta(U,gamma) >= |sin(gamma*(C(S)-C(T)))|/(2*b_N).       (1)

In particular take actual cost extrema to obtain the same bound with
their range R=max C-min C. Those extrema are used ONLY in the theorem's
interpretation; neither the circuit, calibration nor an algorithm is
given an optimum or an optimal-state mask.

For any fixed nonconstant cost and fixed N, no family of these passive
maps has delta=o(|gamma|) as nonzero gamma tends to zero. More explicitly,
when |gamma|R<=pi/2,

    delta >= |gamma|R/(pi*b_N).                            (2)

This is a first-order accuracy obstruction in a specified all-basis norm.
It is not a constant-error impossibility, an optimizer lower bound, or
a uniform-in-N approximation theorem. Identity optics itself achieves
an O(|gamma|) error, so approximate small-angle agreement is possible.

## 2. Named physical stability dependency

Use P81 with its exact quantitative constant C_N. For a fixed U, let
epsilon be the raw probability of code leakage on the uniform incoherent
mixture of ALL balanced basis inputs. P81 constructs a physical V,
consisting of whole-pair permutation and local2x2 unitaries, with

    ||U-V||_F <= sqrt(C_N*epsilon),
    ||Gamma_N(U)-Gamma_N(V)||op <= N*sqrt(C_N*epsilon).

Exact dependency: `theory/P81_dual_rail_balanced_average_stability.md`,
original0a51544a1a449c64b87cb48e82bf637583402278, SHA256
7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f.
Separate reconstruction13ce814 and exact auditf915cf9 are accepted in
`reports/P81_ROOT_STABILITY_CHECKPOINT.md`. P86 uses the quantitative
theorem, not merely P81's exact monomial boundary. No empirical estimate
of epsilon or source-preparation assumption is introduced here.

The phase-error premise provides this counterfactual calibration algebraically:
each target vector lies in the code, so its orthogonal leakage component
has squared norm at most delta². Averaging those inequalities gives

    epsilon <= delta².

Choose a minimizing common chi, set f_S=exp(i chi-i gamma C(S)), and
choose the V supplied by P81. The triangle inequality yields for every S

    ||Gamma_N(V)|S>-f_S|S>|| <= (1+N sqrt(C_N))*delta = e.    (3)

The operator-norm bound in this step comes from P81's tensor telescoping,
not from an invalid conversion of a maximum column error into operator
norm. Only the resulting column inequalities are needed below.

## 3. If the error is small, the whole-pair permutation is identity

If e>=1/2, inequality (1) is already true because |sin|<=1. Assume henceforth
e<1/2. Let A_S=<S|Gamma_N(V)|S>. Both states in (3) are normalized, so

    2-2 Re(conj(f_S)*A_S) <= e²,
    |A_S| >= 1-e²/2 > 7/8.                               (4)

Write pi(a) for the input pair sent to output pair a, and Q_a for its
local2x2 unitary. The product code action gives exactly

    A_S=product_a Q_a[x_a,x_(pi(a))],

with no bosonic permutation sign or factorial: precisely one photon is
sent to each pair. This formula holds whether or not the local matrices
are monomial.

Suppose pi(a)=b!=a for one a. There is a balanced set S0 with x_a=x_b=0,
because N-2>=N/2 for N>=4. There is also a balanced S1 with x_a=0,x_b=1.
All other factors in the displayed product have magnitude at most one.
Equation (4) therefore forces

    |Q_a[0,0]|>7/8 and |Q_a[0,1]|>7/8.

Their squared magnitudes sum to more than one, contradicting a unitary
row. Thus pi is identity. This argument covers N4 and does not assume
all local blocks already are diagonal. Nor does it infer exact code
preservation for the original U.

## 4. Complementary diagonal products yield the bound

With pi identity, even nonmonomial Q_a satisfy

    A_S=product_a Q_a[x_a,x_a],
    A_S*A_(S^c)=product_a Q_a[0,0]*Q_a[1,1] = L,

where L is independent of S. On the other hand f_(S^c)=f_S by complement
symmetry, and (3) implies |A_S-f_S|<=e. Since |A_S|<=1 and |f_S|=1,

    |L-f_S²|
      <= |A_S|*|A_(S^c)-f_S|+|f_S|*|A_S-f_S|
      <= 2e.

Comparing S and T gives

    2*|sin(gamma*(C(S)-C(T)))|
       = |f_S²-f_T²| <= 4e = 4*b_N*delta.

This proves (1), together with the previously disposed e>=1/2 branch.
For (2), use sin(x)>=2x/pi on0<=x<=pi/2. In particular for fixed R>0,
delta/|gamma| cannot tend to zero. No phase-logarithm branch, derivative
of U, spectral gap, graph-label convention or conjectural cost optimum
is used in the argument.

## 5. Interpretation, falsification checks and exclusions

* With delta0, (1) recovers P84's necessary single-angle lattice
  gamma*(C(S)-C(T)) in piZ. It is not a sufficient isolated-angle test.
  Integer-weight graph cuts at gamma=pi admit local degree-parity phases;
  the sine bound correctly vanishes there.
* If the balanced cost is constant, identity with an allowed common
  phase has delta0. The range-zero bound makes no contrary assertion.
* Small gamma does not imply a nonzero absolute error independent of
  gamma. The reference identity bound is at most |gamma|R/2 after centering
  the common phase at the midpoint of the cost range. Both bounds have
  first-order scaling; their constants differ substantially.
* The bound uses a phase-sensitive common-reference state-vector metric
  on ALL balanced basis states. Basis-state PNR/fidelity alone cannot
  observe a cost phase. An identity channel passes probability-only
  comparisons; those are not evidence of coherent oracle implementation.
* The coefficient b_N grows as order N². There is no useful fixed-error
  claim at arbitrary increasing N without a separate scaling analysis.
  A lower bound for the stronger restricted-subspace operator norm follows
  because it bounds every column error; the converse inference is not made.
* N2 is outside P81's quantitative theorem; its balanced cut is constant
  anyway. No unproved code classification at N2 is imported.
* Ancillas, monitored measurements, loss, filters, state-dependent maps,
  a selected input family, a different source encoding or a general
  optical optimizer change the contract. No impossibility or free
  implementation claim for those models follows from this proof.

The proposed mathematical result is limited to approximate cost-phase
representability. It supplies no positive optimization advantage, novelty,
practical gate-error threshold, device availability or hardware permission.
Paper/main/QPU remain frozen. Independent reconstruction and exact-source
review are pending; no scientific numerical experiment was launched.
