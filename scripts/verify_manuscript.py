"""Check the compiled manuscript, references and source inventory without TeX."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from pypdf import PdfReader


def verify(root: Path) -> dict:
    paper = root / "paper"
    pdf, log = paper / "main.pdf", paper / "main.log"
    sources = (sorted(paper.rglob("*.tex"))
               + sorted((paper / "figures").glob("*.pdf"))
               + [paper / "references.bib", paper / "publication_manifest.json"])
    if not pdf.is_file() or not log.is_file():
        raise ValueError("Compile paper/main.tex with --keep-logs first")
    log_text = log.read_text(errors="replace")
    failures = []
    if any(p.stat().st_mtime_ns > pdf.stat().st_mtime_ns for p in sources):
        failures.append("Manuscript input newer than PDF; recompile before verification")
    for pattern in (
        r"(?:Reference|Citation) .+? undefined",
        r"There were undefined references",
        r"LaTeX Error:",
        r"Missing character:",
        r"multiply defined",
    ):
        if re.search(pattern, log_text, re.I):
            failures.append("TeX diagnostic: " + pattern)
    overfull = [float(x) for x in re.findall(r"Overfull \\[hv]box \(([0-9.]+)pt", log_text)]
    if any(x > 1 for x in overfull):
        failures.append("Overfull TeX box larger than one point")
    bib = (paper / "references.bib").read_text()
    keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib))
    citations = set()
    for source in sources:
        if source.suffix != ".tex":
            continue
        text = source.read_text()
        for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", text):
            citations.update(k.strip() for k in group.split(","))
        for name in re.findall(r"\\(?:input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}", text):
            p = paper / name
            if not any(q.is_file() for q in (p, p.with_suffix(".tex"), p.with_suffix(".pdf"))):
                failures.append(f"Missing input or graphic: {name}")
    if citations - keys:
        failures.append("Missing bibliography keys: " + ", ".join(sorted(citations - keys)))
    reader = PdfReader(pdf)
    page_text = [p.extract_text() or "" for p in reader.pages]
    if len(reader.pages) < 8 or sum(map(len, page_text)) < 15000:
        failures.append("Unexpectedly short or empty manuscript PDF")
    if any("??" in t for t in page_text):
        failures.append("Unresolved question-mark reference in PDF text")
    if any(not t.strip() for t in page_text):
        failures.append("Blank or unextractable PDF page")
    hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sources}
    result = {
        "status": "FAIL" if failures else "PASS",
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "pdf_pages": len(reader.pages),
        "pdf_extracted_characters": sum(map(len, page_text)),
        "source_sha256": hashes,
        "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
        "bibliography_keys_cited": sorted(citations),
        "overfull_box_points": overfull,
        "failures": failures,
        "scope": "Build and reference checks, not mathematical correctness or publication readiness",
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = verify(args.root.resolve())
    if args.receipt:
        if args.receipt.exists():
            raise FileExistsError("Use a new receipt path to preserve earlier validation")
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "source_sha256"}))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
