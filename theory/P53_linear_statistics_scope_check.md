# P53 source applicability check — 25 November 2026

Question: does a recent efficient-simulation theorem already replace the
rank-decoded cut statistic used in P52/P53?

Seron, Thomas, Araujo, Arkhipov, Oh and Novo, *Efficient classical algorithm
for estimating linear statistics of Boson Sampling*,
[arXiv:2609.35447v1](https://arxiv.org/html/2609.35447v1), 28 September 2026,
Theorem1, Eq18, proves randomized additive CDF estimation for integer-weighted
linear photon counts in time polynomial in mode count, log(range), inverse
error and log inverse failure probability. Here their modes m=N_project and
photons n=r. Signed/rational weights are treated in AppendixA.

Applicability: **verified for the stated linear CDF; unverified for our ranked
cut**. A fixed edge's topK crossing indicator is not a linear count statistic.
Encoding the entire occupation tuple as one base-(r+1) integer does not close
the gap: its favorable ranked-cut events can require exponentially many
disjoint intervals, whereas the checked result controls one CDF/interval.
Thus this theorem alone supplies neither a scalable ranked-cut sampler nor
a general obstruction to our optimization objective. It does not invalidate
P53's separately constructed, narrowly scoped exact mean certificate attempt.

Authentication/extraction: official versioned arXiv HTML, full Theorem1 and
surrounding definitions/Eqs4–19/AppendixA read; local full-text retention not
requested. Overlap: **partial or adjacent result only**. Search was bounded to
the exact title and primary arXiv version, not a novelty survey. No numerical
experiment, external review, ledger evidence or manuscript edit is implied.
