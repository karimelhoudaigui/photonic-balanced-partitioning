# P45 full-Fock decoding: control obligations, not an advantage claim

Root analysis25-Nov-2026, basee93dfa2. No new numeric execution. This note
qualifies a proposed encoding before its first development results. All P44
inputs, existing raw files and the manuscript remain unchanged.

For K photons in K+1 modes, define a balanced2K-bit word by writing n_1 ones,
then a zero, then n_2 ones, etc., with K separating zeros. Nonnegative integer
occupations summing K biject with balanced bitstrings, by the known stars/bars
construction. There are binom(2K,K) of each. Collisions decode normally. This
does not by itself implement optimization or establish a new physical effect.

## Required classical and physical references

The Dirichlet-multinomial law with K draws and K+1 unit concentrations is
constant on occupations:

    K! Gamma(K+1)/Gamma(2K+1) = 1/binom(2K,K).

Thus a classical Polya urn (initial weight1 at each mode) exactly samples
uniform feasible partitions under this decoder. It is a mandatory control.
The Haar-averaged bosonic output law is also uniform in this Fock space by
the already established Haar law; that average cannot be a new benefit.

For a hand-checkable physics fixture, K=2, three-mode Fourier U and source110
give B probability2/9 at each bunched state and1/9 at each split state.
D instead gives1/9 and2/9, respectively. Under the fixed stars/bars labels
of a four-cycle, bunched states decode to1100,0110,0011, and the fourth good
cut is1001. B therefore gives good-cut probability7/9, D5/9 and uniform2/3.
THIS IS NOT OPTIMIZATION ADVANTAGE: a mode permutation can prepare a known
good split, and a tiny classical graph search solves the fixture immediately.
It is useful solely to check indexing, Fock normalization and a real effect
of interference before testing independently optimized D and strong search.

An ordering based on graph features or a scored anchor is classical work.
Any candidates explicitly evaluated to build an occupation-move Hamiltonian
already belong to the shared frontend. The useful incumbent is the BEST of
ALL those candidates, not the original anchor alone. A photon sample that
merely recovers a preprocessing discovery has zero new optimization credit.

## Mean evaluation is not automatically hard

The j-th zero in the decoded word is at position Z_j=j+N_j, where
N_j=sum_(a<=j)n_a. The zero indicator at vertex v is

    z_v=sum_(j=1)^K 1_{N_j=v-j}.

The events in this sum are disjoint. Each fixed-count indicator is a finite
Fourier sum of passive prefix number phases with total coefficient weight1.
Products of two such indicators are again finite sums of passive phases on
nested mode sets, with coefficient weight1 per j,l term. For identical CF
inputs their expectations are return permanents of occupied-column
compressions U*DU, contractions for unit-modulus diagonal D. The known
Gurvits sign estimator therefore supplies polynomial ADDITIVE mean estimates
for the decoded graph cut, after the polynomial j,l and graph-weight factors
are charged. This is the same established estimator ingredient already
audited for P43 local means, now applied to prefix-count projectors.

This observation is not an exact joint sampler, a relative guarantee on a
rare improvement probability, a constant-cost mean oracle or a global
optimization impossibility. Its polynomial coefficient/accuracy overhead
must be explicit before a numerical oracle is used as a practical baseline.
The proposed pilot trains on genuinely NEW improvement below the shared
frontend incumbent; a useful tail signal still needs actual experiments.

## Loss and scope

Requiring the original K photons restores the old survival factor eta^K under
uniform loss, even though every collision decodes. Do not report conditional
all-survived samples as per-attempt performance. A decoder completing missing
photons is a different proposal and needs its own matched controls and costs.
The first pilot may be ideal; no hardware conclusion follows from that.

All these facts are model/normalization checks, not novelty certification.
Independent proof/audit of a claimed mechanism and source comparison remain
required. No P45 positive result, held-out outcome or QPU event is claimed.
