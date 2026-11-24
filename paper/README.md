# Article de référence — 24 novembre 2026

Le dernier article est **[main.pdf](main.pdf)** (16 pages). Sa source principale
est **[main.tex](main.tex)** ; elle inclut `sections/`, `appendices/`,
`tables/`, `figures/` et `references.bib`. Ces éléments sont tous versionnés.

Titre : *Collision-Aware Certification and Resource Accounting for Photonic
Graph Bisection*.

| Ce que l'article établit | Preuves et données |
| --- | --- |
| Une borne de remplacement classique sous une hypothèse précise de densité | [P33](../theory/phase3_density_certificate.md), preuve dans l'article, famille de saturation et contre-exemple |
| L'optimum du nombre de photons dépend du coût par tentative ou par photon | [P37](../theory/phase3_loss_source_selection.md), calculs exacts archivés |
| Aucun bénéfice d'optimisation démontré sur les instances et budgets testés | [756 trajectoires E05b réconciliées](../results/validated/recovery_2026-11-24/), tous les contrôles conservés |
| Un protocole optique pour une future mesure | Section 6 ; [dossier Lucy/TGCC](../docs/LUCY_TGCC.md), sans résultat matériel inventé |

Le résultat négatif porte sur les expériences rapportées. L'article ne démontre
pas un avantage quantique. L'originalité de la composition complète de la borne
reste à établir : [évaluation de publication](../reports/PUBLICATION_READINESS.md).
Les métadonnées d'auteurs sont encore à finaliser avant diffusion académique.

SHA-256 du PDF livré :
`271946c9043d26c0e00a964591e9a47541d5816c399e7a52a62032630650243f`.
Cette empreinte identifie l'original ; une recompilation peut produire d'autres
octets sans changer les sources scientifiques.

Depuis la racine :

```sh
.venv/bin/python scripts/build_publication.py --check
make paper TECTONIC=/chemin/vers/tectonic
```

Le journal et les reçus de la construction originale sont dans
[reports/recovery_2026-11-24/](../reports/recovery_2026-11-24/).
L'ancien manuscrit aux claims retirés reste dans l'historique Git `6154b46`.
