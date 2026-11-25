# P53b independent exact certificate check: PASS

Actual result: **PASS**, production status
`EXACT_POINT_ENDPOINT71_SEPARATION_CERTIFIED`; exact primal false, exact dual
true, strict rational gap767/327680. All71 vertices and28 coordinates were
checked. This establishes the finite fixed-point separation from ENDPOINT71
on the trusted exact source data; it is not optimization/hardware advantage.

ROOT reviewed the full98-line checker and authorized this single fresh child
on clean `018641ebfe410bc92fb974d0c333f0329be40bb0`. Source SHA256
`1ffc267914f4489d2dac6f602c4aff7328543b9934f874d554703cb97b6450ac`.
The checker imports standard library only, recomputes the target by the direct
sum of power_j*(1/4)^j rather than production Horner, and verifies exact raw
typed fractions/labels/normalizations, source/exported target/library equality,
primal29 equations/nonnegativity, binary dual reconstruction/L1/all71 strict
margins, graph shift/normalization and winning status/success gates. Its
integrated synthetic corruption guards also ran without error. Assertions
were enabled as required, and no simultaneous primal/dual was accepted.

The source graph's normalized gap767/4587520 was checked via its exact weight
normalization and all recomputed margins. This is a posthoc graph for the
fixed endpoint library, not a fresh benchmark. All35 b4 controls at the SAME
theta=pi/3 remain a mandatory separate question; no new value of those controls
was computed here.

Independence is arithmetic/method/code only. I knew ROOT's announced outcome
before writing this checker, as recorded by `posthoc_not_blind=true`. No
production module, NumPy/SciPy, native solver, backend, RNG or hardware was
called. The exact P53 optical source and its probability convention were not
reconstructed anew; their previously audited byte-pinned artifacts are trusted
inputs. The checker is not a new blind/external physics validation.

Actual runner command from the isolated worktree:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication --contract research/P53b_independent_checker_contract.json --output research/P53b_independent_check/run_001 --input research/P53b_independent_checker.py --input research/P53b_independent_checker_contract.json --input experiments/P53_exact_phase/run_001/data/exact_source.json.gz --input experiments/P53_exact_phase/run_001/data/exact_library.json.gz --input experiments/P53b_fixed_point/run_001/data/certificate.json.gz --result research/P53b_independent_check/run_001/data/check.json --timeout 10 --max-output-bytes 1048576 --max-cpu-seconds 5 --max-threads 1 -- /private/tmp/pbp-clean-venv-20261124/bin/python research/P53b_independent_checker.py --output research/P53b_independent_check/run_001/data/check.json
```

Start2026-11-25T12:28:08.354719+00:00, runner wall0.16657s, completed exit0
within CPU5/wall10/threadenv1/log1MiB. Python3.11.15;
child CPU0.092993s and wall0.093050542s. These are the one child process's
measurements, not a solver benchmark. All five input SHA256-before/after
pairs agree. The three raw proof files were copied byte-identically from
primary a2cf5d9; no primary raw was rewritten. No retries or additional
calculations followed. The exclusive slot was released immediately after
reading and validating the outcome.

Sealed outputs under `research/P53b_independent_check/run_001/`:

| File | SHA256 |
|---|---|
| manifest.json | 71f01f0480721cf38e399afe8392929cac08aa6578ea8073dfc57152d20b0720 |
| data/check.json | f01da81d04f914bdaeac239f249b96b9dbb14cb771c0d9c84ddf8ed30b8f6116 |
| stdout.txt | 5ee1f07f5b1209a5e1f12c6e9825f141594fc8d10116ee72b9afa37a0065cb4d |
| stderr.txt (empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |

Actual validation command returned0, valid evidence record status completed:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py research/P53b_independent_check/run_001/manifest.json --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication
```

No claim against continuously reoptimized b4, phase/sphere/Gauss, arbitrary
feasible classical search, tails, full distributions, scalability, total
resources, novelty or hardware follows. P53's inconclusive global Bernstein
result stays unchanged. This receipt verifies a different, one-point exact
claim and is not positive-goal completion.
