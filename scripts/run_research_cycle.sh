#!/bin/sh
set -eu
RESEARCH_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec "$RESEARCH_ROOT/.venv/bin/python" "$RESEARCH_ROOT/scripts/run_research_cycle.py" "$@"
