"""Boundary-cut and transported-label checks; no DEV graphs or optical calls."""
import importlib.util
from itertools import combinations, product
from pathlib import Path


def load_driver():
    path = Path(__file__).resolve().parents[1] / 'research/P145_run_declared_screen.py'
    spec = importlib.util.spec_from_file_location('p145_driver_hand', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EDGES = [(0, 12, 3), (1, 14, 2), (0, 1, 4), (12, 13, 5),
         (2, 7, 2), (13, 20, 6), (7, 20, 1)]


def independent_cut(edges, selected):
    return sum(w * abs(int(a in selected) - int(b in selected)) for a, b, w in edges)


def test_boundary_fields_reconstruct_all20_feasible_cut_changes():
    driver = load_driver()
    current, block = set(range(12)), [0, 1, 2, 12, 13, 14]
    a, h = driver.features(EDGES, current, block)
    assert h == [0, 0, -2, 0, 6, 0]
    def objective(support):
        return sum(sum(a[i]) + h[i] for i in support) - 2 * sum(a[i][j] for i, j in combinations(support, 2))
    for support in combinations(range(6), 3):
        target = (current - set(block[:3])) | {block[i] for i in support}
        assert independent_cut(EDGES, target) - independent_cut(EDGES, current) == objective(support) - objective((0, 1, 2))


def test_public_and_paid_block_rules_transport_under_relabeling():
    driver = load_driver()
    marks, current = list(range(24)), set(range(12))
    value = independent_cut(EDGES, current)
    neighbors = [{'remove': i, 'add': j,
                  'delta': independent_cut(EDGES, (current - {i}) | {j}) - value}
                 for i, j in product(range(12), range(12, 24))]
    mapping = {i: (7 * i + 5) % 24 for i in range(24)}
    edges2 = [(mapping[i], mapping[j], w) for i, j, w in EDGES]
    marks2, current2 = [mapping[i] for i in marks], {mapping[i] for i in current}
    neighbors2 = [{**row, 'remove': mapping[row['remove']], 'add': mapping[row['add']]} for row in neighbors]
    first, second = driver.blocks(current, marks, neighbors), driver.blocks(current2, marks2, neighbors2)
    for (rule, block), (rule2, block2) in zip(first, second):
        assert rule == rule2 and block2 == [mapping[i] for i in block]
        assert driver.features(EDGES, current, block) == driver.features(edges2, current2, block2)
