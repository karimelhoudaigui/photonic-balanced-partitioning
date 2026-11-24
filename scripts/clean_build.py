"""Remove known build auxiliaries only. Experimental data are never targets."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    for suffix in ("aux", "bbl", "blg", "log", "out", "toc", "synctex.gz"):
        (ROOT / "paper" / ("main." + suffix)).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
