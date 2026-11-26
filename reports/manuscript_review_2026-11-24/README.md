# Sources et relectures du manuscrit

La [synthèse finale v3](v3/report.md) rassemble les conclusions. Les versions
v1/v2/v3 conservent leurs sources complètes `full-source.tex`, bibliographies,
contextes, manifestes et relectures. Leurs versions antérieures et leurs
corrections restent distinctes.

Les 36 fichiers `v*/sections/*.tex` ont été retirés comme exports redondants.
Avant suppression, chacun a été vérifié identique au découpage de son
`full-source.tex` décrit par `manifest.json`, entrée `units`, champs
`expanded_start` et `expanded_end`, avec le SHA256 `sha256` correspondant.
Les manifestes historiques restent inchangés : leur champ `file` décrit
l'export original, à restaurer si un outil en a besoin.

Pour retrouver le dossier original complet dans une nouvelle destination :

```sh
review_snapshot=$(mktemp -d "${TMPDIR:-/tmp}/pbp-review.XXXXXX")
git archive b614d5259587fb5ab9897738206bca0d007715ae \
  reports/manuscript_review_2026-11-24 | tar -x -C "$review_snapshot"
```

Cette opération restitue les sources de relecture historiques sans modifier
le manuscrit courant. Les brouillons et découpages ne sont pas des données
QPU ; aucun résultat expérimental ou rapport de relecture n'a été supprimé.
