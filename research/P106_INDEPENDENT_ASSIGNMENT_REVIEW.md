# P106 independent assignment/cut review

2026-11-26. Non-author, manual proof audit; no scientific execution.
Source: `research/P106_ASSIGNMENT_CUT_BRIDGE_COUNTEREXAMPLE.md`, ROOT commit
`96486bb127377eb248c3e63bc2ca42bbf4fca9d8`, all 126 lines read.
Source SHA256: `28cb3e239447ef02f3b860ae2bc43d08688d1d923262a73f6f1ab81a67095790`.
Review parent: `69e4a6fe434a677acfc5a7e616471990b16db86b`.

**PASS for the stated counterexample to universal monotone raw ranking.**
The graph, equal fields, probabilities and common passive realization check.
The result does NOT say that B has a worse unconditional mean than same-T D:
the mean actually favors B here. A separately retuned D nevertheless defeats
the particular B circuit fixed in P106, as verified below. No optimizer,
all-parameter, complexity, held-out, hardware or universal no-go claim passes.

## 1. Independent reconstruction of graph and decoder

Use exactly the eight vertices and eight positive edges listed in P106.
The incumbent S={r1,r2,a1,a2} has cut 12; a2 is isolated, as disclosed.
Each r has crossing weight 5, each receiver y has crossing weight 3;
thus h_r=-5, h_y=-3. Also h_a1=-2 and h_a2=0.
For F=R union Y, counting each edge with two flipped endpoints twice and
correcting it gives Delta C=sum_F h_i-2sum_{edges inside F} w_ij s_i s_j.
There are no R/internal-receiver edges, so Delta C=-16+2W(R,Y).
The complete six-pair pool, not merely its two selected members, is:

| Receiver pair | Multiplicity | W(R,Y) | Delta C | Resulting cut |
|---|---:|---:|---:|---:|
| {y1,y2}, A | 1 | 6 | -4 | 8 |
| one of {y1,y2}, one of {y3,y4}, M | 4 | 5 | -6 | 6 |
| {y3,y4}, B | 1 | 4 | -8 | 4 |

The two optical inputs label the removed vertices, not all four incumbent
vertices. Two distinct receiving clicks produce {a1,a2} union Y; vacuum,
one survival, or a collision leaves the original S unchanged. Consequently
this is a completely specified balanced local move with all attempts paid.
The pool cut 4 is its local minimum, not an asserted global optimum C*.
Equal field-only row/source factors are common scalings and preserve ranks;
additional graph features beyond these fields are outside that statement.

## 2. One contraction and exact CF Born probabilities

Write p=exp(-1), q=exp(-3). The four-by-two unscaled matrix is
F=((1,q),(q,1),(p,p),(p,p)) by rows; T=gamma F, gamma=1/3.
Its operator norm is at most its Frobenius norm, at most sqrt(8), so T is
a strict contraction. More exactly F^dagger F has eigenvalues
(1+q)^2+4p^2 and (1-q)^2. The claimed common normalization is physical.
V=(T;sqrt(I_2-T^dagger T)) has six rows and orthonormal columns; complete
it to a six-mode unitary with four vacuum inputs. Two environment modes
suffice. This is existence, not a device compilation or detector assertion.

With two distinct occupied inputs and two distinct outputs all occupation
factorials are one. Squaring the two-route permanent gives the B column;
summing the two route intensities gives the D column, without conditioning:

| Pair | p_B/gamma^4 | p_D/gamma^4 | (p_B-p_D)/gamma^4 |
|---|---|---|---|
| A | (1+exp(-6))^2 | 1+exp(-12) | 2exp(-6) |
| each M | exp(-2)(1+exp(-3))^2 | exp(-2)(1+exp(-6)) | 2exp(-5) |
| B | 4exp(-4) | 2exp(-4) | 2exp(-4) |

Since exp(4)>1+4>4, p_B(A)>gamma^4>p_B(B), despite cut(A)>cut(B).
Likewise p_D(A)>p_D(B). This refutes the claimed automatic raw-rank bridge.
The relative enrichment p_B/p_D equals 2 at B but is strictly below 2 at A;
relative improvement and absolute rank are different questions.
For general lambda>0, put r=exp(-2lambda). The sign of p_B(A)-p_B(B)
is the sign of 1+r^3-2r=(r-1)(r^2+r-1). Reversal therefore occurs when
lambda>(log((1+sqrt(5))/2))/2; it does not hold at every strength.

## 3. Mean improvement survives at fixed T; a retuned D defeats this circuit

Because every non-CF/failure event is a self-loop of cost 12, the above full
pool table suffices for an unconditional decoded mean, retaining all losses:

E_B[C_out]-E_D[C_out]
  =-8 gamma^4 [exp(-6)+6exp(-5)+2exp(-4)] < 0.

This is a genuine fixed-T, two-photon interference effect on this local
cost. It is not an accepted optimization advantage, and must not be erased
by describing P106 as a counterexample to every favorable B/D statistic.

ROOT suggested the following extra control; I independently checked it.
Keep F and lambda=1, but let D use gamma_D=2/3. The Taylor terms through
degree four give exp(3)>131/8>16, while exp(1)>2. Hence q<1/16, p<1/2,
and gamma_D^2||F||^2 < (4/9)[(17/16)^2+1]=545/576<1.
This is another physical six-mode contraction. Its CF probabilities are
16 times the old D probabilities. For every receiving pair, the elementary
two-route inequality (a+b)^2<=2(a^2+b^2) implies

    p_D,new(Y) >= 8 p_B,old(Y).

All six cut changes are negative, so the expected improvement of this D
control is at least eight times that of the B circuit fixed in P106.
Attempt count and two injected photons per attempt agree; preparation,
wall time and real hardware losses have not been measured or equated.
B could also retune gamma: this control defeats the fixed gamma=1/3
candidate, not every B circuit or a jointly optimized parameter family.
Moreover two indistinguishable photons are already one allowed group-2
control; this example cannot separate full B from that control class.

## 4. Phase map, finite classical frontier and limits

For phase-only entries, |exp(i lambda X)+exp(i lambda Y)|^2 is exactly
4cos^2(lambda(X-Y)/2). Shifting all four entries of a block by c multiplies
its receiving rows by the same phase, preserving PNR probabilities and
T^dagger T while increasing X+Y by 4c. This proves the loss of total-block
information in that phase map. Graph fields change under such a graph
modification: this is not a counterexample to every field-augmented map,
nor does the positive-map rank reversal automatically apply to phase-only.

A classical control with the same graph/incumbent/removal information can
score all six candidates and select cut 4, paying six scores and setup.
No best-of-samples policy confined to this unchanged pool can beat that
local frontier. Comparing this payment to optical attempts is a declared
query accounting, not a measured wall-time or arbitrary trajectory theorem.
Both controls must also pay normalization, source/field construction and
precision; these tasks cannot be treated as a free quantum oracle.

P104 is labeled a candidate in the source. Its prospective all-K-or-FAIL
replacement and rational-approximation transfer are NOT premises verified
by this audit. None is needed for the finite graph counterexample or the
explicit retuned D control above. No claim on retained partial-loss decoders,
nonlocal compilations, adaptive trajectories or asymptotic complexity follows.

Disposition: accept P106's failed automatic monotone-ranking claim with the
fixed-T mean distinction explicit; do not initiate a positive optimizer or
QPU claim from it. Frozen P101/P96, manuscript and raw data remain untouched.
Only text/manual algebra and Git/hash metadata were used; no tests or runs.
