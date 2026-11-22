# Density attribution: second search strategy and sharper overlap

Coordinator second pass, 2026-11-22; not a fresh-searcher review. Starting
checkpoint: P33 theorem75e5831 and attribution report66141f5. The new native
replicationb8b04ac supplies finite validation, not novelty. No manuscript edit.

Search strategy: connect our row-max/second-moment step to statistical decision
theory, rather than search only boson-sampling terminology. Web-index queries
covered Bayes error/Gini impurity bounds, Gram/Bayes/Frobenius and
Gram/Hellinger/permanent, plus arXiv-restricted minimum-intensity,
dominant-support and collision/density/classical-simulation terms. The checked
horizon is2026-11-22. Irrelevant or absent hits do not establish absence of prior
work. Forward-citation and non-English coverage remain incomplete.

Primary source authenticated and extracted: O. Rioul, *The Interplay between
Error, Total Variation, Alpha-Entropy and Guessing*, Entropy25(2023),978,
[published author-hosted copy](https://perso.telecom-paristech.fr/rioul/publis/202306rioul.pdf),
DOI10.3390/e25070978. Equations3/5 define complementary coincidence R2 and
Bayes error Pe. Equation75 gives their sharp unconditional relation; its
Pe<=1/2 branch has lower envelope2Pe(1-Pe). Equation76 gives the conditional
lower bound R2>=Pe. These statements are checked in the published31-page PDF.
No photonic full-law theorem is stated by this extraction.

Our source-to-project dictionary and its limits are as follows. Choose occupied
input label A uniformly from k columns, with joint mass Pr(A=a,I=i)=q_ia/k.
The conditional label probabilities at a nonzero output row are p_a=q_ia/a_i.
Let e_i=1-max_a p_a and g_i=1-sum_a p_a². Direct substitution gives

    delta/k = Pr(MAP label error),
    delta = sum_i a_i e_i,     M = sum_i a_i² g_i.

Thus the row quantities are known statistical objects. The weights in M are
a_i², whereas ordinary conditional averaging uses a_i/k. This prevents silently
identifying the physical expected-pair count with conditional Gini impurity.
The density floor supplies the missing weight comparison:

    M >= c sum_i a_i g_i >= c sum_i a_i e_i = c delta.

For the refined implication, the project's elementary row argument uses
g_i>=2e_i(1-e_i), yielding

    M >= 2c delta - 2 sum_i(a_i e_i)² >= 2c delta - 2delta².

Together with the coarse branch this gives the existing small quadratic root.
It is not valid to replace this rowwise calculation by an unqualified quadratic
bound on a conditional average. The source's unconditional binary branch
overlaps the row step; its conditional bound alone is weaker in the required
weighted setting. These are explicit coordinator translations, not a source
claim about indistinguishable photons.

Overlap labels: row impurity ingredients **known after translation of notation**;
density-floor aggregation **formal corollary not stated**. The standalone
M/c lemma or row quadratic inequality should not be sold as a new discovery.
The remaining photonic composition (dominant-support Gram estimate, density
control, full-law consequence and sharp balanced example) has unresolved exact
attribution. Its novelty remains OPEN, rather than promoted by a failed search.

PDF SHA25657c700e2acbf48044d049f7458ad468e70e4aceaceaf0e1bb764728ca1683b4f;
text SHA2565c9b7fe0ac78c9084afe112d4539eff9f0c32bee4d20e59244155e4f1ce3ef70.
Extraction metadata are in the ignored `.local/references/rioul_2023/source.json`;
the source is CC BY and retained
locally only. Subsequent independent review should check the full composition
and cross-field matrix-norm literature, not merely repeat these elementary
row inequalities. Original optimization benefit remains unestablished.
