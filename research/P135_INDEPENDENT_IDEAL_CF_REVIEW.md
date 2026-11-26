# P135 — Independent ideal shared-phase CF/hold review

2026-11-26. Manual non-author audit, parent aedae48068565c0a15b779d356f96d4dd6714fc1.
FULL 62-line source read: research/P135_IDEAL_PHASE_CF_CONTROL.md,
commit 0691df7e40e9dbfbee54272b19bee2f063eeacb3, SHA256
d36de9023cb325b2430ee2de176adab08326737495e34205925f2f26d66f4484.
No import, AST, code, graph, RNG, reference-outcome read or scientific run.

**ACCEPT in the stated ideal contraction/CF-hold scope.** This review checks
the identities, not novelty, runtime, an implementation or useful grid sign.

For k>=1, ||z||^2=k and T a contraction imply sum_j |(Tz)_j|^2/k<=1.
Hence the conditional k independent categorical trials, including their
residual dump category, form a normalized classical experiment. For a
distinct k-set Y there are exactly k! output orderings. Its conditional
probability is k!/k^k times |P_Y(z)|^2, with
P_Y(z)=product_(j in Y)sum_a T_ja z_a.
For exponents b,b' of degree k, every coordinate of b-b' lies in [-k,k].
Independent M-root characters with M>k therefore give zero unless b=b'.
Thus Q_CF(Y)=k!/k^k sum_b |c_b(Y)|^2, with no output factorial.

Independently reconstruct the two distinct input factorials. Expanding the
normalized condensate (sum_a z_a a_a^dagger/sqrt(k))^k/sqrt(k!) gives
amplitude sqrt(k!/(k^k b!))*z^b on NORMALIZED input occupation b.
The finite twirl removes coherences between distinct b. For fixed b, every
row-to-source assignment with that multiplicity has b! equal labeled-column
copies in the permanent. Hence per(T[Y,b])=b!*c_b(Y), and its normalized
Fock CF probability is |per(T[Y,b])|^2/b!=b!*|c_b(Y)|^2.
Multiplication by mixture weight k!/(k^k b!) recovers the first identity.
Neither of these divisors can be dropped or assigned to an output collision.

Restricting all k outputs to the signal space maps source creation vectors
to columns of T. Their repeated-column Gram is G[b,b], repeating BOTH indices.
The squared norm of that Fock vector is per(G[b,b])/b!, so the mixture gives
Q_all=sum_b k!*per(G[b,b])/(k^k*(b!)^2). This holds without column rank,
invertibility, nonnegative amplitudes or a nonzero survival normalizer.
Equivalently it is the phase average of (z^dagger G z/k)^k.
Then all-signal collisions=Q_all-sum_Y Q_CF(Y), dump=1-Q_all. These are
nonnegative disjoint masses; any dump photon places the whole event in dump.
No resolved environment law is reconstructed by these aggregated identities.

Boundary reconstruction: k=1 removes every factorial issue and gives the
ordinary one-particle law. T=0 at k>=1 gives dump one. If r<k the CF sum is
empty; all-signal events may still occur but are collisional. Rank deficiency
and zero columns require no conditional division. For k=0 set vacuum mass
one separately, rather than evaluate a 0^0 expression.

For prototype injection, T^dagger T=I and each receiver trial is uniform on
the k prototype ports. Q_all=1 and Q_CF=k!/k^k on the unique CF set, whereas
B/D give that set with probability one. At k=4 this is 3/32, collision29/32,
dump0. The FULL RAW signal-count TV from the deterministic CF law is 29/32;
a decoder merging that CF event with holds can reduce the TV. The equal mean
statement concerns unconditional occupations E[n_j]=sum_a|T_ja|^2, not
CF-conditioned means or expected repaired cut quality.

For k=4, exactly 35 weak source compositions and four degree-one factors
suffice for each CF coefficient sum; this is not a measured timing claim.
A raw utility in [0,h_max] contracts TV to error<=h_max*epsilon, with every
hold retained. The ideal law and rounded finite-bit API remain different.
Its own allowed parameter tuning, setup and scoring must be paid and shared.
P134's 9441-row screen is unchanged; this review authorizes no follow-up run.
No inequality against reoptimized B/D/groups, advantage or QPU readiness follows.
