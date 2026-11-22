#!/bin/sh
set -eu
if [ "$#" -ne 1 ]; then
  echo 'Expected exactly one fixed density job mode' >&2
  exit 64
fi
case "$1" in primary|replication|audit-primary|audit-pair) ;; *) exit 64 ;; esac
: "${PASQAL_PYTHON:?Use the controlled project launcher}"
qwen_density_script_dir=$(dirname "$0")
exec "$PASQAL_PYTHON" "$qwen_density_script_dir/qwen_density_job.py" "$1"
