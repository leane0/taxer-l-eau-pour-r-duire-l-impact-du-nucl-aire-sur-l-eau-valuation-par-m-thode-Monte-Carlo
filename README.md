# taxer-l-eau-pour-réduire-l-impact-du-nucléaire-sur-l-eau-évaluation-par-méthode-Monte-Carlo

Ce code est associé au mémoire « Taxer l’eau pour adapter le nucléaire au réchauffement climatique ? Évaluation par simulation Monte Carlo des redevances sur la ressource en eau » réalisé dans le cadre de mon master d'Economie de l'Energie. Il permet de calculer les distribution des VAN, du ROI, et leur fonction de répartition de projets d'ajout de tour aéroréfrigérante à Tricastin, Bugey et Saint-Alban et celui d'ajout d'aéroréfrigérant sur purge sur les autres centrales en bord de rivière et fleuve, en circuit semi-fermé.

## Installation

Le code fonctionne en python 3.8.8. Il nécéssite les bibliothèques suivantes :

- NumPy
- Matplotlib
- Pandas
- SALib

Pour installer les dépendance éxecuter :

`pip install numpy matplotlib pandas SALib`

En cas de problème se référer à la documentation des bibliothèques : [numpy](https://numpy.org/install/), [matplotlib](https://matplotlib.org/stable/install/index.html), [pandas](https://pandas.pydata.org/docs/getting_started/install.html) ou [SALib](https://salib.readthedocs.io/en/latest/user_guide/getting-started.html).

## Exécution

Pour lancer l'ensemble du code et générer les graphiques, exécuter le fichier `main.py` depuis le répertoire principal du projet.

Pour construire les fonctions de répartition, éxecuter `utils/plot_distrib.py`.

## Résultats

Les résultats sont dans le dossier `results/` :

- `results/results.csv` pour les résultats sous format csv
- `results/CNPE/scenario/` pour les graphiques représentant la VAN, le ROI, les graphiques tornade, les indices de Sobol, la convergence.
- `results/CDF/` pour les comparaison de fonctions de répartition entre centrales.
