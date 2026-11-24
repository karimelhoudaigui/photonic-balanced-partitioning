# P42 encoding lane — bounded primary-source comparison

Date: 2026-11-24. Claim under review:
[physical-loss domination](../theory/P42_encoding_loss_domination.md).
This is an attribution and scope check, not an independent proof audit or a
certificate of novelty. No P42 numerical computation is claimed. P41 source
files and raw data remain sealed.

The encoding lane independently reconstructed the random-wave CF and
threshold proposals before receiving the coordinator's spectral threshold
proof. The spectral rank argument in Section 8 is coordinator-origin; its
negative-binomial bound improvement to eta<=1/5 was obtained after reading
that argument. Both lanes share P41 context. There has not been a second
independent literature search in this lane.

## Authenticated dependencies

| Dependency | Primary source and inspected locator | Translation and disposition |
|---|---|---|
| Random-sign permanent identity | Aaronson–Arkhipov, *The Computational Complexity of Linear Optics*, [author PDF](https://www.scottaaronson.com/papers/optics.pdf), Appendix 12, Lemma 64, Eqs. 452–454, PDF pp. 94–95; Lemma 65 immediately follows. | Setting the row linear forms to the selected output modes gives the square-matrix permanent coefficient. Using all size-k sign characters simultaneously for N>=k is the elementary orthogonal-Fourier/Bessel extension. The scalar identity is known, not a new theorem. |
| Uniformly lost input subsets | Aaronson–Brod, *BosonSampling with Lost Photons*, [arXiv:1510.05245v2](https://arxiv.org/pdf/1510.05245), dated 2 November 2015, Section 2, Eqs. 5–6, PDF p. 2. Published Phys. Rev. A 93, 012335 (2016). | Their n+k inputs and n surviving photons correspond here to N and k. Their conditional mixture divides by binom(N,k); the physical per-emission mixture here instead weights every survivor set by eta^k(1-eta)^(N-k). The formula is an established ingredient. Their later Haar/hardness setting is not an assumption of the elementary mixture identity. |
| Fixed-size product-weight sampling | Kulesza–Taskar, *Determinantal Point Processes for Machine Learning*, [author PDF](https://www.alexkulesza.com/pubs/dpps_fnt12.pdf), Foundations and Trends in Machine Learning 5(2–3), 123–286 (2012), DOI 10.1561/2200000044; Eq. 5.13, Algorithm 7, Theorem 5.2 and Algorithm 8, printed pp. 208–212 (PDF pp. 87–91). | The source computes elementary-symmetric normalizers and samples eigenvalue subsets of fixed size in O(Mk). A diagonal kernel with diagonal w_i gives exactly the law proportional to product of selected weights. The suffix recurrence here reverses its index order. Neither the DP nor its complexity is novel. |
| Related amplitude estimators | Yung–Gao–Huh, *Universal Bound on Sampling Bosons in Linear Optics*, [arXiv:1608.00383v1](https://arxiv.org/pdf/1608.00383), dated 1 August 2016; full six-page version inspected in P41. Published expanded work, National Science Review 6(4), 719–729 (2019), DOI 10.1093/nsr/nwz048. | Known permanent/amplitude identities and Monte Carlo estimation overlap with the algebraic ingredient. An unbiased amplitude estimator is not automatically a normalized probability law pointwise dominating the physical accepted-output law. That additional normalization and acceptance problem must be checked separately. |

No source is needed for a theorem merely named without a proof: the sign
coefficient, Bessel inequality, smoothing bound, DP telescoping, Poisson
exponential-moment estimate, Fock projector rank and adaptive survival-product
arguments are all proved in the accompanying note. Primary dependencies
are used for attribution and model comparison, not as substitutes for those
proofs. Uniform loss commuting through a passive circuit also follows
directly by coupling every system mode to a vacuum mode with the same
beamsplitter transmissivity; it must not be extended to arbitrary loss.

## Nearby results and unresolved overlap

The public source search also identified work on classical approximation
of lossy BosonSampling and on lossy Gaussian-boson optimization. Those
problems require separating three tasks:

1. reproducing a normalized full output law, usually in total variation;
2. improving the quality of a conditioned accepted output;
3. dominating a physical subprobability on feasible graph candidates, with
   all rejected emission attempts retained in the denominator.

The P42 claim concerns task 3. The rank-based uniform control additionally
bounds adaptive threshold hitting under its stated model. It does not prove
task 1 and cannot invalidate BosonSampling hardness in another regime.

Examples of relevant primary source records checked at bounded scope:

- Brod–Oszmaniec, *Classical simulation of photonic linear optics with lost
  particles*, [arXiv:1801.06166](https://arxiv.org/abs/1801.06166), New J.
  Phys. 20, 092002 (2018). The source abstracts and prior local source
  context concern approximate output simulation under particle losses and
  the movement of uniform loss through circuits. Its complete proof has
  not been re-audited for P42, so no claim that it excludes the present
  composition is warranted.
- Solomons–Thomas–McCutcheon, *Effect of photonic errors on quantum enhanced
  dense-subgraph finding*, [Phys. Rev. Applied 20, 054043](https://journals.aps.org/prapplied/abstract/10.1103/PhysRevApplied.20.054043)
  (21 November 2023). The primary abstract addresses loss and source impurity
  in Gaussian-boson dense-subgraph heuristics and notes classically simulable
  regimes retaining utility. It does not establish the present passive
  single-photon worst-case threshold domination statement.
- Angrisani–Mhiri, [arXiv:2611.08444v1](https://arxiv.org/abs/2611.08444), and
  Lim, [arXiv:2611.01434v1](https://arxiv.org/abs/2611.01434): contemporary
  primary abstracts were checked during the investigation. Their
  Haar/average-case full-output-loss simulation context differs from the
  stated arbitrary-interferometer utility comparison. Their full proofs
  have not been authenticated in this lane. A global novelty conclusion
  would require checking those proofs and their citation chains.

The following ingredients and implications must therefore be labeled:

- **KNOWN:** random-sign permanent identity; conditional loss mixture;
  fixed-size product-weight DP; basic spectral, combinatorial and Chernoff
  inequalities.
- **SELF-CONTAINED DERIVATION, INDEPENDENT AUDIT PENDING:** simultaneous
  survivor-subset Fourier domination, physical-loss normalization, and
  threshold exponential-wave cover with its uniform sufficient constant.
- **COORDINATOR-ORIGIN, AUDIT PENDING:** threshold Fock-rank cap and adaptive
  uniform benchmark under unequal declared attempt ceilings.
- **NOVELTY OPEN:** whether the normalized covers or the worst-case adaptive
  optimization obstruction have already appeared in this form or as an
  immediate explicitly stated corollary elsewhere.

## Search boundary and remaining work

Searches on 2026-11-24 used the public English-language web index and the
author/arXiv primary pages. Query families included lost BosonSampling
uniform input-subset mixtures; random-sign/Gurvits probability samplers;
elementary-symmetric and Maclaurin normalizers; full-input single-photon loss;
threshold support majorization; photonic optimization with classical uniform
controls; and conditional-Poisson/diagonal-k-DPP algorithms. This is a finite
search, not a claim that no matching result exists.

An independent reviewer should check the exact comparison with full-input
loss results, known phase-randomized coherent-light optimization baselines,
and state/order domination methods. It should also verify whether practical
shot denominators and calibrated transmissions satisfy the hypotheses. An
attractive platform-average number alone cannot instantiate the theorem.

No QPU call, manuscript edit, installation, benchmark or independent
acceptance was performed by this P42 lane.
