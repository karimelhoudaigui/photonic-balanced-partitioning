# Recherche — points d'entrée

État au 27 novembre 2026 : **l'avantage d'optimisation reproductible reste à démontrer**.
Le manuscrit est conservé dans [paper/](../paper/README.md). Aucun résultat QPU
réel n'est disponible. L'historique scientifique complet reste dans
[RESEARCH_LOG.md](../RESEARCH_LOG.md) ; les décisions actuelles sont dans
[P45_LIVE_STATE.md](P45_LIVE_STATE.md).

| À consulter | Documents |
| --- | --- |
| Dernière recherche : P146, interactions effectives et réparation locale d'une ressource connue | **[Résultats et limites](P146_RESEARCH_RECEIPT.md)** ; [borne et instrument](P146_A_INTERACTION_ROUTE.md), [relecture indépendante](P146_A_INDEPENDENT_AUDIT.md), [données physiques](P146_full_instrument/run_001/) |
| P146 : passage à l'algorithme et à Lucy encore ouvert | [Contrôle classique et contre-exemple](P146_ALGORITHM_BRIDGE_VETO.md), [capacités à vérifier pour Laurent](P146_LUCY_INTERACTION_BRIDGE.md) |
| P145, propositions locales et interférence collective | [Résultats, preuves et reproduction](P145_RESEARCH_RECEIPT.md) ; [données exactes](P145_exact_fixture/run_001/), [pilote sur graphes](P145_declared_screen/run_001/) |
| Essai précédent : P141, absence de supériorité sur le meilleur contrôle de la grille | [Compte rendu](P141_FINITE_MAGNETIC_RECEIPT.md), [protocole](P141_FINITE_MAGNETIC_SCREEN_CARD.md), [données brutes](P141_finite_magnetic_main/run_001/) |
| P141 : contrôle des données enregistrées | [Relecture indépendante du lecteur corrigé](P141_RECORDED_READER_V2_INDEPENDENT_REVIEW.md), [sortie du contrôle](../reports/P141_validation_review/recorded_consistency_v2.json) ; le premier contrôle en échec est conservé à côté |
| Bornes récentes, avec hypothèses et limites | [P137](../reports/P137_ROOT_WEAK_REFLECTION_CHECKPOINT.md), [P139](../reports/P139_ROOT_ANALYTIC_OBSTRUCTION_CHECKPOINT.md), [P143](../reports/P143_ROOT_FINITE_INSTRUMENT_CHECKPOINT.md) |
| Dernier essai précédent : P134, absence de signal strict sur la grille | [Compte rendu](P134_RATIONAL_FRAME_RECEIPT.md) |
| Vérifications exactes P130 et P131 | [Identités sous pertes](P130_FEW_LOSS_IDENTITY_RECEIPT.md), [contrôle de phase](P131_PHASE_CONTROL_RECEIPT.md) |
| Portée des mécanismes et des sources | [P142](../reports/P142_ROOT_TRIAD_SCOPE_CHECKPOINT.md), [P144](P144_WEAK_INSTRUMENT_PRIMARY_SCOPE.md) |
| Article livré : P33, P37 et E05b | [Catalogue des résultats](../results/README.md), [article PDF](../paper/main.pdf) |

Sur le graphe ER de P141, le cas bosonique dépasse le contrôle distinguable
réoptimisé, mais reste derrière un contrôle par groupes de photons. Sur le
graphe RR, le contrôle distinguable est meilleur. Ce contraste local favorable
est conservé ; il ne démontre pas un avantage d'optimisation.

Les sources Python, contrats, données, échecs et relectures conservés dans ce
dossier permettent de vérifier les résultats et d'éviter de répéter les mêmes
pistes rejetées. Les contrôles sur données enregistrées ne constituent pas une
réplication physique indépendante.

Les anciennes cartes de questions P45-C/P47 et le plan de contrôle P53b ont été
retirés après remplacement par leurs preuves, programmes et comptes rendus.
Les anciennes copies narratives sont accessibles par les liens Git figés en
tête de l'état courant. Tous ces fichiers restent récupérables dans le
[dépôt avant nettoyage](https://github.com/karimelhoudaigui/photonic-balanced-partitioning/tree/b614d5259587fb5ab9897738206bca0d007715ae/research).

Pour l'équipe locale : [configuration Qwen](../.qwen/README.md).
Pour Laurent : [guide Lucy/TGCC](../docs/LUCY_TGCC.md). Le nettoyage n'autorise
aucune nouvelle expérience ou soumission QPU.
