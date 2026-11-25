"""Frozen deterministic high-N oracle qualification; no DEV graph or sampling."""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import time

from P47_conditional_phase_marginal import conditional_phase_marginal


def pointmass_reference(n,p):
    result = [Q(0)]*(n+1)
    result[0] = 1-p
    for others in range(n):
        active = others+1
        weight = p*math.comb(n-1,others)*p**others*(1-p)**(n-1-others)
        probability = Q(1,active)
        for count in range(active+1):
            result[count] += weight*math.comb(active,count)*probability**count*(1-probability)**(active-count)
    return result


def uniform_reference(n,p):
    """Exact univariate polynomial powers conditional on l, not production DP[l,r]."""
    single = [Q(1,n**r*math.factorial(r)**2) for r in range(n+1)]
    power = [Q(1)]+[Q(0)]*n
    coefficients = [Q(1)]+[Q(0)]*n
    for active in range(1,n+1):
        power = [sum((power[j]*single[r-j] for j in range(r+1)),Q(0)) for r in range(n+1)]
        weight = math.comb(n,active)*p**active*(1-p)**(n-active)
        for r in range(1,active+1):
            falling = math.factorial(active)//math.factorial(active-r)
            coefficients[r] += weight*Q(falling*math.factorial(r),active**r)*power[r]
    return [sum(((-1)**(r-j)*math.comb(r,j)*coefficients[r] for r in range(j,n+1)),Q(0))
            for j in range(n+1)]


def d(value):
    return Decimal(value.numerator)/Decimal(value.denominator)


def check_result(result,n,p,reference):
    precision = result["precision"]
    tolerance = Decimal("1e-60") if precision == 80 else Decimal("1e-100")
    with localcontext() as ctx:
        ctx.prec = 160
        pmf, cdf = result["pmf"], result["cdf"]
        normalization = abs(sum(pmf)-1)
        mean_error = abs(sum(Decimal(j)*v for j,v in enumerate(pmf))-d(p))
        active_expected = [d(math.comb(n,l)*p**l*(1-p)**(n-l)) for l in range(n+1)]
        active_error = max(abs(a-b) for a,b in zip(result["active_count_pmf"],active_expected))
        assert len(pmf) == len(cdf) == n+1 and min(pmf) >= 0
        assert cdf[-1] == 1 and all(a <= b for a,b in zip(cdf,cdf[1:]))
        assert result["shift_pgf_coefficients"][0] == 1
        assert normalization < tolerance and mean_error < tolerance and active_error < tolerance
        reference_error = None
        if reference is not None:
            assert sum(reference) == 1 and min(reference) >= 0
            reference_error = max(abs(a-d(b)) for a,b in zip(pmf,reference))
            assert reference_error < tolerance
        return {"normalization_error":str(normalization),"mean_error":str(mean_error),
                "active_binomial_error":str(active_error),
                "exact_reference_error":None if reference_error is None else str(reference_error),
                "input_normalization_L1":str(result["input_row_normalization_L1"]),
                "raw_minimum_pmf":str(result["raw_minimum_pmf"]),
                "pmf_correction_L1":str(result["pmf_correction_L1"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    start_cpu,start_wall = time.process_time(),time.perf_counter()
    records = []
    with (args.output/"records.jsonl").open("x") as stream:
        for n in (13,17):
            rows = {"uniform":[Q(1,n)]*n,
                    "ramp":[Q(i,n*(n+1)//2) for i in range(1,n+1)],
                    "pointmass":[Q(1)]+[Q(0)]*(n-1)}
            for name,q in rows.items():
                for p in (Q(1,4),Q(1,2)):
                    reference_start = time.perf_counter()
                    reference = (uniform_reference(n,p) if name == "uniform" else
                                 pointmass_reference(n,p) if name == "pointmass" else None)
                    reference_seconds = time.perf_counter()-reference_start
                    results,metadata = {},{}
                    for precision in (80,120):
                        one_start = time.perf_counter()
                        results[precision] = conditional_phase_marginal(q,p,precision=precision)
                        oracle_seconds = time.perf_counter()-one_start
                        metadata[str(precision)] = dict(check_result(results[precision],n,p,reference),
                                                        oracle_seconds=oracle_seconds,
                                                        pmf=[str(v) for v in results[precision]["pmf"]],
                                                        cdf=[str(v) for v in results[precision]["cdf"]])
                    with localcontext() as ctx:
                        ctx.prec = 160
                        pmf_difference = max(abs(a-b) for a,b in zip(results[80]["pmf"],results[120]["pmf"]))
                        cdf_difference = max(abs(a-b) for a,b in zip(results[80]["cdf"],results[120]["cdf"]))
                        assert max(pmf_difference,cdf_difference) < Decimal("1e-60")
                    record = {"N":n,"row":name,"p":str(p),"precision":metadata,
                              "exact_reference": "univariate_fraction_power" if name == "uniform" else
                                                 "pointmass_binomial_mixture" if name == "pointmass" else None,
                              "reference_seconds":reference_seconds,
                              "max_precision_PMF_difference":str(pmf_difference),
                              "max_precision_CDF_difference":str(cdf_difference)}
                    records.append(record);stream.write(json.dumps(record)+"\n");stream.flush()
                    print(json.dumps({"N":n,"row":name,"p":str(p),"precision_difference":str(pmf_difference)}),flush=True)
    assert len(records) == 12
    summary = {"status":"SYNTHETIC_ORACLE_RESOURCE_QUALIFICATION_ONLY", "cases":12,
               "oracle_evaluations":24,"precisions":[80,120],"records":records,
               "cpu_seconds":time.process_time()-start_cpu,"wall_seconds":time.perf_counter()-start_wall,
               "DEV_graphs":0,"photon_samples":0,"QPU_calls":0,"optimizer_positive":False,
               "module_sha256":hashlib.sha256(Path(__file__).with_name("P47_conditional_phase_marginal.py").read_bytes()).hexdigest(),
               "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with (args.output/"summary.json").open("x") as stream:
        json.dump(summary,stream,indent=2);stream.write("\n")


if __name__ == "__main__":
    main()
