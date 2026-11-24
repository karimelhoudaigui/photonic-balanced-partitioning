# Dossier Laurent — contrat scientifique du pilote n=4, deux photons

**Accès matériel ciblé : [Lucy via TGCC — guide de lancement](LUCY_TGCC.md).**
Un adaptateur distinct a été ajouté après le gel du pilote local v1. Il est
testé avec un transport simulé ; aucune connexion au compte ni acquisition
matérielle n'est revendiquée. Le guide précise les confirmations techniques
et l'autorisation opérateur nécessaires. Les exports v1 restent inchangés.

Version du 24 novembre 2026. **Aucune soumission, aucun crédit consommé,
autorisation false.** Le livrable est un outil local fonctionnel de préparation
et d'analyse, accompagné de trois contrôles optiques figés. Il ne constitue
ni une connexion distante opérationnelle ni un résultat QPU.

## Expérience minimale à examiner

L'entrée est `|1,1,0,0>` sur quatre modes. Les graphes sont le chemin
0–1–2–3, K4 et K₂,₂ de bipartition {0,1}/{2,3}, arêtes de poids un.
Toutes les six partitions orientées de taille deux sont évaluées ; les
complémentaires ont le même coût. Leurs coûts minimaux sont respectivement
1, 4 et **2**. L'ancien protocole donnait à tort 4 pour le dernier graphe.

| Circuit figé | Portes, ordre temporel | Loi idéale et contrôle |
| --- | --- | --- |
| `identity` | aucune | Sortie (1,1,0,0) avec probabilité 1 ; CF=1 |
| `hom` | BS.Rx(π/2) sur (0,1) | Sorties (2,0,0,0) et (0,2,0,0), chacune 1/2 ; CF bosons=0, distinguables=1/2 |
| `pair_mixing` | PERM(0,2,1,3), BS.Rx(π/2) sur (0,1), BS.Rx(π/2) sur (2,3), même PERM | (1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1), chacune 1/4 ; CF=1 ; même loi distinguable |

La convention BS.Rx est `cos(θ/2) I + i sin(θ/2) X`. Les portes multiplient
U à gauche, les lignes sont les sorties et les colonnes les entrées. Chaque
bundle contient les occupations, paramètres, matrice U complexe, chaîne de
sérialisation Perceval, dix probabilités Fock complètes avec zéros, lois
distinguables et SLOS, partitions et coûts. Aucune renormalisation CF n'est
appliquée au calcul. Une probabilité conditionnelle sans support est `null`.

Le contrôle par paires ne présente aucune interférence multiphoton utile ;
K4 est un témoin de score constant. Ces circuits ne sont pas entraînés sur
les graphes et ne constituent pas une expérience de gain d'optimisation.
Le pilote n=6 est volontairement hors du périmètre validé.

## Utiliser et reprendre le dossier

Les sept commandes exécutables et la configuration minimale sont dans
[qpu/README.md](../qpu/README.md). L'interpréteur est la venv absolue du dépôt
racine ; `PYTHONPATH` désigne le `src` du worktree testé. Aucun paquet distant
ni authentification n'est nécessaire pour exécuter ces commandes.

1. `check_environment` vérifie les versions locales épinglées, sans lire les
   variables de credentials ni leur stockage.
2. `validate_physics` compare formule indépendante à deux photons, Ryser du
   projet et Perceval SLOS, puis identité/HOM/mélange par paires.
3. `generate_circuits` fige configuration et paramètres sans optimisation.
4. `simulate_reference` conserve les distributions complètes et leurs écarts.
5. `validate_compilation` reconstruit les portes et vérifie export et round-trip
   contre U à une seule phase globale près, tolérance 10⁻¹⁰.
6. `prepare_qpu_job` écrit un **brouillon interne**, avec trois circuits et un
   plafond demandé de 1000 tentatives par circuit, 3000 au total. Ce plafond
   n'est ni autorisé ni consommé. Le nouveau plan Lucy a sa propre syntaxe et
   son plafond en shots fournisseur, qui ne vaut pas tentatives d'émission.
7. `analyze_qpu_results` lit les counts et crée un nouveau rapport séparé.

Les imports Perceval se font avec un stockage persistant temporaire neuf ;
le CLI bloque les connexions socket et DNS. L'API locale ne contient aucune
classe de soumission. Les hashes détectent une modification accidentelle,
pas un adversaire pouvant réécrire le manifeste. Les exports Perceval doivent
provenir de bundles locaux de confiance.

Pour reprendre, conserver toutes les sorties anciennes et choisir un autre
`--output`. Les références se relisent sans recalcul si leur hash est intact.
Un export partiel peut contenir un sous-ensemble des circuits : le rapport
énumère ceux qui manquent. Les fichiers bruts ne sont jamais modifiés et leur
SHA-256 apparaît dans l'analyse.

## Contrat explicite des counts

Le format interne JSON suivant doit être rempli à partir d'un export fournisseur
authentifié. Il ne s'agit pas du format natif garanti de Quandela. Cet exemple
est **synthétique** et ne doit pas être présenté comme une acquisition.

```json
{
  "schema": "pbp.pnr-counts.v1",
  "evidence_kind": "local_synthetic",
  "reference_artifact_sha256": "SHA256_DU_FICHIER_reference/artifact.json",
  "records": [{
    "circuit_id": "identity",
    "input_occupation": [1, 1, 0, 0],
    "detector": "pnr",
    "physical_attempts": 100,
    "attempts_source": "compteur synthétique de 100 déclenchements",
    "filtering": {"kind": "none", "discarded_attempts": 0},
    "counts": [{"occupation": [1, 1, 0, 0], "count": 100}]
  }]
}
```

Pour de véritables données normalisées, `evidence_kind` est `hardware_pnr` et
la provenance de l'acquisition doit être conservée extérieurement. Ce champ
est une déclaration de provenance, que l'outil ne peut authentifier à lui seul.
Les occupations et counts sont des entiers non négatifs ; les quatre modes
sont obligatoires, les doublons sont refusés. Le pilote accepte les pertes
(zéro ou un photon détecté) mais refuse plus de deux photons : conserver ces
événements bruts et auditer les multiphotons/dark counts séparément.

Chaque tentative connue doit être représentée par un count ou un rejet
explicitement compté : `physical_attempts = sum(counts) + discarded_attempts`.
Sans filtre, tous les événements, y compris le vide, doivent être inclus et
`discarded_attempts=0`. Le compteur physique ne doit jamais être reconstruit
depuis un nombre de coïncidences accepté.

Le seul filtrage additionnel pris en charge est
`{"kind":"min_detected_photons","minimum":2,"discarded_attempts":900}`,
avec 0≤minimum≤2. Dans ce cas, 100 événements retournés sur 1000 tentatives
connues donnent CF/tentative=0,1 si les 100 sont CF, et CF/retourné=1.
Les rejets sous le seuil ne peuvent être ni des succès ni des collisions à
deux photons dans ce modèle. Un filtre CF, un filtrage sur modes inutilisés,
un heralding ou un photon recycling non documenté sort de ce contrat.

Si seul le nombre d'échantillons post-sélectionnés est connu, mettre
`physical_attempts:null`, `attempts_source:null` et
`discarded_attempts:null`. Les métriques physiques et les coûts par tentative
restent alors `null`. Le taux optimal parmi les CF peut encore être estimé
sous les hypothèses d'échantillonnage ; il ne mesure pas le rendement physique.
Un résultat threshold ne doit pas être renommé PNR.

## Incertitude et conformité

Les intervalles Wilson à 95 % sont ponctuels, sous essais Bernoulli iid.
Ils couvrent CF, collisions, succès par tentative si le dénominateur est
connu, et optimalité parmi les CF. Ils ne corrigent ni dérive, ni sélection
adaptative, ni comparaison multiple. Zéro succès donne une estimation du
coût géométrique indéfinie et une borne supérieure non finie (`null` avec
`upper_unbounded:true`). Ce coût suppose un taux stationnaire et des
répétitions indépendantes.

Pour les données sans filtre, l'analyse rapporte la TV empirique à la loi
idéale, les intervalles Wilson de chaque occupation (incluant les pertes), et
un rayon conservateur de TV par Hoeffding et union sur les 15 catégories de
zéro, un ou deux photons. Un accord avec cet idéal n'est pas une validation
du modèle de bruit matériel. Une analyse filtrée ne rapporte pas de TV
physique non conditionnelle. Les événements anormaux et rejets ne sont jamais
normalisés silencieusement hors des métriques de coût physique.

## Décisions techniques encore nécessaires

La [matrice de compatibilité officielle](QPU_COMPATIBILITY.md) distingue
spécification publique et statut effectif inconnu. Avant une exécution future,
il faut établir les spécifications autorisées pour le compte, le routage
entrée/sortie, la compilation native, la réponse PNR effective, le compteur
physique, tous les filtres et les effets de photon recycling ; puis documenter
les pertes, la visibilité et la calibration contemporaines. Une autorisation
QPU et un plafond de crédits doivent être explicites. Aucun de ces points
n'est validé par les fichiers locaux, et aucun crédit ne sera engagé par ce CLI.

Les diagnostics numériques traitent un support inférieur à 10⁻¹⁴ comme nul
pour les conditionnelles de référence. Les probabilités Fock calculées restent
conservées, notamment le résidu HOM d'arrondi voisin de 5×10⁻³².

## Contrôle de calibration lié au théorème

Le dossier complémentaire [DENSITY_PILOT.md](DENSITY_PILOT.md) fournit cinq circuits de la famille plate du théorème et45 scénarios locaux de pertes/recouvrement, tous conservés. Les unitaires, angles, sérialisations et distributions complètes sont dans results/validated/P40_sharpness_pilot_2026-11-24/. Ce pilote relie une prédiction quantitative d'interférence au futur travail matériel ; il ne montre pas un avantage d'optimisation.

Ces exports forment une étude locale séparée. La chaîne de sept commandes validée ci-dessus reste limitée à ses trois circuits fixes ; elle ne soumet ni n'ingère automatiquement ces cinq nouveaux circuits. Leur intégration à un adaptateur matériel, le plan statistique, le compteur physique et les calibrations nécessitent une revue avant toute exécution autorisée.

Pour les contrôles P40, η²/3 décrit une occupation faisable choisie uniformément puis effectivement préparée et transmise optiquement. Le sampler classique pur réussit avec1/3 par tir classique et ne subit aucune perte optique ; ces unités de coût sont distinctes.
