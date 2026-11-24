"""Independent truth tables for the elementary examples and graph contract."""
from itertools import combinations, product
import numpy as np
import pytest
from photonic_balanced_partitioning.problems.min_bisection import (
    BalancedGraphPartitioning as B, compute_cut_weight,
)


def test_all_four_vertex_simple_graphs_against_independent_binary_definition():
    pairs=list(combinations(range(4),2))
    for present in product((0,1),repeat=6):
        edges=tuple((i,j,1.) for (i,j),bit in zip(pairs,present) if bit)
        g=B(4,edges);values=[]
        for bits in product((0,1),repeat=4):
            if sum(bits)!=2:continue
            part=tuple(i for i,b in enumerate(bits) if b)
            expected=sum(w*abs(bits[i]-bits[j]) for i,j,w in edges)
            assert compute_cut_weight(4,edges,part)==expected
            complement=tuple(i for i in range(4) if i not in part)
            assert compute_cut_weight(4,edges,complement)==expected
            values.append(expected)
        assert g.solve_exact().energy==min(values)


@pytest.mark.parametrize('factory,minimum,optimal_strings',[
    (lambda:B.complete_graph(4),4,6),
    (lambda:B.complete_bipartite(2,2),2,4),
    (lambda:B.path_graph(4),1,2),
    (lambda:B.cycle_graph(4),2,4),
    (lambda:B.star_graph(4),2,6),
])
def test_elementary_optima_and_complement_degeneracy(factory,minimum,optimal_strings):
    g=factory();values=[compute_cut_weight(4,g.edges,p) for p in combinations(range(4),2)]
    assert min(values)==minimum and values.count(minimum)==optimal_strings


@pytest.mark.parametrize('edges',[
    ((0,0,1.),),((0,4,1.),),((0,1,-1.),),((0,1,float('nan')),),
    ((0,1,float('inf')),),((0,1,1.),(1,0,2.)),((0.5,1,1.),),
])
def test_invalid_simple_graphs_fail_before_cost_evaluation(edges):
    with pytest.raises(ValueError):B(4,edges)


@pytest.mark.parametrize('matrix',[
    np.ones((2,3)),np.array([[0,1],[0,0]]),np.eye(4),
    np.array([[0,-1],[-1,0]]),np.array([[0,np.nan],[np.nan,0]]),
])
def test_adjacency_contract(matrix):
    with pytest.raises(ValueError):B.from_adjacency(matrix)


def test_weighted_random_graphs_exact_solution_and_degree_contract():
    for seed in (20261124,20261125,20261126):
        g=B.random_regular(6,3,seed,weight_range=(.2,2.))
        assert np.count_nonzero(g.adjacency_matrix,axis=1).tolist()==[3]*6
        expected=min(sum(w for i,j,w in g.edges if ((i in p)!=(j in p))) for p in combinations(range(6),3))
        assert g.solve_exact().energy==pytest.approx(expected)
    with pytest.raises(ValueError):B.cycle_graph(2)
    with pytest.raises(ValueError):B(0,())
    with pytest.raises(ValueError):compute_cut_weight(4,(),(0,0))
