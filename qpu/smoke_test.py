#!/usr/bin/env python3
"""The old smoke test ran locally while claiming hardware validation."""
def main():
    print("REFUSED: no hardware smoke test exists. Run pytest tests/test_hom.py locally.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
