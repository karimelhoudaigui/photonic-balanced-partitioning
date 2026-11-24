"""Package committed paper sources and an offline-capable Laurent/Lucy dossier.

This is an archive operation: no installation, client creation or submission.
Existing output directories are refused; all ZIP entries come from Git blobs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-24"
PACKET_NOTE = """# Dossier Laurent — Lucy via TGCC

Commencer par docs/LUCY_TGCC.md et paper/main.pdf.
Le dossier contient le code Python, le pilote figé, deux fichiers de tests
matériels locaux, les sources de l'article et les données sélectionnées.
Il n'inclut pas tout l'historique Git ni toutes les campagnes antérieures.
Le dépôt complet reste la référence pour les 505 tests et la réconciliation :
https://github.com/karimelhoudaigui/photonic-balanced-partitioning

Installation locale : suivre README.md. Contrôle propre à ce dossier :
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python -m pytest tests/test_hardware_offline.py tests/test_lucy_tgcc.py -q

Sur TGCC, utiliser les bibliothèques du conteneur ccc-quantum sans les remplacer
par le lock local. PYTHONPATH=src suffit pour charger le code du dossier.
La commande environment et la préparation plan sont hors ligne.
L'acquisition exige une autorisation opérateur distincte et les contrôles réels.
Aucun résultat QPU n'est inclus ; tous les counts locaux sont synthétiques.
L'absence de .git est enregistrée comme métadonnée de commit indisponible.
Conserver le manifeste de ce dossier pour identifier son commit source.
"""


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def package(commit, output):
    commit = git("rev-parse", "--verify", commit + "^{commit}").decode().strip()
    output.mkdir(parents=True, exist_ok=False)
    paper = output / f"ARTICLE_LATEX_{DATE}.zip"
    packet = output / f"DOSSIER_LAURENT_LUCY_{DATE}_v2.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip",
                    "--output=" + str(paper), commit, "paper"], check=True)
    tracked = git("ls-tree", "-r", "--name-only", commit).decode().splitlines()
    prefixes = ("src/", "qpu/", "paper/", "docs/", "results/validated/recovery_2026-11-24/",
                "results/validated/P40_sharpness_pilot_2026-11-24/",
                "results/P33_density_supervised/20261122T014822Z/", "experiments/P37_loss_source/run/")
    explicit = {"README.md", "AGENTS.md", "LAURENT_HANDOFF.md", "pyproject.toml",
                "requirements-research-lock.txt", "STATUS.md", "CLAIMS.md", "NEGATIVE_RESULTS.md",
                "results/README.md", "tests/test_hardware_offline.py", "tests/test_lucy_tgcc.py",
                "reports/LUCY_TGCC_DELIVERY.md", "reports/QPU_READINESS.md",
                "reports/PUBLICATION_READINESS.md", "reports/PUBLICATION_THESIS.md",
                "reports/SCIENTIFIC_INTEGRITY_AUDIT.md", "reports/NUMERICAL_RECONCILIATION.md",
                "reports/lucy_tgcc_2026-11-24/validation/receipt.json",
                "theory/phase3_density_certificate.md", "theory/phase3_loss_source_selection.md"}
    selected = sorted(p for p in tracked if p.startswith(prefixes) or p in explicit)
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip",
                    "--output=" + str(packet), commit, *selected], check=True)
    with zipfile.ZipFile(packet, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        info = zipfile.ZipInfo("START_HERE.md", date_time=(2000, 1, 1, 0, 0, 0))
        info.external_attr = 0o100644 << 16
        archive.writestr(info, PACKET_NOTE)
    pdf = output / "main.pdf"
    pdf.write_bytes(git("show", commit + ":paper/main.pdf"))
    files = {}
    for path in (paper, packet):
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError("ZIP integrity failure")
            names = [n for n in archive.namelist() if not n.endswith("/")]
            if len(names) != len(set(names)):
                raise ValueError("Duplicate ZIP entry")
            entries = {name: sha(archive.read(name)) for name in names}
            for name, digest in entries.items():
                expected = PACKET_NOTE.encode() if name == "START_HERE.md" else git("show", commit + ":" + name)
                if sha(expected) != digest:
                    raise ValueError("Git blob mismatch: " + name)
        files[path.name] = {"bytes": path.stat().st_size, "sha256": sha(path.read_bytes()),
                            "entries": entries}
    files[pdf.name] = {"bytes": pdf.stat().st_size, "sha256": sha(pdf.read_bytes())}
    manifest = {"schema": "pbp.collaboration-archive.v1", "source_commit": commit,
                "files": files, "qpu_data_included": False, "qpu_submission": False,
                "packet_scope": "Selected code, paper, offline pilot and evidence; full history in GitHub"}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    (output / "SHA256SUMS").write_text("".join(f"{row['sha256']}  {name}\n" for name, row in files.items()))
    print(json.dumps({"source_commit": commit, "files": {n: {k: r[k] for k in ("bytes", "sha256")}
                       for n, r in files.items()}}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package(args.commit, args.output.resolve())


if __name__ == "__main__":
    main()
