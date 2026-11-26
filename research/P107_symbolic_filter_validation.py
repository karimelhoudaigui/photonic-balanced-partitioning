"""P107 prospective exact Gaussian-integer polynomial discriminator; no native imports."""
import argparse, hashlib, json, os, resource, sys, traceback
from fractions import Fraction as F
from itertools import combinations, permutations
from math import comb, factorial, prod
from pathlib import Path

OUTPUT, CAP, RESERVE = "research/P107_symbolic_filter_main/run_001/data", 4194304, 65536
THREADS = ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS","BLIS_NUM_THREADS")
STATIC = ("AGENTS.md","pyproject.toml","requirements-research-lock.txt",
          "research/P107_symbolic_filter_validation.py","research/P107_SYMBOLIC_FILTER_POPULATION.md",
          "research/P107_symbolic_filter_contract_TEMPLATE.json","research/P101_FINITE_FILTER_ALL_OUTPUT_CARD.md",
          "research/P98_FACTORIAL_SURROGATE_HIERARCHY.md")
P101_SHA = "65e4199fb468d02eec4155072a60b8d7818ee0d57ef6205e83c2da51bc60027c"
PHASES, DETECTORS = ((1,0),(0,-1),(-1,0),(0,1)), ("PNR","THRESHOLD")
OPS = [0,0]

def need(ok, message):
    if not ok:
        raise AssertionError(message)

def ga(a,b):
    return (a[0]+b[0],a[1]+b[1])

def gm(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])

def const(value, variables=2):
    value = value if isinstance(value,tuple) else (value,0)
    need(all(type(x) is int for x in value), "integer Gaussian constant")
    return {(0,)*variables:value} if value!=(0,0) else {}

def add(a,b):
    out = dict(a)
    for e,c in b.items():
        out[e] = ga(out.get(e,(0,0)),c)
        if out[e]==(0,0):
            del out[e]
    return out

def scale(a,k):
    need(type(k) is int, "integer polynomial scale")
    return {e:(c[0]*k,c[1]*k) for e,c in a.items() if k}

def multiply(a,b):
    out = {}
    OPS[0] += len(a)*len(b)
    for x,c in a.items():
        for y,d in b.items():
            need(len(x)==len(y), "polynomial dimension")
            e = tuple(i+j for i,j in zip(x,y))
            need(e[0]<=8 and e[1]<=8 and sum(e[2:])<=4, "registered degree bound: "+repr(e))
            out[e] = ga(out.get(e,(0,0)),gm(c,d))
    out = {e:c for e,c in out.items() if c!=(0,0)}
    OPS[1] = max(OPS[1],len(out))
    return out

def conjugate(a):
    return {e:(c[0],-c[1]) for e,c in a.items()}

def swap(a):
    return {(e[1],e[0])+e[2:]:c for e,c in a.items()}

def lift(a,m):
    return {e+(0,)*m:c for e,c in a.items()}

def shift(a,axis):
    return {tuple(x+int(i==axis) for i,x in enumerate(e)):c for e,c in a.items()}

def divide(a,d):
    need(d>0 and all(c[0]%d==c[1]%d==0 for c in a.values()), "exact output factorial division")
    return {e:(c[0]//d,c[1]//d) for e,c in a.items()}

def permanent(matrix,variables):
    k = len(matrix)
    need(k<=4 and all(len(row)==k for row in matrix), "permutation size <=4")
    answer = {}
    for p in permutations(range(k)):
        term = const(1,variables)
        for i,j in enumerate(p):
            term = multiply(term,matrix[i][j])
        answer = add(answer,term)
    return answer

def occupations(total,m):
    if m==1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in occupations(total-first,m-1):
                yield (first,)+tail

def states(m,k):
    return [n for total in range(k+1) for n in occupations(total,m)]

def extract(p,m,k):
    answer = {n:{} for n in states(m,k)}
    for e,c in p.items():
        need(e[2:] in answer, "unexpected signal monomial: "+repr((e,c)))
        answer[e[2:]][e[:2]] = c
    return answer

def laws(numerator,denominator):
    m,k = len(numerator),len(numerator[0])
    need(1<=m<=4 and k<=4 and all(len(row)==k for row in numerator), "finite matrix shape")
    matrix = [[const(denominator**2*int(i==j),2+m) for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range(k):
            for a in range(m):
                c = lift(multiply(conjugate(numerator[a][i]),numerator[a][j]),m)
                matrix[i][j] = add(add(matrix[i][j],scale(c,-1)),shift(c,2+a))
    d = const(1,2+m)
    for i in range(k):
        d = multiply(d,matrix[i][i])
    return extract(permanent(matrix,2+m),m,k),extract(d,m,k),denominator**(2*k)

def moment_alternative(numerator,denominator):
    m,k = len(numerator),len(numerator[0])
    support, moments = states(m,k), {}
    for r in support:
        degree = sum(r)
        rows = [j for j,count in enumerate(r) for unused in range(count)]
        a = {}
        for columns in combinations(range(k),degree):
            amplitude = permanent([[numerator[j][i] for i in columns] for j in rows],2)
            a = add(a,multiply(amplitude,conjugate(amplitude)))
        moments[r] = scale(divide(a,prod(factorial(x) for x in r)),denominator**(2*(k-degree)))
    answer = {}
    for n in support:
        p = {}
        for r,a in moments.items():
            if all(x>=y for x,y in zip(r,n)):
                p = add(p,scale(a,(-1)**(sum(r)-sum(n))*prod(comb(x,y) for x,y in zip(r,n))))
        answer[n] = p
    return answer

def family():
    monomials = ((0,0),(1,0),(1,1),(0,1))
    return [[{e:PHASES[((j-k)*r)%4] for r,e in enumerate(monomials)} for k in range(4)] for j in range(4)]

def fixtures():
    return [("vacuum",[[]],1,{(0,):F(1)},{(0,):F(1)}),
            ("unary",[[1]],2,{(0,):F(3,4),(1,):F(1,4)},{(0,):F(3,4),(1,):F(1,4)}),
            ("identity2",[[1,0],[0,1]],1,{(1,1):F(1)},{(1,1):F(1)}),
            ("rotation2",[[3,4],[-4,3]],5,{(2,0):F(288,625),(0,2):F(288,625),(1,1):F(49,625)},
             {(2,0):F(144,625),(0,2):F(144,625),(1,1):F(337,625)}),
            ("rankone2",[[1,1],[1,1]],2,{(0,0):F(1,2),(2,0):F(1,8),(0,2):F(1,8),(1,1):F(1,4)},
             {(0,0):F(1,4),(1,0):F(1,4),(0,1):F(1,4),(2,0):F(1,16),(0,2):F(1,16),(1,1):F(1,8)})]

def cut(pair):
    chosen = set(pair)
    return F(sum((2 if (i,j) in ((0,2),(1,3)) else 1) for i in range(4) for j in range(i+1,4)
                 if (i in chosen)!=(j in chosen)),2)

def decoded_cost(n,detector):
    if detector=="PNR":
        candidates = [sorted(range(4),key=lambda j:(-n[j],priority.index(j)))[:2] for priority in permutations(range(4))]
    else:
        need(detector=="THRESHOLD", "known decoder")
        clicked = [j for j,count in enumerate(n) if count]
        candidates = list(combinations(clicked,2)) if len(clicked)>=2 else ([(clicked[0],j) for j in range(4) if j not in clicked] if clicked else list(combinations(range(4),2)))
    return sum((cut(pair) for pair in candidates),F(0))/len(candidates)

def real_polynomial(p,denominator):
    need(all(c[1]==0 for c in p.values()), "real probability coefficients")
    return {e:F(c[0],denominator) for e,c in p.items()}

def evaluate(p,x,y):
    return sum((c*x**i*y**j for (i,j),c in p.items()),F(0))

def mean(p,weights):
    out = {}
    for n,polynomial in p.items():
        cost = weights[n]
        for e,c in polynomial.items():
            out[e] = out.get(e,F(0))+cost*c
    return {e:c for e,c in out.items() if c}

def difference(a,b):
    return {e:a.get(e,F(0))-b.get(e,F(0)) for e in set(a)|set(b) if a.get(e,F(0))!=b.get(e,F(0))}

def bernstein(p,a,b,width):
    def transform(lo):
        return [[sum((F(comb(k,r)*comb(i,r),comb(8,r))*lo**(k-r)*width**r for r in range(min(i,k)+1)),F(0)) for k in range(9)] for i in range(9)]
    tx,ty = transform(a),transform(b)
    return [[sum((c*tx[i][k]*ty[j][l] for (k,l),c in p.items()),F(0)) for j in range(9)] for i in range(9)]

def bernstein_value(coefficients,u,v):
    return sum((coefficients[i][j]*comb(8,i)*u**i*(1-u)**(8-i)*comb(8,j)*v**j*(1-v)**(8-j) for i in range(9) for j in range(9)),F(0))

def polynomial_record(p):
    return [[list(e),list(c)] for e,c in sorted(p.items())]

def encode(value):
    if isinstance(value,F):
        return str(value)
    raise TypeError(type(value).__name__)

def safe(root,relative):
    p = Path(relative)
    need(p.as_posix()==relative and not p.is_absolute() and p.parts and all(x not in (".","..") for x in p.parts), "canonical relative input")
    current = root
    for part in p.parts:
        current /= part
        need(not current.is_symlink(), "input symlink")
    need(current.is_file(), "regular input")
    return current

def authorize(root,relative):
    b = json.loads(safe(root,relative).read_text())
    need(b["binding_state"]=="ROOT_AUTHORIZED" and b["run_authorized"] is True, "separate ROOT authorization")
    names = [r["path"] for r in b["artifacts"]]
    need(relative not in names and len(names)==len(set(names)) and set(STATIC)<=set(names), "static closure")
    need(len(b["execution_artifacts"])==len(names)+1 and set(b["execution_artifacts"])==set(names)|{relative}, "exact runner closure")
    for row in b["artifacts"]:
        path = safe(root,row["path"])
        need(type(row["bytes"]) is int and path.stat().st_size==row["bytes"] and hashlib.sha256(path.read_bytes()).hexdigest()==row["sha256"], "input hash/size")
        if row["path"]=="research/P101_FINITE_FILTER_ALL_OUTPUT_CARD.md":
            need(row["sha256"]==P101_SHA, "exact P101 source")
    need(hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==b["source_sha256"], "frozen checker")
    return b

class Evidence:
    def __init__(self,out):
        need(out.parent.is_dir() and not out.parent.is_symlink() and not out.parent.parent.is_symlink() and not out.exists() and not out.is_symlink(), "fresh runner child")
        out.mkdir()
        self.out,self.used,self.rows = out,0,0
        self.handle = (out/"records.jsonl").open("x",encoding="ascii")
    def emit(self,row):
        payload = json.dumps(row,default=encode,sort_keys=True,allow_nan=False,separators=(",",":"))+"\n"
        size = len(payload.encode("ascii"))
        need(self.used+size<=CAP-RESERVE, "combined scientific reserve")
        self.handle.write(payload)
        self.handle.flush()
        self.used += size
        self.rows += 1
    def finish(self,summary,failure):
        self.handle.close()
        payloads = [json.dumps(v,default=encode,sort_keys=True,allow_nan=False)+"\n" for v in (summary,failure)]
        need(self.used+sum(len(v.encode("ascii")) for v in payloads)<=CAP, "combined scientific cap")
        for name,payload in zip(("summary.json","failure.json"),payloads):
            with (self.out/name).open("x",encoding="ascii") as handle:
                handle.write(payload)

def main():
    resource.setrlimit(resource.RLIMIT_FSIZE,(CAP,CAP))
    resource.setrlimit(resource.RLIMIT_CPU,(60,60))
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding",required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    need(sys.version_info[:3]==(3,11,15) and all(os.environ.get(k)=="1" for k in THREADS), "Python/thread profile")
    binding = authorize(root,args.binding)
    writer = Evidence(root/OUTPUT)
    plan = [("fixture",name) for name in ("vacuum","unary","identity2","rotation2","rankone2")]+[("decoder_hand",),("bernstein_hand",),("symbolic",),("endpoint",0),("endpoint",1)]
    plan += [("grid",i,j) for i in range(5) for j in range(5)]
    plan += [("box",d,l,i,j) for d in DETECTORS for l in range(3) for i in range(2**l) for j in range(2**l)]
    plan += [("classification",)]
    attempted,completed,counts,failure,certificates = [],[],{"coefficients":0,"boxes":0,"bernstein_coefficients":0,"grid":0},None,{}
    task,phase = None,"authorization complete"
    try:
        writer.emit({"kind":"provenance","source_sha256":binding["source_sha256"],"Python":sys.version,"environment":{k:os.environ.get(k) for k in THREADS},"caps":{"CPU":60,"wall_runner":90,"science":CAP,"reserve":RESERVE}})
        for name,rows,denominator,eb,ed in fixtures():
            task,phase = ("fixture",name),name
            attempted.append(task)
            matrix = [[const(v) for v in row] for row in rows]
            pb,pd,den = laws(matrix,denominator)
            alt = moment_alternative(matrix,denominator)
            for n in states(len(rows),len(rows[0])):
                writer.emit({"kind":"fixture","case":name,"occupation":n,"denominator":den,"B":polynomial_record(pb[n]),"D":polynomial_record(pd[n]),"B_moment":polynomial_record(alt[n]),"expected_B":eb.get(n,F(0)),"expected_D":ed.get(n,F(0))})
                need(pb[n]==alt[n] and real_polynomial(pb[n],den)==({(0,0):eb[n]} if eb.get(n,F(0)) else {}) and real_polynomial(pd[n],den)==({(0,0):ed[n]} if ed.get(n,F(0)) else {}), "literal physical fixture")
            completed.append(task)
        task,phase = ("decoder_hand",),"decoder_hand"
        attempted.append(task)
        for n,ep,et in (((0,0,0,0),F(8,3),F(8,3)),((1,1,1,1),F(8,3),F(8,3)),((2,1,1,0),F(5,2),F(8,3)),((1,2,1,0),F(3),F(8,3))):
            actual = [decoded_cost(n,d) for d in DETECTORS]
            writer.emit({"kind":"decoder_hand","occupation":n,"means":actual,"expected":[ep,et]})
            need(actual==[ep,et], "exact uniform tie/click decoder")
        completed.append(task)
        task,phase = ("bernstein_hand",),"bernstein_hand"
        attempted.append(task)
        for name,p in (("constant",{(0,0):F(1)}),("linear",{(1,0):F(1),(0,1):F(1)}),("highest",{(8,8):F(1)})):
            b = bernstein(p,F(0),F(0),F(1))
            expected = [[F(1) if name=="constant" else (F(i+j,8) if name=="linear" else F(i==j==8)) for j in range(9)] for i in range(9)]
            writer.emit({"kind":"bernstein_hand","case":name,"coefficients":b,"expected":expected})
            need(b==expected, "hand Bernstein basis conversion")
        completed.append(task)
        task,phase = ("symbolic",),"target PGF"
        attempted.append(task)
        matrix = family()
        writer.emit({"kind":"matrix","denominator":4,"N":[[polynomial_record(p) for p in row] for row in matrix]})
        need(all(matrix[j][i]==conjugate(matrix[i][j]) and swap(matrix[i][j])==conjugate(matrix[i][j]) for i in range(4) for j in range(4)), "Hermitian / x-y conjugation")
        pb,pd,den = laws(matrix,4)
        alt = moment_alternative(matrix,4)
        support = states(4,4)
        need(len(support)==70 and den==65536, "target population and scale")
        for n in support:
            for i in range(9):
                for j in range(9):
                    phase = str(("coefficient",n,i,j))
                    b,d,a = pb[n].get((i,j),(0,0)),pd[n].get((i,j),(0,0)),alt[n].get((i,j),(0,0))
                    writer.emit({"kind":"coefficient","occupation":n,"powers":[i,j],"denominator":den,"B":b,"D":d,"B_minus_D":ga(b,(-d[0],-d[1])),"B_moment":a})
                    counts["coefficients"] += 1
                    need(b==a and b[1]==d[1]==0 and b==pb[n].get((j,i),(0,0)) and d==pd[n].get((j,i),(0,0)), "independent B / realness / x-y symmetry")
        phase,sb,sd = "formal normalization",{},{}
        for n in support:
            sb,sd = add(sb,pb[n]),add(sd,pd[n])
        writer.emit({"kind":"normalization","denominator":den,"B":polynomial_record(sb),"D":polynomial_record(sd)})
        need(sb==sd==const(den), "formal full raw normalization")
        phase = "mean polynomials"
        bp,dp = {n:real_polynomial(p,den) for n,p in pb.items()},{n:real_polynomial(p,den) for n,p in pd.items()}
        costs = {d:{} for d in DETECTORS}
        for n in support:
            for d in DETECTORS:
                costs[d][n] = decoded_cost(n,d)
                writer.emit({"kind":"decoder_cost","decoder":d,"occupation":n,"mean_cut":costs[d][n]})
                need(2<=costs[d][n]<=3, "decoded graph-cut range")
        mb,md = {d:mean(bp,costs[d]) for d in DETECTORS},{d:mean(dp,costs[d]) for d in DETECTORS}
        diff = {d:difference(mb[d],md[d]) for d in DETECTORS}
        for d in DETECTORS:
            for i in range(9):
                for j in range(9):
                    writer.emit({"kind":"mean_coefficient","decoder":d,"powers":[i,j],"B":mb[d].get((i,j),F(0)),"D":md[d].get((i,j),F(0)),"B_minus_D":diff[d].get((i,j),F(0))})
        completed.append(task)
        for endpoint in (0,1):
            task,phase = ("endpoint",endpoint),str(("endpoint",endpoint))
            attempted.append(task)
            for n in support:
                total = sum(n)
                multinomial = F(factorial(total),4**total*prod(factorial(v) for v in n))
                eb = F(n==(1,1,1,1)) if endpoint else (F(15,32),F(1,4),F(3,16),F(0),F(3,32))[total]*multinomial
                ed = F(n==(1,1,1,1)) if endpoint else F(comb(4,total)*3**(4-total),4**4)*multinomial
                vb,vd = evaluate(bp[n],F(endpoint),F(endpoint)),evaluate(dp[n],F(endpoint),F(endpoint))
                writer.emit({"kind":"endpoint","point":[endpoint,endpoint],"occupation":n,"B":vb,"D":vd,"expected_B":eb,"expected_D":ed})
                need(vb==eb and vd==ed, "identity / rank-one full raw law")
            completed.append(task)
        negative,levels = {d:[] for d in DETECTORS},{d:{l:[] for l in range(3)} for d in DETECTORS}
        for i in range(5):
            for j in range(5):
                task,phase = ("grid",i,j),str(("grid",i,j))
                attempted.append(task)
                x,y = F(i,4),F(j,4)
                values_b,values_d = [evaluate(bp[n],x,y) for n in support],[evaluate(dp[n],x,y) for n in support]
                observations = {d:{"B":evaluate(mb[d],x,y),"D":evaluate(md[d],x,y),"B_minus_D":evaluate(diff[d],x,y)} for d in DETECTORS}
                writer.emit({"kind":"grid","point":[x,y],"occupation_order":support,"B_probabilities":values_b,"D_probabilities":values_d,"means":observations})
                need(min(values_b+values_d)>=0 and sum(values_b)==sum(values_d)==1, "grid physical probabilities")
                for d in DETECTORS:
                    need(observations[d]["B"]==sum(v*costs[d][n] for n,v in zip(support,values_b)) and observations[d]["D"]==sum(v*costs[d][n] for n,v in zip(support,values_d)), "mean polynomial / direct decoder sum")
                    if observations[d]["B_minus_D"]<0:
                        negative[d].append([x,y,observations[d]["B_minus_D"]])
                counts["grid"] += 1
                completed.append(task)
        for d in DETECTORS:
            for level in range(3):
                for i in range(2**level):
                    for j in range(2**level):
                        task,phase = ("box",d,level,i,j),str(("box",d,level,i,j))
                        attempted.append(task)
                        a,b,width = F(i,2**level),F(j,2**level),F(1,2**level)
                        coefficients = bernstein(diff[d],a,b,width)
                        for u in range(9):
                            for v in range(9):
                                writer.emit({"kind":"bernstein_coefficient","decoder":d,"level":level,"box":[i,j],"lower":[a,b],"width":width,"index":[u,v],"value":coefficients[u][v]})
                                counts["bernstein_coefficients"] += 1
                        checks = [[u,v,evaluate(diff[d],a+width*u,b+width*v),bernstein_value(coefficients,u,v)] for u in (F(0),F(1,2),F(1)) for v in (F(0),F(1,2),F(1))]
                        nonnegative = all(c>=0 for row in coefficients for c in row)
                        writer.emit({"kind":"box","decoder":d,"level":level,"box":[i,j],"nonnegative":nonnegative,"checks":checks})
                        need(all(z[2]==z[3] for z in checks), "exact box Bernstein reconstruction")
                        levels[d][level].append(nonnegative)
                        counts["boxes"] += 1
                        completed.append(task)
        task,phase = ("classification",),"classification"
        attempted.append(task)
        for d in DETECTORS:
            full = [l for l in range(3) if len(levels[d][l])==4**l and all(levels[d][l])]
            need(not (full and negative[d]), "grid / whole-level certificate consistency")
            certificates[d] = {"status":"COUNTEREXAMPLE_TO_SQUARE_ONLY" if negative[d] else ("NONNEGATIVE_ON_WHOLE_SQUARE" if full else "INCONCLUSIVE"),"whole_levels":full,"negative_grid_points":negative[d],"physical_beta_curve_decided_by_negative_grid":False}
        need(completed+[task]==plan and len(plan)==78 and writer.rows==9612 and counts=={"coefficients":5670,"boxes":42,"bernstein_coefficients":3402,"grid":25}, "complete fixed finite population")
        completed.append(task)
    except Exception as exc:
        failure = {"phase":phase,"task":task,"exception":repr(exc),"traceback":traceback.format_exc()}
    summary = {"ENGINE_PASS":failure is None,"records":writer.rows,"counts":counts,"certificates":certificates if failure is None else "NOT_ACCEPTED_ENGINE_FAILURE","FAILED_TASK":[x for x in attempted if x not in completed],"NOT_RUN":[x for x in plan if x not in attempted],"polynomial_products":OPS[0],"peak_polynomial_terms":OPS[1],"native_calls":0,"RNG_draws":0,"optimizer_advantage":False,"physical_curve":"0<y<x<1; y=x^(2+sqrt(3))"}
    writer.finish(summary,failure)
    if failure is not None:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
