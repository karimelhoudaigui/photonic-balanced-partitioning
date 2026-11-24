# Pilote QPU : préparation et analyse hors ligne

Le nouveau CLI produit des circuits et références locaux. Il ne consulte pas
les credentials, n'interroge aucun compte et ne soumet aucun job. Les anciens
`run_qpu.py`, `check_backend.py` et `smoke_test.py` restent désactivés.

Depuis la racine de la branche scientific-recovery-publication, avec la venv installée selon README.md :

```sh
export PBP_WORKTREE="$PWD"
export PBP_PYTHON="$PBP_WORKTREE/.venv/bin/python"
export PYTHONPATH="$PBP_WORKTREE/src"
cd "$PBP_WORKTREE"
export PBP_RUN=/tmp/pbp-laurent-new-run
"$PBP_PYTHON" -m photonic_balanced_partitioning.hardware check_environment --output "$PBP_RUN/environment"
"$PBP_PYTHON" -m photonic_balanced_partitioning.hardware validate_physics --config qpu/configs/pilot_offline_n4.json --output "$PBP_RUN/physics"
"$PBP_PYTHON" -m photonic_balanced_partitioning.hardware generate_circuits --config qpu/configs/pilot_offline_n4.json --output "$PBP_RUN/circuits"
"$PBP_PYTHON" -m photonic_balanced_partitioning.hardware simulate_reference --bundle "$PBP_RUN/circuits" --output "$PBP_RUN/reference"
"$PBP_PYTHON" -m photonic_balanced_partitioning.hardware validate_compilation --bundle "$PBP_RUN/reference" --output "$PBP_RUN/compiled"
"$PBP_PYTHON" -m photonic_balanced_partitioning.hardware prepare_qpu_job --bundle "$PBP_RUN/compiled" --output "$PBP_RUN/job-draft"
```

Choisir une destination nouvelle pour chaque étape et chaque reprise. Chaque
bundle contient `artifact.json` et `manifest.json` : configuration, hash,
versions, UTC, commit, hashes des sources, parent et résultats. Le manifeste
contrôle l'intégrité du payload ; ce n'est pas une signature ni une preuve
matérielle. Le code refuse l'écrasement et les hashes incohérents. Un dossier
incomplet après interruption est conservé et ne doit pas être réparé en place.

Pour analyser un export normalisé et conservé en lecture seule :

```sh
"$PBP_PYTHON" -m photonic_balanced_partitioning.hardware analyze_qpu_results --bundle "$PBP_RUN/reference" --results /chemin/vers/counts.json --output "$PBP_RUN/analysis-001"
```

Le schéma et l'exemple synthétique figurent dans
[le dossier Laurent](../docs/LAURENT_HANDOFF.md). Les résultats matériels ne
peuvent être remplacés par les références idéales. Sans compteur de tentatives,
les probabilités par tentative physique restent `null`.

```sh
"$PBP_PYTHON" -m pytest tests/test_hardware_offline.py -q
```

Voir [compatibilité officielle](../docs/QPU_COMPATIBILITY.md) et
[rapport technique](../reports/QPU_TECHNICAL_RECOVERY.md).
