# P45-B — full-Fock cost-hop walk: negative DEV discriminator

Date:25-Nov-2026. Source revision92d542bbc3856312144ae01a570403e0ec42aa1f.
Design/code freeze bc89be5; execution contract67745d6; targeted preflight92d542b.
This is a completed DEV screen, not held-out evidence or independent physical
replication. It leaves the wider full-Fock mechanism route open.

## Outcome

**REJECT this frozen circuit family/budget as a useful optimization result.**
The full-Fock decoder worked: all800 bosonic samples were feasible balanced
partitions, including730 collisional occupations that the old decoder would
discard. Yet one fixed classical annealing control, with the same200 new
score budget and common frontend, found a better cut on EVERY graph.

| Fixed DEV graph | Common C_front | Bosonic best | Reoptimized D best | Fixed anneal best | Best classical control observed |
|---|---:|---:|---:|---:|---:|
|16 weighted ER|104|89|85|78|78|
|16 weighted RR|50|47|50|38|28|
|20 weighted ER|140|116|119|96|96|
|20 weighted RR|70|52|61|33|29|

All best values include common-front, training and fresh candidate discoveries.
The last column is diagnostic best-of-controls, not a200-score portfolio;
the single predeclared annealing column alone already supplies the veto.
Each standalone algorithm pays common68/104 scores on16/20vertices, plus200
new scores. No preprocessing candidate is credited as a quantum discovery.

The globally selected B setting was t=2.1,kappa=0, also selected by D. The
nonzero graph-dependent phase was therefore NOT selected for B. The outcome
does not support the proposed chiral cycle-flux explanation.

Fresh selected B batches produced16 improving samples out of512, with total
clipped gain87 below C_front. D's fresh total clipped gain was also87;
phase-multinomial gave109, source-Pólya88 and the inclusion process105.
These are finite DEV observations, not expectation inequalities or statistical
significance claims. In the16-RR case B's best47 occurred during training;
both fresh batches gave no improvement below the common50. No positive
independent replication or hardware preparation is justified.

## Execution and verification

The three new deterministic decoder/frontend/relabel tests passed in1.20s;
the actual XML and command receipt are in
`experiments/P45_encoding/preflight_001/`. The Clifford2017 backend method
was unchanged from the separately validated P43 implementation.

The unique bounded pilot was executed with the existing pinned venv via
Mathbox `run_experiment.py`, using the EXACT9 artifacts listed in
`research/P45_encoding_execution_contract.json`. The exact child argv,
versions, clean source Git state, before/after input hashes and limits are in
`experiments/P45_encoding/run_001/manifest.json`. Status is `completed`,
exit0, all inputs unchanged. The manifest validator accepted it.

Wall time was17.303786s. Script-reported process CPU after imports was
1.497181s; this is not total process-tree CPU or a hardware-latency measure.
The runner enforced60CPU/90wall seconds and one conventional numerical
thread, without an unsupported Darwin affinity or address-space claim.
Output occupied2.9MiB, below the32MiB plan. Stderr retains real Perceval and
Matplotlib cache-directory warnings; no dependency installation or remote
service occurred.

There are11552 raw records:11544 scored candidates and8 relabel-map records.
The scored total is344 common discoveries plus56 case/model groups of200
new scores each. All occupations, subsets, raw cuts, clipped gains, seeds,
accepted classical moves and collision data are retained. Modeled ideal B
source photons total7200; actual QPU photons and calls are zero.

A post-run AUTHOR check using only the standard library independently
reimplemented the decoder and cut arithmetic, verified all11544 raw costs,
all occupancies and transported labels, common fronts, each200-score group,
terminal minima and all independently selected settings. Its receipt is
`experiments/P45_encoding/author_raw_check_001.json`. This is an author
consistency check, not independent backend/physics replication. The exact
check command was executed after the pilot and does not change its frozen
design or raw outputs.
`research/P45_encoding_author_raw_check.py` preserves equivalent standard-library
checks for reproduction with --run and a fresh --output. It was written after
the pilot and is not part of its preregistered physical execution closure.

Raw SHA256:
`58b0d5db60597332c7de4029c3a99554816f67daafb4cd556852f5c6e3a43323`.
Summary SHA256:
`eb4451be89da4f06e1037252cfcf20d9dd3dadca815dd46d28f048981e7d2b9f`.
Selection SHA256:
`5fdd11cf0bcc7da8e2bf51b4c1cd1019acb92ae333f6487e9ac5af116368affd`.

## Interpretation and attribution

The encoding is a genuine change of candidate geometry and uses collisions,
but that is not an optimization benefit by itself. The simple cost-hop
generator failed against strong feasible search and several nonquantum
proposal explanations. A wider parameter sweep of this unchanged protocol
is not warranted by the observed screen. Any new run should change a
scientific bottleneck and freeze another hypothesis first. The result does
not refute every possible graph-dependent full-Fock interferometer or source.

Stars/bars and Haar-average uniform Fock occupations are known. The exact
primary preprint inspected was Clifford–Clifford,
[arXiv:2005.04214v2](https://arxiv.org/pdf/2005.04214v2),26May2020:
Theorem3/Eq6, printed p6, and Section6, pp7–8. The later journal record is
Phys. Scr.99(2024)065121, DOI10.1088/1402-4896/ad4688. The source's combinatorial
bijection and averaging result do not prove optimization enrichment for a
graph-programmed fixed circuit. The uniform Dirichlet/Pólya control makes
that null explanation explicit here. No novelty clearance is claimed for
this composition; root's additional coarse-graining literature leads remain
future source-checking work if a different positive mechanism emerges.

No held-out graph, optimum cost/mask, new manuscript text, QPU preparation,
hardware acquisition or message to Laurent was used. Loss/preparation costs
remain mandatory for any future physical use, as stated in the frozen contract.
