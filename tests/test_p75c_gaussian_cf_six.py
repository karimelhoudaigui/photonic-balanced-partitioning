"""Prospective tiny fixtures only; no six-mode matrix, baseline, search or RNG."""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import math
import sys

import pytest

PATH = Path(__file__).resolve().parents[1] / 'research/P75c_gaussian_cf_six.py'
SPEC = importlib.util.spec_from_file_location('p75c_tiny_fixtures', PATH)
p75 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p75)


def test_zero_and_symmetric_two_mode_mapping():
    np = p75.numpy_module()
    z, metadata = p75.decode([0, 0, 0, 0, 0, 0, 1], 2)
    assert np.array_equal(z, np.zeros((2, 2)))
    assert metadata['zero_B']
    z, metadata = p75.decode([0, 0, 1, 0, 0, 0, 1], 2)
    assert np.array_equal(z, z.T)
    assert np.linalg.svd(z, compute_uv=False)[0] == pytest.approx(metadata['alpha'])
    assert metadata['alpha'] < 1


def test_registered_parameter_domain_rejection():
    with pytest.raises(ValueError):
        p75.decode([0] * 6, 2)
    with pytest.raises(ValueError):
        p75.decode([0, 0, 2, 0, 0, 0, 1], 2)
    with pytest.raises(ValueError):
        p75.decode([0, 0, 1, 0, 0, 0, 4], 2)


def test_two_mode_probability_three_fifths(record_property):
    value, diagnostics = p75.probability([[0, F(3, 5)], [F(3, 5), 0]])
    record_property('tiny_two_mode_observation', json.dumps({'probability': value, **diagnostics}))
    assert value == pytest.approx(144 / 625, abs=1e-12, rel=1e-10)
    assert all(diagnostics['physical_flags'].values())


def test_log_map_and_nonfloor_inverse():
    # Hand-derived q=144/625 gives loss=log(625/144), not its negative.
    loss = p75.optimizer_loss(144 / 625)
    assert loss == pytest.approx(math.log(625 / 144), abs=1e-14)
    assert loss > 0
    inverse = p75.inverse_loss(loss)
    assert not inverse['floor_boundary']
    assert inverse['probability'] == pytest.approx(144 / 625, abs=1e-14)


def test_floor_and_inverse_domain_do_not_invent_probability():
    maximum = 300 * math.log(10)
    assert p75.optimizer_loss(0.0) == pytest.approx(maximum)
    assert p75.optimizer_loss(1e-310) == p75.optimizer_loss(0.0)
    boundary = p75.inverse_loss(p75.optimizer_loss(0.0))
    assert boundary['floor_boundary']
    assert boundary['probability'] is None
    assert boundary['probability_upper_bound'] is None
    assert boundary['registered_floor'] == 1e-300
    for invalid in (-1.0, float('nan'), float('inf')):
        with pytest.raises(ValueError):
            p75.optimizer_loss(invalid)
    with pytest.raises(ValueError):
        p75.inverse_loss(maximum + 1)


def test_complex_exact_ldl_and_determinant():
    C = p75.exact_class()
    result = p75.exact_ldl([[C(1), C(0, 1)], [C(0, -1), C(2)]])
    assert result['positive_definite']
    assert result['pivots'] == [F(1), F(1)]
    assert result['leading_minors'] == [F(1), F(1)]
    assert result['determinant'] == 1


def test_two_mode_exact_probability_and_field_membership():
    C = p75.exact_class()
    result = p75.exact_witness([[C(), C(F(3, 5))], [C(F(3, 5)), C()]])
    assert result['physical']
    assert result['LDL']['determinant'] == F(256, 625)
    assert result['hafnian_norm_squared'] == F(9, 25)
    assert result['probability_squared'] == F(20736, 390625)
    assert result['probability_squared'] < F(1, 16)  # True two-photon cap squared.
    assert all(result['field_membership'].values())


def test_exact_nonpositive_boundary_and_asymmetry_rejected():
    C = p75.exact_class()
    result = p75.exact_witness([[C(1), C()], [C(), C()]])
    assert not result['physical']
    assert result['LDL']['pivots'] == [0]
    assert not p75.exact_witness([[C(), C(F(1, 2))], [C(), C()]])['physical']


def test_rounding_and_exact_serialization_two_modes():
    result = p75.rounded_witness([[complex(0), complex(0.6)], [complex(0.6), complex(0)]])
    assert result['physical']
    assert result['Z'][0][1].r == F(3, 5)
    payload = json.loads(p75.encoded(result))
    assert payload['Z'][0][1] == ['3/5', '0']
    assert payload['probability_squared'] == '20736/390625'


def test_strict_budget_and_exclusive_record_prefix(tmp_path):
    counter = p75.Counter(2)
    assert counter.reserve() == 1
    assert counter.reserve() == 2
    with pytest.raises(p75.BudgetStop):
        counter.reserve()
    assert counter.count == 2
    path = tmp_path / 'tiny_records'
    ledger = p75.Ledger(path)
    ledger.emit({'kind': 'tiny_fixture', 'probability': F(144, 625)})
    ledger.handle.close()
    with pytest.raises(FileExistsError):
        p75.Ledger(path)


def test_cli_profile_rejects_before_any_population(monkeypatch, tmp_path):
    output = tmp_path / 'must_not_exist'
    monkeypatch.setattr(p75, 'ROOT', tmp_path)
    monkeypatch.setattr(p75, 'PYTHON', tmp_path / 'other_environment/bin/python')
    monkeypatch.setattr(sys, 'argv', [str(PATH), '--output', str(output)])

    def forbidden(_):
        pytest.fail('population executed before the CLI profile guard')

    monkeypatch.setattr(p75, 'run', forbidden)
    with pytest.raises(RuntimeError, match='contracted persistent Python'):
        p75.main()
    assert not output.exists()
