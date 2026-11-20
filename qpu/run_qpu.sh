#!/bin/bash
# QPU experiment runner script

set -e

if [ -z "$QPU_TOKEN" ]; then
    echo "ERROR: QPU_TOKEN not set"
    exit 1
fi

BACKEND=${1:-qpu:belenos}
CONFIG=${2:-qpu/configs/n4_smoke.yaml}

echo "Running QPU experiment..."
echo "Backend: $BACKEND"
echo "Config: $CONFIG"

python qpu/run_qpu.py --backend "$BACKEND" --config "$CONFIG"
