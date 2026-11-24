"""Compatibility entrypoint for the source-linked publication generator."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parents[2] / "scripts/build_publication.py"), run_name="__main__")
