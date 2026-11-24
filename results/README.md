# Retrouver les résultats scientifiques

Les chemins historiques restent inchangés pour préserver leurs empreintes.
Ce catalogue distingue les données utilisées par l'article, les reproductions
et les recherches antérieures. Un test logiciel ou un export optique n'est pas
une acquisition QPU.

| Étude | Données à utiliser | Interprétation |
| --- | --- | --- |
| E05b, comparaison complète n=4,6,8 | [validated/recovery_2026-11-24/](validated/recovery_2026-11-24/) : `benchmark.csv`, `summary.json`, `campaigns.json`, `source_hashes.json`, `manifest.json` | 756 trajectoires archivées, réconciliées sans relancer l'optimisation. Bosons moins bons en moyenne finale que distinguables à chaque taille testée. Les répétitions de graphes et limites statistiques sont divulguées. |
| P33, certificat sous densité | [P33_density_supervised/20261122T014822Z/](P33_density_supervised/20261122T014822Z/) : `primary/`, `replication/`, `audit/` | Illustration numérique d'une preuve analytique ; les copies P33 non supervisées ne fondent pas l'article. |
| P37, pertes et sélection de source | [experiments/P37_loss_source/run/](../experiments/P37_loss_source/run/) | Calculs exacts, deux unités de coût distinctes ; faisabilité Haar, sans enrichissement en qualité de coupe. |
| P40, calibration optique théorique | [validated/P40_sharpness_pilot_2026-11-24/](validated/P40_sharpness_pilot_2026-11-24/) | 45 cellules de modèle, cinq comparaisons SLOS ; aucune mesure matérielle. |
| Reproductions P40 | [replay superviseur](validated/P40_replay_supervisor_2026-11-24/), [guide](../docs/P40_REPRODUCTION.md) | Reproductions des mêmes lois, pas de nouvelles découvertes indépendantes. |
| Pilote hors ligne | [reproduction superviseur](validated/offline_pilot_2026-11-24_supervisor/), [pilote figé](../qpu/offline_pilot_20261124_v1/) | Circuits/références et counts explicitement synthétiques. |
| Futur matériel Lucy | `results/qpu/` local, exclu de Git par défaut | Aucun résultat QPU livré. Les acquisitions futures conservent leur résultat natif et leurs métadonnées, séparés des analyses. |

[NUMERICAL_RECONCILIATION.md](../reports/NUMERICAL_RECONCILIATION.md) détaille
le recensement ; [NEGATIVE_RESULTS.md](../NEGATIVE_RESULTS.md) conserve les
échecs et retraits. Les manifestes indiquent leurs commits et sources d'origine.
Le dossier `_recovery_2026-11-24_preliminary` est préliminaire et ne remplace
pas le dataset final `recovery_2026-11-24`.

Pour préserver les données, utiliser une nouvelle destination à chaque replay.
Certains anciens scripts écrivent à un emplacement fixe : consulter leur contrat
avant exécution. Contrôle des 602 fichiers scientifiques préexistants :

```sh
.venv/bin/python scripts/check_archive_preservation.py
```
