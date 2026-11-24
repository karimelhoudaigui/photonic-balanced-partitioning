"""The checked PDF must follow the supplied source, not just exist."""
import importlib.util
import os
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("manuscript_verify", ROOT / "scripts/verify_manuscript.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def test_changed_source_invalidates_an_existing_compiled_pdf(tmp_path):
    shutil.copytree(ROOT / "paper", tmp_path / "paper")
    (tmp_path / "paper/main.log").write_text(
        "Synthetic log for the file-age regression fixture; no compilation is claimed.\n"
    )
    pdf = tmp_path / "paper/main.pdf"
    # A fresh checkout may have arbitrary file times; emulate a finished build.
    latest = max(p.stat().st_mtime_ns for p in (tmp_path / "paper").rglob("*") if p.is_file())
    os.utime(pdf, ns=(latest + 1_000_000, latest + 1_000_000))
    assert check.verify(tmp_path)["status"] == "PASS"
    source = tmp_path / "paper/sections/02_model.tex"
    source.write_text(source.read_text() + "\n% changed scientific source\n")
    os.utime(source, ns=(latest + 2_000_000, latest + 2_000_000))
    result = check.verify(tmp_path)
    assert result["status"] == "FAIL"
    assert any("newer than PDF" in failure for failure in result["failures"])
