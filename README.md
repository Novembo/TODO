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

## Déploiement gratuit recommandé : Render + Neon

Pour déployer l'API gratuitement de manière fiable et alignée avec vos autres projets (`auth-rbac-api`, `freelance-site`), la combinaison **[Render](https://render.com/)** + **[Neon](https://neon.tech/)** est la solution éprouvée.

### Pourquoi Render + Neon ?
- **Cohérence :** Même plateforme que vos projets en production.
- **Base PostgreSQL pérenne :** La base PostgreSQL gratuite de Neon (1 Go de stockage, SSL inclus) ne subit pas l'expiration à 30 jours de la base native de Render.
- **Simplicité :** Déploiement direct en mode **Web Service** standard (sans complexité de Blueprint).

### Déploiement en 4 étapes simples

1. **Créer la base de données PostgreSQL gratuite sur Neon :**
   - Créez un projet gratuit sur [neon.tech](https://neon.tech/) et nommez la base `todo`.
   - Copiez la chaîne de connexion fournie `DATABASE_URL` (assurez-vous qu'elle inclut `?sslmode=require`).

2. **Créer le Web Service sur Render :**
   - Sur votre tableau de bord [dashboard.render.com](https://dashboard.render.com/), cliquez sur **New +** → **Web Service**.
   - Connectez votre dépôt GitHub `Novembo/TODO` (branche `main`).
   - Renseignez les paramètres suivants :
     - **Name :** `novembo-todo-api`
     - **Region :** Frankfurt (EU Central)
     - **Runtime :** Python 3 (ou Docker)
     - **Build Command :** `bash build.sh`
     - **Start Command :** `gunicorn Todo.wsgi:application --bind 0.0.0.0:$PORT`
     - **Instance Type :** Free

3. **Définir les variables d'environnement dans Render :**
   Dans la section **Environment Variables** :
   - `DEBUG` : `False`
   - `SECRET_KEY` : Cliquez sur *Generate* ou saisissez une clé secrète forte.
   - `DATABASE_URL` : Collez l'URL de connexion Neon copiée à l'étape 1.
   - `TYPE_DATABASE` : `POSTGRES`
   - `DATABASE_ENGINE` : `django.db.backends.postgresql`
   - `DATABASE_NAME` : `todo`

4. **Déployer et tester :**
   - Cliquez sur **Deploy Web Service**.
   - Une fois le déploiement terminé, testez les routes :
     - `/` : Message d'accueil JSON.
     - `/api/docs/` : Documentation Swagger UI.
     - `/api/tasks/` : CRUD des tâches.

---

### Alternative 100% permanente : Alwaysdata

Si vous préférez un hébergeur entièrement gratuit à vie sans mise en veille :
- **[Alwaysdata](https://www.alwaysdata.com/)** propose un plan gratuit permanent (1 Go d'espace, 256 Mo de RAM, 0.25 vCPU, certificats HTTPS Let's Encrypt automatiques, bases PostgreSQL et MySQL natives).
- La configuration se fait via l'espace d'administration ou SSH en déclarant un site WSGI pointant vers `Todo/wsgi.py`.

> **Note sur Koyeb :** Suite au rachat de Koyeb par Mistral AI (Mistral Compute), la création autonome d'applications web classiques et de bases de données grand public a été suspendue sur leur console.  
> **Note sur PythonAnywhere :** L'ancienne instance (`solv2.pythonanywhere.com`) n'est plus maintenue en raison de ses limitations (absence de PostgreSQL natif gratuit, mise en pause trimestrielle).

---

## Limites du plan gratuit Render

- **Mise en veille après inactivité :** Les services web gratuits se mettent en veille après 15 minutes d'inactivité. La première requête après une période d'inactivité peut nécessiter 40 à 60 secondes pour réveiller le conteneur.
- **Stockage éphémère :** Le conteneur Web réinitialise son système de fichiers à chaque redémarrage. Toutes les données persistantes sont conservées dans la base Neon PostgreSQL.

---

## Récapitulatif des variables d'environnement

| Variable | Local (.env) | Production (Render / Neon) | Rôle |
|---|---|---|---|
| `DEBUG` | `True` | `False` | Active/désactive le mode débogage Django |
| `SECRET_KEY` | *(auto-générée si DEBUG)* | Clé aléatoire robuste | Clé cryptographique Django |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | `.onrender.com,localhost` | Domaines autorisés pour les requêtes HTTP |
| `DATABASE_URL` | *(vide en local)* | `postgresql://...` | Chaîne de connexion PostgreSQL Neon |
| `TYPE_DATABASE` | `SQLITE` | `POSTGRES` | Type de base de données |
| `CORS_ALLOWED_ORIGINS`| `http://localhost:8000` | Domaines frontend autorisés | Origines CORS acceptées |
