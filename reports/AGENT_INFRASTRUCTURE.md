# Agent infrastructure audit — 2026-11-21

Detected on the actual host before installing Qwen/Ollama. No serial number or
machine UUID is retained. No existing application was stopped to free memory.

| Component | Observed |
|---|---|
| OS / architecture | macOS26.2, build25C56; Darwin25.2.0; arm64 |
| Machine | MacBook Air, Mac14,2 |
| CPU | Apple M2;8 physical/logical cores (4 performance+4 efficiency) |
| RAM |8GiB unified memory |
| GPU | Apple M2 integrated GPU; dedicated VRAM not reported; shares8GiB RAM |
| Swap at audit |24,576MiB allocated,23,373.94MiB used |
| Disk at audit |6,064,807,936 bytes free (~5.65GiB) |
| System Python |3.9.6 /Library/Developer/CommandLineTools/usr/bin/python3 |
| Scientific Python |3.11.15 .venv/bin/python;NumPy2.4.6,SciPy1.17.1 |
| Node.js |26.0.0 /opt/homebrew/bin/node |
| npm |11.12.1 /opt/homebrew/bin/npm |
| Homebrew |6.0.7 /opt/homebrew/bin/brew |
| Docker |CLI29.9.1 installed;daemon unavailable at /var/run/docker.sock |
| Ollama |Absent before installation |
| vLLM |Neither executable nor Python module detected;not chosen for this Apple GPU |
| Qwen Code |Absent before installation;official npm latest resolves0.28.0,Node>=22 |

Commands:uname -a;sw_vers;sysctl -n machdep.cpu.brand_string hw.memsize
hw.ncpu hw.physicalcpu hw.logicalcpu vm.swapusage;system_profiler
SPDisplaysDataType SPHardwareDataType -json (only nonidentifying fields retained);
vm_stat;shutil.disk_usage;command discovery and --version;docker info.
System inspection required sandbox escalation;these are observed values,not estimates.

Decision:one local inference request at a time,one active agent role at a time,
no resident model ensemble. Small bounded cycles;do not use paid/cloud fallback.
Ollama is suitable for Apple Silicon,subject to an actual load/tool smoke test.
The current pressure rules out calling any large local model comfortable.
Qwen installation,model operation,agent delegation and scientific validity are
separate gates;see QWEN_INFRASTRUCTURE_VALIDATION.md for executed evidence.

## Installed external tools

- `qwen --version`:0.28.0 (official npm @qwen-code/qwen-code@latest).
- `ollama` server `/api/version`:0.32.0 (Homebrew stable).
- Homebrew installed its own Python3.14.6,MLX0.32.0 and mlx-c0.6.0, and upgraded
  its OpenSSL/SQLite dependencies. The scientific .venv remains Python3.11.15.
- No daemon was registered to start at login. The cycle launcher starts a
  loopback-only server if needed;the validation server is temporary.
- Model store:.local/ollama/models (git-ignored). Qwen state:.local/qwen/home;
  the user's ~/.qwen provider settings and credentials are not overwritten.
- Docker remains unnecessary/unstarted. All macOS worker processes inherit an
  explicit sandbox-exec profile:write only in the assigned worktree/local runtime,
  manuscript writes denied,network only localhost:11435. No unconfined fallback.
- Initial native model tool-call probe passed. Full CLI/worker/team validation
  is reported separately;installation alone is not a PASS for these capabilities.
