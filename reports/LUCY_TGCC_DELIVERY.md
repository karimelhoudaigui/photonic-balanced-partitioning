# Livraison du dépôt et du pilote Lucy/TGCC — 24 novembre 2026

**505 tests PASS dans l'environnement Python épinglé ; aucun appel QPU.**
Le dernier article et les 602 fichiers scientifiques historiques sont conservés
sans modification. Cette livraison organise l'accès aux preuves et ajoute
un adaptateur d'acquisition future ; elle ne transforme pas les simulations
en résultats matériels ni en avantage d'optimisation.

## Livrables

- [Article PDF](../paper/main.pdf), [source principale LaTeX](../paper/main.tex)
  et [index de toutes les sources](../paper/README.md).
- [Catalogue des résultats](../results/README.md) : dataset E05b final,
  preuves P33/P37, modèle P40, reproductions et résultats négatifs.
- [Guide Laurent pour Lucy via TGCC](../docs/LUCY_TGCC.md) : route officielle
  CEA, environnement, plan, specs, autorisation et analyse.
- Configuration VS Code versionnée : quatre tâches locales, sans lancement QPU.
- [Code de l'adaptateur](../src/photonic_balanced_partitioning/hardware/lucy_tgcc.py)
  et [21 tests dédiés](../tests/test_lucy_tgcc.py).

Le papier principal garde exactement la SHA-256
`271946c9043d26c0e00a964591e9a47541d5816c399e7a52a62032630650243f`.
Les `.tex`, figures, tableaux et bibliographie scientifiques n'ont pas été édités.

## Validation réellement exécutée

Le [reçu complet](lucy_tgcc_2026-11-24/validation/receipt.json) conserve les huit
commandes, stdout/stderr, temps, commits de départ et hashes avant/après.
Les modifications étaient encore non commitées lors de ce contrôle ; le SHA
du source testé identifie précisément le code validé.

| Contrôle | Résultat |
| --- | --- |
| Suite complète `pytest tests/ -q` | 505 PASS, six avertissements de cache Perceval, 12,43 s |
| Tests nouveaux de l'adaptateur | 21 PASS, transport local simulé, vrais payloads Perceval |
| Préservation de l'archive | 602 fichiers inchangés, aucun manquant |
| Manifestes de l'article | Sept sorties vérifiées, données sources intactes |
| PDF déjà construit | 16 pages, 14 clés citées, aucun renvoi indéfini ni input périmé |
| CLI Lucy local | Versions et trois plans identity/HOM/pair_mixing produits, sans client distant |
| Compte TGCC, specs live et compilation native | NON TESTÉS |
| Soumission matérielle / crédits | AUCUNE / ZÉRO |

Les paquets publics Interop et QLMaas ont été téléchargés pour inspection
d'API, sans installation dans l'environnement scientifique et sans instancier
de client matériel. Versions/empreintes et sources primaires sont dans
[official_api_audit.json](lucy_tgcc_2026-11-24/official_api_audit.json).
Le module utilise `MyQLMHelper.make_job(params=...)` ; l'ancienne supposition
`Experiment.set_parameter` a été écartée après inspection de Perceval1.3.

## Relecture séparée et corrections

Un agent natif distinct a relu le code et les contrats sans écrire de fichier
ni lancer de test ou d'appel QPU durant sa revue. Il a demandé de lier le
nom du fournisseur à l'autorisation, de traiter le filtrage possible par
`final_mode_number`, et de préciser la portée locale de l'anti-doublon.
Ces trois points sont corrigés et documentés, avec refus testés pour les deux
premiers. Son verdict final est **PASS pour la livraison locale**, avec le
SHA d'adaptateur
`4eb8f58524266ccfd9a012524d76669dfd992d796703bf0c32ed5cb1948f341d`.
Ce contrôle de code n'est ni une mesure Lucy ni une revue humaine du papier.

## Limites et reprise

La route CEA est implémentée ; l'accès réel reste à confirmer sur Irène.
Les bibliothèques de `ccc-quantum` doivent être recensées sur TGCC sans
écraser leur environnement. Une calibration, PNR, routage complet, filtres
effectifs et autorisation du plan sont nécessaires avant acquisition.

Un job au plus par invocation ; plafond absolu 10 000 détections non vides ;
aucun retry. Le marqueur avant `submit` empêche la resoumission depuis le même
dossier de plan. Il ne fournit pas d'idempotence globale entre clones. Le délai
arrête l'attente locale, sans garantie d'annulation du job distant : après
interruption, rechercher le job existant avec TGCC avant toute nouvelle action.

Le résultat natif est conservé avant décodage. L'export PNR repose sur des
confirmations opérateur explicites ; toute anomalie détectée conserve le natif
et bloque la normalisation. `physical_attempts` reste inconnu : aucune
performance fournisseur n'est convertie en compteur d'émission. Aucun calcul
de TV physique complète ou succès par tentative n'est inventé.

Les exports historiques v1 et le premier ZIP Laurent restent intacts. Les
autorisations locales et acquisitions futures sont ignorées par Git ; les
agents Qwen ont une interdiction explicite du chemin de soumission.
La CI n'utilise que calculs et compilation locaux, jamais cet accès matériel.

L'objectif scientifique initial demeure ouvert. Les gates matériels et de
soumission académique restent ceux de [QPU_READINESS](QPU_READINESS.md) et
[PUBLICATION_READINESS](PUBLICATION_READINESS.md).
