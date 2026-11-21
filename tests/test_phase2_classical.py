"""Independent known-cut cases and query-budget invariants for P21."""
import importlib.util
from pathlib import Path
import numpy as np
import pytest

spec=importlib.util.spec_from_file_location('phase2_classical_search',Path(__file__).resolve().parents[1]/'experiments/phase2_classical_search.py')
p21=importlib.util.module_from_spec(spec);spec.loader.exec_module(p21)


def test_exact_reference_known_path_and_query_count():
    edges=[(0,1,1.),(1,2,1.),(2,3,1.)]
    ref=p21.exact_reference(4,edges)
    assert ref['query_count']==6
    assert ref['optimum']==1
    assert ref['optimal_count']==2
    assert ref['worst']==3


@pytest.mark.parametrize('algorithm',['random_feasible','swap_anneal','spectral_swap_local'])
def test_full_budget_feasibility_reproducibility_without_optimum(algorithm):
    edges=[(i,i+1,float(i+1)) for i in range(5)]
    a=p21.feasible_search(6,edges,algorithm,37,90210)
    b=p21.feasible_search(6,edges,algorithm,37,90210)
    assert a['n_queries']==37
    assert a['trace']==b['trace']
    assert len(a['trace'])==37
    for row in a['trace']:
        assert len(row['partition'])==len(set(row['partition']))==3
        chosen=set(row['partition'])
        independent=sum(w for i,j,w in edges if (i in chosen)!=(j in chosen))
        assert row['cost']==independent
    assert a['best_cost']==min(row['cost'] for row in a['trace'])
    ref=p21.exact_reference(6,edges)
    result=p21.retrospective(a,ref)
    hits=[row['query'] for row in a['trace'] if abs(row['cost']-ref['optimum'])<1e-9]
    assert result['first_optimum_query']==(hits[0] if hits else None)


def test_relabeling_preserves_exact_cost_multiset():
    edges=[(0,1,.25),(1,2,1.2),(2,3,3.5),(0,2,.7)]
    relabeled=p21.relabel_edges(edges,np.array([3,0,2,1]))
    a=p21.exact_reference(4,edges);b=p21.exact_reference(4,relabeled)
    np.testing.assert_allclose(sorted(a['energies']),sorted(b['energies']))


def test_one_query_spectral_cost_is_charged():
    edges=[(i,i+1,1.) for i in range(5)]
    r=p21.feasible_search(6,edges,'spectral_swap_local',1,17)
    assert r['eigensolves']==1
    assert r['n_queries']==1
    assert r['trace'][0]['stage']=='spectral_start'
    assert r['trace'][0]['cost']==1
