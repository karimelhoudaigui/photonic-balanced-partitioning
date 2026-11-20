#!/usr/bin/env python3
"""Fail closed: the previous implementation silently simulated QPU jobs."""
import argparse


def main():
    parser = argparse.ArgumentParser(description="Hardware runner disabled pending scientific gates")
    parser.add_argument("--backend", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--resume")
    args = parser.parse_args()
    print(f"REFUSED: {args.backend}. No hardware execution is implemented or authorized.")
    print("See reports/QPU_READINESS.md. Ideal simulation: experiments/run_research.py.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
