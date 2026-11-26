"""P130 prospective exact few-loss qualification; no producer is imported."""
import argparse, hashlib, json, os, resource, sys, traceback
from fractions import Fraction as F
from itertools import combinations
from math import comb, factorial
from pathlib import Path

CAP, RESULT_CAP = 4194304, 65536
OUT = "research/P130_few_loss_main/run_001/data"
THREADS = ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS","BLIS_NUM_THREADS")
BASES = {"P96":"research/P96_column_loss_main/run_001","P107":"research/P107_symbolic_filter_main/run_001"}
SEALS = {"P96":"240c7e5518fbcd69d8f22bbe5e8ead3c1bbbc9c1","P107":"99f2d98d93f13c7fc088218bfb06ff39af4c40e9"}
SUFFIXES = ("manifest.json","stdout.txt","stderr.txt","data/records.jsonl","data/summary.json","data/failure.json")
STATIC = ("AGENTS.md","pyproject.toml","requirements-research-lock.txt",
 "research/P130_few_loss_validation.py","research/P130_population.md","research/P130_contract_TEMPLATE.json",
 "research/P126_FEW_LOSS_POSITIVE_SAMPLER_ROUTE.md","reports/P126_ROOT_FEW_LOSS_CHECKPOINT.md",
 "research/P96_column_loss_validation.py","research/P107_symbolic_filter_validation.py",
 "reports/P130_validation_review/reference_blob_bindings.json")
PINS = {"research/P126_FEW_LOSS_POSITIVE_SAMPLER_ROUTE.md":"7dd13002498e0e582be85e7a7b8636cdac97425409b964cb1db10b70720f4736",
 "research/P96_column_loss_validation.py":"ee3592ef608b0b7ad19ba81babcdc369bf4da50e319f3f00baf868074d83c223",
 "research/P107_symbolic_filter_validation.py":"4e0973ebfe8a250dbf012719087dcb0b7390932acd3ddab4e7055b3808cb2bbc"}
EXPECTED = {"cases":14,"sectors":39,"reference_bins":361,"top_states":327,"FAIL":14,"principal_minors":1468,"moments":59}

def require(test,message):
    if not test: raise ValueError(message)
def permanent(a):
    n = len(a)
    require(n<=4 and all(len(row)==n for row in a),"subset-DP permanent shape: "+repr(a))
    values = {0:F(1)}
    for row in a:
        following = {}
        for mask,weight in values.items():
            for j,v in enumerate(row):
                if (mask & (1<<j))==0:
                    key = mask|(1<<j)
                    following[key] = following.get(key,F(0))+weight*v
        values = following
    return values[(1<<n)-1]
def determinant(a):
    n = len(a)
    require(n<=6 and all(len(row)==n for row in a),"determinant shape: "+repr(a))
    work,answer = [list(row) for row in a],F(1)
    for j in range(n):
        pivot = next((i for i in range(j,n) if work[i][j]),None)
        if pivot is None: return F(0)
        if pivot!=j:
            work[pivot],work[j] = work[j],work[pivot]; answer = -answer
        diagonal = work[j][j]; answer *= diagonal
        for i in range(j+1,n):
            multiple = work[i][j]/diagonal
            for k in range(j+1,n): work[i][k] -= multiple*work[j][k]
            work[i][j] = F(0)
    return answer
def submatrix(a,rows,columns): return [[a[i][j] for j in columns] for i in rows]
def subsets(n): return [s for size in range(n+1) for s in combinations(range(n),size)]
def occupation(total,m):
    if m==1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in occupation(total-first,m-1): yield (first,)+tail
def alphabet(m,k): return [n for total in range(k+1) for n in occupation(total,m)]
def matrix(rows): return [[F(v) for v in row] for row in rows]
def catalog():
    cases = [("V0",[[]]),("U1",[["1/2"]]),
      ("D3",[["1/4",0,0],[0,"1/4",0],[0,0,"1/4"]]),
      ("R3a",[["1/4"]*3]),("R3b",[["1/8"]*3]),("B4",[["1/4"]*4]*2),
      ("D4",[["1/4" if i==j else 0 for j in range(4)] for i in range(4)]),
      ("Z4",[[0]*4]*2),("R4",[["1/4"]*4]),("C3",[["1/2",0,0],[0,"1/2",0]]),
      ("X4",[["1/2"]*4])]
    out = [(name,matrix(rows),"P96",name) for name,rows in cases]
    out += [("F0",[[F(1,4)]*4 for unused in range(4)],"P107",F(0)),
      ("Fhalf",[[F((9,3,1,3)[(j-i)%4],16) for j in range(4)] for i in range(4)],"P107",F(1,2)),
      ("F1",[[F(int(i==j)) for j in range(4)] for i in range(4)],"P107",F(1))]
    return out
def sha(path):
    with path.open("rb") as f: return hashlib.file_digest(f,"sha256").hexdigest()
def safe(root,name):
    p = Path(name)
    require(p.parts and not p.is_absolute() and p.as_posix()==name and all(v not in (".","..") for v in p.parts),"canonical relative input")
    cursor = root
    for part in p.parts:
        cursor /= part; require(not cursor.is_symlink(),"symlinked input")
    require(cursor.is_file(),"missing/nonregular input")
    return cursor
def load(path): return json.loads(path.read_text(encoding="ascii"),parse_float=F)
def hexadecimal(v,n): return isinstance(v,str) and len(v)==n and all(c in "0123456789abcdef" for c in v)
def authorize(root,name):
    b = load(safe(root,name))
    require(b["binding_state"]=="ROOT_AUTHORIZED" and b["run_authorized"] is True,"separate ROOT authority")
    require(b["reference_seals"]==SEALS,"two exact original reference seals")
    roles = {g:{r:base+"/data/"+r+".json"+("l" if r=="records" else "") for r in ("records","summary","failure")} for g,base in BASES.items()}
    require(b["reference_roles"]==roles,"exact reference roles")
    refs = {base+"/"+s for base in BASES.values() for s in SUFFIXES}
    rows = b["artifacts"]; table = {r["path"]:r for r in rows}
    require(len(rows)==len(table) and name not in table and set(STATIC)|refs<=set(table),"unique required descriptor closure")
    extra = set(table)-set(STATIC)-refs
    require(all((p.startswith("research/") or p.startswith("reports/")) and p.endswith((".md",".json")) and not any(p.startswith(v+"/") for v in BASES.values()) for p in extra),"only extra frozen review metadata")
    reference = b["artifacts_reference"]
    require(len(reference)==12 and {r["path"] for r in reference}==refs and all(r==table[r["path"]] for r in reference),"exact twelve reference descriptors")
    require(len(b["execution_artifacts"])==len(table)+1 and set(b["execution_artifacts"])==set(table)|{name},"active binding self-input")
    for p,row in table.items():
        f = safe(root,p)
        require(type(row["bytes"]) is int and row["bytes"]==f.stat().st_size and hexadecimal(row["sha256"],64) and sha(f)==row["sha256"],"descriptor hash/bytes")
        require(p not in PINS or row["sha256"]==PINS[p],"frozen source context")
    require(hexadecimal(b["source_sha256"],64) and sha(Path(__file__))==b["source_sha256"]==table[STATIC[3]]["sha256"],"actual source bytes")
    return b
def encode(v):
    if isinstance(v,F): return str(v)
    raise TypeError(type(v).__name__)
class Evidence:
    def __init__(self,path):
        require(path.parent.is_dir() and not path.parent.is_symlink() and not path.parent.parent.is_symlink() and not path.exists() and not path.is_symlink(),"fresh exclusive output child")
        path.mkdir(); self.path,self.bytes,self.rows = path,0,0
        self.f = (path/"records.jsonl").open("x",encoding="ascii")
    def emit(self,row):
        text = json.dumps(row,default=encode,sort_keys=True,allow_nan=False,separators=(",",":"))+"\n"
        require(self.bytes+len(text.encode("ascii"))<=CAP-RESULT_CAP,"aggregate science reserve")
        self.f.write(text); self.f.flush(); self.bytes += len(text.encode("ascii")); self.rows += 1
    def finish(self,summary,failure):
        self.f.close()
        payloads = [json.dumps(v,default=encode,sort_keys=True,allow_nan=False)+"\n" for v in (summary,failure)]
        size = sum(len(v.encode("ascii")) for v in payloads)
        require(size<=RESULT_CAP and self.bytes+size<=CAP,"final-result/scientific cap")
        for name,text in zip(("summary.json","failure.json"),payloads):
            with (self.path/name).open("x",encoding="ascii") as f: f.write(text)
def hands(writer):
    for name,a,ep,ed in (("empty",[],1,1),("two",[[1,2],[3,4]],10,-2),
                         ("pivot",[[0,1],[1,0]],1,-1),("singular",[[1,1],[1,1]],2,0)):
        p,d = permanent(matrix(a)),determinant(matrix(a))
        writer.emit({"kind":"algebra_hand","name":name,"matrix":a,"permanent":p,"determinant":d,"expected":[ep,ed]})
        require((p,d)==(ep,ed),"literal DP/determinant hand")
def reference96(root,writer,state,specs):
    base = BASES["P96"]; dimensions = {name:(len(a),len(a[0])) for name,a,group,key in specs if group=="P96"}
    dimensions.update(H2=(2,2),S3=(2,3))
    values,inputs,seen,audits = {},{},set(),{}
    with safe(root,base+"/data/records.jsonl").open(encoding="ascii") as f:
        for number,line in enumerate(f,1):
            if not any('"kind": "'+k+'"' in line for k in ("exact_case_start","exact_raw","exact_audit")): continue
            state["reference"] = {"group":"P96","line":number,"prefix":line[:12000]}
            r = json.loads(line,parse_float=F); name = r["case"]
            require(name in dimensions,"known P96 case")
            if r["kind"]=="exact_case_start":
                require(name not in inputs,"duplicate P96 input"); inputs[name] = matrix(r["T"])
                require((len(inputs[name]),len(inputs[name][0]))==dimensions[name],"P96 input dimensions")
                require(r["expected_domain"] is (name!="X4"),"original P96 domain annotation")
            elif r["kind"]=="exact_audit":
                require(name not in audits,"duplicate P96 audit"); audits[name] = r["status"]
            else:
                n = tuple(r["signal"]); key = name,n
                require(n in alphabet(*dimensions[name]) and key not in seen and r["loss"]==dimensions[name][1]-sum(n),"P96 full raw metadata")
                seen.add(key)
                if name not in ("H2","S3"): values[key] = F(r["p"]),F(r["q"])
    expected = {(name,n) for name,(m,k) in dimensions.items() for n in alphabet(m,k)}
    require(seen==expected and len(seen)==167 and set(inputs)==set(audits)==set(dimensions),"complete P96 reference metadata")
    require(all(any(v<0 for row in inputs[name] for v in row) for name in ("H2","S3")),"signed-input exclusions only")
    for name,a,group,key in specs:
        if group=="P96": require(inputs[name]==a,"same literal nonnegative P96 transfer")
    summary,failure = load(safe(root,base+"/data/summary.json")),load(safe(root,base+"/data/failure.json"))
    projection = {k:summary[k] for k in ("status","valid_cases","invalid_cases","exact_points","native_calls","native_calls_attempted")}
    writer.emit({"kind":"reference_completion","group":"P96","original_state":projection,"failure":failure,"metadata_bins":len(seen),"selected_bins":len(values),"excluded_signed":["H2","S3"],"legacy_X4_audit":audits["X4"]})
    require(projection=={"status":"FINITE_VALIDATION_PASS","valid_cases":12,"invalid_cases":1,"exact_points":167,"native_calls":159,"native_calls_attempted":159} and failure=={"status":"NO_FAILURE"},"complete original P96 engine")
    require(len(values)==151 and audits["X4"]=="EXPECTED_OUTSIDE_DOMAIN" and all(audits[n]=="EXACT_PASS" for n in dimensions if n!="X4"),"P96 physical comparison/legacy domain")
    return values
def reference107(root,writer,state):
    base = BASES["P107"]; values,points,lines = {},set(),0
    with safe(root,base+"/data/records.jsonl").open(encoding="ascii") as f:
        for number,line in enumerate(f,1):
            lines += 1
            if '"kind":"grid"' not in line: continue
            state["reference"] = {"group":"P107","line":number,"prefix":line[:12000]}
            r = json.loads(line,parse_float=F); x,y = map(F,r["point"])
            require((x,y) not in points,"duplicate P107 grid"); points.add((x,y))
            require([tuple(n) for n in r["occupation_order"]]==alphabet(4,4),"P107 dense occupation order")
            if x==y and x in (F(0),F(1,2),F(1)):
                require(len(r["B_probabilities"])==70,"P107 70-bin grid")
                for n,p in zip(alphabet(4,4),r["B_probabilities"]): values[x,n] = F(p)
    require(lines==9612 and points=={(F(i,4),F(j,4)) for i in range(5) for j in range(5)} and len(values)==210,"complete P107 selected reference")
    summary,failure = load(safe(root,base+"/data/summary.json")),load(safe(root,base+"/data/failure.json"))
    projection = {k:summary[k] for k in ("ENGINE_PASS","records","counts","FAILED_TASK","NOT_RUN")}
    writer.emit({"kind":"reference_completion","group":"P107","original_state":projection,"failure":failure,"grid_points":len(points),"selected_bins":len(values)})
    require(projection=={"ENGINE_PASS":True,"records":9612,"counts":{"coefficients":5670,"boxes":42,"bernstein_coefficients":3402,"grid":25},"FAILED_TASK":[],"NOT_RUN":[]} and failure is None,"complete original P107 engine")
    return values
def main():
    resource.setrlimit(resource.RLIMIT_FSIZE,(CAP,CAP)); resource.setrlimit(resource.RLIMIT_CPU,(60,60))
    parser = argparse.ArgumentParser(); parser.add_argument("--binding",required=True); args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    require(sys.version_info[:3]==(3,11,15) and all(os.environ.get(v)=="1" for v in THREADS),"persistent Python/thread profile")
    binding = authorize(root,args.binding); binding_sha = sha(safe(root,args.binding)); writer = Evidence(root/OUT)
    state,counts,mismatches,failure,done = {"phase":"initial"},{k:0 for k in EXPECTED},0,None,[]
    def observation(row,ok):
        nonlocal mismatches
        row["match"] = ok; state["last_observation"] = row; writer.emit(row)
        if not ok: mismatches += 1
    try:
        writer.emit({"kind":"provenance","source_sha256":binding["source_sha256"],"binding":args.binding,"binding_sha256":binding_sha,"reference_seals":SEALS,"reference_artifacts":binding["artifacts_reference"],"Python":sys.version,"environment":{v:os.environ.get(v) for v in THREADS}})
        state["phase"] = "algebra hands"; hands(writer); done.append("hands")
        specs = catalog(); state["phase"] = "sealed reference parsing"
        r96,r107 = reference96(root,writer,state,specs),reference107(root,writer,state)
        state.pop("reference",None); done.append("references")
        for name,a,group,key in specs:
            state.update(phase="reference bins",case=name)
            m,k = len(a),len(a[0]); support = alphabet(m,k); reference = {}
            for n in support:
                p = r96[key,n][0] if group=="P96" else r107[key,n]
                reference[n] = p
                writer.emit({"kind":"reference_bin","case":name,"signal":n,"p":p,"legacy_P96_surrogate_q":r96[key,n][1] if group=="P96" else None})
                counts["reference_bins"] += 1
            require(all(p>=0 for p in reference.values()) and sum(reference.values())==1,"complete normalized reference law")
            g = [[sum((a[j][i]*a[j][l] for j in range(m)),F(0)) for l in range(k)] for i in range(k)]
            h = [[F(int(i==j))-g[i][j] for j in range(k)] for i in range(k)]
            h_certificate = [(s,determinant(submatrix(h,s,s))) for s in subsets(k)]
            writer.emit({"kind":"case_context","case":name,"A":a,"G":g,"H":h,"H_principal_determinants":h_certificate,"r0":2})
            require(all(v>=0 for row in a for v in row) and all(v>=0 for s,v in h_certificate),"nonnegative physical contraction")
            state["phase"] = "binomial moments"; moments = {}
            for size in range(k+1):
                value = sum((permanent(submatrix(g,s,s)) for s in combinations(range(k),size)),F(0)); moments[size] = value
                expected = sum((p*comb(sum(n),size) for n,p in reference.items()),F(0))
                observation({"kind":"moment","case":name,"order":size,"Gram_sum":value,"reference_moment":expected},value==expected)
                counts["moments"] += 1
            top_mass = F(0)
            for r in range(min(2,k)+1):
                state.update(phase="sector context",lost=r); nphotons = k-r
                ss = list(combinations(range(k),nphotons)); complements = [tuple(i for i in range(k) if i not in s) for s in ss]
                loss = [[permanent(submatrix(h,u,v)) for v in complements] for u in complements]
                d = len(ss); complement = [[F(int(i==j))-loss[i][j] for j in range(d)] for i in range(d)]
                inverse = sum(((-1)**(l-nphotons)*comb(l,nphotons)*moments[l] for l in range(nphotons,k+1)),F(0))
                writer.emit({"kind":"sector_context","case":name,"lost":r,"N":nphotons,"subsets":ss,"lost_subsets":complements,"L":loss,"I_minus_L":complement,"Q":moments[nphotons],"P_inversion":inverse})
                require(d==comb(k,r) and all(loss[i][j]==loss[j][i] for i in range(d) for j in range(d)),"CF compression dimensions/symmetry")
                state["phase"] = "all principal minors"
                for label,operator in (("L",loss),("I_MINUS_L",complement)):
                    for s in subsets(d):
                        value = determinant(submatrix(operator,s,s))
                        writer.emit({"kind":"principal_minor","case":name,"lost":r,"operator":label,"indices":s,"determinant":value})
                        counts["principal_minors"] += 1
                        require(value>=0,"exact L/I-L PSD principal minor")
                total_p,total_q = F(0),F(0); state["phase"] = "state identities"
                for n in occupation(nphotons,m):
                    state["signal"] = n; rows = [j for j,count in enumerate(n) for unused in range(count)]
                    amplitudes = [permanent(submatrix(a,rows,s)) for s in ss]
                    norm = sum((x*x for x in amplitudes),F(0))
                    numerator = sum((amplitudes[i]*loss[i][j]*amplitudes[j] for i in range(d) for j in range(d)),F(0))
                    divisor = 1
                    for v in n: divisor *= factorial(v)
                    p,q = numerator/divisor,norm/divisor
                    ratio = numerator/norm if norm else F(0)
                    observation({"kind":"state_comparison","case":name,"lost":r,"signal":n,"a":amplitudes,"n_factorial":divisor,"numerator":numerator,"a_norm_squared":norm,"p":p,"q_P126":q,"Rayleigh":ratio,"reference":reference[n]},p==reference[n])
                    counts["top_states"] += 1
                    require(all(x>=0 for x in amplitudes) and 0<=p<=q and 0<=ratio<=1,"exact positive proposal/Rayleigh bounds")
                    total_p += p; total_q += q
                reference_p = sum((p for n,p in reference.items() if sum(n)==nphotons),F(0))
                observation({"kind":"sector_totals","case":name,"lost":r,"p_sum":total_p,"q_sum":total_q,"Q_Gram":moments[nphotons],"P_inversion":inverse,"P_reference":reference_p},total_p==inverse==reference_p and total_q==moments[nphotons])
                require(0<=total_p<=total_q<=comb(k,r),"sector domination/bound")
                counts["sectors"] += 1; top_mass += total_p
            state["phase"] = "coarse FAIL"
            tail = sum((p for n,p in reference.items() if sum(n)<max(0,k-2)),F(0))
            observation({"kind":"FAIL","case":name,"calculated":1-top_mass,"reference":tail,"top_mass":top_mass},1-top_mass==tail)
            require(0<=1-top_mass<=1,"physical aggregate FAIL")
            counts["FAIL"] += 1; counts["cases"] += 1; done.append(name)
        require(counts==EXPECTED and writer.rows==2328 and len(done)==16,"complete deterministic population")
        state["phase"] = "final input integrity"
        for row in binding["artifacts"]:
            f = safe(root,row["path"])
            observed = {"path":row["path"],"expected_sha256":row["sha256"],"observed_sha256":sha(f),"expected_bytes":row["bytes"],"observed_bytes":f.stat().st_size}
            state["input_check"] = observed
            require(observed["expected_sha256"]==observed["observed_sha256"] and observed["expected_bytes"]==observed["observed_bytes"],"bound input changed")
        state["input_check"] = {"path":args.binding,"expected_sha256":binding_sha,"observed_sha256":sha(safe(root,args.binding))}
        require(state["input_check"]["observed_sha256"]==binding_sha,"active binding changed")
    except Exception as exc: failure = {"state":state,"exception":repr(exc),"traceback":traceback.format_exc()}
    status = "INCONCLUSIVE_FIRST_FAILURE" if failure else ("EXACT_COMPARISON_FAILED" if mismatches else "EXACT_QUALIFICATION_PASS")
    writer.finish({"status":status,"counts":counts,"records":writer.rows,"completed":done,"mismatches":mismatches,"RNG_draws":0,"native_calls":0,"FPRAS_calls":0,"sampler_claim":False,"optimizer_advantage":False},failure)
    if status!="EXACT_QUALIFICATION_PASS": raise SystemExit(1)
if __name__=="__main__": main()
