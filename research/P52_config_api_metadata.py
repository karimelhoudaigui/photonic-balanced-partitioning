"""Read-only exqalibur.Config class metadata; no instance or scientific call."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import resource
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    output = parser.parse_args().output
    if output.exists():
        raise ValueError("metadata output must be fresh")
    wall, cpu = time.monotonic(), time.process_time()
    import exqalibur as xq
    config = xq.Config  # class object only; do not instantiate or set anything
    names = dir(config)
    members = {}
    for name in names:
        if "thread" in name.lower() or "cpu" in name.lower():
            member = getattr(config, name)
            members[name] = {"type": type(member).__name__, "doc": getattr(member, "__doc__", None)}
    if any(name == "perceval" or name.startswith("perceval.") for name in sys.modules):
        raise AssertionError("unexpected Perceval import")
    binaries = {}
    for name, module in tuple(sys.modules.items()):
        path = getattr(module, "__file__", None)
        if name.startswith("exqalibur") and path:
            binaries[name] = {"path": path, "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()}
    result = {
        "scope": "read-only Config class docs/dir and thread/cpu member descriptors; no instance/setter/getter/permanent/Fock/Perceval call",
        "python": sys.version, "exqalibur_version": importlib.metadata.version("exqalibur"),
        "Config_doc": config.__doc__, "Config_dir": names, "thread_cpu_members": members,
        "files": binaries, "cpu_seconds": time.process_time() - cpu,
        "wall_seconds": time.monotonic() - wall,
        "maxrss_native": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "perceval_imported": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
