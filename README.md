# Photonic balanced partitioning

This repository studies collision-aware photonic graph bisection, sufficient classical-replacement certificates and physical resource accounting. The tested generic bosonic optimizer **has not demonstrated the sought benefit** over distinguishable and serious classical controls. No QPU measurement is reported.

Current discovery work on `research/p45-positive-discovery` starts at the
[research index](research/README.md) and [live state](research/P45_LIVE_STATE.md).
The latest [P145 investigation](research/P145_RESEARCH_RECEIPT.md) tests collective
three-photon local proposals and establishes scoped classical-mirror, support
and growing-layer filters. Its positive constructed interference contrast is
beaten by stronger classical controls. P141's favorable ER bosonic/distinguishable
contrast remains preserved. P137/P139/P143 retain their stated local assumptions.
The optimization-advantage objective remains open. These results are not yet
integrated into the frozen article; no positive replication or QPU gate is claimed.

Start with the [rebuilt article PDF](paper/main.pdf), [scientific overview](docs/SCIENTIFIC_OVERVIEW.md), [integrity audit](reports/SCIENTIFIC_INTEGRITY_AUDIT.md) and [publication assessment](reports/PUBLICATION_READINESS.md). The single primary thesis is the density-qualified certificate, supported by a loss/source theorem and an honest negative benchmark. Originality of the full certificate composition remains unresolved.

## Accès rapide — article, résultats et Laurent

| Besoin | Point d'entrée |
| --- | --- |
| **Dernier article PDF** | **[paper/main.pdf](paper/main.pdf)** — 16 pages, version du 24 novembre 2026 |
| **Sources LaTeX complètes** | **[paper/main.tex](paper/main.tex)** et [guide de construction](paper/README.md) |
| Résultats, preuves et reproductions | [Catalogue des résultats](results/README.md), [état scientifique](STATUS.md) |
| **Recherche récente et rapports** | **[Recherche](research/README.md)**, **[rapports](reports/README.md)** et [état courant détaillé](research/P45_LIVE_STATE.md) |
| **Laurent : accès Lucy via TGCC** | **[docs/LUCY_TGCC.md](docs/LUCY_TGCC.md)** — environnement, plan local, specs, lancement autorisé et analyse |
| Contrat scientifique et counts | [Dossier technique détaillé](docs/LAURENT_HANDOFF.md) |
| Archives PDF, LaTeX et dossier Lucy | [Téléchargements et empreintes](deliverables/README.md) |
| Reprendre dans VS Code | Ouvrir ce dossier ; `Terminal → Run Task` : tests, vérification de l'article, pilote local, plan Lucy |

Le PDF livré et ses sources sont préservés. La partie QPU du manuscrit décrit
une expérience à réaliser ; aucun résultat Lucy n'est revendiqué. Le nouveau
lanceur emploie la passerelle officielle CEA et nécessite une autorisation
explicite pour un plan précis. Sa validation locale utilise un transport simulé ;
l'accès réel au compte TGCC et les capacités PNR restent à vérifier.

## Reproduce locally

Python3.11 is the tested series; numerical, test, Perceval and publication dependencies are pinned in pyproject.toml. The recorded environment is Python3.11.15, NumPy2.4.6, SciPy1.17.1, Perceval1.3.0 and exqalibur1.4.2.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements-research-lock.txt
.venv/bin/python -m pip install -e '.[all]'
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python -m pytest tests/ -q
.venv/bin/python scripts/build_publication.py --check
```

The accepted data and generated figures are tracked. Regenerate paper artifacts with `make figures`; compile with `make paper TECTONIC=/path/to/tectonic`. Tectonic0.16.9 was used locally. The first TeX build may download composition packages; no device service is used. [Reproducibility](docs/REPRODUCIBILITY.md) explains fresh-output analysis, archive integrity and build checks.

## Reproduce the offline hardware pilot

```sh
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  .venv/bin/python qpu/offline_pilot_20261124_v1/reproduce.py \
  --output /tmp/pbp-offline-pilot-new
```

Use a new output directory. This executes all seven local preparation/analysis commands and creates explicitly synthetic counts. [Laurent's dossier](docs/LAURENT_HANDOFF.md), [commands](qpu/README.md), [compatibility matrix](docs/QPU_COMPATIBILITY.md) and [readiness gates](reports/QPU_READINESS.md) distinguish verified local compilation from unknown actual backend compatibility. The separate [Lucy/TGCC adapter](docs/LUCY_TGCC.md) supports one explicitly authorized job; it is never used by the offline pipeline or CI.

## Evidence and layout

- `src/.../problems`: validated weighted simple graphs and exact small bisections.
- `photonic` and `classical`: full Fock laws, mesh/threshold models and explicit classical controls.
- `optimization`: optimum-blind loss interface; success-to-known-optimum belongs to retrospective evaluation.
- `noise`: bounded internal-state Gram interference and full loss sectors, with numerical diagnostics.
- `hardware`: offline circuit/reference/export/count-analysis pipeline and separately guarded Lucy/TGCC adapter.
- `results/validated/recovery_2026-11-24/`: the single publication dataset; all756 E05b runs reconstructed, with source hashes and documented provenance gaps.
- `experiments/`, prior `results/`, `theory/`, `research/`: unchanged historical captures, proofs, contracts, counterexamples and source audits.
- `paper/`: new LaTeX, generated tables/figures and PDF; historical unsupported article is retained in Git6154b46.
- `reports/` and root registers: execution evidence, negative results, reviews, decisions and open obligations.
- `.qwen/`: versioned local worker roles and bounded research infrastructure; tiny-model prose is not accepted as scientific evidence.

Historical manifests refer to their recorded source commits or frozen snapshots, not today's changing status text. Some older drivers overwrite fixed paths: inspect their contracts before any replay and always choose a fresh destination. The [numerical census](reports/NUMERICAL_RECONCILIATION.md) separates verified output integrity from new experiment replication. No raw data have been silently rewritten.

The original algorithmic goal remains open. Tests, PDF compilation, local circuit export and novelty are different standards of evidence.

Recorded local research validation: **1569 tests passed**, with 602 historical
scientific files unchanged and the existing16-page manuscript verified.
[P145's receipt](research/P145_RESEARCH_RECEIPT.md) identifies the raw source
revisions and the separate56-point Perceval qualification. The earlier
[P141 CI receipt](reports/P141_validation_review/ci_success.json) remains tied
to its own revision, not a moving-HEAD or independent optimization/hardware claim.

The 24-Nov delivery had 505 local tests, including 21 mocked Lucy adapter checks;
[its receipts](reports/LUCY_TGCC_DELIVERY.md) and the separately extracted
Laurent v2 packet's 46-test validation remain available. The
[portable P40 replay](docs/P40_REPRODUCTION.md) covers 45 physical-model cells.
No QPU measurement is reported.
