# EpitechEventPlanner
Planificateur d'evenements automatique pour l'activitée `W-ADM-007/LYN-0-1/acti-505014`

## CLI 
`pipenv run python .` 

## Interface 
`pipenv run python interface.py`

## Build Interface
`pipenv run python setup.py`

## Tests
`pipenv run python tests.py`

## Les formations supportés
- Wac1
- Wac2
- Pre-msc
- Msc1
- Msc2

# Installer les dépendances du projet
Le projet à peu de dépendances mais pour des raisons de maintenabilité un environnement pipenv, un `Pipfile`, est fourni avec le projet.

## Installer les dépendances
```sh
pipenv install
```
# Executer le script
```sh
pipenv run pyton . --promotion wac1 "2022-01-17" "2022-01-18"
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

# TODO
- [x] Permettre à l'utilisateur de cocher les jours de création des activitées
- [x] Permettre à l'utilisateur de spécifier les heures de planification
- [ ] Permettre à l'utilisateur de spécifier l'activitée dans laquelle créer des evenements