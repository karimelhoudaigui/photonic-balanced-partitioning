# Hardware access disabled

The old runner, connectivity check and smoke test simulated hardware and are
withdrawn. They now exit with status 2 without contacting any service or
creating result files. No local result can be labelled as QPU evidence.

Use `PYTHONPATH=src .venv/bin/python experiments/run_research.py --help` for
ideal research simulations. See `reports/QPU_READINESS.md` for hardware gates.
Any future actual QPU call requires explicit authorization. Credentials must
never be placed in source code or recorded experiment artifacts.
