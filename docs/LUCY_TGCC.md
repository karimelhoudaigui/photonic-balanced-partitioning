# Laurent — lancer le pilote sur Lucy via TGCC

Version du 24 novembre 2026. **L'adaptateur est implémenté et testé localement
avec un transport simulé. L'accès réel TGCC, la compilation matérielle et
l'acquisition restent à vérifier sur le compte autorisé. Aucune soumission
matérielle n'a été faite lors de cette livraison.**

## Accès confirmé par la documentation officielle

Le [CEA, pile quantique TGCC, sections Connection et Using Lucy](https://www-hpc.cea.fr/tgcc-public/en/html/toc/QuantumSoftwareStack.html#using-lucy)
documente Irène, le conteneur `ccc-quantum` et la passerelle
`qlmaas.qpus.QuandelaQPU` avec `perceval_interop.MyQLMHelper`. Les droits
relèvent d'un projet eDARI. Le présent dépôt utilise cette route ; aucun jeton
Quandela Cloud n'est à ajouter au dépôt. La connexion est configurée par TGCC.
Les capacités et performances annoncées ne certifient pas le compte ni la
calibration du jour.

L'[API officielle Perceval Interop](https://perceval.quandela.net/interopdocs/v1.3/reference/myqlm.html)
documente la conversion des requêtes et résultats. Les versions du conteneur
doivent être enregistrées avant mesure ; ne pas remplacer ses bibliothèques par
une installation globale du lock macOS. Le venv local épinglé et l'environnement
TGCC sont deux environnements distincts. Le code utilise les seules interfaces
documentées et refuse une reconstruction optique incohérente avec le pilote.

## 1. Récupérer le dépôt et vérifier le calcul local

```sh
git clone https://github.com/karimelhoudaigui/photonic-balanced-partitioning.git
cd photonic-balanced-partitioning
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements-research-lock.txt
.venv/bin/python -m pip install -e '.[all]'
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python -m pytest tests/ -q
.venv/bin/python scripts/build_publication.py --check
PYTHONPATH=src .venv/bin/python qpu/offline_pilot_20261124_v1/reproduce.py --output /tmp/pbp-pilot-new
```

Ce dernier calcul est intégralement local. Utiliser un nouveau dossier.
Lire ensuite [le PDF](../paper/main.pdf), [le catalogue des résultats](../results/README.md)
et [le contrat d'analyse PNR](LAURENT_HANDOFF.md).

## 2. Sur la session TGCC habituelle de Laurent

L'alias SSH, le projet et la partition dépendent du compte. Ils ne sont pas
déduits du nom de la machine et aucun faux endpoint n'est fourni. Depuis la
copie du dépôt accessible à la session autorisée :

```sh
pcocc-rs run ccc-quantum
# Dans le conteneur, se placer à la racine du dépôt.
export PYTHONPATH="$PWD/src"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python3 -m photonic_balanced_partitioning.hardware.lucy_tgcc environment
python3 -m photonic_balanced_partitioning.hardware.lucy_tgcc plan \
  --circuit identity --max-shots 1000 --max-samples 1000 \
  --wall-seconds 600 --output results/qpu/lucy-identity-plan-01
```

Ces deux commandes ne chargent aucun client distant. Le plan contient une
seule entrée `|1,1,0,0>`, quatre modes et le circuit déjà validé. `identity`
vérifie le routage ; `hom` et `pair_mixing` se préparent dans des plans séparés
après examen du premier résultat. Aucun optimiseur n'est lancé sur le QPU.
Les cinq circuits P40 ne sont pas encore inclus dans cet adaptateur.

Les simulations lourdes doivent utiliser un nœud de calcul. Le CEA documente
`ccc_mprun -C ccc-quantum -p <partition> -c <coeurs> python3 <script.py>` ; les
paramètres concrets restent ceux de l'allocation. Une réservation HPC ne vaut
pas autorisation QPU. Le lanceur ne soumet aucun job au scheduler et n'invente
aucune partition TGCC.

## 3. Examiner les spécifications sans lancer d'acquisition

Cette commande, à exécuter par l'opérateur sur TGCC, contacte uniquement la
passerelle pour les spécifications ; elle n'appelle pas `submit` :

```sh
python3 -m photonic_balanced_partitioning.hardware.lucy_tgcc specs \
  --allow-remote-query --output results/qpu/lucy-specs-01
```

Vérifier modes/photons autorisés, mapping entrée/sortie, détection réellement
PNR, filtres, absence de mitigation/recycling et calibration contemporaine.
Les spécifications numériques et le nom exact du fournisseur attendu sont
contrôlés à nouveau juste avant soumission. Recopier `provider_name` depuis
`specs.json` dans `expected_provider_name` ; aucun identifiant n'est inventé.
Les autres vérifications sont des confirmations explicites de l'opérateur,
pas des propriétés que l'adaptateur peut démontrer depuis un nom de backend.
Si PNR n'est pas confirmé, conserver le plan et adapter le protocole avec
Laurent avant de lancer ce pilote de collisions.

## 4. Après autorisation explicite pour le plan exact

Copier `qpu/configs/lucy_authorization.example.json` vers
`qpu/authorization.local.json` (ignoré par Git). Renseigner l'opérateur,
la référence d'autorisation, les preuves techniques examinées et la SHA-256
du fichier `plan.json` (`sha256sum` sur TGCC). Les indicateurs restent `false`
dans l'exemple ; ils ne doivent devenir `true` qu'après les vérifications
effectives. Ne pas ajouter de mot de passe, jeton ou clé dans ce fichier.

```sh
python3 -m photonic_balanced_partitioning.hardware.lucy_tgcc run \
  --execute-qpu \
  --plan results/qpu/lucy-identity-plan-01/plan.json \
  --authorization qpu/authorization.local.json \
  --output results/qpu/lucy-identity-capture-01
```

Un appel crée au maximum **un job**, sans retry automatique. Le plafond du
plan ne peut dépasser celui autorisé ; la limite logicielle absolue est de
10 000 shots. Le dossier de sortie doit être neuf et le plan est marqué
exclusivement avant `submit`. Un plan déjà marqué ne peut pas resoumettre.
Cette protection est locale au dossier du plan ; elle ne fournit pas
d'idempotence globale entre ses copies ou plusieurs clones. Ne pas copier
un plan pour contourner une interruption.
Le délai limite l'attente du processus ; il **n'annule pas** un job distant.
Après interruption, consulter le job existant avec les outils/support TGCC
avant toute nouvelle acquisition. Aucune API de reprise par ID non documentée
n'a été inventée. Les identifiants disponibles sont conservés lorsqu'exposés
par le client ; leur disponibilité dépend de sa version.

## 5. Données conservées et unités de coût

Le résultat binaire natif `vendor-result.res` et `vendor-metadata.json` sont
écrits **avant** décodage. La requête, les versions, le commit, les specs et
les empreintes sont conservés ; `perceval-result.json` est une copie décodée
sérialisée. Les anomalies restent dans le résultat natif, même si l'export
PNR normalisé échoue. Aucun fichier brut n'est écrasé.

Le [tutoriel officiel Perceval v1.3](https://perceval.quandela.net/docs/v1.3/notebooks/Remote_Computation_Tutorial.html)
définit les shots comme des détections non vides. Le pilote demande
`min_detected_photons=1`, `use_photon_recycling=false`, quatre modes retournés,
avec plafonds de shots et d'échantillons. Le vide n'est pas reconstruit.
**`physical_attempts:null` est conservé**, même si une performance fournisseur
est disponible. Aucune probabilité par photon injecté, par tentative ou TV
physique complète n'est déduite de ces seuls counts. La désactivation demandée
du recycling doit être confirmée côté fournisseur ; sa présence dans le payload
ne prouve pas qu'elle a été honorée.

`final_mode_number=4` peut aussi provoquer un rejet des événements contenant
des photons dans des modes non retournés. L'opérateur doit donc confirmer
explicitement `no_unreported_output_filtering:true` : tous les canaux du
protocole sont couverts et aucun filtre additionnel sur modes omis ne biaise
les counts. Sinon ce pilote refuse de démarrer ; il faut revoir le routage
ou préparer un protocole conservant tous les modes. Cette confirmation ne
peut pas être déduite de la seule taille de la matrice U ni d'un tableau
de counts déjà filtrés. Le contrat PNR v1 ne couvre pas un filtre de fuite
vers des modes omis.

L'export `normalized-counts.json`, s'il est valide, peut être analysé séparément :

```sh
python3 -m photonic_balanced_partitioning.hardware analyze_qpu_results \
  --bundle qpu/offline_pilot_20261124_v1/run-v1/reference \
  --results results/qpu/lucy-identity-capture-01/normalized-counts.json \
  --output results/qpu/lucy-identity-analysis-01
```

Les counts ne sont étiquetés PNR qu'en vertu de la confirmation opérateur.
Les événements à plus de deux photons ou de dimension inattendue bloquent
l'export normalisé et nécessitent une analyse dédiée ; ils ne sont pas éliminés
des données natives. Sans compteur d'émission authentifié, l'analyse conserve
les métriques physiques à `null` et ne calcule pas de TV non conditionnelle.

Les données matérielles et autorisations locales sont exclues de Git par défaut.
Après revue de provenance/confidentialité, une publication de données se prépare
explicitement ; ne jamais envoyer les credentials avec les résultats.

## Ce qui complétera la section QPU de l'article

Pour chaque circuit et session : résultat natif, calibration/source/détecteur,
mapping, filtres/mitigations effectifs, budgets et durée, compteur physique si
disponible, analyse avec intervalles, écarts aux références et contrôles
distinguables réalisables. Une visibilité différente ne peut pas être remplacée
par un paramètre fictif. Ce premier pilote teste la préparation et les effets
d'interférence ; un avantage d'optimisation demande un autre protocole comparatif.
Le manuscrit livré reste inchangé tant qu'aucune mesure authentique n'est acquise.
