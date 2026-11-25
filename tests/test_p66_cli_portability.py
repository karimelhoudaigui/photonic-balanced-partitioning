"""Keep machine-pinned experiments separate from portable native unit tests."""
from fractions import Fraction
import importlib.util
from pathlib import Path
import sys

import pytest


@pytest.fixture(scope="module")
def helper():
    path = Path(__file__).resolve().parents[1] / "research/P66_exact_finite_check.py"
    spec = importlib.util.spec_from_file_location("p66_portability_regression", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_experiment_cli_rejects_an_uncontracted_interpreter(helper, monkeypatch, tmp_path):
    output = tmp_path / "must_not_exist"
    monkeypatch.setattr(helper, "ROOT", tmp_path)
    monkeypatch.setattr(helper, "PERSISTENT_PYTHON", tmp_path / "different_environment/bin/python")
    monkeypatch.setattr(sys, "argv", [str(helper.__file__), "--output", str(output)])

    def forbidden_run(_):
        pytest.fail("The experiment must reject the interpreter before starting")

    monkeypatch.setattr(helper, "run", forbidden_run)
    with pytest.raises(RuntimeError, match="contracted persistent Python"):
        helper.main()
    assert not output.exists()


def test_native_loader_remains_portable_with_a_real_physics_check(helper, monkeypatch, tmp_path):
    monkeypatch.setattr(helper, "PERSISTENT_PYTHON", tmp_path / "different_environment/bin/python")
    api, metadata = helper.native_api()
    assert Path(metadata["interpreter"]) == Path(sys.executable).resolve()
    assert metadata["threads"] == 1
    # Rational unbalanced splitter: its CF two-photon probability is 49/625.
    u = [[helper.C(Fraction(3, 5)), helper.C(Fraction(4, 5))],
         [helper.C(Fraction(-4, 5)), helper.C(Fraction(3, 5))]]
    backend = helper.native_backend(u, api)
    _, probability = helper.native_point(backend, [1, 1], [1, 1], api)
    assert probability == pytest.approx(49 / 625, abs=1e-12, rel=1e-7)
    assert helper.native_readback(api[1]) == 1
