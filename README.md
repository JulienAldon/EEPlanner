# EventOtron
Ce script sert à planifier des session de l'activitée `W-ADM-007/LYN-0-1/acti-505014` pour les signatures de présence des formations courtes à Epitech Lyon.

## Les formations supportés
- Wac1
- Wac2
- Pre-msc
- Msc1
- Msc2

## Que fait le script ? (En détail)

Le script instancie, à une date donnée (ou liste de dates), les sessions de l'activité `acti-505014` créée pour l'emargement des formations courtes (pce)
Le script créé 4 sessions pour une date donnée, une à 9:00-9:30, une à 12:00-12:30, une à 13:30-14:00 et une à 17:00-17h30.
Les heures de création de sessions sont evidement configurable grâce à la variable `planification_hours` dans le script.
Il inscrit ensuite, de force, tous les apprenant d'une formation à cette session.
Le script peut ajouter plusieurs formations à une même session.

# Installer les dépendances du projet
Le projet à peu de dépendances mais pour des raisons de maintenabilité un environnement pipenv, un `Pipefile`, est fourni avec le projet.

## Installer les dépendances
```sh
pipenv install
```

# Executer le script
```sh
pipenv run pyton create_sign_sessions.py --promotion wac1 "2022-01-17" "2022-01-18"
```

```sh
Usage: 
create_sign_sessions.py [-h] --promotion promotion [--events [events ...]] [dates in %Y-%m-%d ...]

Select promotions and dates or events

Positional arguments:
  dates in %Y-%m-%d

Optional arguments:
  -h, --help            show this help message and exit
  --promotion promotion, -p promotion
  --events [events ...]
```

Une fois le script éxécuté avec des dates et les différentes sessions instanciés, le script doit afficher sur la sorte standard une liste d'evenements créés.

Vous pouvez reutiliser cette liste pour inscrire les differentes promotions aux activités créées à l'aide du flag `--events`

# Lancer l'interface (dev)
```
pipenv run python interface.py
```

# Build l'interface
```
pipenv run python setup.py build
```

# TODO
- [ ] Permettre à l'utilisateur de cocher les jours de création des activitées
- [ ] Permettre à l'utilisateur de spécifier les heures de planification
- [ ] Permettre à l'utilisateur de spécifier l'activitée dans laquelle créer des evenements