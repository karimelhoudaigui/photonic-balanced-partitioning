# P82: independent exact null for zero loading contrast

Primary verdict: **proved under the independent-mark hypotheses stated
below**. At eta=0 the specified compiler leaves the initial phases
unchanged. After averaging the fresh uniform receiver-port assignment,
the repaired bosonic decoded proposal has exactly the flat-D proposal
law, for every graph, current subset and replacement cardinality. This
is a decoded-kernel statement, not equality of full count laws or costs.

The design was read completely, 145 lines, at
`research/P82_HARDWARE_COMPATIBLE_ESCAPE_DESIGN.md`, source commit
`f7cb5d99fa35b6ab9e6ff60839f985d81ea87001`, SHA256
`c008f60143a1c4b0e81dcec1ba7a07c28d89244b10d4d69695070d27b0916723`.
ROOT supplied and relayed the proposed null argument before this
reconstruction. The separate P82 independent design review and P82a
draft were not read or contacted. Thus this is an independent
before-review-reading derivation, not independent discovery.

Written on 26 November 2026 in `.local/p66-dark-barrier`, starting at
`17ba1d4568621870cf18d6766d79e6714654b5ac`. Only this new file is written;
the earlier proofs are unchanged. No code/import, AST, collection, test,
RNG, matrix numerics, native backend, probability query, QPU or manuscript
action was performed. No numerical output was read.

## 1. Conditional setting and the independence actually required

Fix any past classical history H, including a weighted graph G, a
possibly graph-dependent current subset S of size K and its complement
T, also of size K. Here K=2d>=4, with K photons on 2K vertex modes;
this is NOT the N-qubit/N-photon dual-rail model of P81.

At this conditional history use eta=0, rho>0 and p=rho/(1+rho). Let
sigma assign input labels S to the K occupied input ports and Pi assign
the K receiving ports to labels T. The design's orderings are uniform
and independent conditional on H. Pi must be a full uniform K-port
permutation, including order and orientation of its paired ports.

The phase initialization consists of independent uniform fourth roots,
independent of Pi, input-order marks and future measurement/repair
randomness. More generally the proof only needs the receiving-port
count mechanism, conditional on R and its other private marks, to be
independent of Pi. The stronger declared independence suffices. Marginal
uniform phase values alone do not suffice if they are correlated with
receiver labels, graph-based port marks or a hidden target.
Independence concerns the marks/primitive coins, not the measured port
counts, whose conditional law can depend on the phases.

The repair uniformly fills unused RECEIVER LABELS as specified in design
lines 75-79. Its coins are independent conditional on the observed
support. All shots, collisions and raw marks are retained. No rejection
of repeated port assignments or repeated decoded subsets is allowed;
such rejection would change the fresh conditional mark law.

These conditions are statements about the mathematical experiment. They
must be preserved by a future random-stream/tie contract, not inferred
from deterministic pseudorandom seeds or marginal histograms alone.

## 2. The exact eta=0 compiler is graph/receiver-label blind

At eta=0 all odds o_j equal rho, in both input halves, so

    A=F*(rho I)*F^dagger=rho I.

For r!=s, A_rs=0 and therefore J_rs=Q_rs*|A_rs|^2=0, irrespective
of G, S or the receiving-label permutation. Every coordinate field H_r
in the design is exactly zero. Its prescribed zero-field branch keeps
phi_r, so any prospective number of sweeps leaves phi=phi_initial.

Thus W_phi depends only on the fixed port construction and its initial
phase marks, with no dependence on Pi or graph labels. Its entries have
modulus 1/sqrt(K), but the bosonic uniformization below does not require
flatness: it requires the independence from the receiving assignment.
Flatness is needed when identifying the specified D control.

## 3. The removed set is a Bernoulli subset, independent of Pi

Kept-bank rows are diagonal in the occupied input ports. Conditioning on
the missing kept labels R forces precisely their input columns to have
transferred; the others contribute their distinct kept rows. The raw
factorization in the design is

    Pr_B(R,y | marks,H)
       =p^r*(1-p)^(K-r)
          *|per W_phi[y,I_R]|^2/product_a y_a!,
    r=|R|,       sum_a y_a=r,

where I_R is the set of removed input PORTS corresponding to R under
sigma. The repeated receiving rows give the output factorials. There
is no input factorial because the transferred columns are distinct.
For each R the receiving unitary's Fock law sums to one. Hence

    Pr(R | marks,H)=p^|R|*(1-p)^(K-|R|).

It is independent of sigma, Pi and the initial phases. Thus the labeled
removed set consists of independent Bernoulli-p choices on S. In
particular R is independent of Pi, even after conditioning on any
particular R and input/phase marks the receiver permutation stays
uniform. The input port selection I_R may influence the receiving
PORT count law; that law is still independent of Pi at eta=0.

This argument conditions on an arbitrary graph-dependent S already
chosen by the history. It does not assume that S or the graph itself
is random or label independent.

## 4. Uniform receiver assignment plus repair: the exact lemma

Condition on H, R, the input/phase marks and a realized receiving count
vector n in port coordinates, before drawing the repair coins. Put r=sum n and
B={j:n_j>0}, h=|B|. There are r received photons, so 0<=h<=r<=K.
Because Pi is independent and uniform, Pi(B) is a uniform h-subset
of T. Conditional on that clicked set, the specified decoder appends
a uniform (r-h)-subset of T minus Pi(B), yielding Y of size r.

For any fixed A subset T of size r,

    Pr(Y=A | H,R,port variables)
      = [binom(r,h)/binom(K,h)] / binom(K-h,r-h)
      =1/binom(K,r).

The first factor asks that the uniform h-subset lie inside A; once
it does, the unique required fill A minus Pi(B) has the stated
conditional probability. The equality follows from

    binom(K,h)*binom(K-h,r-h)=binom(K,r)*binom(r,h).

The answer does not depend on h, the detailed multiplicities, phases,
input ports or R except its cardinality. Averaging all these variables
therefore proves

    Y | (H,R) is uniform over the r-subsets of T.             (1)

At r=0 the support/fill are empty and Y is the unique empty subset.
At r=K the fill completes every support to Y=T. Both boundaries are
included; no binomial denominator is zero in the formula.

The repair must be uniform in LABEL space, or equivalently uniform in
port space transported by Pi. Arbitrary law-equivariant uniform coins
are sufficient; pathwise relabel equivariance of a deterministic seed
implementation is not needed for the probability identity. If priorities
can tie, their tie rule must still give the declared uniform subset.
Filling by smallest vertex labels generally biases Y and is not this
decoder. Uniform permutations of only receiving PAIRS, without within-
pair swaps, are not automatically the full permutation assumption.

## 5. Equality with flat D, without cardinality postselection

For flat W, the distinguishable receiving law at fixed R consists of
r independent uniform draws over T. It is permutation invariant even
for a fixed port assignment, and the same uniform repair yields a
uniform r-subset. Combining this with the same Bernoulli removed-set
law gives the common joint decoded law

    Pr_B(R=A,Y=B | H)=Pr_Dflat(R=A,Y=B | H)
      =p^r*(1-p)^(K-r)/binom(K,r),                          (2)

for A subset S, B subset T and |A|=|B|=r. Other pairs have zero
probability. All receiver marks in the B equality are averaged as
specified; conditioning on their realized assignment need not give
the D law.

Writing X=(S minus R) union Y, each feasible X determines its R and
Y uniquely. With r=|S minus X| the transition is exactly

    Pr(X | H)=p^r*(1-p)^(K-r)/binom(K,r).                    (3)

There are binom(K,r)^2 proposals at that distance. Their total mass is
binom(K,r)*p^r*(1-p)^(K-r), so r is Binomial(K,p), and conditional on
r the pair (R,Y) is uniform among those binom(K,r)^2 choices. Equations
(2)-(3), not conditioning on a favorable r, are the raw proposal law.
The identity move has probability (1-p)^K, and full transfer to T has
probability p^K. No collision, r or repeated subset is discarded.

Read the design's informal phrase 'independent of R' as conditional
uniformity at the specified cardinality. Y and R are not unconditionally
independent, since their sizes are equal. In (1), Y is independent of
the particular removed labels given H,r.

## 6. Full counts differ, and controller information matters

The full optical law is NOT D. For r=2, two distinct transferred input
ports and flat W, the bosonic probability of both photons at a specific
receiver is 2/K^2: the repeated-row permanent is 2 W_ai W_aj and the
output factorial divides its squared modulus by 2. D gives 1/K^2.
Summing over receivers preserves this distinction after assignment
averaging. Collision count, support size, repair workload and marks
can therefore have different joint laws despite (3).

Decoded X contains R=S minus X and its r, so controller use of those
derived variables does not invalidate (3). But the fresh receiver
assignment, initial phases, clicked-versus-filled split and raw count
multiplicities are additional side information. Equality of X marginals
does not imply equality of their joint law with that information.
Keeping it in archival raw records is appropriate; using it for
selection, future parameters, postprocessing or stopping changes the
information model of an exact decoded-trajectory null.

For a measured/reset algorithm whose state and decisions depend only
on past decoded proposals, G, the current/incumbent state and common
classical coins, the proof applies at each conditional history. Use
the same conditional rho and the same local descent Q and tie coins.
Q may depend on G,S,X; it need not be graph blind. Its coins must have
the same law conditional on these arguments and not encode different
fresh optical/port side information. Both next-X kernels are (3), so
one can couple the proposals identically, then all descent intermediate
states, scores, incumbent updates and future decoded histories match.
Induction proves equality of those trajectories at a common raw-shot
cap or common decoded-history stopping rule.

This coupling is a probability statement, not a claim that raw optical
or simulator work is identical. Raw-count-dependent controllers,
mark-dependent selection, elapsed-time/CPU quotas or raw-dependent
descent/tie budgets need not have equal trajectories. The costs of
mapping, quantum attempts, repair, compilation and descent remain paid.
There is no equal-wall-time conclusion or free postselection credit.

## 7. A necessary prospective numerical null guard

The exact zero-field branch is singular with respect to a careless
floating implementation. If floating F*(rho I)*F^dagger produces
tiny nonzero off-diagonal entries Ahat_rs, then

    Jhat_rs=Q_rs*|Ahat_rs|^2

can carry graph- and receiving-label-dependent information, however
small its magnitude. A nonzero field Hhat then triggers arg(Hhat).
Multiplying a nonzero field by an arbitrarily small positive scalar
does not change its argument. Thus roundoff-sized J can cause O(1)
phase rotations and destroy the independence used in section 4.
Small field norm is not a bound on phase-update error at H=0.

A faithful eta=0 control must therefore use the analytic identity:
set A=rho I and off-diagonal J=0 exactly, and preserve the initial
phases through every sweep. It must not infer this null from a
floating matrix product and nonzero test. A generic numerical
tolerance is a separately specified algorithmic choice, especially
near nonzero eta; no threshold may be fitted after outcomes.
This is a pre-data model-fidelity requirement, not authorization to
write or run a new implementation. Other finite-precision, source,
normalization and cost errors still require their own qualification.

Any apparent decoded eta=0 B/D discrepancy would first require review
of this branch, independence/mark conditioning, uniform repair and
ties, shot selection, resources and statistical uncertainty. It is
not by itself evidence against the exact null or for an optimizer.

## 8. Why this does not close the eta>0 route

For eta>0, the compiler uses the receiver-assignment-dependent Q_rs
and nonzero |A_rs|^2 to select phases. The port count law can then
depend on Pi and G. Conditioning on port counts no longer leaves an
independent uniform Pi, so the crucial premise in section 4 fails.
Uniformly relabeling the receivers while carrying their graph compiler
along does not average a correlated source into a uniform subset.
Flat single-particle intensities alone do not prove the null.

The argument also does not rule out a different, expressly graph-aware
phase compiler at eta=0; that would be a changed model rather than the
J=0 compiler specified here. Conversely the general independence lemma
may apply in other degenerate parameter cases, but no blanket eta>0
or all-P82 impossibility is inferred.

KEEP this exact decoded eta=0 null and its analytic numerical guard
as prospective validation obligations. REJECT an eta=0 decoded B/D
contrast as positive evidence under the stated model. Full count
interference can remain real while the proposal law is classically
identical. The nonuniform high-order, full-cost optimizer hypothesis
remains OPEN and still faces the design's stronger independent controls.
No experimental allocation, code execution, novelty, hardware capability
or positive optimizer advantage follows from this proof.

Final hand proofreading checked the conditional history, R/Pi/phase
independence, factorials, the uniform-support/fill identity, r=0/K,
cardinality versus label independence, coupling information, raw costs
and the discontinuity of arg at the exact zero field.
