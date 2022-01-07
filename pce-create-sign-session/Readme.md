# PCE Sign Session planner
Ce script sert à planifier des session de l'activitée `W-ADM-007/LYN-0-1/acti-505014` pour les signatures de présence des formations courtes à Epitech Lyon.

## Les formations supportés
- Wac1
- Wac2
- Codac
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
```
pipenv install
```

# Executer le script
```
pipenv run pyton create_sign_sessions.py
```
## Prérequis
Pour que le script fonctionne correctement, un dossier `Promotions` contenant les listes des apprenants par formations est requis. Par default, les fichier doivent être només comme suit :
```
{
    'codac': 'CODAC.csv',
    'msc1': 'MSC1.csv',
    'msc2': 'MSC2.csv',
    'premsc': 'PreMSC.csv',
    'wac1': 'WAC1.csv',
    'wac2': 'WAC2.csv'
}
```
# Informations pratiques
Pour le moment un peu de configuration au sein du script est nécéssaire 

## Si l'on veux choisir les formations à inscrire de force aux sessions créés
Il faut modifier la variable `selected_formation` et y ajouter les noms des formations en minuscule.

## Si l'on veux choisir la date de création des sessions
Il faut modifier la variable `selected_dates` et y ajouter les dates sous le format `%YYYY-%MM-%DD` 

**Exemple :** `'2022-01-17'`

## Pour l'authentification à l'intranet
Ce script utilise deux manière de s'authentifier :
- En allant chercher la variable d'environnement `INTRANET_TOKEN` (c'est à l'utilisateur de renseigner dans son environnement son token d'intra)
- Si le token n'est pas présent dans l'environnement le script va chercher le `cookie` de firefox si il existe
sinon le script fera une erreur.