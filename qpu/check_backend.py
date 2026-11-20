#!/usr/bin/env python3
"""Never report simulated connectivity as a verified backend connection."""
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", default="qpu:belenos")
    args = parser.parse_args()
    print(f"UNVERIFIED: {args.backend}. No network connection attempted; hardware gate closed.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
