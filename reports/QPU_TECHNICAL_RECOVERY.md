# Récupération technique du pilote QPU — 2026-11-24

**Résultat : outil hors ligne opérationnel, aucun accès distant validé.**
Périmètre : branche `recovery/qpu-20261124`, base `6154b46`, worktree isolé
`recovery-qpu-20261124`. Aucun credential consulté par le nouvel outil,
aucun objet distant instancié, aucune soumission, aucun crédit consommé.
Les anciens entrypoints et rapports racine ne sont pas modifiés.

## Livraison

- CLI `python -m photonic_balanced_partitioning.hardware` avec les sept
  sous-commandes demandées : environnement, physique, circuits, référence,
  compilation locale, brouillon de job et analyse des counts.
- Pilote fixé n=4, k=2, entrée (1,1,0,0), seed 20261124, graphes chemin/K4/K₂,₂,
  identité/HOM/mélange par paires. Aucun circuit entraîné ni n=6 revendiqué.
- Matrices U complexes, portes/paramètres, sérialisation Perceval, lois Fock
  complètes et contrôles distinguables, partitions et coûts conservés dans
  les bundles successifs. Les collisions ne sont pas retirées du calcul.
- Écritures dans de nouvelles destinations seulement ; relecture avec contrôle
  de hash et reprise par nouvelle destination. Aucun raw QPU réel utilisé.
- Schéma counts PNR explicite, dénominateurs physiques connus ou inconnus,
  rejets audités, pertes, Wilson et conformité à l'idéal avec incertitude.
- Documentation autonome : `docs/LAURENT_HANDOFF.md`,
  `docs/QPU_COMPATIBILITY.md`, `qpu/README.md` et configuration minimale.

## Vérification réellement exécutée

Interpréteur : `/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python`,
Python 3.11.15. `PYTHONPATH` est le `src` absolu du worktree.
Versions : Perceval 1.3.0, Exqalibur 1.4.2, NumPy 2.4.6, SciPy 1.17.1,
pytest 8.4.2. Aucune dépendance ajoutée.

Commande finale :

```sh
PYTHONPATH=/Users/karimelhoudaigui/Desktop/pasqal/.qwen/worktrees/recovery-qpu-20261124/src /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -m pytest tests/ -q
```

La suite a été lancée sous un wrapper CPU de 120 secondes, avec
`PCVL_PERSISTENT_PATH`, `MPLCONFIGDIR` et `XDG_CACHE_HOME` pointant vers un
répertoire temporaire neuf. **312 passed in 60.31s**, retour 0, durée du wrapper
61.569 s. Les 25 cas de `tests/test_hardware_offline.py` sont inclus : réseau
interdit par mocks, formule deux photons/Ryser/SLOS, identité/HOM, mélange par
paires, coût exact K₂,₂, phase globale/export, brouillon non soumis,
non-écrasement/hash, données incohérentes, pertes, filtres documentés,
tentatives inconnues, reprise et timeout de provenance Git.

Le contrôle indépendant à deux photons utilise
`p(ii)=2|U_i0 U_i1|²` et
`p(ij)=|U_i0 U_j1+U_i1 U_j0|²` pour i≠j.
Le contrôle distinguable somme les routages indépendants, sans terme
d'interférence. Les erreurs de comparaison les plus grandes observées sur
les trois contrôles sont de l'ordre de 10⁻¹⁶ ; elles figurent exactement dans
chaque référence. Tolérance d'acceptation : 10⁻¹⁰. Cette vérification porte
sur les trois circuits n=4, pas sur un compilateur générique de tous unitaires.

## Échecs conservés et correction

La première suite complète s'est arrêtée en collection parce que le sparse
checkout ne rendait pas visible `experiments/phase2_classical_search.py`.
Après ajout des fichiers d'expérience existants au checkout, 308 tests ont
passé et deux tests d'infrastructure ont échoué faute des fichiers `.qwen`
versionnés. Ceux-ci ont été rendus visibles, sans édition.

Un essai suivant a donné 310 PASS et un échec nouveau : `git status` a dépassé
son timeout de cinq secondes pendant la production d'une provenance. Le
code traite maintenant les métadonnées Git indisponibles comme `null`, avec
`git_metadata_status="unavailable"`, en conservant les hashes des sources.
Un test mock impose cet échec et empêche de le convertir en arbre « propre ».
La suite finale ci-dessus passe après ce correctif.

## Démonstration conservée

`qpu/offline_pilot_20261124_v1/reproduce.py` recrée huit bundles dans une
nouvelle destination. Le dossier `run-v1` contient les résultats exécutés,
1000 tirages synthétiques par circuit et deux fichiers de counts
`local_synthetic`. Les analyses avec et sans dénominateur utilisent exactement
les mêmes counts ; dans la seconde, les métriques physiques restent `null`.
Le manifeste global donne les hashes, versions, UTC et hash du driver.

Les références ont été générées avant le commit de livraison : le manifeste
identifie donc le commit de base, l'état dirty explicite ou indisponible,
et surtout les hashes exacts du code exécuté. Il ne prétend pas que le code
non committé appartenait au commit de base. Une reproduction après commit
écrira une nouvelle provenance, sans modifier cette démonstration.

## Non-validations et portes restantes

La compilation vérifiée est la construction locale de portes BS/PERM et
leur sérialisation, à une phase globale commune près. Aucune compilation
native Belenos, préparation d'entrée réelle, efficacité, visibilité,
réponse PNR, calibration ou allocation de compte n'est validée.
Le JSON de job est un contrat interne non soumis ; aucun adaptateur de
soumission, polling ou récupération distante n'est livré.

Les documents officiels actuels ont été ouverts sur les domaines Quandela
et Perceval v1.3 ; leur dictionnaire et leurs limites sont cités dans
`docs/QPU_COMPATIBILITY.md`. Le catalogue Belenos annonce 24 modes ; cela
ne valide ni les anciens « 12 modes », ni une topologie Clements native,
ni l'accès PNR de ce compte. Le workflow 1.3 a changé ; l'exécution distante
exigerait un adaptateur distinct, vérifié et autorisé.

L'analyse suppose des essais iid et une définition documentée des filtres.
Elle refuse les seuils ou filtres non pris en charge, les comptes incohérents,
les données threshold et plus de deux photons. Un vrai événement hors modèle
doit rester dans le raw et motiver une extension séparée ; son rejet par le
pilote n'autorise pas à l'effacer des données matérielles.
Aucune conclusion de performance matérielle ou d'avantage quantique ne
provient de cette livraison.

## Contrôle final des artefacts

Le driver de démonstration a terminé avec retour 0 en **65.021 secondes**,
sous une limite de 120 secondes. `run-v1/` contient **19 fichiers, 82 694
octets**. Une vérification séparée a recalculé tous les hashes du manifeste
global, des huit manifests d'étape et des sources exécutées : PASS. Le job
reste non soumis/non autorisé ; le contrôle des dénominateurs inconnus et de
la borne géométrique non finie du HOM sans succès a également passé.

- Manifeste global SHA-256 :
  `4dcbf4f496f32f4c02f927689da706cc574fe01238ae50cfd9fb8512ebe0d4ed`.
- Référence `artifact.json` SHA-256 :
  `a2a71dbf9ee678a87419cb66b1d274eb18954cf6da0221c380b15b3ab010f2c4`.
- Counts locaux synthétiques SHA-256 :
  `d0f609c98c8c10a2990bc0dc73068e5169aa2db6f823f0229cfa26cd10b105e3`.

Reproduction exacte du chemin de calcul, vers une **nouvelle destination** :

```sh
PYTHONPATH=/Users/karimelhoudaigui/Desktop/pasqal/.qwen/worktrees/recovery-qpu-20261124/src /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python qpu/offline_pilot_20261124_v1/reproduce.py --output /tmp/pbp-laurent-reproduced-new
```
