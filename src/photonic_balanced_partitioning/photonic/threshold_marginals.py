"""Known fixed-rank vacuum marginals, evaluated with exact Gaussian rationals.

Distinct singly occupied input columns only. See phase3_threshold_lowrank.md.
This computes threshold moments, not a complete-output sampler. Encoding a
binary floating matrix exactly does not certify an unknown physical unitary.
"""
from dataclasses import dataclass
from fractions import Fraction
import math
from numbers import Integral


def _real(value):
    if isinstance(value,Fraction):return value
    if isinstance(value,Integral):return Fraction(int(value))
    raise TypeError('Use integers/Fraction; encode_binary_frame explicitly for binary floating entries')


@dataclass(frozen=True)
class GaussianRational:
    real: Fraction = Fraction(0)
    imag: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self,'real',_real(self.real))
        object.__setattr__(self,'imag',_real(self.imag))

    def conjugate(self):return GaussianRational(self.real,-self.imag)

    def __add__(self,other):
        other=_gaussian(other);return GaussianRational(self.real+other.real,self.imag+other.imag)

    __radd__=__add__

    def __neg__(self):return GaussianRational(-self.real,-self.imag)

    def __sub__(self,other):return self+-_gaussian(other)

    def __mul__(self,other):
        other=_gaussian(other)
        return GaussianRational(self.real*other.real-self.imag*other.imag,
                                self.real*other.imag+self.imag*other.real)

    __rmul__=__mul__

    def __complex__(self):return complex(float(self.real),float(self.imag))


def _gaussian(value):
    return value if isinstance(value,GaussianRational) else GaussianRational(_real(value))


def encode_binary_frame(frame):
    """Exactly encode the supplied finite binary64 entries, without physical validation."""
    result=[]
    for row in frame:
        encoded=[]
        for value in row:
            z=complex(value)
            if not math.isfinite(z.real) or not math.isfinite(z.imag):
                raise ValueError('Binary entries must be finite')
            encoded.append(GaussianRational(Fraction.from_float(z.real),Fraction.from_float(z.imag)))
        result.append(encoded)
    return result


@dataclass
class MarginalStats:
    """Recorded DP work; bit sizes scan stage coefficients/results, not all temporaries."""
    calls: int = 0
    cache_hits: int = 0
    state_visits: int = 0
    transitions: int = 0
    peak_states: int = 0
    max_integer_bits: int = 0


def vacuum_probability(rows,*,stats=None,max_states=100000,max_transitions=10000000):
    """Evaluate per(I-V*V) for 0,1,2 selected rows via a known coefficient DP.

    Integer coefficients have a common denominator at each stage. No clipping
    or float cancellation occurs. The rows alone do not establish that a full
    physical frame exists; ThresholdMarginals validates the complete frame.
    """
    v=[[_gaussian(x) for x in row] for row in rows];r=len(v)
    if r>2:raise ValueError('This implementation supports at most two output rows')
    if r and any(len(row)!=len(v[0]) for row in v):raise ValueError('Ragged rows')
    if max_states<1 or max_transitions<0:raise ValueError('Nonnegative resource limits required')
    counter=stats if stats is not None else MarginalStats();counter.calls+=1
    n=len(v[0]) if r else 0
    if r==0 or n==0:return Fraction(1)
    denominator=1
    for row in v:
        for z in row:denominator=math.lcm(denominator,z.real.denominator,z.imag.denominator)
    integers=[[(int(z.real*denominator),int(z.imag*denominator)) for z in row] for row in v]
    square=denominator**2;zero=(0,)*(2*r);coefficients={zero:(1,0)};transitions=0
    for column in range(n):
        following={key:(a*square,b*square) for key,(a,b) in coefficients.items()}
        terms=[]
        for a in range(r):
            ar,ai=integers[a][column]
            for b in range(r):
                br,bi=integers[b][column]
                real,imag=ar*br+ai*bi,ar*bi-ai*br
                if real or imag:terms.append((a,b,real,imag))
        counter.state_visits+=len(coefficients)
        for key,(cr,ci) in coefficients.items():
            for a,b,real,imag in terms:
                transitions+=1;counter.transitions+=1
                if transitions>max_transitions:raise RuntimeError('Exact marginal transition budget exceeded')
                target=list(key);target[a]+=1;target[r+b]+=1;target=tuple(target)
                old_r,old_i=following.get(target,(0,0))
                following[target]=(old_r-real*cr+imag*ci,old_i-real*ci-imag*cr)
                if len(following)>max_states:raise RuntimeError('Exact marginal state budget exceeded')
        coefficients={key:z for key,z in following.items() if z!=(0,0)}
        counter.peak_states=max(counter.peak_states,len(following))
        counter.max_integer_bits=max(counter.max_integer_bits,
            max((max(abs(a).bit_length(),abs(b).bit_length()) for a,b in following.values()),default=0))
    numerator=imaginary=0
    for key,(real,imag) in coefficients.items():
        if key[:r]!=key[r:]:continue
        weight=math.prod(math.factorial(x) for x in key[:r])
        numerator+=weight*real;imaginary+=weight*imag
    if imaginary:raise ArithmeticError('Exact diagonal extraction must be real')
    final_denominator=denominator**(2*n)
    counter.max_integer_bits=max(counter.max_integer_bits,abs(numerator).bit_length(),final_denominator.bit_length())
    return Fraction(numerator,final_denominator)


class ThresholdMarginals:
    """Exact threshold moments of distinct-input Fock states from a supplied frame.

    Default validation is exact, including complex orthogonality. With validation
    disabled this evaluates formal polynomials of encoded entries only. That
    mode carries no physical-probability or numerical-input error guarantee.
    """
    def __init__(self,frame,*,check_orthonormal=True,max_states=100000,max_transitions=10000000):
        self.frame=tuple(tuple(_gaussian(z) for z in row) for row in frame)
        self.m=len(self.frame);self.n=len(self.frame[0]) if self.m else 0
        if any(len(row)!=self.n for row in self.frame) or self.n>self.m:
            raise ValueError('Expected rectangular m-by-N frame with N<=m')
        if check_orthonormal:
            for a in range(self.n):
                for b in range(self.n):
                    inner=sum((row[a].conjugate()*row[b] for row in self.frame),GaussianRational())
                    if inner!=GaussianRational(int(a==b)):raise ValueError('Frame is not exactly orthonormal')
        self.physical_input_validated=bool(check_orthonormal)
        self.input_semantics=('EXACT_ORTHONORMAL_RATIONAL_FRAME' if check_orthonormal else
                              'FORMAL_POLYNOMIAL_ONLY_UNVALIDATED_FRAME')
        self.stats=MarginalStats();self._cache={}
        self.max_states=max_states;self.max_transitions=max_transitions

    def vacuum(self,indices):
        indices=tuple(sorted(indices))
        if len(set(indices))!=len(indices) or len(indices)>2 or any(not isinstance(i,Integral) or not 0<=i<self.m for i in indices):
            raise ValueError('Expected at most two distinct valid output indices')
        if indices in self._cache:
            self.stats.cache_hits+=1;return self._cache[indices]
        result=vacuum_probability([self.frame[i] for i in indices],stats=self.stats,
            max_states=self.max_states,max_transitions=self.max_transitions)
        if self.physical_input_validated and not 0<=result<=1:
            raise ArithmeticError('Physical vacuum probability is outside [0,1]')
        self._cache[indices]=result;return result

    def click_means(self):return [1-self.vacuum((i,)) for i in range(self.m)]

    def pair_moments(self):
        means=self.click_means();result=[[Fraction(0) for _ in range(self.m)] for _ in range(self.m)]
        for i in range(self.m):
            result[i][i]=means[i]
            for j in range(i+1,self.m):
                result[i][j]=result[j][i]=1-self.vacuum((i,))-self.vacuum((j,))+self.vacuum((i,j))
        return result

    def qubo_expectation(self,qubo):
        q=[[_real(x) for x in row] for row in qubo]
        if len(q)!=self.m or any(len(row)!=self.m for row in q):raise ValueError('QUBO shape mismatch')
        if any(q[i][j]!=q[j][i] for i in range(self.m) for j in range(self.m)):
            raise ValueError('Expected real symmetric QUBO; off-diagonal factor is two')
        means=self.click_means();value=sum((q[i][i]*means[i] for i in range(self.m)),Fraction(0))
        for i in range(self.m):
            for j in range(i+1,self.m):
                if q[i][j]:value+=2*q[i][j]*(1-self.vacuum((i,))-self.vacuum((j,))+self.vacuum((i,j)))
        return value
