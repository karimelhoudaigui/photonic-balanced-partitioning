"""Twelve prospective literal tiny fixtures; never call main cases() or a draw."""
from fractions import Fraction as F
import importlib.util
import json
import math
from pathlib import Path
import sys

import pytest

PATH = Path(__file__).resolve().parents[1] / 'research/P79_even_loop_validation.py'
SPEC = importlib.util.spec_from_file_location('p79_tiny_fixtures', PATH)
p79 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p79)


def test_one_mode_even_coefficients_by_binomial_series():
    z = [[F(1, 2)]]
    loop, log = p79.loop_coefficients(z)
    expected = {(0,): F(1), (2,): F(1, 8)}
    for counts, coefficient in expected.items():
        assert p79.gaussian_coefficient(z, counts) == coefficient
        assert loop[counts] == coefficient
    assert log[(2,)] == F(1, 8)
    assert log[(4,)] == F(1, 64)
    assert log[(6,)] == F(1, 384)


def test_two_mode_pair_geometric_and_impossible_bunches():
    z = [[F(0), F(3, 5)], [F(3, 5), F(0)]]
    loop, log = p79.loop_coefficients(z)
    assert log[(1, 1)] == F(9, 25)
    for counts, expected in (((0, 0), F(1)), ((1, 1), F(9, 25)), ((2, 0), F(0))):
        assert p79.gaussian_coefficient(z, counts) == expected
        assert loop.get(counts, F(0)) == expected


def test_collided_and_distinct_two_photon_coefficients():
    z = [[F(1, 5), F(2, 5)], [F(2, 5), F(1, 5)]]
    # Two photons in one mode have coefficient a^2/2!, versus b^2 for11.
    assert p79.gaussian_coefficient(z, (2, 0)) == F(1, 50)
    assert p79.gaussian_coefficient(z, (1, 1)) == F(4, 25)
    loop, _ = p79.loop_coefficients(z)
    assert loop[(2, 0)] == F(1, 50)
    assert loop[(1, 1)] == F(4, 25)


def test_nonuniform_perron_rows_and_rooted_cycle_weight():
    z = [[F(1, 10), F(1, 5)], [F(1, 5), F(2, 5)]]
    tables = p79.component_tables(z, [{'indices': (0, 1), 'r': F(1, 2), 'v': (1, 2)}])
    table = tables[0]
    assert table['P'] == [[F(1, 5), F(4, 5)], [F(1, 5), F(4, 5)]]
    assert table['cdf'] == [(5, [1, 5]), (5, [1, 5])]
    assert F(1, 2)**2 * table['P'][0][1] * table['P'][1][0] / 2 == F(1, 50)
    assert table['poisson_mean'] == pytest.approx(-math.log(F(3, 4)))


def test_invalid_perron_data_and_no_probability_row_repair():
    with pytest.raises(ValueError):
        p79.integer_cdf([F(1, 3), F(1, 3)])
    with pytest.raises(ValueError):
        p79.component_tables([[F(1, 2)]], [{'indices': (0,), 'r': F(1, 3), 'v': (1,)}])
    with pytest.raises(ValueError):
        p79.component_tables([[F(0)]], [{'indices': (0,), 'r': F(0), 'v': (1,)}])


def test_raw_normalizers_and_strict_physical_boundary():
    single = p79.normalizer([[F(3, 5)]])
    assert single['determinant_Q'] == F(16, 25)
    assert single['raw_prefactor'] == pytest.approx(4 / 5)
    pair = p79.normalizer([[F(0), F(3, 5)], [F(3, 5), F(0)]])
    assert pair['determinant_Q'] == F(256, 625)
    assert pair['raw_prefactor'] == pytest.approx(16 / 25)
    with pytest.raises(ValueError):
        p79.normalizer([[F(1)]])
    with pytest.raises(ValueError):
        p79.normalizer([[F(0), F(-1, 3)], [F(-1, 3), F(0)]])


def test_exact_determinant_pivot_swap_and_poly_cross_terms():
    assert p79.determinant([[F(0), F(2)], [F(3), F(4)]]) == -6
    polynomial = {(0, 0): F(1), (1, 0): F(2), (0, 1): F(3)}
    squared = p79.poly_mul(polynomial, polynomial, degree=2)
    assert squared[(1, 1)] == 12
    assert squared[(2, 0)] == 4
    assert squared[(0, 2)] == 9


def test_signed_squeeze_coherent_coefficients_and_zero_source():
    assert p79.input_coefficient([F(-3, 5), F(0)], (2, 0)) == pytest.approx(-3 / (5 * math.sqrt(2)))
    assert p79.input_coefficient([F(3, 5), F(0)], (0, 2)) == 0
    coefficient = p79.input_coefficient([F(1, 2)], (2,))
    assert coefficient**2 == pytest.approx(1 / 8)
    with pytest.raises(ValueError):
        p79.input_coefficient([F(1, 2)], (1,))


def test_clopper_pearson_zero_and_full_count_boundaries():
    delta = 0.01 / 272
    low, high = p79.cp_interval(0, 10, delta)
    assert low == 0
    assert high == pytest.approx(1 - (delta / 2)**(1 / 10))
    low, high = p79.cp_interval(10, 10, delta)
    assert high == 1
    assert low == pytest.approx((delta / 2)**(1 / 10))


def test_strict_resource_prefix_exclusivity_and_serialization(tmp_path):
    budget = p79.StepBudget(1)
    budget.reserve()
    with pytest.raises(p79.ResourceStop):
        budget.reserve()
    assert budget.count == 1
    ledger = p79.Ledger(tmp_path / 'tiny_prefix')
    ledger.emit('fixture', exact=F(1, 3), amplitude=complex(0, 1))
    ledger.handle.close()
    assert json.loads((ledger.output / 'records.jsonl').read_text())['exact'] == '1/3'
    with pytest.raises(FileExistsError):
        p79.Ledger(ledger.output)


def test_cli_profile_rejected_before_factory_or_output(monkeypatch, tmp_path):
    output = tmp_path / 'must_not_exist'
    monkeypatch.setattr(p79, 'ROOT', tmp_path)
    monkeypatch.setattr(p79, 'PYTHON', tmp_path / 'other/bin/python')
    monkeypatch.setattr(sys, 'argv', [str(PATH), '--output', str(output)])
    def forbidden():
        pytest.fail('main factory executed before CLI guard')
    monkeypatch.setattr(p79, 'cases', forbidden)
    with pytest.raises(RuntimeError, match='contracted persistent Python'):
        p79.main()
    assert not output.exists()


def test_native_hom_two_fixed_points_and_thread_readback(record_property):
    # Literal 2modes/2photons. No cases(), Gaussian source, population or RNG.
    api, metadata, helper = p79.native_setup()
    pcvl, xq, backend_type = api
    h = math.sqrt(0.5)
    backend = backend_type()
    backend.set_circuit(pcvl.Circuit(2).add(0, pcvl.Unitary(pcvl.Matrix([[h, h], [h, -h]]))))
    observations = []
    try:
        for target, reference in (((1, 1), 0.0), ((2, 0), 0.5)):
            helper.native_readback(xq)
            backend.set_input_state(pcvl.BasicState([1, 1]))
            amplitude = complex(backend.prob_amplitude(pcvl.BasicState(list(target))))
            helper.native_readback(xq)
            observed = abs(amplitude)**2
            observations.append({'source': [1, 1], 'target': target,
                                 'amplitude': [amplitude.real, amplitude.imag],
                                 'reference': reference, 'observed': observed})
            tolerance, _ = p79.mixed_tolerance(observed, reference)
            assert abs(observed - reference) <= tolerance
    finally:
        record_property('native_hom_points', json.dumps(observations))
        record_property('native_runtime_provenance', json.dumps(metadata))
    assert helper.native_readback(xq) == 1
