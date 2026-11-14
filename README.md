# TODO — API de gestion de tâches

[![CI](https://github.com/Novembo/TODO/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Novembo/TODO/actions/workflows/ci.yml)

API REST de gestion de tâches construite avec Django REST Framework. Elle propose les opérations CRUD complètes, la pagination configurable et une documentation OpenAPI / Swagger interactive.

**Stack technique :** Django 5 · Django REST Framework · drf-spectacular · WhiteNoise · SQLite (local) · PostgreSQL (hébergement) · Gunicorn · Docker

---

## Fonctionnalités et documentation

- **CRUD complet des tâches :** `/api/tasks/` et `/api/tasks/{id}/` (création, lecture, modification complète `PUT`, modification partielle `PATCH`, suppression `DELETE`)
- **Pagination configurable :** via le paramètre `page_size` (taille par défaut : 10, maximum : 100)
- **Documentation interactive Swagger UI :** `/api/docs/`
- **Schéma de spécification OpenAPI v3 :** `/api/schema/`
- **Point d'entrée racine :** `/` (présentation de l'API et liens rapides vers les endpoints)

---

## Lancer en local

### Prérequis
- Python 3.10 ou version ultérieure (testé avec Python 3.11 et 3.12).

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

L'API est immédiatement accessible sur `http://127.0.0.1:8000/`.

Les paramètres de `.env` sont chargés automatiquement au démarrage. La clé `SECRET_KEY` est générée à la volée lorsque `DEBUG=True`. En environnement de production avec `DEBUG=False`, définissez obligatoirement une clé secrète via la variable d'environnement `SECRET_KEY`.

---

## Tests et vérifications CI

Exécutez la suite de vérifications et les 20 tests unitaires :

```bash
python manage.py check
python manage.py test tasks
```

Le workflow GitHub Actions (`.github/workflows/ci.yml`) exécute automatiquement ces vérifications à chaque push et pull request sur la branche `main`.

---

## Hébergement gratuit recommandé : Koyeb (+ PostgreSQL Serverless)

Pour déployer l'API gratuitement et de manière pérenne, **[Koyeb](https://www.koyeb.com/)** est la solution recommandée.

### Pourquoi Koyeb est conseillé face aux alternatives :
1. **Pas d'expiration de la base de données :** Contrairement à Render dont la base PostgreSQL gratuite est automatiquement détruite après 30 jours, Koyeb intègre une base PostgreSQL Serverless gratuite et permanente (1 Go de stockage, propulsée par le moteur Neon).
2. **Instance Nano gratuite :** 512 Mo de RAM, 0.1 vCPU, région Europe (Francfort `fra`), aucun renseignement de carte bancaire requis à l'inscription.
3. **Déploiement déclaratif & automatique :** Déploiement continu automatisé à chaque `git push` sur `main` via `koyeb.yaml` ou le `Dockerfile` prêt à l'emploi.
4. **HTTPS & domaine mondial :** Certificat SSL géré automatiquement sur `*.koyeb.app`.

### Déploiement en 4 étapes simples sur Koyeb

1. **Créer la base de données PostgreSQL gratuite :**
   - Dans la console Koyeb, cliquez sur **Create** → **Database Service**.
   - Choisissez le moteur PostgreSQL (plan gratuit), nommez-le `todo-db`, région **Frankfurt (fra)**.
   - Copiez l'URL de connexion fournie (`DATABASE_URL`). *(Vous pouvez également utiliser directement une base gratuite [Neon](https://neon.tech/))*.

2. **Créer le service Web :**
   - Cliquez sur **Create** → **Service** → sélectionnez **GitHub**.
   - Connectez votre compte et choisissez le dépôt `Novembo/TODO` (branche `main`).
   - Le fichier `koyeb.yaml` configure automatiquement la commande de build (`bash build.sh`) et de démarrage (`gunicorn Todo.wsgi:application --bind 0.0.0.0:8000`).

3. **Configurer les variables d'environnement dans Koyeb :**
   Dans l'onglet **Environment variables** du service :
   - `DEBUG` : `False`
   - `SECRET_KEY` : *[votre clé secrète aléatoire de production]*
   - `DATABASE_URL` : *[la chaîne de connexion PostgreSQL avec sslmode=require]*
   - `TYPE_DATABASE` : `POSTGRES`
   - `ALLOWED_HOSTS` : `127.0.0.1,localhost,.koyeb.app`

4. **Déployer et vérifier :**
   - Cliquez sur **Deploy**.
   - Une fois le statut passé à `Healthy`, testez les routes :
     - `/` : Retour JSON de bienvenue.
     - `/api/docs/` : Interface Swagger UI interactive.
     - `/api/tasks/` : Liste et création des tâches.

---

### Alternative : Déploiement sur Render

Le dépôt conserve également la configuration `render.yaml` pour un déploiement sur [Render](https://render.com/). Pour Render, il est fortement conseillé de connecter une base externe gratuite sur [Neon](https://neon.tech/) car la base native de Render expire au bout de 30 jours.

> **Note sur l'ancien hébergement PythonAnywhere :** L'ancienne instance PythonAnywhere (`solv2.pythonanywhere.com`) n'est plus maintenue en raison de ses limitations (absence de PostgreSQL natif dans le plan gratuit, mise en pause trimestrielle manuelle).

---

## Limites du plan gratuit

- **Koyeb Free Tier :** 1 service web Nano gratuit (512 Mo RAM, calcul Eco avec mise en veille après inactivité puis réveil transparent à la première requête), 1 service PostgreSQL Serverless gratuit (1 Go de stockage).
- **Système de fichiers éphémère :** Les fichiers uploadés ou modifications locales du conteneur ne persistent pas lors des redémarrages (les données doivent impérativement résider dans la base PostgreSQL).

---

## Récapitulatif des variables d'environnement

| Variable | Local (.env) | Production (Koyeb / Render) | Rôle |
|---|---|---|---|
| `DEBUG` | `True` | `False` | Active/désactive le mode débogage Django |
| `SECRET_KEY` | *(auto-générée si DEBUG)* | Clé aléatoire robuste | Clé cryptographique Django |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | `.koyeb.app,.onrender.com` | Domaines autorisés pour les requêtes HTTP |
| `DATABASE_URL` | *(vide en local)* | `postgresql://...` | Chaîne de connexion PostgreSQL de production |
| `TYPE_DATABASE` | `SQLITE` | `POSTGRES` | Type de base de données |
| `CORS_ALLOWED_ORIGINS`| `http://localhost:8000` | Domaines frontend autorisés | Origines CORS acceptées |
