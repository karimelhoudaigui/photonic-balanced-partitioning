"""Recorded local release validation. No specs/run command or hardware client.

Use the pinned research Python and a fresh --output. Existing evidence is never
overwritten; stdout, stderr, exact commands and source hashes are preserved.
"""
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    sources = [ROOT / "src/photonic_balanced_partitioning/hardware/lucy_tgcc.py",
               ROOT / "src/photonic_balanced_partitioning/hardware/offline.py",
               ROOT / "tests/test_lucy_tgcc.py", ROOT / "paper/main.pdf"]
    sources += sorted((ROOT / "paper").rglob("*.tex"))
    before = {str(p.relative_to(ROOT)): sha(p) for p in sources}
    commands = [
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        [sys.executable, "scripts/check_archive_preservation.py"],
        [sys.executable, "scripts/build_publication.py", "--check"],
        [sys.executable, "scripts/verify_manuscript.py"],
        [sys.executable, "-m", "photonic_balanced_partitioning.hardware.lucy_tgcc", "environment"],
    ] + [[sys.executable, "-m", "photonic_balanced_partitioning.hardware.lucy_tgcc",
          "plan", "--circuit", circuit, "--output", str(output / (circuit + "-plan"))]
         for circuit in ("identity", "hom", "pair_mixing")]
    env = os.environ | {"PYTHONPATH": str(ROOT / "src"), "OPENBLAS_NUM_THREADS": "1",
                        "OMP_NUM_THREADS": "1", "MPLBACKEND": "Agg"}
    runs = []
    for index, command in enumerate(commands):
        stdout, stderr = output / f"command-{index}.stdout.txt", output / f"command-{index}.stderr.txt"
        started = time.monotonic()
        with stdout.open("x") as out, stderr.open("x") as err:
            proc = subprocess.run(command, cwd=ROOT, env=env, stdout=out, stderr=err, timeout=240)
        runs.append({"argv": command, "exit_code": proc.returncode,
                     "wall_seconds": time.monotonic() - started,
                     "stdout": stdout.name, "stderr": stderr.name,
                     "stdout_sha256": sha(stdout), "stderr_sha256": sha(stderr)})
        if proc.returncode:
            break
    after = {str(p.relative_to(ROOT)): sha(p) for p in sources}
    receipt = {"created_utc": datetime.now(timezone.utc).isoformat(),
               "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "source_before": before, "source_after": after,
               "sources_unchanged": before == after, "commands": runs,
               "status": "PASS" if len(runs) == len(commands) and all(r["exit_code"] == 0 for r in runs) and before == after else "FAIL",
               "scope": "Local tests, archive/publication checks and offline Lucy plans only",
               "tgcc_account_connection": False, "qpu_submission": False,
               "hardware_credits_consumed": 0}
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "commands": len(runs),
                      "sources_unchanged": before == after, "qpu_submission": False}))
    raise SystemExit(receipt["status"] != "PASS")


if __name__ == "__main__":
    main()
