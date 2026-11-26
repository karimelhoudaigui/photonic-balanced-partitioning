"""Second integration check after a diagnosed fixture-copy FSIZE failure."""
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT/"reports/P96_validation_review/local_suite_run002"
PROGRAM = (
    "import exqalibur as xq; xq.Config.compute_max_thread_count=1; "
    "assert xq.Config.compute_max_thread_count==1; import pytest; "
    "status=pytest.main(['tests/','-q','-p','no:cacheprovider']); "
    "assert xq.Config.compute_max_thread_count==1; raise SystemExit(status)"
)


def child_limits():
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_FSIZE, (33554432, 33554432))


if __name__ == "__main__":
    OUTPUT.mkdir(exist_ok=False)
    environment = os.environ.copy()
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
        environment[key] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = [sys.executable, "-B", "-c", PROGRAM]
    begin = time.perf_counter()
    timeout = False
    with (OUTPUT/"stdout.txt").open("xb") as stdout, (OUTPUT/"stderr.txt").open("xb") as stderr:
        process = subprocess.Popen(argv, cwd=ROOT, env=environment,
            stdout=stdout, stderr=stderr, start_new_session=True, preexec_fn=child_limits)
        try:
            status = process.wait(timeout=180)
        except subprocess.TimeoutExpired:
            timeout = True
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
            status = process.wait()
    record = {"git_commit": subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(), "argv": argv, "exit_status": status, "timeout": timeout,
        "wall_seconds": time.perf_counter()-begin, "wall_limit_seconds": 180,
        "per_process_CPU_limit_seconds": 120, "environment_threads": 1,
        "native_configuration_before_and_after": 1 if status == 0 else None,
        "log_bytes": sum((OUTPUT/name).stat().st_size for name in ("stdout.txt", "stderr.txt")),
        "expected_items": 1559, "per_regular_file_limit_bytes": 33554432,
        "scope": "Complete integration tests including11 P96 pure fixtures; repeated old qualified fixtures, no P96 native main, DEV optimizer or real QPU call. Test-suite limits are separate from scientific CPU60/WALL90."}
    with (OUTPUT/"execution.json").open("x") as stream:
        json.dump(record, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"exit_status": status, "timeout": timeout, "raw_logs": str(OUTPUT)}))
    raise SystemExit(status if status >= 0 else 1)
