# syspathmodif

## FRANÇAIS

Cette bibliothèque offre des manières concises de modifier la liste `sys.path`.
L'utilisateur ne devrait pas avoir besoin d'interagir directement avec cette
liste.

### Contenu

Les fonctions de `syspathmodif` prennent un chemin de type `str` ou
`pathlib.Path` comme argument.
Elles convertissent les arguments de type `pathlib.Path` en `str` puisque
`sys.path` n'est censée contenir que des chaînes de caractères.

* `sp_append` ajoute le chemin donné à la fin de `sys.path`.
* `sp_contains` indique si `sys.path` contient le chemin donné.
* `sp_remove` enlève le chemin donné de `sys.path`.

Pour plus d'informations, consultez la documentation des fonctions et les démos
dans le dépôt de code source.

### Dépendances

Installez les dépendances de `syspathmodif` avant de l'utiliser.
```
pip install -r requirements.txt
```

Cette commande installe les dépendances de développement en plus des
dépendances ordinaires.
```
pip install -r requirements-dev.txt
```

### Démo

Le script dans le dossier `demo` montre comment `syspathmodif` permet
d'importer un paquet qui est indisponible tant qu'on n'a pas ajouté son chemin
à `sys.path`.
Il dépend du paquet `demo_package`.

Lancez la démo avec la commande suivante.
```
python demo/demo.py
```

### Tests automatiques

Cette commande exécute les tests automatiques.
```
pytest tests
```

## ENGLISH

This library offers concise manners to modify list `sys.path`.
The user should not need to directly interact with that list.

### Content

The functions in `syspathmodif` take a path of type `str` or `pathlib.Path`
as an argument.
They convert arguments of type `pathlib.Path` to `str` since `sys.path` is
supposed to contain only character strings.

* `sp_append` appends the given path to the end of `sys.path`.
* `sp_contains` indicates whether `sys.path` contains the given path.
* `sp_remove` removes the given path from `sys.path`.

For more information, consult the functions' documentation and the demos in the
source code repository.

### Dependencies

Install the dependencies before using `syspathmodif`.
```
pip install -r requirements.txt
```

This command installs the development dependencies in addition to the ordinary
dependencies.
```
pip install -r requirements-dev.txt
```

### Demo

The script in directory `demo` shows how `syspathmodif` allows to import a
package unavailable unless its path is added to `sys.path`.
It depends on `demo_package`.

Run the demo with the following command.
```
python demo/demo.py
```

### Automated Tests

Run the tests.
```
pytest tests
```
