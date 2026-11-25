"""Exact balanced minimum photon-imbalance decoding, with no graph or sampler.

Every input returns a uniform minimizer when sample() receives an exact
uniform arbitrary-integer randbelow oracle. No physical shot is rejected.
"""
from numbers import Integral

MAX_VERTICES = 128
MAX_TOTAL = 4096
MAX_CELLS = 2_000_000


class NeutralityDecoder:
    """Count all minimizers, then unrank one integer in [0, ways).

    Bounds are prototype resource bounds, not postselection criteria. A caller
    must preserve an out-of-domain failure instead of resampling a shot.
    Counts may sum above N, e.g. for the independent-marginal classical null.
    """

    def __init__(self, counts):
        counts = tuple(counts)
        if any(isinstance(x, bool) or not isinstance(x, Integral) for x in counts):
            raise TypeError("Nonnegative integer multiplicities are required")
        counts = tuple(int(x) for x in counts)
        n, total = len(counts), sum(counts)
        if n < 2 or n % 2 or n > MAX_VERTICES or any(x < 0 for x in counts):
            raise ValueError("Prototype requires even 2<=N<=128 and nonnegative counts")
        k = n // 2
        cells = (n + 1) * (k + 1) * (total + 1)
        if total > MAX_TOTAL or cells > MAX_CELLS:
            raise ValueError("Prototype DP resource bound exceeded before allocation")
        self.counts, self.n, self.k, self.total, self.cells = counts, n, k, total, cells
        initial = [[0] * (total + 1) for _ in range(k + 1)]
        initial[0][0] = 1
        tables = [initial]
        for i, value in enumerate(counts, start=1):
            previous = tables[-1]
            current = [[0] * (total + 1) for _ in range(k + 1)]
            for chosen in range(min(i, k) + 1):
                for photons in range(total + 1):
                    include = (previous[chosen - 1][photons - value]
                               if chosen and photons >= value else 0)
                    current[chosen][photons] = previous[chosen][photons] + include
            tables.append(current)
        last = tables[-1][k]
        available = [s for s, ways in enumerate(last) if ways]
        if not available:
            raise ArithmeticError("Balanced subsets unexpectedly missing")
        self.minimum_imbalance = min(abs(2 * s - total) for s in available)
        self.target_sums = tuple(s for s in available if abs(2 * s - total) == self.minimum_imbalance)
        self.target_ways = tuple(last[s] for s in self.target_sums)
        self.ways = sum(self.target_ways)
        self._tables = tables

    def unrank(self, rank):
        """Bijection from all exact ranks to all minimum-imbalance K-subsets."""
        if isinstance(rank, bool) or not isinstance(rank, Integral):
            raise TypeError("The exact rank must be an integer")
        rank = int(rank)
        if not 0 <= rank < self.ways:
            raise ValueError("Rank outside the complete minimizer set")
        for photons, ways in zip(self.target_sums, self.target_ways):
            if rank < ways:
                break
            rank -= ways
        else:
            raise ArithmeticError("Target-sum unranking failed")
        chosen, selected = self.k, []
        for i in range(self.n, 0, -1):
            exclude = self._tables[i - 1][chosen][photons]
            if rank < exclude:
                continue
            rank -= exclude
            value = self.counts[i - 1]
            if chosen == 0 or photons < value:
                raise ArithmeticError("Impossible inclusion branch")
            include = self._tables[i - 1][chosen - 1][photons - value]
            if not 0 <= rank < include:
                raise ArithmeticError("Inclusion rank outside its count block")
            selected.append(i - 1)
            chosen -= 1
            photons -= value
        if chosen or photons or rank:
            raise ArithmeticError("Incomplete exact unranking")
        return tuple(reversed(selected))

    def sample(self, randbelow):
        """Use ONE uniform integer; target sums get weights proportional to ways.

        The injected oracle must support arbitrarily large bounds. Its internal
        random-bit rejection is not rejection of physical photon attempts.
        """
        if not callable(randbelow):
            raise TypeError("An exact uniform randbelow oracle is required")
        return self.unrank(randbelow(self.ways))
