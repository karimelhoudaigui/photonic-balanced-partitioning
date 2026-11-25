# P46 — absolute conditioning of the hollow marginal inversion

Supplement to `P46_review_pit_blind_derivation.md`, frozen before any encoding
code or physics-author proof was read. The statement card
`a6d7a278654099ac970b2defb0e06c0896fd6a02:research/P46_BLIND_CLAIM_CARD.md`
was subsequently read; it supplies the additional hollow transfer restriction
p_transfer<=1/2. This is a card-based reconstruction, not a fresh numerical test.

For one new output mode put q_a=p_transfer*|W_ia|^2. Unitarity of W gives
mu=sum_a q_a=p_transfer<=1/2. Let c_r=r!*e_r(q). Expanding mu^r includes r!
times every distinct-index product and additional nonnegative repeated-index
products, so0<=c_r<=mu^r. The absolute sum of ordinary-PMF inversion terms for
occupation j therefore satisfies

    sum_(r=j)^N binom(r,j)*c_r
      <=sum_(r=j)^infinity binom(r,j)*mu^r
       =mu^j/(1-mu)^(j+1) <=2.

The old block has only one nonzero occupied input per row, so its PGF is the
Bernoulli PGF p_transfer+(1-p_transfer)z. Its PMF inversion likewise has term
sum at most2. Hence the whole hollow family has a uniform ABSOLUTE inversion
bound2, independent of N, including the N12/14 proposal.

This corrects the need for a generic large-cancellation warning within this
restricted family. It is not a relative-error bound for rare probabilities,
a proof of exact float64 probabilities, or a justification for unreported
clipping. Source-row normalization, PMF sum and correction diagnostics still
matter. The bound does not apply unchanged if the transfer probability exceeds
1/2, lossless old rows have additional populated-input couplings, or W is not
unitary. Physical attenuation can only reduce each new row's mass when applied
uniformly; general loss models need their actual row mass bound checked.

A positive-coefficient recurrence can compute c_r directly as each q_a enters:

    c_r(new)=c_r(old)+r*q_a*c_(r-1)(old),   descending r, c_0=1.

Then compensated/safe summation of the at mostN+1 signed PMF terms has the stated
absolute term bound. This removes an unnecessary factorial multiplication but
does not substitute for a roundoff analysis or independent small Fock reference.
No implementation, test, or experiment has been executed for this supplement.
