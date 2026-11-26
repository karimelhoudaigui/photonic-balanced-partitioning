# P140 — Independent fixed-source instrument review

26-Nov-2026. Manual non-author audit, parent deb8d9ae24af4a9e39553b00c2a25a09fdb3ad56.
FULL 117 lines read: research/P140_NONCONJUGATE_INSTRUMENT_SCOPE.md at
4a82c48bc0787099c8273b7952852b905d83b615, SHA256
93627e18cc92cf5849af79b0bc296e8ab8f49e9d33b2412ffcca79d25c551340.
No imported/evaluated scientific source, AST, program, RNG, empirical raw
preview, numerical/native/QPU run, source overwrite or manuscript change.

**ACCEPT the fixed-source nonstatic-count witness and its optimization veto.**
The derivations below were reconstructed, rather than adopting the author's
verdict. No novelty, finite-resource optimizer or hardware capability is certified.

## Static invariant and exact causal table

For the fixed CF source |1a,1b,1c>, the spatial one-body matrix is the
projector P onto those inputs. A passive unitary gives W P W^dagger<=I;
its jth diagonal is sum_(i=a,b,c)|W_ji|^2<=1. Vacuum dilation/loss preserves
this inequality, as does an outcome-independent mixture of settings. It is
a bound for one FIXED physical output port, not a postselected or relabeled
record. Bunched sources/nonvacuum preparation are different premises.

The balanced a/b splitter maps a^dagger b^dagger c^dagger to
[(a^dagger)^2-(b^dagger)^2]*c^dagger/2. Swapping b into flag f1 yields
normalized Fock amplitudes +1/sqrt2 and -1/sqrt2 on the two stated branches.
Flag 0 leaves data 2a+1c; flag 2 leaves 1c, changed to 1a by the conditional a/c
swap. Therefore both complete records have probability 1/2 and E[n_a]=3/2.
The 120 three-photon/eight-mode occupations equal C(10,3); exactly 118 are
zero. All photons/flags are accounted, with no herald division or restart.
The mean contradicts every static W on this same source, already on the
data marginal. It need not distinguish the retained quantum states.

## Complex prefix and the smaller independent hand

For C=DFT3 on(a,c,d), omega=exp(2pi*i/3), W=(C directsum I_flags)W0 has rectangle
rows(a,c),columns(a,c) = [[1/sqrt6,1/sqrt3],[1/sqrt6,omega/sqrt3]].
The invariant product W_aa W_cc conj(W_ac)conj(W_ca)=omega/18 is nonreal,
so row/column phases cannot make this whole prefix real. Nonetheless flag
projectors commute with C and C^dagger. V_f=C^dagger or P_ac C^dagger
cancels C branchwise, restoring the SAME table exactly for every species arm.
These mixers are neither equal nor literal complex conjugates: their first
rows already differ from the required conjugate row. Thus the phase is not
the load-bearing resource; the measurement-conditioned routing is.

For the two-photon/three-mode check, multiplying the first two occupied
linear forms of the stated real orthogonal matrix gives

    -(d^dagger)^2/2+(s^dagger)^2/6
                   +(sqrt2/3)*s^dagger f^dagger+(f^dagger)^2/3.

Flag 0 weight is 1/2+1/18=5/9, with unnormalized n_d contribution 1.
Flag 1 is sqrt2*s^dagger/3, weight 2/9; flag 2 weight 2/9. Swapping d/s only
for flag 1 adds 2/9 to n_d, giving 11/9. For D, flag 0 contributes 2/3 to n_d;
flag 1 swaps the old s weight 1/9 into d, giving 7/9. This is not a bound on
globally reoptimized D protocols. No extra input probe was needed.

## Distinguishable, group and graph controls

Orthogonal a/b tags give probabilities 1/4 for each same-port pair and 1/2
for one-a/one-flag. With c unchanged and the SAME feedback, the extra record
is data 1a+1c,flag 1. Thus D's mean is 2/4+1/4+1/2=5/4, also above the
static-source invariant. The fact that D also violates it is further reason
to distinguish nonstatic routing from an interference-dependent optimizer win.
For splitter R, q=R(1-R), B flags have(2q,1-4q,2q), D(q,1-2q,q).
Counting the conditional data a photons gives 1+2q and 1+q, respectively,
with maxima 3/2 and 5/4 at R=1/2. This checks ONLY that retuned-R family.
Arbitrary D prefixes, feedback mixers or richer controllers were not optimized.

After branchwise C cancellation, only photons a/b ever interfere; c is a
spectator or deterministically routed single photon. Hence proper partition
{a,b}|{c} reproduces B's FULL law, not just its mean, for every such R.
There is no unique three-input mechanism or proper-group advantage.

The completion rule starts from all positive DATA support, with at most
three vertices, and greedily fills to three using paid incremental scores
and public ties. Flag photons are removed physically but retained in records.
With S0 size 9 disjoint from the receiver pool, completed candidates are
balanced 12-sets; partial helpers never become feasible incumbents. The rule
extends to every zero-probability record, including empty data support.
B's two supports are {a,c} and {a}; D's extra branch again has {a,c}. Thus

    E_B h=(h(Y2)+h(Y1))/2,
    E_D h=3h(Y2)/4+h(Y1)/4,
    E_B h-E_D h=(h(Y1)-h(Y2))/4.

The sign is graph-dependent; if completions coincide, it is zero. A classical
fair bit directly draws the same two FULL virtual records as B and performs
the identical greedy work, paying its RNG/features/scores but no optical
attempt. Computing both completions also exposes their credited best feasible
candidate. Neither a favorable graph nor unpaid repair establishes advantage.

Scope: a genuine eight-mode/three-CF-photon causal count witness, even with
one fixed source, with an explicit proper-group/classical optimization veto.
Protected flag measurement, data storage and in-shot conditional routing
need calibrated capabilities. PNR, latencies and Lucy's feed-forward API
remain uncertified; no public mode count establishes them. No experiment,
new implementation, QPU authorization or paper revision follows. Source frozen.
