"""Exact algebra tests, no P52 data, graph, stochastic draw or full proof fit."""
from fractions import Fraction as Q
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"research"))
SPEC=importlib.util.spec_from_file_location("p53",ROOT/"research/P53_exact_continuous_phase.py")
p53=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(p53)


def direct_integer_columns(last=8):
    """Independent full-column product in t=exp(i theta), not the F factorization."""
    polynomial={((0,)*8,0):1}
    for column in range(last):
        updated={}
        for (n,power),coefficient in polynomial.items():
            for row in range(8):
                changed=tuple(value+(i==row) for i,value in enumerate(n))
                phase=power+(row%4 if column>=4 else 0)
                sign=p53.SIGNS[row%4][column%4]*(-1 if row>=4 and column>=4 else 1)
                key=(changed,phase);updated[key]=updated.get(key,0)+coefficient*sign
        polynomial={key:value for key,value in updated.items() if value}
    return polynomial


@pytest.fixture(scope="module")
def exact_source():
    wave=p53.wave_coefficients();return wave,p53.probability_cosine(wave)


def test_closed_walsh_factor_is_the_independent_four_column_integer_product():
    actual=p53.walsh_factor()
    assert actual==direct_integer_columns(4)
    assert len(actual)==90 and sum(map(abs,actual.values()))==384
    assert len(p53.walsh_factor(True,True))==90


def test_full_factorization_matches_independent_eight_column_t_polynomial_and_odd_cancellation(exact_source):
    wave,_=exact_source;reference=direct_integer_columns(8)
    assert all(power%2==0 for (_,power) in reference)
    for n,values in wave.items():
        assert tuple(reference.get((n,2*h),0) for h in range(7))==values
    assert len(wave)==6435


def test_normalized_fock_output_factorial_and_all_patterns_are_exact(exact_source):
    wave,probability=exact_source
    assert tuple(sum(row[h] for row in probability.values()) for h in range(7))==(8**8,0,0,0,0,0,0)
    for row in range(8):
        n=tuple(8 if i==row else 0 for i in range(8))
        expected=[0]*7;expected[2*(row%4)]=1
        assert wave[n]==tuple(expected)
        assert probability[n]==(math.factorial(8),0,0,0,0,0,0)


def test_analytic_eight_photon_quartic_witness_has_exact_one_plus_half_cosine(exact_source):
    _,probability=exact_source
    total=[0]*7
    for n,values in probability.items():
        witness=((n[0]-n[4])**2-n[0]-n[4])*((n[1]-n[5])**2-n[1]-n[5])
        for h,value in enumerate(values):total[h]+=witness*value
    assert total==[p53.DEN,p53.DEN//2,0,0,0,0,0]


def test_every_admissible_tie_divides420_and_full_integer_rank_mass_is_preserved(exact_source):
    _,probability=exact_source;counts=tuple(probability)
    ties=p53.tie_scaled_rows(counts)
    denominators={420//weight for row in ties for _,weight in row}
    assert math.lcm(*denominators)==420
    assert all(sum(weight for _,weight in row)==420 for row in ties)
    uniform=p53.tie_scaled_rows([(1,)*8])[0]
    assert len(uniform)==70 and {weight for _,weight in uniform}=={6}
    bunch=p53.tie_scaled_rows([(8,0,0,0,0,0,0,0)])[0]
    assert len(bunch)==35 and all(mask&1 for mask,_ in bunch)
    rank,edge=p53.rank_and_crossing(probability)
    assert len(rank)==70 and len(edge)==28
    assert tuple(sum(row[h] for row in rank) for h in range(7))==(p53.KERNEL_DEN,0,0,0,0,0,0)


@pytest.mark.parametrize("endpoint",[0,1])
def test_gaussian_integer_four_photon_probabilities_have_correct_denominator_and_bunch_factor(endpoint):
    counts=tuple(p53.compositions(8,4));index={n:i for i,n in enumerate(counts)}
    columns=p53._gaussian_columns(endpoint)
    values=p53.gaussian_group_law(columns,(0,2,5,7),counts)
    assert sum(values)==8**4
    for row in range(8):
        assert values[index[tuple(4 if i==row else 0 for i in range(8))]]==math.factorial(4)
    with pytest.raises(ValueError):p53.gaussian_group_law(columns,(0,0,1,2),counts)


def test_all_fixed_classical_vertices_are_rational_normalized_and_include_no_favorable_filter():
    library=p53.classical_library()
    assert len(library["labels"])==71 and len(library["occupation_numerators"])==70
    assert library["occupation_denominator"]==8**8 and library["group_probability_denominator"]==8**4
    assert sum(label["theta"]=="0" for label in library["labels"] if label["kind"]=="b4")==35
    assert sum(label["theta"]=="pi/2" for label in library["labels"] if label["kind"]=="b4")==35
    for law in library["occupation_numerators"]:
        assert len(law)==6435 and min(law)>=0 and sum(law)==8**8
    assert library["crossing_numerators"][-1]==(4*p53.KERNEL_DEN//7,)*28


def test_chebyshev_transform_known_shifted_polynomials_and_exact_types():
    assert p53.cosine_to_power((0,0,1))==(Q(1),Q(-8),Q(8))
    assert p53.cosine_to_power((0,0,0,1))==(Q(-1),Q(18),Q(-48),Q(32))
    with pytest.raises(TypeError):p53.cosine_to_power((.5,))


@pytest.mark.parametrize("degree",[6,12])
def test_bernstein_exact_power_reconstruction_and_evaluation_for_all_monomials(degree):
    for k in range(7):
        power=(Q(0),)*k+(Q(1),)
        controls=p53.power_to_bernstein(power,degree)
        assert p53.bernstein_to_power(controls)==power+(Q(0),)*(degree-k)
        for x in (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)):
            value=sum((coefficient*math.comb(degree,j)*x**j*(1-x)**(degree-j) for j,coefficient in enumerate(controls)),Q(0))
            assert value==x**k


def test_degree_elevation_is_an_independent_convex_identity_and_internal_face_touch_can_fail():
    power=(Q(1,4),Q(-1),Q(1))  # (x-.5)^2>=0 but touches zero internally.
    six=p53.power_to_bernstein(power,6);twelve=p53.elevate_bernstein(six,12)
    assert twelve==p53.power_to_bernstein(power,12)
    assert min(six)<0 and min(twelve)<0
    assert sum((Q(math.comb(12,j),2**12)*value for j,value in enumerate(twelve)),Q(0))==0


def test_rational_rref_positive_negative_inconsistent_and_free_zero_semantics():
    matrix=[[1,1],[0,1]];before=[row[:] for row in matrix]
    result=p53.rational_rref_solution(matrix,[1,Q(1,3)])
    assert result["solution"]==(Q(2,3),Q(1,3)) and result["pivots"]==[0,1] and matrix==before
    assert p53.rational_rref_solution(matrix,[1,2])["solution"]==(Q(-1),Q(2))
    assert not p53.rational_rref_solution([[1,1],[2,2]],[1,3])["consistent"]
    free=p53.rational_rref_solution([[1,1,1],[0,0,1]],[1,Q(1,3)])
    assert free["free_columns"]==[1] and free["solution"]==(Q(2,3),Q(0),Q(1,3))
    with pytest.raises(TypeError):p53.rational_rref_solution([[.5]],[1])


def test_exact_support_primary_fallback_and_nonmembership_are_conservative():
    library=[(Q(0),)*28,(Q(1),)*28]
    first=p53.exactify_support(library,(Q(1,3),)*28,[2/3,1/3])
    assert first["verified"] and first["weights"]==[Q(2,3),Q(1,3)]
    tiny=Q(1,10**12)
    fallback=p53.exactify_support(library,(tiny,)*28,[1.-1e-12,1e-12])
    assert fallback["verified"] and len(fallback["attempts"])==2
    assert fallback["weights"]==[1-tiny,tiny]
    unresolved=p53.exactify_support(library,(Q(2),)*28,[0.,1.])
    assert unresolved["verified"] is False


def test_continuous_certificate_is_reconstructed_in_power_basis_and_detects_corruption():
    power=((Q(0),Q(1)),)*28;library=[(Q(0),)*28,(Q(1),)*28]
    controls=tuple((Q(j,6),)*28 for j in range(7))
    weights=[[1-Q(j,6),Q(j,6)] for j in range(7)]
    assert p53.verify_polynomial_certificate(power,controls,weights,library)
    broken=[row[:] for row in weights];broken[3][0]+=Q(1,1000);broken[3][1]-=Q(1,1000)
    assert not p53.verify_polynomial_certificate(power,controls,broken,library)
    encoded=p53.encoded({"weights":weights})
    assert json.loads(json.dumps(encoded))["weights"][1][1]=={"numerator":1,"denominator":6}


@pytest.mark.parametrize("solved",[True,False])
def test_driver_uses_only_proposed_support_with_exact_verification_and_conservative_solver_gate(monkeypatch,solved):
    def proposal(library,target):
        value=target[0]
        return {"solver_fit_solved":solved,"verification":{"verified":True,"used_coefficients":[1-value,value]}}
    monkeypatch.setattr(p53,"convex_fit",proposal)
    records=[];power=((Q(0),Q(1)),)*28;library=[(Q(0),)*28,(Q(1),)*28]
    result=p53.fit_degree(power,library,6,records)
    assert len(records)==7 and result["exact_polynomial_identity"] is True
    assert result["certified"] is solved
    assert all(record["exactification"]["verified"] for record in records)
    with pytest.raises(ArithmeticError):p53.fit_degree(power,library,6,[{}]*20)


def test_solved_float_nonmatch_can_propose_support_for_a_different_exact_certificate(monkeypatch):
    def proposal(library,target):
        return {"solver_fit_solved":True,"solver_status":0,"solver_success":True,
                "status":"NO_VERIFIED_TOLERANCE_MATCH",
                "verification":{"verified":True,"used_coefficients":[.5,.5],
                                "verified_Linfty_residual":abs(.5-target[0])}}
    monkeypatch.setattr(p53,"convex_fit",proposal)
    library=[(Q(0),)*28,(Q(1),)*28];power=((Q(1,3),),)*28;records=[]
    result=p53.fit_degree(power,library,6,records)
    assert result["certified"] and result["exact_polynomial_identity"]
    assert len(records)==7
    for record in records:
        assert record["float_proposal"]["status"]=="NO_VERIFIED_TOLERANCE_MATCH"
        assert record["float_proposal"]["verification"]["used_coefficients"]==[.5,.5]
        assert record["float_proposal"]["verification"]["verified_Linfty_residual"]>1e-9
        assert record["exactification"]["weights"]==[Q(2,3),Q(1,3)]
        assert record["run_gate_passed"] is True
