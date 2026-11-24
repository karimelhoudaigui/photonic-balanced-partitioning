# Compatibilité Quandela / Perceval — contrôle officiel du 24 novembre 2026

**Outil local opérationnel ; exécution distante non implémentée et non vérifiée.**
Ce document remplace les hypothèses techniques du protocole ancien pour ce
pilote. Il n'atteste aucun accès au compte, créneau, crédit ou étalonnage.
Aucune connexion à un service de compte n'a été effectuée.

## Sources primaires consultées

| Source officielle, version et section | Ce qu'elle permet d'affirmer | Ce qu'elle ne vérifie pas ici |
| --- | --- | --- |
| [Quandela, Belenos, « Technical Specifications »](https://www.quandela.com/products-and-services/belenos/) ; consultée 2026-11-24 | Le produit public MOSAIQ-12 annonce 24 modes, une puce universelle et Perceval parmi les environnements. | Disponibilité effective d'un backend, allocation de ces modes, native Clements, PNR ou fidélité du pilote. Douze qubits ne signifie pas douze modes. |
| [Perceval v1.3, « Remote Computing », sections II et V](https://perceval.quandela.net/docs/v1.3/notebooks/Remote_Computation_Tutorial.html) | L'exemple `sim:belenos` affiche des contraintes de 24 modes et 12 photons, sans multiphotons à l'entrée ; les maxima de shots et d'échantillons arrêtent l'acquisition au premier seuil atteint. Le filtrage et le photon recycling sont des paramètres distincts. | Ce snapshot de tutoriel ne vaut pas interrogation des spécifications du QPU ni du compte. Les 12 photons de cet exemple ne sont pas une garantie de préparation aujourd'hui. |
| [Perceval v1.3, « RemoteProcessor », Input state et Miscellaneous](https://perceval.quandela.net/docs/v1.3/reference/runtime/legacy/remote_processor.html) | Le workflow legacy documente des capacités et contraintes par plateforme ; le type de détection peut dépendre du matériel. Les commandes illustrées sont `sample_count` et `samples`. | La documentation ne certifie pas notre accès ni un détecteur PNR. Aucun objet distant n'est créé par le nouvel outil. |
| [Perceval v1.3, « Legacy », Breaking changes in Perceval 1.3](https://perceval.quandela.net/docs/v1.3/legacy.html) | Le nouveau workflow distingue `Experiment`, `RemoteComputer` et `ExecutionFactory`. Le runtime ancien demeure dans `perceval.runtime.legacy` ; les deux workflows ne doivent pas être mélangés. | Aucun adaptateur distant n'a été implémenté ou testé ici. Le brouillon JSON local n'est pas une requête fournisseur. |
| [Perceval v1.3, « Circuit », add et compute_unitary](https://perceval.quandela.net/docs/v1.3/reference/components/circuit.html) | Les circuits locaux sont composables avec des composants unitaires ; `compute_unitary` fournit leur matrice. | La construction BS/PERM vérifiée localement ne valide ni le routage physique ni la compilation vers la puce. |
| [Perceval v1.3, « serialization legacy »](https://perceval.quandela.net/docs/v1.3/reference/serialization/legacy.html) | `serialize` et `deserialize` permettent le round-trip des circuits et composants ; cette API est documentée comme legacy. | Les exports ne sérialisent aucun Processor/compte. La compatibilité hors de la version épinglée nécessite une nouvelle validation. |

Les liens ont été ouverts sur les domaines officiels. Les spécifications
publicitaires de fidélité ne sont pas employées comme modèle de bruit.
La compatibilité locale repose en plus sur les tests exécutés avec
`perceval-quandela==1.3.0`, `exqalibur==1.4.2`, NumPy 2.4.6 et SciPy 1.17.1.
Ces versions sont déjà épinglées dans le projet ; aucune dépendance ajoutée.

## Matrice de décision pour le pilote

| Besoin du pilote | Vérifié localement | Reste à obtenir avant toute exécution autorisée |
| --- | --- | --- |
| Quatre modes ; entrée Fock `|1,1,0,0>` | Oui, matrice 4×4 et SLOS | Préparation, routage réel, contraintes d'entrée et mapping des sorties |
| Identité, BS Rx HOM, mélange par paires | Oui, portes BS/PERM, matrice analytique indépendante | Traduction vers les composants effectivement programmables et sa validation |
| Distribution complète des dix occupations à deux photons | Oui, formule fermée, Ryser et SLOS | PNR effectif, réponse du détecteur, pertes, multiphotons et événements hors modèle |
| Bisection de taille deux | Oui, CF signifie exactement deux occupations unitaires dans le modèle idéal | Traitement des pertes et du filtrage ; un faible taux de coïncidences n'est pas une validation isolée de la source ou du détecteur |
| Coût par tentative physique | Simulation idéale seulement | Compteur physique authentifié, détail des rejets et définition de l'arrêt |
| Données brutes et reprise | Analyse locale versionnée par hash | Export fournisseur, provenance et conservation brute ; aucune récupération réseau automatisée |
| Autorisation/crédits | Faux / zéro | Autorisation explicite avec plafond distinct ; aucune soumission par cet outil |

Pour le contrôle HOM idéal, la probabilité CF vaut zéro pour deux photons
indiscernables et 1/2 pour deux photons distinguables. Une mesure réelle demande
un modèle de pertes, de détection et de visibilité ; le seul accord avec ce
nombre ne prouve pas la disponibilité PNR.

Le statut « READY FOR SUBMISSION », « Clements natif », « PNR disponible » et les
disponibilités annoncées dans `reports/QPU_PROTOCOL.md` sont donc **non établis**.
Le nouveau chemin est exclusivement
`python -m photonic_balanced_partitioning.hardware` ; les anciens entrypoints
restent inchangés et fermés.
