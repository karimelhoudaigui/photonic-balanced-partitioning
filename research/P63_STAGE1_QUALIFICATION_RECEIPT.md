# P63 stage-one qualification actually executed

ROOT executed the frozen synthetic qualification once at original worker
commit `8b20dca7bbe476a2eed75433b31e5ca582809484`. Source SHA256 is
`7f60cb437a9936323851d926ca18f16c7899b16a8d5353c69df88cf21a03d5d6`;
tests SHA256 is
`1bf5baac5740e75a37096dd841c10d4b5486691811259062bd15a569f7d2bd9b`.
ROOT read the full source, tests, spec, both contracts and caller amendment
before execution. A separate static adversarial review is being recorded.

The exact child argv in the frozen preflight contract was launched through
the installed computation-audit v2 runner, with all18 declared execution
artifacts as inputs. Actual interpreter: persistent project
`.venv/bin/python`, Python3.11.15; all37 lock versions were checked during
recovery. CPU60/wall90, environment threads1, logs32MiB. Logical256MiB is a
prospective plan, not hard Darwin RSS/affinity enforcement.

Observed result: **46 passed**, pytest15.85s, runner16.399157s, exit0,
manifest status completed. Validation with `validate_manifest.py --root .`
passed, with no missing or invalid declared result. The real native fixture
was only the two-photon/two-mode HOM case, eight draws; native maximum1 was
set and read back. Mocked B80 and matrix18 checks are not native18 sampling.
No DEV graph, true18-photon sample, training data or phase search occurred.

Six Perceval warnings report its inaccessible default persistent directory
and fallback to the allowed temporary directory. This did not change the
local backend/source or require credentials. No remote client was created.

Raw runner logs, JUnit and input/output hashes are preserved under
`research/P63_spsa_fast_stage_preflight/run_001/`. No retry or source change
followed this run. Qualification verifies these finite synthetic assertions;
it is not an independent18-photon physical replication, optimizer advantage,
performance forecast or automatic main/QPU authorization. ROOT must separately
authorize and inspect the sole prospective B80/FAST main.
