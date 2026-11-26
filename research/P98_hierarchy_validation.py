"""Prospective exact P98 checker; no module-level scientific work or native imports."""
import argparse, hashlib, json, os, resource, sys, traceback
from fractions import Fraction as F
from itertools import combinations, permutations
from math import comb, factorial, prod
from pathlib import Path
POP = (("V0",1,0,1),("U1",1,1,2),("H2",2,2,6),("D3",3,3,20),
       ("R3a",1,3,4),("R3b",1,3,4),("S3",2,3,10),("B4",2,4,15),
       ("D4",4,4,70),("Z4",2,4,15),("R4",1,4,5),("C3",2,3,10),("X4",1,4,5))
RAW = "research/P96_column_loss_main/run_001/"
THREADS = ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS","BLIS_NUM_THREADS")
OUTPUT, CAP, RESERVE = "research/P98_hierarchy_main/run_001/data", 4194304, 65536
STATIC = ("AGENTS.md","pyproject.toml","requirements-research-lock.txt","research/P98_hierarchy_validation.py",
          "research/P98_hierarchy_contract_TEMPLATE.json","research/P98_HIERARCHY_VALIDATION_POPULATION.md",
          "research/P98_FACTORIAL_SURROGATE_HIERARCHY.md","research/P96_INDEPENDENT_SURROGATE_REVIEW.md")
def need(ok, message):
    if not ok:
        raise AssertionError(message)
def occupations(total, modes):
    if modes == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in occupations(total-first, modes-1):
                yield (first,)+tail
def binomial(n, r):
    return prod(comb(x,y) for x,y in zip(n,r)) if all(x>=y for x,y in zip(n,r)) else 0
def moments(law):
    return {r:sum((p*binomial(n,r) for n,p in law.items()),F(0)) for r in law}
def coefficients(a, degree):
    return {n:sum((v*binomial(r,n)*(-1)**(sum(r)-sum(n)) for r,v in a.items()
                   if sum(r)<=degree and all(x>=y for x,y in zip(r,n))),F(0)) for n in a}
def permanent(t, rows, columns):
    need(len(rows)<=4, "no permanent above four photons")
    return sum((prod(t[row][columns[p[i]]] for i,row in enumerate(rows))
                for p in permutations(range(len(rows)))),F(0))
def from_transfer(t, r):
    rows = [j for j,count in enumerate(r) for unused in range(count)]
    return sum((permanent(t,rows,I)**2 for I in combinations(range(len(t[0])),len(rows))),F(0))/prod(factorial(x) for x in r)
def elementary(c):
    e = [F(1)]+[F(0)]*(len(c)+1)
    for x in c:
        for d in range(len(c),0,-1):
            e[d] += x*e[d-1]
    return e
def choose(mu, k, epsilon):
    if mu == 0 or epsilon >= mu:
        return 0
    if epsilon == 0 or mu >= F(1,2):
        return k
    return next(s for s in range(k+1) if s==k or mu*(2*mu)**s<=epsilon)
def encode(value):
    if isinstance(value,F):
        return str(value)
    raise TypeError(type(value).__name__)
def safe(root, relative):
    p = Path(relative)
    need(p.as_posix()==relative and not p.is_absolute() and p.parts and all(x not in (".","..") for x in p.parts), "canonical relative input")
    current = root
    for part in p.parts:
        current /= part
        need(not current.is_symlink(), "input symlink")
    need(current.is_file(), "input regular file")
    return current
def binding(root, relative):
    b = json.loads(safe(root,relative).read_text())
    need(b["binding_state"]=="SEALED_ROOT_AUTHORIZED" and b["raw_sealed"] is True, "raw seal authorization")
    seal = b["producer_raw_seal_commit"]
    need(len(seal)==40 and set(seal)<=set("0123456789abcdef"), "full original seal commit")
    rows = b["artifacts"]
    names = [x["path"] for x in rows]
    need(relative not in names and len(names)==len(set(names)) and len(b["execution_artifacts"])==len(names)+1 and set(b["execution_artifacts"])==set(names)|{relative}, "binding closure")
    required = {RAW+x for x in ("manifest.json","stdout.txt","stderr.txt","data/records.jsonl","data/summary.json","data/failure.json")}
    need((required|set(STATIC))<=set(names) and b["input_records"]==RAW+"data/records.jsonl", "static and six producer files")
    for row in rows:
        p = safe(root,row["path"])
        need(type(row["bytes"]) is int and p.stat().st_size==row["bytes"] and hashlib.sha256(p.read_bytes()).hexdigest()==row["sha256"], "input hash/size")
    need(hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==b["source_sha256"], "frozen source")
    return b
def main():
    resource.setrlimit(resource.RLIMIT_FSIZE,(CAP,CAP))
    resource.setrlimit(resource.RLIMIT_CPU,(30,30))
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding",required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    need(sys.version_info[:3]==(3,11,15) and all(os.environ.get(x)=="1" for x in THREADS), "Python/environment profile")
    b = binding(root,args.binding)
    out = root/OUTPUT
    need(out.parent.is_dir() and not out.parent.is_symlink() and not out.parent.parent.is_symlink() and not out.exists() and not out.is_symlink(), "fresh runner child")
    out.mkdir()
    handle = (out/"records.jsonl").open("x",encoding="ascii")
    plan = [(name,s) for name,m,k,bins in POP for s in range(k+1)]+[("R16",s) for s in range(17)]
    used, finished, attempted, coefficient_rows, phase = 0, [], [], 0, "literal"
    def emit(row):
        nonlocal used
        payload = json.dumps(row,default=encode,sort_keys=True,allow_nan=False,separators=(",",":"))+"\n"
        need(used+len(payload.encode("ascii"))<=CAP-RESERVE, "scientific byte reserve")
        handle.write(payload)
        handle.flush()
        used += len(payload.encode("ascii"))
    failure = None
    try:
        q = coefficients(moments({(n,):F(n==3) for n in range(4)}),2)
        emit({"kind":"literal","q":[q[(n,)] for n in range(4)]})
        need(list(q.values())==[F(1),F(-3),F(3),F(0)], "pointmass N3 coefficients")
        need(sum(abs(F(n==3)-q[(n,)]) for n in range(4))/2==4, "literal signed half-l1")
        phase, cases = "producer", {}
        need(safe(root,b["input_records"]).stat().st_size<=8388608, "producer records cap")
        with safe(root,b["input_records"]).open() as source:
            for line in source:
                if '"kind": "exact_case_start"' not in line and '"kind": "exact_raw"' not in line:
                    continue
                row = json.loads(line)
                name = row["case"]
                if row["kind"]=="exact_case_start":
                    need(name not in cases, "duplicate case")
                    need(all(type(x) in (str,int) for r in row["T"] for x in r), "exact rational T tokens")
                    cases[name] = ([[F(x) for x in r] for r in row["T"]],{})
                else:
                    t,p = cases[name]
                    n = tuple(row["signal"])
                    need(len(n)==len(t) and all(type(x) is int and x>=0 for x in n) and type(row["p"]) is str and n not in p and type(row["loss"]) is int and row["loss"]==len(t[0])-sum(n), "raw row/total loss")
                    p[n] = F(row["p"])
        need(list(cases)==[x[0] for x in POP], "literal thirteen-case order")
        p16 = {(n,):sum((F(factorial(d)*comb(16,d)*comb(d,n)*(-1)**(d-n),64**d) for d in range(n,17)),F(0)) for n in range(17)}
        cases["R16"] = ([[F(1,8)]*16],p16)
        for name,m,k,bins in POP+(("R16",1,16,17),):
            phase = name
            t,p = cases[name]
            emit({"kind":"case","case":name,"T":t,"law":[{"n":n,"p":v} for n,v in p.items()]})
            support = [n for d in range(k+1) for n in occupations(d,m)]
            need(len(t)==m and all(len(row)==k for row in t) and set(p)==set(support) and len(p)==bins, "dense physical population")
            need(all(v>=0 for v in p.values()) and sum(p.values())==1, "physical law")
            c = [sum((t[j][i]**2 for j in range(m)),F(0)) for i in range(k)]
            mu, e, a = sum(c,F(0)), elementary(c), moments(p)
            need((mu==1 if name=="X4" else mu<=F(1,2)) and a.get((0,)*m)==1 and sum(v*sum(n) for n,v in p.items())==mu, "domain/normalization/first moment")
            for r,v in a.items():
                phase = str((name,"moment",r))
                expected = from_transfer(t,r) if k<=4 else F(factorial(sum(r))*comb(16,sum(r)),64**sum(r))
                emit({"kind":"moment","case":name,"r":r,"law":v,"transfer":expected})
                need(v==expected, "independent factorial moment (D)")
            selected = choose(mu,k,F(1,1000))
            need(0<=selected<=k and (selected==k or mu*(2*mu)**selected<=F(1,1000)), "selected degree certificate")
            need(choose(mu,k,mu)==0 and choose(mu,k,F(0))==(0 if mu==0 else k), "degree endpoints")
            need(name!="R16" or selected==8, "exact rational target degree")
            for s in range(k+1):
                phase = str((name,s))
                attempted.append((name,s))
                q = coefficients(a,s)
                alpha = -sum((v for v in q.values() if v<0),F(0))
                repaired = {n:max(v,F(0))/(1+alpha) for n,v in q.items()}
                signed = sum(abs(p[n]-q[n]) for n in p)/2
                tv = sum(abs(p[n]-repaired[n]) for n in p)/2
                vs = sum(v*sum(comb(sum(n),j)*comb(sum(n)-j-1,s-j) for j in range(s+1) if (s-j)%2==0) for n,v in p.items() if sum(n)>s)
                cb = 2**s*sum(v*comb(sum(n),s+1) for n,v in p.items())
                eb, mb = 2**s*factorial(s+1)*e[s+1], 2**s*mu**(s+1)
                for n in support:
                    emit({"kind":"coefficient","case":name,"s":s,"n":n,"p":p[n],"q":q[n],"repaired":repaired[n]})
                    coefficient_rows += 1
                emit({"kind":"pair","case":name,"s":s,"mu":mu,"alpha":alpha,"signed":signed,"V":vs,"binomial":cb,"e_bound":eb,"mu_bound":mb,"tv":tv,"selected":selected,"geometric":mu<F(1,2)})
                need(sum(q.values())==sum(repaired.values())==1 and tv<=signed==vs<=cb<=eb<=mb, "hierarchy gates")
                need(s!=k or q==p, "full degree exact")
                need(name!="R16" or s not in (6,8) or (q[(s-1,)]<0 and alpha>0), "predeclared negative coefficients")
                finished.append((name,s))
        need(finished==plan and len(plan)==68 and coefficient_rows==1054, "all 68 pairs / 1054 rows")
    except Exception as exc:
        failure = {"status":"FAILED","phase":phase,"exception":repr(exc),"traceback":traceback.format_exc()}
    handle.close()
    summary = {"status":"PASS" if failure is None else "FAILED","pairs":len(finished),"coefficient_rows":coefficient_rows,"FAILED_PAIR":[p for p in attempted if p not in finished],"NOT_RUN":[p for p in plan if p not in attempted],"producer_raw_seal_commit":b["producer_raw_seal_commit"],"native_calls":0,"RNG_draws":0,"positive_optimization":False}
    payloads = [json.dumps(x,sort_keys=True,allow_nan=False)+"\n" for x in (summary,failure)]
    need(used+sum(len(x.encode("ascii")) for x in payloads)<=CAP, "combined scientific cap")
    for name,payload in zip(("summary.json","failure.json"),payloads):
        (out/name).write_text(payload,encoding="ascii")
    if failure is not None:
        raise SystemExit(1)
if __name__ == "__main__":
    main()
