"""Tiny administrative/analytic guards; scientific fixtures live in --mode qualify.

No production permanent loop, no archived probability inspection, no random draw.
"""
import importlib.util
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "research/P52_naive_replication.py"
SPEC = importlib.util.spec_from_file_location("p52_naive_independent", SOURCE)
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


def test_enumeration_all_multisets():
    rows = probe.occupations()
    assert len(rows) == len(set(rows)) == 6435
    assert all(sum(row) == 8 and len(row) == 8 for row in rows)
    assert (8, 0, 0, 0, 0, 0, 0, 0) in rows
    assert (1,) * 8 in rows
    assert probe.occupations(3, 0) == [(0, 0, 0)]


def test_scalar_zero_phase_is_walsh_tensor():
    matrix = probe.scalar_unitary(0)
    expected = [1, 1, 1, 1, -1, -1, -1, -1]
    assert [round(x.real * (8 ** .5)) for x in matrix[4]] == expected
    for i in range(8):
        for j in range(8):
            product = sum(matrix[a][i].conjugate() * matrix[a][j] for a in range(8))
            assert abs(product - (i == j)) < 1e-14


def test_existing_output_refused_before_physics(tmp_path, monkeypatch):
    def forbidden():
        raise AssertionError("scientific backend must not load")
    monkeypatch.setattr(probe, "load_backend", forbidden)
    monkeypatch.setattr(probe.sys, "argv", ["probe", "--mode", "qualify", "--output", str(tmp_path)])
    with pytest.raises(ValueError, match="fresh"):
        probe.main()


def test_historical_destination_and_traversal_refused():
    with pytest.raises(ValueError, match="historical"):
        probe.fresh_output(probe.ROOT / probe.REFERENCE / "never_created_replica")
    with pytest.raises(ValueError, match="fresh"):
        probe.fresh_output(probe.ROOT / "../never_created_replica")


def test_reference_pins_and_phase_grid():
    assert len(probe.check_reference()) == 6
    with pytest.raises(ValueError):
        probe.scalar_unitary(4)
    assert len(probe.PINNED) == 6


def test_optional_observation_failure_is_nonblocking(monkeypatch):
    # No real ps call: both denied process observation and timeout are optional.
    for error in (PermissionError(1, "mock sandbox denial"),
                  probe.subprocess.TimeoutExpired("ps", 2)):
        def denied(*args, **kwargs):
            raise error
        monkeypatch.setattr(probe.subprocess, "run", denied)
        result = probe.thread_snapshot()
        assert result["available"] is False
        assert result["error_type"] == type(error).__name__
        assert result["errno"] == getattr(error, "errno", None)
        assert result["error"] == str(error)
    def denied_platform():
        raise PermissionError(1, "mock metadata denial")
    monkeypatch.setattr(probe.platform, "platform", denied_platform)
    assert probe.platform_snapshot()["available"] is False
