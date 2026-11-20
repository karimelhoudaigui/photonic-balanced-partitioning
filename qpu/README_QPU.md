# QPU Experiment Guide for Laurent

## Quick Start

```bash
git clone <repo-url>
cd photonic-balanced-partitioning
python -m venv .venv
source .venv/bin/activate
pip install -r qpu/requirements_qpu.txt
python qpu/check_environment.py
python qpu/check_backend.py
python qpu/smoke_test.py
python qpu/run_qpu.py --backend qpu:belenos --config qpu/configs/n4_smoke.yaml
```

## Environment Setup

### Requirements
- Python 3.11+
- Quandela Perceval package
- QPU access token (set in `QPU_TOKEN` environment variable)

### Install QPU Dependencies
```bash
pip install -r qpu/requirements_qpu.txt
```

## Backend Configuration

### Belenos (Quandela QPU)
```bash
export QPU_TOKEN="your-token-here"
python qpu/check_backend.py --backend qpu:belenos
```

### Local Simulator
```bash
python qpu/run_qpu.py --backend sim:ideal --config qpu/configs/n4_smoke.yaml
```

## Experiment Stages

### Stage 0: Connectivity Check
```bash
python qpu/check_backend.py --backend qpu:belenos
```

### Stage 1: Smallest Physical Smoke Test
```bash
python qpu/run_qpu.py --backend qpu:belenos --config qpu/configs/n4_smoke.yaml
```

### Stage 2: Replicated n=4
```bash
python qpu/run_qpu.py --backend qpu:belenos --config qpu/configs/n4_full.yaml
```

### Stage 3: n=6
```bash
python qpu/run_qpu.py --backend qpu:belenos --config qpu/configs/n6.yaml
```

## Output Location

Results are saved to:
```
results/qpu/<timestamp>_<run_id>/
```

Contents:
- `config.yaml` - Experiment configuration
- `git_commit.txt` - Git commit hash
- `environment.txt` - Python environment
- `backend_metadata.json` - Backend info
- `raw_samples.json` - Raw QPU samples
- `processed_results.json` - Processed results
- `stdout.log` - Execution log
- `analysis.json` - Analysis results

## Shots and Jobs

- n=4 smoke: ~100 shots, 1 job
- n=4 full: ~1000 shots, 1 job
- n=6: ~1000 shots, 1 job

## Resume Interrupted Runs

```bash
python qpu/run_qpu.py --backend qpu:belenos --config qpu/configs/n4_smoke.yaml --resume <run_id>
```

## Where to Put Token

Set the environment variable:
```bash
export QPU_TOKEN="your-quandela-token"
```

Or create a `.env` file:
```
QPU_TOKEN=your-quandela-token
```
