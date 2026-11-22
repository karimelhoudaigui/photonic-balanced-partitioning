"""P36 bounded algebra checks and a new pinched-state discriminator.

The pinched trace-distance is an upper bound on the fine occupation TV, not
the TV of a coarsened occupation law. No finite run proves its proposed delta
bound. All diagnostics below are distinct from a broad occupation-TV sweep.
"""
import resource
resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations
from math import comb, factorial
from pathlib import Path
import datetime
import hashlib
import json
import platform
import time
import numpy as np
import scipy
from scipy.linalg import expm
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DECLARED = [str((OUT/"receipt.json").relative_to(ROOT))]
PERMS = np.array(list(permutations(range(3))))
K = np.ones((6, 6))-np.eye(6)


def full_laws(v):
    b, d = {}, {}
    for rows in combinations_with_replacement(range(len(v)), 3):
        amp = [np.prod(v[np.array(rows), p]) for p in PERMS]
        fac = np.prod([factorial(rows.count(i)) for i in set(rows)])
        b[rows] = float(abs(sum(amp))**2/fac)
        d[rows] = float(sum(abs(x)**2 for x in amp)/fac)
    assert abs(sum(b.values())-1) < 1e-12
    assert abs(sum(d.values())-1) < 1e-12
    return b, d


def convolve(*measures):
    result = {(): 1.}
    for measure in measures:
        nxt = defaultdict(complex)
        for rows, w in result.items():
            for i, z in measure.items():
                nxt[tuple(sorted(rows+(i,)))] += w*z
        result = nxt
    return result


def phase_difference(v):
    q = [{i: abs(v[i, a])**2 for i in range(len(v))} for a in range(3)]
    mu = {(a,b): {i: v[i,a].conjugate()*v[i,b] for i in range(len(v))}
          for a,b in ((0,1),(0,2),(1,2),(2,0))}
    result = defaultdict(complex)
    for a,b,c in ((0,1,2),(0,2,1),(1,2,0)):
        for rows,z in convolve(mu[a,b],{i:w.conjugate() for i,w in mu[a,b].items()},q[c]).items():
            result[rows] += z
    for rows,z in convolve(mu[0,1],mu[1,2],mu[2,0]).items():
        result[rows] += 2*z.real
    return result


def pinched_distance(v):
    q = abs(v)**2
    groups = np.argmax(q, axis=1)
    remainder = q.copy(); remainder[np.arange(len(v)),groups] = 0
    delta = float(remainder.sum())
    effects = [v[groups==g].conj().T@v[groups==g] for g in range(3)]
    assert np.linalg.norm(sum(effects)-np.eye(3)) < 1e-12
    value = trace_residual = 0.
    minimum_gram_eigenvalue = 0.
    sector_values = []
    for r in combinations_with_replacement(range(3),3):
        gram = np.ones((6,6),dtype=complex)
        for j,g in enumerate(r):
            gram *= effects[g][PERMS[:,j,None],PERMS[None,:,j]]
        eigenvalues,eigenvectors = np.linalg.eigh((gram+gram.conj().T)/2)
        minimum_gram_eigenvalue = min(minimum_gram_eigenvalue,float(min(eigenvalues)))
        assert min(eigenvalues)>-1e-12
        root = (eigenvectors*np.sqrt(np.maximum(eigenvalues,0)))@eigenvectors.conj().T
        compressed = root@K@root/6
        ev = np.linalg.eigvalsh((compressed+compressed.conj().T)/2)
        multiplicity = factorial(3)//np.prod([factorial(r.count(g)) for g in range(3)])
        contribution = float(multiplicity*sum(abs(ev))/2)
        value += contribution
        trace_residual += float(multiplicity*sum(ev))
        sector_values.append({"groups":r,"contribution":contribution})
    b,d = full_laws(v)
    fine_tv = sum(abs(b[x]-d[x]) for x in b)/2
    phase = phase_difference(v)
    identity_error = max(abs(phase[x]-(b[x]-d[x])) for x in b)
    assert identity_error<1e-12 and fine_tv<=value+1e-12
    return {"m":len(v),"delta":delta,"pinched_trace_distance":value,"fine_occupation_TV":fine_tv,
        "pinched_minus_delta":value-delta,"phase_identity_error":identity_error,
        "orthogonality_residual":float(np.linalg.norm(v.conj().T@v-np.eye(3))),
        "pinched_trace_residual":trace_residual,"minimum_gram_eigenvalue":minimum_gram_eigenvalue,
        "sectors":sector_values}


def algebra():
    c,s,x = sp.symbols("c s x",real=True)
    chain = sp.Matrix([[c,-s*c,s*s],[s,c*c,-c*s],[0,s,c]])
    table = {}
    for rows in combinations_with_replacement(range(3),3):
        amps = [sp.prod(chain[rows[j],p[j]] for j in range(3)) for p in PERMS]
        fac = np.prod([factorial(rows.count(i)) for i in set(rows)])
        poly = sp.Poly(sp.expand((sum(amps)**2-sum(a*a for a in amps))/int(fac)),c,s)
        assert all(ec%2==es%2==0 for (ec,es),v in poly.terms())
        value = sp.factor(sum(v*(1-x)**(ec//2)*x**(es//2) for (ec,es),v in poly.terms()))
        table["".join(map(str,rows))] = value
    assert sp.simplify(sum(table.values())) == 0
    F0 = 4*x*(1-x)*(3*x*x-3*x+1)
    delta = 4*x-x*x
    differences = [sp.factor(delta-F0),sp.factor(delta-F0+table["011"]),
                   sp.factor(delta-F0+table["011"]+2*table["002"])]
    z = sp.symbols("z",nonzero=True)
    U = sp.eye(3)+(z-1)*sp.ones(3)/3
    assert sp.simplify(U.T.subs(z,1/z)*U-sp.eye(3)) == sp.zeros(3)
    A,B = (5+4*x)/9,(2-2*x)/9
    tritter = {}
    for rows in combinations_with_replacement(range(3),3):
        amps = [sp.prod(U[rows[j],p[j]] for j in range(3)) for p in PERMS]
        fac = np.prod([factorial(rows.count(i)) for i in set(rows)])
        laurent = sp.expand(sum(amps)*sum(amps).subs(z,1/z)/int(fac))
        pb = laurent.coeff(z,0)
        for degree in range(1,4):
            assert laurent.coeff(z,degree)==laurent.coeff(z,-degree)
            pb += 2*laurent.coeff(z,degree)*sp.chebyshevt(degree,x)
        pd = sum(sp.prod(A if rows[j]==p[j] else B for j in range(3)) for p in PERMS)/int(fac)
        tritter["".join(map(str,rows))] = sp.factor(pb-pd)
    assert sp.simplify(sum(tritter.values())) == 0
    t=sp.symbols("t",positive=True);D=t*t+2;b=(2*t+1)/D
    obstruction=sp.factor(3*b*b+2*b**3-12/D)
    assert sp.simplify(obstruction-(28*t**3+3*t*t+36*t-40)/D**3)==0
    d=sp.symbols("delta",real=True)
    small=sp.factor(-tritter["012"].subs(x,1-3*d/4))
    assert sp.simplify(small-(d-sp.Rational(13,12)*d*d+sp.Rational(5,18)*d**3))==0
    return {"chain_signed_table":{a:str(b) for a,b in table.items()},
        "chain_delta_minus_TV":[str(a) for a in differences],
        "tritter_signed_table":{a:str(b) for a,b in tritter.items()},
        "tritter_small_delta_TV":str(small),"gram_obstruction":str(obstruction)}


def main():
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    wall,cpu=time.monotonic(),time.process_time()
    script_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    exact = algebra()
    w=np.zeros((6,3));w[0,0]=w[1,0]=w[2,1]=w[3,1]=w[4,2]=w[5,2]=1/np.sqrt(2)
    vac=w.copy();vac[1::2]*=-1
    basis=np.column_stack([w,vac])
    rng=np.random.default_rng(1729)
    generators=[]
    for edges in [[(0,1)],[(0,4),(1,3)],[(0,4),(1,5),(2,3)]]:
        H=np.zeros((6,6),complex)
        for i,j in edges:H[i,j]=1;H[j,i]=1
        generators.append(H)
    raw=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6))
    generators.append(raw+raw.conj().T)
    diagnostics=[]
    for generator,H in enumerate(generators):
        H=H/np.linalg.norm(H,2)
        for angle in (.1,.4,.8):
            v=basis@expm(1j*angle*H)[:,:3]
            result=pinched_distance(v)
            result.update({"construction":"six_mode_generator","generator":generator,"angle":angle})
            diagnostics.append(result)
    fourier=np.exp(2j*np.pi*np.outer(np.arange(3),np.arange(3))/3)/np.sqrt(3)
    for eps in (.01,.05,.12):
        routing=np.full((3,3),eps);np.fill_diagonal(routing,1-2*eps)
        v=np.vstack([fourier*np.sqrt(routing[g]) for g in range(3)])
        result=pinched_distance(v)
        result.update({"construction":"diagonal_effects_flat_fourier","epsilon":eps})
        diagnostics.append(result)
    result={"base_commit":"de77a1404cbab6f98d3187bad4ab42b772789f29","exact_algebra":exact,
        "assertion_tested":"Exact identities for two fixed connected families and Gram obstruction; finite trace-distance pinching discriminator on 15 specified frames, not a universal bound",
        "diagnostics":diagnostics,"maximum_pinched_minus_delta":max(r["pinched_minus_delta"] for r in diagnostics),
        "cpu_seconds":time.process_time()-cpu,"numerical_semantics":"FLOAT64_DIAGNOSTIC_NOT_INTERVAL_CERTIFIED"}
    path=OUT/"receipt.json";path.write_text(json.dumps(result,indent=2)+"\n")
    manifest={"schema_version":2,"claim_id":"P36-phase-aware-analytic-attempt",
        "repository":{"commit":result["base_commit"],"dirty":True},
        "command":["/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python","experiments/P36_analytic_attempt/check.py"],
        "environment":{"software":[{"name":"Python","version":platform.python_version()},{"name":"NumPy","version":np.__version__},{"name":"SciPy","version":scipy.__version__},{"name":"SymPy","version":sp.__version__}],"hardware":platform.platform()+" "+platform.machine()},
        "mathematics":{"assertion_tested":result["assertion_tested"],"coefficient_domain":"Exact rational symbolic algebra and float64 diagnostics","conventions":"Full Fock occupations, halved TV, no postselection","inputs":[str(Path(__file__).relative_to(ROOT))],"bounds":{"k":3,"m_max":9,"specified_frames":15},"non_claims":["No universal pinched-state inequality proved by this finite test","No general conjecture verdict from data","No novelty or QPU claim"]},
        "randomness":{"used":True,"generator":"NumPy default_rng PCG64 for one fixed dense Hermitian generator","seed":1729},
        "run":{"started_at":started,"runtime_seconds":time.monotonic()-wall,"exit_status":0,"status":"completed","resource_limits":{"memory_bytes":None,"cpu_seconds":60,"max_cores":1,"max_threads":1}},
        "outputs":[{"path":str(path.relative_to(ROOT)),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"kind":"result"}],
        "checks":["Exact family polynomials normalize in difference","Exact positive-Gram counterexample","Phase-aware signed convolution agrees with direct Fock expansion","Fine TV <= pinched trace distance on specified frames"],
        "result":"Partial exact results; remaining pinched inequality only finitely tested","residual_risks":["Float eigensolver with tiny negative eigenvalues clipped after recording","Finite frames do not establish universal inequality"],
        "input_artifacts":[{"path":str(Path(__file__).relative_to(ROOT)),"sha256":script_hash,"sha256_after":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}],"declared_results":DECLARED}
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps({"frames":len(diagnostics),"maximum_pinched_minus_delta":result["maximum_pinched_minus_delta"],"cpu_seconds":result["cpu_seconds"],"receipt_sha256":hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))


if __name__=="__main__":main()
