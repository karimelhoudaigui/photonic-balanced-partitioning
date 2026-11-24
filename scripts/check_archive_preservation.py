"""Compare historical scientific inputs with the pre-edit recovery snapshot."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    snapshot = root / "reports/recovery_2026-11-24/initial_state.json"
    initial = json.loads(snapshot.read_text())
    rows = [r for r in initial["files"] if Path(r["path"]).parts[0] in
            {"experiments", "results", "theory", "research"}]
    failures = []
    for row in rows:
        path = root / row["path"]
        if not path.is_file() or digest(path) != row["sha256"]:
            failures.append(row["path"])
    result = {"status": "FAIL" if failures else "PASS",
              "snapshot_sha256": digest(snapshot),
              "snapshot_base_commit": initial["base_commit"],
              "historical_files_checked": len(rows),
              "changed_or_missing": failures,
              "scope": "Pre-existing experiments/results/theory/research; active reports/manuscript/code may change"}
    if args.receipt:
        if args.receipt.exists():
            raise FileExistsError("Use a fresh receipt path")
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
