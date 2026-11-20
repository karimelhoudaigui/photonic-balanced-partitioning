import numpy as np
from photonic_balanced_partitioning.problems.min_bisection import BalancedGraphPartitioning, solve_qubo_with_penalty
from photonic_balanced_partitioning.classical.baselines import greedy_balanced


def test_regular_generator_preserves_all_degrees():
    for n in [4, 6, 8, 10]:
        for degree in range(n):
            for seed in [3, 7]:
                graph = BalancedGraphPartitioning.random_regular(n, degree, seed)
                np.testing.assert_array_equal((graph.adjacency_matrix != 0).sum(axis=1), np.full(n, degree))


def test_penalty_exact_really_searches_unbalanced():
    graph = BalancedGraphPartitioning.path_graph(4)
    assert not solve_qubo_with_penalty(4, graph.edges, lam=0).is_balanced
    assert solve_qubo_with_penalty(4, graph.edges, lam=10).is_balanced
    assert set(graph.solve_exact().v1) == {2, 3}


def test_greedy_swap_terminates_at_no_worse_energy():
    graph = BalancedGraphPartitioning(4, ((0, 2, 2.), (1, 3, 2.), (0, 1, 1.)))
    result = greedy_balanced(4, list(graph.edges))
    assert result.energy <= 4.0
    assert result.energy == graph.solve_exact().energy
