"""Physical assumptions and integer budgets in the new spectrum certificate."""
from fractions import Fraction as Q
import importlib.util
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("p42_certificate",ROOT/"research/P42_loss_spectrum_probe.py")
p42 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p42)


def test_single_input_spectrum_and_threshold_rank_are_separate():
    total, sectors = p42.spectra((1,)*8)
    assert total == 8
    assert all(terms == {1:math.comb(8,r)} for r,terms in sectors.items())
    eta = Q(1,10)
    assert p42.support_cap((1,1,1),eta,2) == eta**2
    assert p42.support_cap((1,1,1),eta,2,pnr_only=True) == eta**2*(1-eta)


def test_general_source_refutes_wrong_single_input_assumption():
    eta = Q(1,10)
    actual = 1-2*(1-eta/2)**4+(1-eta)**4
    assert actual == Q(2167,80000)
    assert actual > p42.support_cap((1,)*4,eta,2)
    assert actual <= p42.support_cap((4,0,0,0),eta,2)
    assert p42.support_cap((4,),eta,2) == sum(Q(math.comb(4,r))*eta**r*(1-eta)**(4-r) for r in range(2,5))


def test_unknown_internal_states_cannot_use_the_pure_bosonic_rank():
    eta = Q(1,100)
    lower = Q(7,6)*eta**4*(1-eta)**4
    assert lower > (eta/(1-eta))**4
    assert lower <= p42.support_cap((1,)*8,eta,4,internal="arbitrary")


def test_source_ceiling_must_check_every_source_size():
    eta = Q(1,10)
    assert p42.support_cap((1,)*5,eta,3) > p42.support_cap((1,)*6,eta,3)


def test_finite_budget_rounding_and_query_cap_matter():
    # Fractional nQ/nC is unsafe; the proof uses ceil and at least one block.
    cap = Q(1,math.comb(4,2))
    assert p42.budget_certificate(cap,2,1000,1000)["certified_under_stated_model"]
    assert not p42.budget_certificate(cap,2,1001,1000)["certified_under_stated_model"]
    assert not p42.budget_certificate(Q(1),2,1,6)["certified_under_stated_model"]
    assert not p42.budget_certificate(Q(0),2,1,0)["certified_under_stated_model"]
    assert p42.budget_certificate(Q(1),2,0,0)["certified_under_stated_model"]


@pytest.mark.parametrize("source,eta,k", [((1,)*13,Q(1,2),2),((True,),Q(1,2),1),
    ((1,1),float('nan'),1),((1,1),.2,1),((1,1),Q(1,2),True)])
def test_invalid_parameters_fail_before_large_allocation(source,eta,k):
    with pytest.raises(ValueError):
        p42.support_cap(source,eta,k)


def test_loss_endpoints_and_hardware_flags():
    assert p42.support_cap((1,)*5,Q(0),2) == 0
    assert p42.support_cap((1,)*5,Q(1),2) == 1
    assert p42.support_cap((1,1),Q(1,2),3) == 0
    certificate = p42.budget_certificate(Q(1,1000),2,10,10)
    assert certificate["physical_device_parameters_verified"] is False
    assert certificate["qpu_gate_opened"] is False
