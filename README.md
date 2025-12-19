# 🚀 API de Gestion de Tâches (TODO) - Django REST Framework

## 📋 Description du Projet

API REST complète pour la gestion de tâches développée avec **Django** et **Django REST Framework**. Ce projet répond aux spécifications du test technique pour un poste de Développeur Backend.

### ✨ Fonctionnalités principales
- ✅ **CRUD complet** via API REST
- ✅ **Documentation interactive** Swagger/OpenAPI
- ✅ **Tests unitaires** complets (20 tests)
- ✅ **Déploiement** sur PythonAnywhere
- ✅ **Pagination automatique** des résultats
- ✅ **Validation des données** robuste

## 🔗 URLs du Projet Déployé

- 🌐 **URL principale de l'API** : `https://[votre-username].pythonanywhere.com`
- 📚 **Documentation Swagger UI** : `https://[votre-username].pythonanywhere.com/api/docs/`
- 📄 **Schéma OpenAPI** : `https://[votre-username].pythonanywhere.com/api/schema/`

## ⚠️ Limitations du Plan Gratuit PythonAnywhere

Le projet est déployé sur le plan gratuit de PythonAnywhere, qui présente les limitations suivantes :

| Limitation | Impact sur le projet |
|------------|----------------------|
| **Mise en veille après 3 mois d'inactivité** | Le compte est désactivé après 3 mois sans connexion |
| **Redémarrage manuel requis** | Après modifications du code, redémarrage manuel nécessaire via le dashboard |
| **512 Mo d'espace disque** | Suffisant pour ce projet (base de données SQLite + code) |
| **Pas de processus en arrière-plan** | Impossible d'exécuter des tâches planifiées (non nécessaire ici) |
| **Base de données SQLite uniquement** | Parfait pour un projet de démonstration |

**Note importante** : Si l'API semble lente au premier chargement, c'est normal car PythonAnywhere réveille l'application après une période d'inactivité.

---

## 🛠️ Installation Locale

### Prérequis
- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Étapes d'installation

1. **Cloner le dépôt**
   git clone https://github.com/votre-username/todo-api-django.git
   cd todo-api-django

2. **Créer un environnement virtuel**
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

3. **Installer les dépendances**
    pip install -r requirements.txt

4. **Initialiser la base de données**
    ### Si vous utilisez une base de données autre que SQLITE, 
    ### vous devez d'abord créer la base de données avant de l'initialiser
    python manage.py migrate

5. **Lancer le serveur**
    python manage.py runserver


6. **L'application sera accessible aux URLs suivantes :**
    _Interface API : http://localhost:8000/_
    _Administration Django : http://localhost:8000/admin/_
    _Documentation Swagger : http://localhost:8000/api/docs/_

7. **Exécuter les tests**
    # Exécuter tous les tests
    python manage.py test tasks



8. **Informations Supplémentaires**
## Justification du choix
    PythonAnywhere pour le déploiement

        Support natif de Django

        Base de données SQLite incluse

        Interface de gestion simple

        Idéal pour projets de démonstration

    Structure d'API RESTful

        URLs sémantiques (/api/tasks/, /api/tasks/{id}/)

        Méthodes HTTP appropriées (GET, POST, PUT, PATCH, DELETE)

        Codes de statut HTTP significatifs

    Documentation auto-générée

        drf-spectacular pour OpenAPI 3.0

        Interface Swagger UI interactive

        Exemples de requêtes intégrés


Pour tester l'application déployée :

    Visitez l'URL principale pour voir la page d'accueil de l'API

    Utilisez /api/docs/ pour explorer l'API interactivement

    Testez les endpoints CRUD directement depuis Swagger UI

    Vérifiez les tests unitaires dans le dépôt Git
