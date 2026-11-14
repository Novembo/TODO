# TODO — API de gestion de tâches

[![CI](https://github.com/Novembo/TODO/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Novembo/TODO/actions/workflows/ci.yml)

API REST de gestion de tâches construite avec Django REST Framework. Elle propose les opérations CRUD, la pagination et une documentation OpenAPI/Swagger.

**Stack :** Django · Django REST Framework · drf-spectacular · SQLite en local · PostgreSQL en hébergement · WhiteNoise

## Fonctionnalités et documentation

- CRUD des tâches sur `/api/tasks/` et `/api/tasks/{id}/`
- Pagination configurable par `page_size` (maximum : 100)
- Documentation Swagger UI : `/api/docs/`
- Schéma OpenAPI : `/api/schema/`

## Lancer en local

Prérequis : Python 3.10 ou plus récent.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

L'API est disponible sur `http://127.0.0.1:8000/`.

Les paramètres de `.env` sont chargés en local. `SECRET_KEY` est générée temporairement lorsque `DEBUG=True`; définissez une clé via l'environnement pour tout déploiement avec `DEBUG=False`.

## Tests

```bash
python manage.py check
python manage.py test tasks
```

Le workflow GitHub Actions exécute ces commandes sur les pull requests vers `main` et les pushes sur `main`.

## Déploiement gratuit recommandé : Render + Neon

Le dépôt contient `render.yaml` et `build.sh` pour créer un service Django gratuit sur Render. Le déploiement automatique est déclenché uniquement lorsque les vérifications CI réussissent.

1. Créez une base PostgreSQL gratuite sur [Neon](https://neon.tech/) et copiez sa chaîne de connexion `DATABASE_URL` avec SSL.
2. Dans Render, choisissez **New → Blueprint** et connectez `Novembo/TODO`.
3. Fournissez la chaîne Neon lorsque Render demande `DATABASE_URL`. Render génère `SECRET_KEY`; ne la placez pas dans Git.
4. Après le premier déploiement, vérifiez `/`, `/api/docs/` et `/api/tasks/`.

`DATABASE_URL` et `SECRET_KEY` sont configurées dans Render, pas dans les variables GitHub Actions. Le nouveau déploiement démarre avec une base Neon vide : les données de l'ancienne instance PythonAnywhere ne sont pas transférées automatiquement. Gardez cette instance jusqu'à validation et export des données si nécessaire.

**Limites du gratuit (vérifiées en novembre 2026) :** Render met en veille un service inactif après 15 minutes; le réveil peut prendre environ une minute, et son système de fichiers est éphémère. Neon Free offre jusqu'à 1 Go de stockage et suspend le calcul après inactivité; il n'inclut pas les sauvegardes des plans payants. La base PostgreSQL gratuite de Render expire après 30 jours, elle n'est donc pas utilisée ici. Cette combinaison convient à une démo ou un projet personnel, pas à une application exigeant une disponibilité ou des sauvegardes garanties.

## Configuration des variables

Les variables non secrètes `DEBUG`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CORS_ALLOW_METHODS`, `TYPE_DATABASE`, `DATABASE_ENGINE` et `DATABASE_NAME` sont enregistrées comme variables du dépôt pour le CI. Les secrets de déploiement restent dans le gestionnaire de secrets de l'hébergeur.
