# P49 caller — static correction review

**Verdict: PASS STATIC REVIEW**, closing the constructor-setup reservation of
`research/P49_review_caller_927448a.md` (review commit `45717ae`). No P49 import,
test, graph or numerical execution was performed here; the 42-case preflight
remains a separate coordinator-authorized obligation.

Reviewed only the frozen delta from `927448ab1e3434e83c93f436cbfa9681284dc5f2`
to `3d6a1f2e2333f8c7bee39bfe6753a0423b2e3c18` in the encoding worktree.
Exact SHA256 values checked by reading bytes:

- Primary `research/P49_trained_source_probe.py`:
  `384057373739a90bbe6ec0f37726324b222ceeed2609bec57ae0dfebd700b7f5`
- Integration tests `tests/test_p49_trained_source.py`:
  `1baeb2e478417e1cd1dcb9f456ee65c8a506e5a1401046b63fbb23dc691e03af`
- Spec, unchanged:
  `275bb9bcae40e0f4d7ba7ee8945c40435b617c89134f83e8e598ab7437387a42`
- Main contract:
  `ab145c57f48a8e197f116e593de94ee7681b9531a9ef4ba6d426617bfc99b363`
- Preflight contract:
  `420a348aa24d722e2d0b79f7ba2a3c8eb70d6956b49f81da5cce90606363d8b0`

The backend interval now brackets `make_optical_sampler` alone. The caller
measures total constructor wall/CPU, subtracts that backend interval, guards
against invalid negative remainders, and records classical setup separately.
Thus the previously omitted constructor role hashes, seeds, jitter/noise RNGs
and closures contribute to B's classical setup ledger and FAST wall-derived
CPU grant. Total setup and components are explicitly labelled subtotals;
adding them twice is forbidden. Backend/count generation and JSON remain
excluded from that grant. This does not turn simulator latency into QPU cost.

Controlled-clock tests now specify total7=backend5+classical2, plus a FAST
allowance .01 common+.004 classical setup+.03 post+.001 selection=.045.
These assertions were read, not executed by this reviewer. Main and preflight
closures retain their 13/14 exact paths; the preflight seed declaration adds
the already-qualified FAST fixture seeds, not new experimental seeds.

There is no change to training loss, selection/evaluation order, photon source,
policy grid, graph population, random streams or the FAST module. The original
static findings on those caller components therefore stand. This review is
scoped to the caller: I authored FAST, whose independent module audit belongs
to physics. Same broad research context is disclosed. No encoding files were
edited and no scientific positive, timing benchmark, held-out, hardware or
novelty claim follows from this PASS.
