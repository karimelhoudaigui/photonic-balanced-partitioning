"""Passive adjacent-mode meshes; no device access or implicit postselection."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class RectangularMesh:
    """Alternating adjacent two-mode layers with phase-controlled rotations.

    depth=n has the rectangular Clements topology. This is a parametrization,
    not an implementation of the Clements synthesis algorithm. Each gate is
    D(phi/2) R(theta) D(-phi/2), realizable with phases and a beamsplitter.
    Input diagonal phases complete the U(n) parametrization; Fock output
    probabilities are insensitive to those final input phases.
    """
    n: int
    depth: int | None = None

    def __post_init__(self):
        if self.n < 2 or (self.depth is not None and self.depth < 1):
            raise ValueError("Require n>=2 and positive depth")

    @property
    def pairs(self):
        return tuple((a, a + 1) for layer in range(self.depth or self.n)
                     for a in range(layer % 2, self.n - 1, 2))

    @property
    def num_parameters(self):
        return 2 * len(self.pairs) + self.n

    @staticmethod
    def gate(theta, phi):
        c, s = np.cos(theta), np.sin(theta)
        return np.array([[c, -np.exp(1j * phi) * s],
                         [np.exp(-1j * phi) * s, c]], dtype=complex)

    def unitary(self, parameters, anchor=None):
        p = np.asarray(parameters, dtype=float)
        if p.shape != (self.num_parameters,) or not np.all(np.isfinite(p)):
            raise ValueError("Wrong mesh parameter shape or nonfinite values")
        U = np.diag(np.exp(1j * p[-self.n:]))
        for idx, (a, b) in enumerate(self.pairs):
            U[[a, b], :] = self.gate(*p[2*idx:2*idx+2]) @ U[[a, b], :]
        return U if anchor is None else U @ anchor

    def to_perceval(self, parameters):
        """Export the identical gate sequence to a local Perceval circuit."""
        import perceval as pcvl
        p = np.asarray(parameters, dtype=float)
        self.unitary(p)  # validates shape
        circuit = pcvl.Circuit(self.n)
        for a, phase in enumerate(p[-self.n:]):
            circuit.add(a, pcvl.PS(float(phase)))
        for idx, pair in enumerate(self.pairs):
            circuit.add(pair, pcvl.Unitary(pcvl.Matrix(self.gate(*p[2*idx:2*idx+2]))))
        return circuit


def partition_permutation(n, partition):
    """Route the first k input photons to a supplied partition.

    Discovering that partition is a CLASSICAL cost; this routine cannot solve
    an unknown graph. It is the oracle/anchor control, never a quantum gain.
    """
    part = tuple(partition)
    if len(set(part)) != len(part) or any(i < 0 or i >= n for i in part):
        raise ValueError("Invalid partition")
    outputs = part + tuple(i for i in range(n) if i not in part)
    return np.eye(n, dtype=complex)[:, outputs].T.conj().T
