# Archives à transmettre et à conserver

La référence courante reste [le dépôt complet](https://github.com/karimelhoudaigui/photonic-balanced-partitioning)
avec **[paper/main.pdf](../paper/main.pdf)** et **[paper/main.tex](../paper/main.tex)**.

Le dossier [RESEARCH_LUCY_2026-11-24_v2/](RESEARCH_LUCY_2026-11-24_v2/)
archive le commit scientifique `c8b6161a35778d354b8136a86172addda9f5aba7` :

- **[main.pdf](RESEARCH_LUCY_2026-11-24_v2/main.pdf)** : le PDF original de 16 pages.
- **[ARTICLE_LATEX_2026-11-24.zip](RESEARCH_LUCY_2026-11-24_v2/ARTICLE_LATEX_2026-11-24.zip)** : sources complètes, bibliographie, tableaux, figures et PDF, directement compilables avec Tectonic.
- **[DOSSIER_LAURENT_LUCY_2026-11-24_v2.zip](RESEARCH_LUCY_2026-11-24_v2/DOSSIER_LAURENT_LUCY_2026-11-24_v2.zip)** : commencer par `START_HERE.md`. Code, pilote local figé, guide Lucy/TGCC, données sélectionnées et deux fichiers de tests. Ce dossier extrait a réellement passé ses **46 tests locaux** ; il n'inclut pas toute l'histoire Git ou les 505 tests du dépôt complet.
- [manifest.json](RESEARCH_LUCY_2026-11-24_v2/manifest.json) et [SHA256SUMS](RESEARCH_LUCY_2026-11-24_v2/SHA256SUMS) : commit, hashes des archives et de chaque entrée ZIP.

Les bibliothèques scientifiques doivent être installées localement selon le
README. Sur TGCC, conserver l'environnement `ccc-quantum` de la plateforme.
Les ZIP ne contiennent ni credentials ni données QPU. Le pilote n'a pas été
exécuté sur Lucy ; les contrôles réels et l'autorisation sont dans
[docs/LUCY_TGCC.md](../docs/LUCY_TGCC.md).

Recréation dans une nouvelle destination, depuis le dépôt complet :

```sh
python3 scripts/package_collaboration.py \
  --commit c8b6161a35778d354b8136a86172addda9f5aba7 \
  --output /tmp/pbp-collaboration-archive-new
```

Le premier `DOSSIER_LAURENT_2026-11-24.zip` reste inchangé comme archive du
pilote hors ligne antérieur ; utiliser la version Lucy v2 pour le nouvel accès.
