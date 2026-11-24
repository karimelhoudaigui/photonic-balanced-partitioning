# P42 encoding lane — exact scope checks

Date: 2026-11-24. Analytic checks only; no P42 program or experiment was run.
Companion proof: [loss domination](P42_encoding_loss_domination.md).

## 1. Partial distinguishability breaks the simple full-source CF projector cap

The identical-photon assumption in the Section 4 claim is load-bearing.
Here is a hand-computable conditional counterexample to extending that
particular claim to every internal-state Gram matrix.

Use m=N=8 input photons, one per input mode. On spatial modes 0,...,5 take
the six-point Fourier matrix

    F6[r,j]=exp(2 pi i r j/6)/sqrt(6),

and let U=F6 direct-sum I2. Even active inputs 0,2,4 carry internal species A;
odd active inputs 1,3,5 carry a perfectly orthogonal species B. The two
spectator photons in modes 6 and 7 can have arbitrary fixed pure species,
since their spatial modes never mix. Loss is uniform and species-blind.

Condition on exactly k=4 surviving photons and choose target CF spatial
support S={0,3,6,7}. Its contributing survivor sets must include both
spectators and two of the six active inputs. There are six same-species
active pairs and nine opposite-species active pairs. For a same-species pair
j,j' of equal parity, the 2-by-2 permanent into output modes 0,3 is

    [(-1)^j+(-1)^j']/6,

whose squared modulus is 1/9. For an opposite-species pair the particles
are distinguishable; the two labeled assignments add as probabilities and
give 2/36=1/18. Therefore the SUM of conditional survivor-transition
probabilities is

    6(1/9)+9(1/18)=7/6 > 1.                              (S1)

The actual conditional support probability is consequently

    (7/6)/binom(8,4)=1/60 > 1/70=1/binom(8,4).            (S2)

Thus the full-source CF conditional uniform bound derived from a scalar
bosonic Fock-space projector does not hold for arbitrary distinguishability.
The output projector has internal-state multiplicity, which that scalar
rank-one argument omitted. With all six active photons identical, the
opposite-parity permanents cancel; the corresponding sum is 2/3, so there
is no contradiction with the identical-photon theorem.

This is NOT a counterexample to physical per-emission domination at a
given loss. The unconditional probability for this example is

    (7/6) eta^4(1-eta)^4 <= 7/1536 < 1/70.

Nor does it refute the separate vector-valued random-wave construction
suggested in Section 7. That proposed extension uses a different argument,
requires a known Gram matrix, costs more than the scalar O(mk) construction
in general, and still requires independent proof audit.

## 2. Arbitrary frontend candidates cannot be free

Suppose the graph has a nonempty good set B smaller than all feasible
partitions. A purported optical algorithm can first use an unrestricted
classical solver in its frontend, score a member of B, and return that
partition regardless of every optical outcome. Its terminal success is 1.
Uniform search with a finite number n_C of feasible draws has success
1-(1-|B|/D)^n_C < 1.

This does not challenge the optical-support first-hit bound. It shows that
the theorem must not identify the hybrid's overall best cost with its
best optical support unless frontend candidates are shared and charged.
The same issue arises from graph-aware repair which maps an arbitrary
support to a classically optimized partition. A fixed shared decoder can
be analyzed by its preimage good-set cardinality; a history-dependent
many-to-one decoder is not covered by the fixed-cardinality uniform proof.

## 3. Pointwise covers have different adaptive scope

The wave covers in Sections 3 and 5 depend on the actual circuit V. They
give a cheap per-attempt substitute for a frozen circuit and for fixed
nonnegative output utilities, but do not reproduce the optical feedback
history. Local domination is insufficient for a general identical-policy
adaptive assertion; the previously sealed P41 abstract trap counterexample
already establishes the logical gap.

The uniform spectral criterion is different: its per-good-set cap is
independent of V and of the history, so conditional survival probabilities
can be multiplied. This yields a genuine adaptive support-hitting theorem
under its own hypotheses, even though no full quantum law is simulated.

None of these statements equates emission attempts with realized objective
queries or wall time. A valid classical sample costs a score; many failed
optical attempts may not. Declared attempt ceilings, score ceilings, source
photons and measured time must remain distinct resource quantities.
