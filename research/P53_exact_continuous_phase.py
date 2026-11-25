"""P53 exact integer/rational continuous edge-MEAN certificate construction.

No P52 data or floating creation/ranking output is an input. Only the immutable
qualified convex_fit provider proposes supports; every accepted identity is Q.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

import P52_collective_phase_probe as lp_provider
convex_fit = lp_provider.convex_fit

DEN = 8**8
TIE_DEN = 420
KERNEL_DEN = TIE_DEN*DEN
SUPPORT_THRESHOLD = 1e-10
LP_PROVIDER_SHA256 = "56a71f048973cae7d4922d9da7d3952943c52f5a11597fc46bbb1a2bab84d242"
SIGNS = ((1,1,1,1),(1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1))
SUBSETS = tuple(itertools.combinations(range(8),4))
MASKS = tuple(sum(1<<i for i in subset) for subset in SUBSETS)
MASK_INDEX = {mask:i for i,mask in enumerate(MASKS)}
EDGES = tuple(itertools.combinations(range(8),2))
CUT_INDICES = tuple(tuple(e for e,(i,j) in enumerate(EDGES) if (i in subset)!=(j in subset)) for subset in SUBSETS)


def exact_q(value):
    if not isinstance(value,(int,Q)):
        raise TypeError("Exact proof inputs must be Python integers/Fractions, never floating reconstructions")
    return Q(value)


def compositions(m,total):
    if m == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(m-1,total-first):
                yield (first,)+rest


def factorial_product(n):
    return math.prod(math.factorial(int(value)) for value in n)


def _multiply(first,second):
    out={}
    for (n,h),a in first.items():
        for (m,k),b in second.items():
            key=(tuple(x+y for x,y in zip(n,m)),h+k)
            out[key]=out.get(key,0)+a*b
    return {key:value for key,value in out.items() if value != 0}


def _pair_power(j,power,negative):
    out={}
    for lower in range(power+1):
        n=[0]*8;n[j]=power-lower;n[j+4]=lower
        out[(tuple(n),0)]=math.comb(power,lower)*((-1)**lower if negative else 1)
    return out


def walsh_factor(negative=False,phased=False):
    """F(A) or F_z(B), exactly90 sparse integer monomials each."""
    out={}
    def add(poly,coefficient,phase):
        for (n,h),value in poly.items():
            key=(n,h+phase);out[key]=out.get(key,0)+coefficient*value
    for j in range(4):
        add(_pair_power(j,4,negative),1,2*j if phased else 0)
    for j,k in itertools.combinations(range(4),2):
        add(_multiply(_pair_power(j,2,negative),_pair_power(k,2,negative)), -2, j+k if phased else 0)
    product={((0,)*8,0):1}
    for j in range(4):product=_multiply(product,_pair_power(j,1,negative))
    add(product,8,3 if phased else 0)
    out={key:value for key,value in out.items() if value}
    if len(out)!=90:raise ArithmeticError("Quartic support identity failed")
    return out


def wave_coefficients():
    """All6435 rows, degree0..6, including exact zero arrays."""
    sparse=_multiply(walsh_factor(),walsh_factor(True,True))
    result={n:[0]*7 for n in compositions(8,8)}
    for (n,h),value in sparse.items():
        if not 0<=h<=6:raise ArithmeticError("Unexpected phase degree")
        result[n][h]=int(value)
    for n,values in result.items():
        if sum(map(abs,values))>math.factorial(8)//factorial_product(n):
            raise ArithmeticError("Integer source assignment bound exceeded")
    return {n:tuple(values) for n,values in result.items()}


def probability_cosine(wave):
    result={}
    for n,values in wave.items():
        f=factorial_product(n)
        result[n]=tuple([f*sum(value*value for value in values)]+
            [2*f*sum(values[j]*values[j+h] for j in range(7-h)) for h in range(1,7)])
    expected=(DEN,0,0,0,0,0,0)
    if tuple(sum(row[h] for row in result.values()) for h in range(7))!=expected:
        raise ArithmeticError("Exact source normalization polynomial failed")
    return result


def tie_scaled_rows(counts):
    """Admissible subset MASK/INTEGER-weight pairs, common denominator420."""
    rows=[]
    for n in counts:
        threshold=sorted(n)[-4]
        high=tuple(i for i,value in enumerate(n) if value>threshold)
        tied=tuple(i for i,value in enumerate(n) if value==threshold)
        needed=4-len(high);den=math.comb(len(tied),needed)
        if TIE_DEN%den:raise ArithmeticError("Admissible tie denominator does not divide420")
        row=[(sum(1<<i for i in high+choice),TIE_DEN//den)
             for choice in itertools.combinations(tied,needed)]
        if sum(value for _,value in row)!=TIE_DEN:raise ArithmeticError("Tie normalization failed")
        rows.append(row)
    return rows


def rank_and_crossing(cosine):
    counts=tuple(cosine);rows=tie_scaled_rows(counts)
    rank=[[0]*7 for _ in SUBSETS]
    for n,ties in zip(counts,rows):
        values=cosine[n]
        for mask,weight in ties:
            for h in range(7):rank[MASK_INDEX[mask]][h]+=weight*values[h]
    crossing=[[0]*7 for _ in EDGES]
    for index,values in enumerate(rank):
        for edge in CUT_INDICES[index]:
            for h in range(7):crossing[edge][h]+=values[h]
    if tuple(sum(row[h] for row in rank) for h in range(7))!=(KERNEL_DEN,0,0,0,0,0,0):
        raise ArithmeticError("Rank normalization polynomial failed")
    for i in range(8):
        actual=tuple(sum(crossing[e][h] for e,edge in enumerate(EDGES) if i in edge) for h in range(7))
        if actual!=(4*KERNEL_DEN,0,0,0,0,0,0):raise ArithmeticError("Incident mean identity failed")
    return tuple(map(tuple,rank)),tuple(map(tuple,crossing))


def _gaussian_columns(endpoint):
    columns=[]
    for column in range(8):
        values=[]
        for row in range(8):
            j=row%4;sign=SIGNS[j][column%4]*(-1 if row>=4 and column>=4 else 1)
            unit=((1,0),(0,1),(-1,0),(0,-1))[j%4] if endpoint and column>=4 else (1,0)
            values.append((sign*unit[0],sign*unit[1]))
        columns.append(tuple(values))
    return tuple(columns)


def gaussian_group_law(columns,sources,counts4):
    if len(sources)!=4 or len(set(sources))!=4 or any(not 0<=s<8 for s in sources):
        raise ValueError("Exactly four distinct source labels required")
    polynomial={(0,)*8:(1,0)}
    for source in sources:
        updated={}
        for n,(a,b) in polynomial.items():
            for row,(c,d) in enumerate(columns[source]):
                m=list(n);m[row]+=1;m=tuple(m)
                real,imag=updated.get(m,(0,0))
                updated[m]=(real+a*c-b*d,imag+a*d+b*c)
        polynomial=updated
    values=[]
    for n in counts4:
        real,imag=polynomial.get(n,(0,0))
        values.append(factorial_product(n)*(real*real+imag*imag))
    if min(values)<0 or sum(values)!=8**4:raise ArithmeticError("Exact four-photon law failed")
    return tuple(values)


def _push_scalar(probability,ties):
    rank=[0]*70
    for value,row in zip(probability,ties):
        if value:  # Exact zero arithmetic only; every output row is retained.
            for mask,weight in row:rank[MASK_INDEX[mask]]+=value*weight
    crossing=[0]*28
    for index,value in enumerate(rank):
        for edge in CUT_INDICES[index]:crossing[edge]+=value
    if sum(rank)!=KERNEL_DEN or any(value<0 for value in rank):raise ArithmeticError("Control rank mass failed")
    if any(sum(crossing[e] for e,edge in enumerate(EDGES) if i in edge)!=4*KERNEL_DEN for i in range(8)):
        raise ArithmeticError("Control incident identity failed")
    return tuple(rank),tuple(crossing)


def classical_library():
    counts8=tuple(compositions(8,8));counts4=tuple(compositions(8,4))
    index={n:i for i,n in enumerate(counts8)};ties=tie_scaled_rows(counts8)
    mapping=tuple(tuple(index[tuple(a+b for a,b in zip(n,m))] for m in counts4) for n in counts4)
    groups=tuple(itertools.combinations(range(8),4))
    firsts=tuple((0,)+other for other in itertools.combinations(range(1,8),3))
    labels=[];rank=[];crossing=[];raw=[];group_records=[]
    for endpoint in (0,1):
        columns=_gaussian_columns(endpoint)
        laws={group:gaussian_group_law(columns,group,counts4) for group in groups}
        group_records.append([laws[group] for group in groups])
        for first in firsts:
            second=tuple(i for i in range(8) if i not in first)
            values=[0]*len(counts8)
            for i,a in enumerate(laws[first]):
                if a:
                    for j,b in enumerate(laws[second]):
                        if b:values[mapping[i][j]]+=a*b
            if sum(values)!=DEN or min(values)<0:raise ArithmeticError("Exact b4 convolution failed")
            ranked,edges=_push_scalar(values,ties)
            labels.append({"kind":"b4","theta":"0" if endpoint==0 else "pi/2","groups":(first,second)})
            rank.append(ranked);crossing.append(edges);raw.append(values)
    labels.append({"kind":"uniform70"});rank.append((KERNEL_DEN//70,)*70)
    crossing.append((4*KERNEL_DEN//7,)*28)
    if len(labels)!=71:raise ArithmeticError("Complete fixed library missing")
    for row,edges in zip(rank,crossing):
        if sum(row)!=KERNEL_DEN or min(row)<0 or sum(edges)!=16*KERNEL_DEN:
            raise ArithmeticError("Library mass/total identity failed")
        if any(sum(edges[e] for e,edge in enumerate(EDGES) if i in edge)!=4*KERNEL_DEN for i in range(8)):
            raise ArithmeticError("Library incident identity failed")
    return {"labels":labels,"rank_numerators":rank,"crossing_numerators":crossing,
            "occupation_numerators":raw,"group_probability_numerators":group_records,
            "groups":groups,"counts4":counts4,"counts8":counts8,"denominator":KERNEL_DEN,
            "occupation_denominator":DEN,"group_probability_denominator":8**4}


def _poly_add(a,b,scale=1):
    out=[Q(0)]*max(len(a),len(b))
    for i,value in enumerate(a):out[i]+=value
    for i,value in enumerate(b):out[i]+=scale*value
    return tuple(out)


def _poly_mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return tuple(out)


def cosine_to_power(coefficients):
    chebyshev=[(Q(1),),(Q(-1),Q(2))]
    while len(chebyshev)<len(coefficients):
        chebyshev.append(_poly_add(_poly_mul((Q(-2),Q(4)),chebyshev[-1]),chebyshev[-2],-1))
    out=(Q(0),)
    for value,poly in zip(coefficients,chebyshev):out=_poly_add(out,tuple(exact_q(value)*x for x in poly))
    return out


def power_to_bernstein(power,degree):
    if degree<len(power)-1:raise ValueError("Cannot lower polynomial degree")
    return tuple(sum((exact_q(value)*Q(math.comb(j,k),math.comb(degree,k)) for k,value in enumerate(power) if k<=j),Q(0))
                 for j in range(degree+1))


def bernstein_to_power(controls):
    degree=len(controls)-1;out=[Q(0)]*(degree+1)
    for j,value in enumerate(controls):
        for k in range(degree-j+1):
            out[j+k]+=exact_q(value)*math.comb(degree,j)*math.comb(degree-j,k)*((-1)**k)
    return tuple(out)


def elevate_bernstein(controls,degree):
    old=len(controls)-1
    if degree<old:raise ValueError("No negative degree elevation")
    return tuple(sum((exact_q(controls[j])*Q(math.comb(old,j)*math.comb(degree-old,k-j),math.comb(degree,k))
                      for j in range(max(0,k-degree+old),min(old,k)+1)),Q(0)) for k in range(degree+1))


def rational_rref_solution(matrix,target):
    if len(matrix)!=len(target) or not matrix:raise ValueError("Nonempty rectangular exact system required")
    columns=len(matrix[0])
    if any(len(row)!=columns for row in matrix):raise ValueError("Ragged exact matrix")
    rows=[[exact_q(x) for x in row]+[exact_q(y)] for row,y in zip(matrix,target)]
    pivots=[];active=0
    for column in range(columns):
        pivot=next((i for i in range(active,len(rows)) if rows[i][column]!=0),None)
        if pivot is None:continue
        rows[active],rows[pivot]=rows[pivot],rows[active]
        divisor=rows[active][column];rows[active]=[x/divisor for x in rows[active]]
        for i in range(len(rows)):
            if i!=active and rows[i][column]:
                factor=rows[i][column];rows[i]=[a-factor*b for a,b in zip(rows[i],rows[active])]
        pivots.append(column);active+=1
        if active==len(rows):break
    if any(all(value==0 for value in row[:-1]) and row[-1]!=0 for row in rows):
        return {"consistent":False,"rank":len(pivots),"pivots":pivots,"reason":"exact_inconsistency"}
    solution=[Q(0)]*columns
    for i,column in enumerate(pivots):solution[column]=rows[i][-1]
    return {"consistent":True,"rank":len(pivots),"pivots":pivots,
            "free_columns":[j for j in range(columns) if j not in pivots],"solution":tuple(solution)}


def exactify_support(library,target,used_float_weights):
    if len(used_float_weights)!=len(library) or not all(math.isfinite(x) for x in used_float_weights):
        return {"verified":False,"reason":"invalid_support_proposal","attempts":[]}
    supports=[tuple(i for i,value in enumerate(used_float_weights) if value>SUPPORT_THRESHOLD),
              tuple(i for i,value in enumerate(used_float_weights) if value>0)]
    attempts=[]
    for label,support in zip(("threshold_1e-10","all_strictly_positive"),supports):
        if any(tuple(row["support"])==support for row in attempts):continue
        matrix=[[Q(1)]*len(support)]+[[exact_q(library[i][coordinate]) for i in support] for coordinate in range(28)]
        solved=rational_rref_solution(matrix,[Q(1)]+list(target))
        record={"strategy":label,"support":support,"linear_result":solved}
        valid=False
        if solved["consistent"]:
            weights=[Q(0)]*len(library)
            for i,value in zip(support,solved["solution"]):weights[i]=value
            valid=(all(value>=0 for value in weights) and sum(weights)==1
                   and all(sum((weights[i]*exact_q(library[i][c]) for i in range(len(library))),Q(0))==exact_q(target[c]) for c in range(28)))
            record["nonnegative_exact_identity"]=valid
            record["candidate_weights"]=weights
        attempts.append(record)
        if valid:return {"verified":True,"weights":weights,"attempts":attempts}
    return {"verified":False,"attempts":attempts,"reason":"bounded_support_exactification_unresolved"}


def verify_polynomial_certificate(power,controls,weights,library):
    if len(controls)!=len(weights):return False
    for target,vector in zip(controls,weights):
        if len(vector)!=len(library):return False
        exact_vector=tuple(exact_q(x) for x in vector)
        if any(x<0 for x in exact_vector) or sum(exact_vector,Q(0))!=1:return False
        if any(sum((exact_vector[i]*exact_q(library[i][c]) for i in range(len(library))),Q(0))!=exact_q(target[c]) for c in range(28)):return False
    degree=len(controls)-1
    for coordinate in range(28):
        reconstructed=bernstein_to_power([sum((exact_q(vector[i])*exact_q(library[i][coordinate]) for i in range(len(library))),Q(0)) for vector in weights])
        expected=tuple(map(exact_q,power[coordinate]))+(Q(0),)*(degree+1-len(power[coordinate]))
        if reconstructed!=expected:return False
    return True


def encoded(value):
    if isinstance(value,Q):return {"numerator":value.numerator,"denominator":value.denominator}
    if isinstance(value,dict):return {str(k):encoded(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [encoded(x) for x in value]
    return value


def save(path,payload):
    with path.open("xb") as raw,gzip.GzipFile(fileobj=raw,mode="wb",mtime=0,compresslevel=3) as stream:
        stream.write((json.dumps(encoded(payload),separators=(",",":"),allow_nan=False)+"\n").encode())


def fit_degree(power,library,degree,records):
    coefficients=[power_to_bernstein(row,degree) for row in power]
    controls=tuple(tuple(row[j] for row in coefficients) for j in range(degree+1))
    weights=[];all_gates=True
    for j,target in enumerate(controls):
        if len(records)>=20:raise ArithmeticError("Frozen20-fit guard exceeded")
        proposal=convex_fit([[float(x) for x in row] for row in library],[float(x) for x in target])
        verification=proposal.get("verification",{})
        exact=exactify_support(library,target,verification["used_coefficients"]) if verification.get("verified") else {
            "verified":False,"reason":"no_verified_float_support","attempts":[]}
        gate=bool(proposal.get("solver_fit_solved",False) and exact["verified"])
        records.append({"degree":degree,"control_index":j,"float_proposal":proposal,
                        "exactification":exact,"run_gate_passed":gate})
        all_gates &= gate
        weights.append(exact.get("weights"))
    identity=bool(all(vector is not None for vector in weights)
                  and verify_polynomial_certificate(power,controls,weights,library))
    return {"degree":degree,"controls":controls,"weights":weights,"all_solver_and_exact_gates":all_gates,
            "exact_polynomial_identity":identity,"certified":bool(all_gates and identity)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec",type=Path,required=True);parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args();spec=json.loads(args.spec.read_text())
    if spec!={"degrees":[6,12],"support_threshold":SUPPORT_THRESHOLD,"maximum_fits":20,
              "LP_seconds_per_fit":1,"maximum_cpu_seconds":60,"maximum_wall_seconds":90,
              "maximum_threads":1,"maximum_planned_arrays_bytes":268435456,
              "maximum_new_output_bytes":33554432,"positive_optimizer_accepted":False}:
        raise ValueError("Frozen P53 protocol changed")
    provider_hash=hashlib.sha256(Path(lp_provider.__file__).read_bytes()).hexdigest()
    if provider_hash!=LP_PROVIDER_SHA256:raise ValueError("Qualified LP provider changed")
    args.output.mkdir(parents=True,exist_ok=False);started_cpu,started_wall=time.process_time(),time.perf_counter()
    wave=wave_coefficients();cosine=probability_cosine(wave);rank,crossing=rank_and_crossing(cosine)
    power=tuple(cosine_to_power([Q(x,KERNEL_DEN) for x in row]) for row in crossing)
    save(args.output/"exact_source.json.gz",{"counts":tuple(wave),"wave_z_integer":tuple(wave.values()),
        "probability_cosine_integer":tuple(cosine.values()),"probability_denominator":DEN,
        "rank_cosine_integer":rank,"crossing_cosine_integer":crossing,"kernel_denominator":KERNEL_DEN,
        "crossing_power":power})
    library_raw=classical_library();save(args.output/"exact_library.json.gz",library_raw)
    library=tuple(tuple(Q(x,KERNEL_DEN) for x in row) for row in library_raw["crossing_numerators"])
    records=[];attempts=[]
    first=fit_degree(power,library,6,records);attempts.append(first)
    if not first["certified"]:attempts.append(fit_degree(power,library,12,records))
    successful=next((attempt for attempt in attempts if attempt["certified"]),None)
    save(args.output/"certificate.json.gz",{"library_labels":library_raw["labels"],"attempts":attempts,"fit_records":records,
        "continuous_formula":"Lambda_c(x)=sum_j binom(d,j)*x^j*(1-x)^(d-j)*lambda[j,c]",
        "scope":"edge-MEAN only, fixed U8/full8CF/uniform top4 ties, eta1, every realtheta",
        "no_P52_data_or_floating_creation_used":True})
    summary={"status":"EXACT_CONTINUOUS_MEAN_REPLACEMENT_CERTIFIED" if successful else "INCONCLUSIVE_BERNSTEIN_OR_SUPPORT",
        "certified_degree":None if successful is None else successful["degree"],"LP_fits":len(records),
        "source_probability_normalization_exact":True,"rank_and_incident_identities_exact":True,
        "all6435_source_patterns_retained":True,"all71_control_vertices_retained":True,
        "positive_optimizer_accepted":False,"new_graph_or_photonic_or_MC_sample":False,
        "not_full_law_tail_runtime_loss_or_arbitraryN_theorem":True,"independent_review_required":True,
        "CPU_seconds_inside_main":time.process_time()-started_cpu,"wall_seconds_inside_main":time.perf_counter()-started_wall,
        "LP_provider_sha256":provider_hash,
        "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "spec_sha256":hashlib.sha256(args.spec.read_bytes()).hexdigest()}
    (args.output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    if sum(path.stat().st_size for path in args.output.rglob("*") if path.is_file())>spec["maximum_new_output_bytes"]:
        raise RuntimeError("P53 output cap exceeded; preserve failure without retry")
    print(json.dumps(summary))


if __name__=="__main__":main()
