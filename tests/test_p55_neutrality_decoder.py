"""Exact synthetic count/rank fixtures only: no graph, RNG draw or optics."""
import importlib.util
import itertools
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p55", ROOT / "research/P55_neutrality_decoder.py")
p55 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p55)


def compositions(length, total):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(length - 1, total - first):
                yield (first,) + tail


def brute_minimizers(counts):
    subsets = list(itertools.combinations(range(len(counts)), len(counts) // 2))
    error = {s: abs(2 * sum(counts[i] for i in s) - sum(counts)) for s in subsets}
    minimum = min(error.values())
    return minimum, {s for s, value in error.items() if value == minimum}


@pytest.mark.parametrize("n", [2, 4, 6])
def test_ALL_small_count_vectors_and_ALL_mock_ranks_are_exact_uniform_bijections(n):
    for total in range(n + 1):
        for counts in compositions(n, total):
            decoder = p55.NeutralityDecoder(counts)
            minimum, expected = brute_minimizers(counts)
            actual = [decoder.unrank(rank) for rank in range(decoder.ways)]
            assert decoder.minimum_imbalance == minimum
            assert decoder.ways == len(expected)
            assert len(actual) == len(set(actual)) and set(actual) == expected
            assert sum(decoder.target_ways) == decoder.ways
            for rank, subset in enumerate(actual):
                calls = []
                def mock_randbelow(bound):
                    calls.append(bound)
                    return rank
                assert decoder.sample(mock_randbelow) == subset
                assert calls == [decoder.ways]


@pytest.mark.parametrize("counts", [(0, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0),
                                    (6, 0, 0, 0, 0, 0), (3, 0, 0, 0, 0, 0),
                                    (1, 1, 1, 1, 1, 1)])
def test_vacuum_one_photon_all_bunched_and_all_one_return_UNIFORM_ALL_subsets(counts):
    decoder = p55.NeutralityDecoder(counts)
    assert decoder.ways == math.comb(6, 3)
    assert {decoder.unrank(r) for r in range(decoder.ways)} == set(itertools.combinations(range(6), 3))


@pytest.mark.parametrize("n", [4, 6])
def test_doublon_hole_forces_THE_SAME_side_without_conditioning_physical_shots(n):
    counts = (2, 0) + (1,) * (n - 2)
    decoder = p55.NeutralityDecoder(counts)
    expected = {s for s in itertools.combinations(range(n), n // 2) if (0 in s) == (1 in s)}
    assert decoder.minimum_imbalance == 0
    assert {decoder.unrank(r) for r in range(decoder.ways)} == expected


def test_smallest_N2_uses_minimum_error_when_exact_neutrality_is_impossible():
    decoder = p55.NeutralityDecoder((2, 0))
    assert decoder.minimum_imbalance == 2 and decoder.target_sums == (0, 2)
    assert {decoder.unrank(0), decoder.unrank(1)} == {(0,), (1,)}


@pytest.mark.parametrize("counts", [(4, 1, 0, 0), (6, 6, 0, 0, 0, 0)])
def test_M_above_N_and_odd_no_exact_half_are_decoded_not_rejected(counts):
    decoder = p55.NeutralityDecoder(counts)
    minimum, expected = brute_minimizers(counts)
    assert decoder.total > decoder.n
    assert decoder.minimum_imbalance == minimum
    assert {decoder.unrank(r) for r in range(decoder.ways)} == expected
    if counts == (4, 1, 0, 0):
        assert minimum == 3 and decoder.target_sums == (1, 4)


def test_complement_symmetry_and_relabeling_are_LAW_identities_not_same_rank_couplings():
    counts = (0, 2, 0, 1, 2, 1)
    decoder = p55.NeutralityDecoder(counts)
    law = {decoder.unrank(r) for r in range(decoder.ways)}
    assert {tuple(i for i in range(6) if i not in s) for s in law} == law
    permutation = (2, 0, 5, 1, 4, 3)
    other = p55.NeutralityDecoder(tuple(counts[i] for i in permutation))
    mapped = {tuple(sorted(permutation[i] for i in other.unrank(r))) for r in range(other.ways)}
    assert mapped == law and decoder.ways == other.ways


def test_python_integer_ways_exceed_64_bits_without_overflow_or_float_draws():
    decoder = p55.NeutralityDecoder((0,) * 70)
    assert decoder.ways == math.comb(70, 35) and decoder.ways > 2**64
    assert decoder.unrank(0) == tuple(range(35))
    assert decoder.unrank(decoder.ways - 1) == tuple(range(35, 70))
    assert decoder.sample(lambda bound: bound - 1) == tuple(range(35, 70))


@pytest.mark.parametrize("counts", [(), (0,), (0, 0, 0), (-1, 0), (True, 0),
                                    (1., 0), (0,) * 130, (4097, 0), (32,) * 128])
def test_invalid_or_oversized_inputs_fail_BEFORE_a_DP_allocation(counts):
    with pytest.raises((TypeError, ValueError)):
        p55.NeutralityDecoder(counts)


@pytest.mark.parametrize("rank", [-1, 6, .5, True, None])
def test_invalid_integer_ranks_or_bad_oracle_values_are_not_resampled(rank):
    decoder = p55.NeutralityDecoder((1, 1, 1, 1))
    with pytest.raises((TypeError, ValueError)):
        decoder.unrank(rank)
    calls = []
    def wrong(bound):
        calls.append(bound)
        return rank
    with pytest.raises((TypeError, ValueError)):
        decoder.sample(wrong)
    assert calls == [decoder.ways]
