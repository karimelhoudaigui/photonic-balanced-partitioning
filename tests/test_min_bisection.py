"""Unit tests for min_bisection problem."""

import pytest
import numpy as np
from photonic_balanced_partitioning.problems.min_bisection import (
    BalancedGraphPartitioning,
    PartitionResult,
    compute_cut_weight,
    enumerate_balanced_partitions,
    solve_exact_min_bisection,
    get_normalized_gap,
)


def test_path_graph_creation():
    """Test creating a path graph."""
    problem = BalancedGraphPartitioning.path_graph(4)
    assert problem.n == 4
    assert len(problem.edges) == 3
    assert problem.k == 2


def test_cycle_graph_creation():
    """Test creating a cycle graph."""
    problem = BalancedGraphPartitioning.cycle_graph(6)
    assert problem.n == 6
    assert len(problem.edges) == 6


def test_complete_graph_creation():
    """Test creating a complete graph."""
    problem = BalancedGraphPartitioning.complete_graph(4)
    assert problem.n == 4
    assert len(problem.edges) == 6  # n*(n-1)/2


def test_odd_n_rejected():
    """Test that odd n raises an error."""
    with pytest.raises(ValueError):
        BalancedGraphPartitioning.path_graph(5)


def test_exact_solution_path_graph():
    """Test exact solution for path graph."""
    # Path 0-1-2-3: optimal bisection is {0,1}|{2,3} with cut weight 1
    problem = BalancedGraphPartitioning.path_graph(4)
    result = problem.solve_exact()
    
    assert result.is_optimal
    assert result.energy == 1.0
    assert len(result.partition) == 2


def test_exact_solution_cycle_graph():
    """Test exact solution for cycle graph."""
    # Cycle 0-1-2-3: optimal bisection has cut weight 2
    problem = BalancedGraphPartitioning.cycle_graph(4)
    result = problem.solve_exact()
    
    assert result.is_optimal
    assert result.energy == 2.0


def test_exact_solution_complete_graph():
    """Test exact solution for complete graph."""
    # Complete graph K4: any balanced partition has cut weight 4
    problem = BalancedGraphPartitioning.complete_graph(4)
    result = problem.solve_exact()
    
    assert result.is_optimal
    assert result.energy == 4.0


def test_enumerate_partitions():
    """Test partition enumeration."""
    partitions = enumerate_balanced_partitions(4, 2)
    assert len(partitions) == 6  # C(4,2) = 6
    assert all(len(p) == 2 for p in partitions)


def test_cut_weight_computation():
    """Test cut weight computation."""
    edges = [(0, 1, 1.0), (1, 2, 2.0), (2, 3, 1.5)]
    
    # Partition {0, 1} | {2, 3}: cut edges are (1,2) with weight 2.0
    weight = compute_cut_weight(4, tuple(edges), (0, 1))
    assert weight == 2.0
    
    # Partition {0, 2} | {1, 3}: cut edges are (0,1), (1,2), (2,3) = 1+2+1.5 = 4.5
    weight = compute_cut_weight(4, tuple(edges), (0, 2))
    assert weight == 4.5


def test_normalized_gap():
    """Test normalized gap computation."""
    edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
    
    # Optimal energy is 1.0, worst is 3.0
    gap = get_normalized_gap(4, tuple(edges), 1.0)
    assert gap == 0.0  # Optimal
    
    gap = get_normalized_gap(4, tuple(edges), 3.0)
    assert gap == 1.0  # Worst


def test_adjacency_matrix():
    """Test adjacency matrix generation."""
    problem = BalancedGraphPartitioning.path_graph(4)
    A = problem.adjacency_matrix
    
    assert A[0, 1] == 1.0
    assert A[1, 0] == 1.0
    assert A[0, 2] == 0.0


def test_laplacian_matrix():
    """Test Laplacian matrix generation."""
    problem = BalancedGraphPartitioning.path_graph(4)
    L = problem.laplacian_matrix
    
    # Diagonal should be degrees
    assert L[0, 0] == 1.0  # degree of vertex 0
    assert L[1, 1] == 2.0  # degree of vertex 1
    assert L[2, 2] == 2.0  # degree of vertex 2
    assert L[3, 3] == 1.0  # degree of vertex 3


def test_is_connected():
    """Test connectivity check."""
    # Connected graph
    problem = BalancedGraphPartitioning.path_graph(4)
    assert problem.is_connected
    
    # Disconnected graph
    edges = [(0, 1, 1.0), (2, 3, 1.0)]
    problem = BalancedGraphPartitioning(4, tuple(edges))
    assert not problem.is_connected


def test_from_adjacency_matrix():
    """Test creating problem from adjacency matrix."""
    A = np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0]
    ])
    
    problem = BalancedGraphPartitioning.from_adjacency(A)
    assert problem.n == 4
    assert len(problem.edges) == 3


def test_weighted_random_graph():
    """Test creating weighted random graph."""
    problem = BalancedGraphPartitioning.erdos_renyi(6, 0.5, seed=42)
    assert problem.n == 6
    assert problem.is_connected or len(problem.edges) > 0


def test_planted_partition():
    """Test creating planted partition graph."""
    problem = BalancedGraphPartitioning.planted_partition(6, 3, seed=42)
    assert problem.n == 6


def test_copy():
    """Test copying a problem."""
    problem = BalancedGraphPartitioning.path_graph(4)
    copy = problem.copy()
    
    assert copy.n == problem.n
    assert copy.edges == problem.edges
    assert copy is not problem


def test_with_added_edge():
    """Test adding an edge."""
    problem = BalancedGraphPartitioning.path_graph(4)
    new_problem = problem.with_added_edge(0, 3, 1.0)
    
    assert len(new_problem.edges) == 4
    assert (0, 3, 1.0) in new_problem.edges or (3, 0, 1.0) in new_problem.edges


def test_with_added_weight():
    """Test adding weight to an edge."""
    problem = BalancedGraphPartitioning.path_graph(4)
    new_problem = problem.with_added_weight(0, 1, 0.5)
    
    # Find the edge (0, 1) and check its weight
    for i, j, w in new_problem.edges:
        if (i, j) == (0, 1):
            assert w == 1.5
            break