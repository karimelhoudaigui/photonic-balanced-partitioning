# P51 exact-source review by ROOT

2026-11-25. Reviewed original8f371df, integrated4ad3086:

- theory/P51_Hadamard_low_order_invariance.md, SHA256
  3c0bf304d65472561f8364450fc97bd535907ffe1ff06d4e99d342e870ed7502.
- theory/P51_uniform_loss_matched_moment_lemma.md, SHA256
  d36c5f507562cdb6d4944042a261c4fad2b8eaf3bbb437bbb18c0a29502614ee.

Verdict: both proofs are correct under their stated assumptions. ROOT proposed
the initial invariance/loss questions and H4 attenuation hypothesis; physics
authored the complete derivations. This is a separate same-team reconstruction
of those proofs, not external/blind review, numerical validation or novelty
clearance. No experiment/import/graph or hardware call supports this verdict.

## Permanent expansion reconstructed

For an all-occupied square CF input the second-quantized diagonal observable
has expectation per(U* diag(z)U), with no factorial factor. In per(I+A),
selecting the A columns leaves exactly the principal-submatrix permanents.
For flat square U, diag(A^j)=T_j/N and Tr(A^j)=T_j. These are the actual
load-bearing hypotheses; they do not follow for arbitrary truncated columns.

Independently counting cycles through degree3 gives

    W1=(T2-Nm²)/2,
    C3=(T3-Nm³-6mW1)/3,
    P2=binom(N,2)m²+W1,
    P3=binom(N,3)m³+(N-2)mW1+C3.

Substitution reproduces the author's P2/P3. Extracting coefficients, including
the multi-index factorials, reproduces every listed mixed moment. For example
the coefficient of t_i² t_j in P3 is (N-2)(N-3)/N², hence its moment is TWICE
that value. N1/N2 absent degrees cancel as polynomial identities; fixed-total
substitution t_i=t gives the binomial generating function.

For degree4 I checked each closed-walk multiplicity separately. One off-diagonal
edge plus two diagonals contributes12m² W1 to Tr(A4); alternating two-vertex
walks contribute2W2; a triangle with one diagonal contributes12m C3; two
edges meeting at a vertex contribute4M2; distinct four-cycles contribute4C4.
These give the printed trace identity. Since each vertex has off-diagonal
row-product sum R=(A²)_aa-m², M2=NR²/2-W2. The two disjoint transpositions
contribute D2=(W1²-W2)/2-M2. Eliminating M2,D2,C4 leaves EXACTLY coefficient+1
on W2, and the other terms match Eq9. Thus Eq10 is a polynomial identity,
not merely a real-t fit. Absolute fourth powers apply only on real t, where
A is Hermitian. H4's known phase-dependent fourth moment is compatible with
the fixed moments through degree3.

## Loss derivation reconstructed

For a detected occupation t, multiplying conditional binomial probabilities
gives eta^|t|(1-eta)^(r-|t|) E[prod(n_i)_(t_i)]/prod(t_i!). Pulling the lost
power outside requires FIXED common r and UNIFORM efficiencies. Summing a
sector uses the multivariate Vandermonde identity and gives binom(r,s).
The common conditional shapes are normalized and the sectors are disjoint;
their TV contributions add with sector masses, with no extra factor2.

If moments agree through r-1, only the all-surviving sector can differ, giving
the exact eta^r SIGNED-LAW identity. Applying the SAME linear Markov decoder
preserves that identity and its TV scaling, even if its output sectors overlap.
For a common D_eta the right-hand side must use D_eta as well; replacing it
with D_1 would be invalid. Conditioning on survival removes the attenuation
only by paying survival probability eta^r per attempt, as the proof states.

The first-differing-degree expansion follows by isolating the first nonzero
sector; higher sectors begin one power later. I checked the random-total
counterexample's vacuum difference eta²/2 and the nonuniform two-mode example's
(eta1-eta2)²/2. Endpoints r0, eta0/1, b>=r are handled without evaluating0^0.
For H4, full-law endpoint TV1/2 and decoded TV1/12 therefore acquire eta4.
For general N>4, no eta^N conclusion follows from agreement only through3.

## Accepted scope

KEEP these mathematical identities/bounds. No proof of classical domination
of an arbitrary full-input Hadamard, a B-vsD comparison, a calibrated hardware
loss value, novelty or optimization advantage is supplied. A global decoded
effect at order>=4 remains possible; P52 is a prospective finite discriminator
with independent regrouped-b4 and phase controls. Existing negative data and
the manuscript are unchanged.
