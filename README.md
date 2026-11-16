# TODO — API REST de Gestion de Tâches

[![CI](https://github.com/Novembo/TODO/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Novembo/TODO/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0-092e20?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.15-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon%20Serverless-4169e1?logo=postgresql)
![Statut](https://img.shields.io/badge/D%C3%A9mo-Publique-informational)

API REST de gestion de tâches construite avec Django REST Framework. Elle propose les opérations CRUD, la validation des entrées, la pagination et une documentation OpenAPI.

> **Démo publique :** l’API n’exige pas d’authentification et toutes les tâches sont partagées. Elle sert à la démonstration; n’y envoyez pas de données personnelles ou sensibles. Utilisez l’environnement local pour les exemples qui créent, modifient ou suppriment des tâches.

Le dépôt illustre un backend Django/DRF avec pagination, schémas OpenAPI, tests automatisés et configuration de déploiement Render.

**Stack technique :** Python 3.12 · Django 5 · Django REST Framework · drf-spectacular · PostgreSQL (Neon Serverless) · SQLite (local) · Gunicorn · WhiteNoise · Docker · GitHub Actions

## Périmètre et limites

- les tâches ne sont pas rattachées à un compte utilisateur;
- les endpoints de création, modification et suppression sont accessibles sans authentification;
- la démo hébergée est publique et ne doit pas recevoir de données réelles.

## Méthodologie de travail

1. Définir les cas d’usage métier et la structure des ressources.
2. Construire un modèle et des sérialiseurs lisibles et cohérents.
3. Ajouter validation, pagination et schémas API explicites.
4. Tester les cas de succès et d’erreur avant mise en production.
5. Documenter l’API pour que le projet soit utilisable et maintenable.

---

## 🚀 Démo en ligne

L'API est hébergée sur **Render** et reliée à une base de données **PostgreSQL serverless sur Neon** :

- 📖 **Documentation Swagger UI :** [https://novembo-todo-api.onrender.com/api/docs/](https://novembo-todo-api.onrender.com/api/docs/)
- 🌐 **Point d'entrée racine :** [https://novembo-todo-api.onrender.com/](https://novembo-todo-api.onrender.com/)
- 📋 **Schéma OpenAPI v3 :** [https://novembo-todo-api.onrender.com/api/schema/](https://novembo-todo-api.onrender.com/api/schema/)
- ⚡ **Endpoint API des tâches :** [https://novembo-todo-api.onrender.com/api/tasks/](https://novembo-todo-api.onrender.com/api/tasks/)

---

## 📌 Endpoints de l'API

| Méthode | Endpoint | Description | Paramètres / Payload |
|---|---|---|---|
| `GET` | `/` | Informations sur l'API, version et sitemap | Aucun |
| `GET` | `/api/tasks/` | Liste paginée de toutes les tâches | `page` (défaut: 1), `page_size` (défaut: 10, max: 100) |
| `POST` | `/api/tasks/` | Création d'une nouvelle tâche | `title` *(requis)*, `description`, `is_completed` |
| `GET` | `/api/tasks/{id}/` | Détail d'une tâche spécifique | `id` (entier dans l'URL) |
| `PUT` | `/api/tasks/{id}/` | Remplacement complet d'une tâche | Tous les champs requis |
| `PATCH` | `/api/tasks/{id}/` | Modification partielle d'une tâche | Un ou plusieurs champs |
| `DELETE` | `/api/tasks/{id}/` | Suppression définitive d'une tâche | `id` (entier dans l'URL) |
| `GET` | `/api/docs/` | Interface interactive Swagger UI | Visualisation et test direct des requêtes |
| `GET` | `/api/schema/` | Spécification brute OpenAPI (YAML/JSON) | Consommable par Postman ou des générateurs SDK |

---

## 📂 Structure du projet

```text
TODO/
├── Todo/                       # Module de configuration global Django
│   ├── asgi.py                 # Point d'entrée ASGI
│   ├── settings.py             # Paramètres (env, BDD, WhiteNoise, DRF, CORS, Swagger)
│   ├── urls.py                 # Routage principal et endpoints de documentation
│   └── wsgi.py                 # Point d'entrée WSGI pour Gunicorn
├── tasks/                      # Application de gestion des tâches
│   ├── migrations/             # Historique des migrations du schéma de données
│   ├── admin.py                # Configuration de l'administration Django
│   ├── apps.py                 # Déclaration de l'application
│   ├── models.py               # Modèle Task (titre, description, is_completed, timestamps)
│   ├── serializers.py          # Validation des données et sérialisation REST
│   ├── tests.py                # Suite complète de 20 tests unitaires et d'intégration
│   ├── urls.py                 # Routage des vues tâches
│   └── views.py                # Vues API (home_view, liste, CRUD unitaire)
├── .github/workflows/          # Intégration continue (CI/CD)
│   └── ci.yml                  # Pipeline GitHub Actions (check, migrations, tests)
├── .dockerignore               # Fichiers exclus de l'image Docker
├── .env.example                # Modèle de variables d'environnement
├── .gitignore                  # Fichiers exclus du suivi Git
├── .python-version             # Épinglage de la version Python pour l'hébergeur (3.12.8)
├── build.sh                    # Script automatisé de déploiement (install, static, migrate)
├── Dockerfile                  # Image Docker multi-plateforme
├── manage.py                   # CLI de gestion Django
├── requirements.txt            # Dépendances de production et de test
└── README.md
```

---

## 💻 Lancer en local

### Prérequis
- Python 3.10 ou version ultérieure (recommandé : 3.11 ou 3.12).
- Git.

### Windows (PowerShell)

```powershell
# 1. Cloner le dépôt et entrer dans le dossier
git clone https://github.com/Novembo/TODO.git
cd TODO

# 2. Créer et activer l'environnement virtuel
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Installer les dépendances
python -m pip install -r requirements.txt

# 4. Configurer les variables d'environnement
Copy-Item .env.example .env

# 5. Appliquer les migrations de base de données
python manage.py migrate

# 6. Démarrer le serveur de développement
python manage.py runserver
```

### Linux / macOS (Bash)

```bash
# 1. Cloner le dépôt et entrer dans le dossier
git clone https://github.com/Novembo/TODO.git
cd TODO

# 2. Créer et activer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances
python -m pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env

# 5. Appliquer les migrations
python manage.py migrate

# 6. Démarrer le serveur
python manage.py runserver
```

L'application démarre immédiatement sur **`http://127.0.0.1:8000/`**.  
La documentation Swagger locale est disponible sur **`http://127.0.0.1:8000/api/docs/`**.

---

## 🧪 Tests unitaires et vérifications CI

Le projet dispose d'une suite complète de **20 tests unitaires** couvrant :
- L'intégrité du modèle `Task` (valeurs par défaut, contraintes de validation, ordonnancement).
- Les opérations de création, lecture, modification complète (`PUT`), partielle (`PATCH`) et suppression (`DELETE`).
- La validation des données d'entrée (titres vides, dépassement de 200 caractères).
- La pagination des résultats et le respect du `max_page_size`.
- Les codes de retour HTTP standards (200, 201, 204, 400, 404).

Pour exécuter les vérifications en local :

```bash
python manage.py check
python manage.py test tasks
```

Le workflow GitHub Actions (`.github/workflows/ci.yml`) exécute `manage.py check` et les tests sur chaque push et pull request vers `main`. Le manifeste Render configure l’auto-déploiement après succès des vérifications.

---

## 💡 Exemples locaux avec `curl`

L’API locale doit être démarrée sur `http://127.0.0.1:8000`. Les requêtes d’écriture ci-dessous ne ciblent volontairement pas la démo publique.

### 1. Consulter les tâches existantes
```bash
curl http://127.0.0.1:8000/api/tasks/
```

### 2. Créer une nouvelle tâche
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Découvrir l API TODO", "description": "Test de création en direct", "is_completed": false}'
```

### 3. Marquer une tâche comme terminée (`PATCH`)
```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"is_completed": true}'
```

### 4. Supprimer une tâche (`DELETE`)
```bash
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/
```

---

## ⚙️ Hébergement de démonstration

La démo est hébergée sur Render et utilise une base PostgreSQL configurée séparément :
- **Serveur d'application :** Hébergé sur **Render** (plan Web Service Free), propulsé par le serveur WSGI **Gunicorn**.
- **Fichiers statiques :** Optimisés, compressés et servis directement avec des en-têtes de cache pérennes via **WhiteNoise**.
- **Base de données :** Instance gérée **PostgreSQL Serverless sur Neon**, accessible via une connexion sécurisée chiffrée SSL (`sslmode=require`).
- **Automatisation du build :** Le script `build.sh` applique automatiquement les migrations de schéma (`migrate --noinput`) et rassemble les fichiers statiques (`collectstatic --no-input`) à chaque livraison.

### Variables d'environnement

| Variable | Exemple Local | Production (Render) | Rôle |
|---|---|---|---|
| `DEBUG` | `True` | `False` | Désactive les traces de débogage en production |
| `SECRET_KEY` | *(générée à la volée)* | Clé cryptographique forte | Sécurise les sessions, signatures et jetons |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | `.onrender.com,localhost` | Hôtes et noms de domaine autorisés par Django |
| `DATABASE_URL` | *(laissée vide)* | `postgresql://...neon.tech/...` | Chaîne de connexion PostgreSQL avec SSL requis |
| `TYPE_DATABASE` | `SQLITE` | `POSTGRES` | Pilote de base de données à charger |
| `DATABASE_ENGINE` | `django.db.backends.sqlite3` | `django.db.backends.postgresql` | Moteur ORM Django |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:8000` | Origines autorisées (ex: frontend web) | Autorisation des requêtes cross-origin |
