"""Regression against local simulations being labelled as QPU results."""
import subprocess
import sys
from pathlib import Path


def test_all_old_hardware_entrypoints_fail_closed(tmp_path):
    root = Path(__file__).resolve().parents[1]
    for script, args in [
        ("run_qpu.py", ["--backend", "qpu:belenos", "--config", "missing.yaml"]),
        ("check_backend.py", []), ("smoke_test.py", []),
    ]:
        proc = subprocess.run([sys.executable, str(root / "qpu" / script), *args],
                              cwd=tmp_path, capture_output=True, text=True)
        assert proc.returncode == 2, proc.stderr
    assert not list(tmp_path.iterdir())
