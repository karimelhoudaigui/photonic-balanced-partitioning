# Démonstration locale figée, 24 novembre 2026

`run-v1/` contient les huit étapes scellées et deux fichiers de counts
**local_synthetic**, seed 20261124, 1000 tirages idéaux par circuit.
Aucun fichier ne provient d'un QPU. Le manifeste global donne le hash de chaque
fichier et du script ; chaque étape conserve son manifeste propre.

Recréer dans un dossier neuf, avec le code du même commit et les versions
épinglées ; l'horodatage, le commit de provenance et les manifests changent
normalement lors d'une reproduction :

```sh
export PBP_WORKTREE=/Users/karimelhoudaigui/Desktop/pasqal/.qwen/worktrees/recovery-qpu-20261124
export PYTHONPATH="$PBP_WORKTREE/src"
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python "$PBP_WORKTREE/qpu/offline_pilot_20261124_v1/reproduce.py" --output /tmp/pbp-laurent-reproduced-new
```

Les deux analyses utilisent les mêmes counts. Dans `analysis-known-attempts`,
les métriques physiques ont un dénominateur synthétique de 1000. Dans
`analysis-unknown-attempts`, ce dénominateur et tous les coûts physiques sont
`null`. Cela vérifie le traitement d'une métadonnée manquante ; ce n'est pas
un modèle expérimental de pertes.
