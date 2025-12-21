# tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from .models import Task
import json

class TaskAPITestCase(TestCase):
    """Classe de test pour l'API Task"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.client = APIClient()

        # Création de tâches de test avec des dates explicites
        now = timezone.now()
        
        # Création de tâches de test
        self.task1 = Task.objects.create(
            title="Tâche de test 1",
            description="Description de la tâche 1",
            is_completed=False
        )
        # task1 est plus ancien
        Task.objects.filter(pk=self.task1.pk).update(created_at=now - timezone.timedelta(minutes=5))
        self.task1.refresh_from_db()
        
        self.task2 = Task.objects.create(
            title="Tâche de test 2",
            description="Description de la tâche 2",
            is_completed=True
        )
        # task2 est plus récente
        Task.objects.filter(pk=self.task2.pk).update(created_at=now)
        self.task2.refresh_from_db()
        
        # Données valides pour la création
        self.valid_payload = {
            "title": "Nouvelle tâche",
            "description": "Description de la nouvelle tâche",
            "is_completed": False
        }
        
        # Données invalides (titre trop long)
        self.invalid_payload = {
            "title": "x" * 201,  # > 200 caractères
            "description": "Description",
            "is_completed": False
        }
        
        # Données pour mise à jour complète (PUT)
        self.update_payload = {
            "title": "Tâche mise à jour",
            "description": "Description mise à jour",
            "is_completed": True
        }
        
        # Données pour mise à jour partielle (PATCH)
        self.partial_update_payload = {
            "is_completed": True
        }
    
    # ============ TESTS LISTE DES TÂCHES (GET /api/tasks/) ============
    def test_get_all_tasks(self):
        """Test GET /api/tasks/ - Liste toutes les tâches"""
        url = reverse('task-list-create')
        response = self.client.get(url)
        
        # Vérification statut HTTP
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérification structure de réponse paginée
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        
        # Vérification nombre de tâches
        self.assertEqual(response.data['count'], 2)
        
        # Vérification ordre (plus récent en premier)
        self.assertEqual(response.data['results'][0]['title'], self.task2.title)
        self.assertEqual(response.data['results'][1]['title'], self.task1.title)
    
    def test_get_all_tasks_with_pagination(self):
        """Test pagination de la liste des tâches"""
        url = reverse('task-list-create') + '?page=1&page_size=1'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Vérification lien de pagination
        self.assertIsNotNone(response.data['next'])
    
    # ============ TESTS CRÉATION TÂCHE (POST /api/tasks/) ============
    def test_create_valid_task(self):
        """Test POST /api/tasks/ - Création d'une tâche valide"""
        url = reverse('task-list-create')
        response = self.client.post(
            url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        
        # Vérification statut HTTP
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Vérification données retournées
        self.assertEqual(response.data['title'], self.valid_payload['title'])
        self.assertEqual(response.data['description'], self.valid_payload['description'])
        self.assertEqual(response.data['is_completed'], self.valid_payload['is_completed'])
        
        # Vérification création en base
        self.assertEqual(Task.objects.count(), 3)
        self.assertTrue(Task.objects.filter(title=self.valid_payload['title']).exists())
    
    def test_create_task_with_missing_title(self):
        """Test création sans titre (doit échouer)"""
        url = reverse('task-list-create')
        invalid_data = {
            "description": "Description sans titre",
            "is_completed": False
        }
        
        response = self.client.post(
            url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_create_task_with_empty_title(self):
        """Test création avec titre vide (doit échouer)"""
        url = reverse('task-list-create')
        invalid_data = {
            "title": "   ",
            "description": "Description",
            "is_completed": False
        }
        
        response = self.client.post(
            url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_create_task_with_title_too_long(self):
        """Test création avec titre trop long (>200 caractères)"""
        url = reverse('task-list-create')
        
        response = self.client.post(
            url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    # ============ TESTS RÉCUPÉRATION TÂCHE (GET /api/tasks/<id>/) ============
    def test_get_valid_single_task(self):
        """Test GET /api/tasks/<id>/ - Récupération d'une tâche existante"""
        url = reverse('task-detail-update-delete', kwargs={'pk': self.task1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task1.title)
        self.assertEqual(response.data['description'], self.task1.description)
        self.assertEqual(response.data['is_completed'], self.task1.is_completed)
        self.assertIn('id', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
    
    def test_get_invalid_single_task(self):
        """Test GET /api/tasks/<id>/ - Récupération d'une tâche inexistante"""
        url = reverse('task-detail-update-delete', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No Task matches the given query.')
    
    # ============ TESTS MISE À JOUR COMPLÈTE (PUT /api/tasks/<id>/) ============
    def test_valid_update_task_put(self):
        """Test PUT /api/tasks/<id>/ - Mise à jour complète"""
        url = reverse('task-detail-update-delete', kwargs={'pk': self.task1.pk})
        response = self.client.put(
            url,
            data=json.dumps(self.update_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérification données mises à jour
        self.assertEqual(response.data['title'], self.update_payload['title'])
        self.assertEqual(response.data['description'], self.update_payload['description'])
        self.assertEqual(response.data['is_completed'], self.update_payload['is_completed'])
        
        # Rafraîchir depuis la base
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, self.update_payload['title'])
    
    def test_update_invalid_task_put(self):
        """Test PUT /api/tasks/<id>/ - Mise à jour d'une tâche inexistante"""
        url = reverse('task-detail-update-delete', kwargs={'pk': 999})
        response = self.client.put(
            url,
            data=json.dumps(self.update_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_task_with_invalid_data_put(self):
        """Test PUT /api/tasks/<id>/ - Mise à jour avec données invalides"""
        url = reverse('task-detail-update-delete', kwargs={'pk': self.task1.pk})
        
        response = self.client.put(
            url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    # ============ TESTS MISE À JOUR PARTIELLE (PATCH /api/tasks/<id>/) ============
    def test_valid_partial_update_task_patch(self):
        """Test PATCH /api/tasks/<id>/ - Mise à jour partielle"""
        url = reverse('task-detail-update-delete', kwargs={'pk': self.task1.pk})
        
        response = self.client.patch(
            url,
            data=json.dumps(self.partial_update_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_completed'], True)
        
        # Vérification que seul le champ spécifié est modifié
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.is_completed, True)
        self.assertEqual(self.task1.title, "Tâche de test 1")  # Inchangé
    
    def test_partial_update_invalid_task_patch(self):
        """Test PATCH /api/tasks/<id>/ - Mise à jour partielle d'une tâche inexistante"""
        url = reverse('task-detail-update-delete', kwargs={'pk': 999})
        
        response = self.client.patch(
            url,
            data=json.dumps(self.partial_update_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ============ TESTS SUPPRESSION (DELETE /api/tasks/<id>/) ============
    def test_valid_delete_task(self):
        """Test DELETE /api/tasks/<id>/ - Suppression d'une tâche"""
        url = reverse('task-detail-update-delete', kwargs={'pk': self.task1.pk})
        
        # Comptage avant suppression
        initial_count = Task.objects.count()
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Vérification suppression en base
        self.assertEqual(Task.objects.count(), initial_count - 1)
        
        # Vérification que la tâche n'existe plus
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.pk)
    
    def test_delete_invalid_task(self):
        """Test DELETE /api/tasks/<id>/ - Suppression d'une tâche inexistante"""
        url = reverse('task-detail-update-delete', kwargs={'pk': 999})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ============ TESTS VALIDATION JSON ============
    def test_json_response_structure(self):
        """Test structure JSON des réponses"""
        url = reverse('task-detail-update-delete', kwargs={'pk': self.task1.pk})
        response = self.client.get(url)
        
        # Vérification que la réponse est bien du JSON
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Vérification champs obligatoires
        data = response.json()
        required_fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'updated_at']
        
        for field in required_fields:
            self.assertIn(field, data)
    
    def test_json_creation_response(self):
        """Test structure JSON après création"""
        url = reverse('task-list-create')
        
        response = self.client.post(
            url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Vérification type des données
        data = response.json()
        self.assertIsInstance(data['id'], int)
        self.assertIsInstance(data['title'], str)
        self.assertIsInstance(data['description'], str)
        self.assertIsInstance(data['is_completed'], bool)
        self.assertIsInstance(data['created_at'], str)  # ISO format string
        self.assertIsInstance(data['updated_at'], str)


class TaskModelTest(TestCase):
    """Tests spécifiques pour le modèle Task"""
    
    def test_task_creation(self):
        """Test création d'une tâche via le modèle"""
        task = Task.objects.create(
            title="Test modèle",
            description="Description test",
            is_completed=False
        )
        
        self.assertEqual(task.title, "Test modèle")
        self.assertEqual(task.description, "Description test")
        self.assertFalse(task.is_completed)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)
    
    def test_task_string_representation(self):
        """Test la méthode __str__ du modèle"""
        task = Task.objects.create(
            title="Tâche test",
            is_completed=True
        )
        
        expected_str = f"{task.title} => Terminée"
        self.assertEqual(str(task), expected_str)
        
        task.is_completed = False
        task.save()
        
        expected_str = f"{task.title} => En cours"
        self.assertEqual(str(task), expected_str)
    
    def test_default_ordering(self):
        # Test l'ordre par défaut des tâches
        now = timezone.now()
        
        # Créer des tâches avec des dates explicites
        task1 = Task.objects.create(title="Tâche 1")
        Task.objects.filter(pk=task1.pk).update(created_at=now - timezone.timedelta(minutes=10))
        
        task2 = Task.objects.create(title="Tâche 2")
        Task.objects.filter(pk=task2.pk).update(created_at=now - timezone.timedelta(minutes=5))
        
        task3 = Task.objects.create(title="Tâche 3")
        Task.objects.filter(pk=task3.pk).update(created_at=now)
        
        # Recharger les instances
        task1.refresh_from_db()
        task2.refresh_from_db()
        task3.refresh_from_db()
        
        # Récupérer dans l'ordre par défaut
        tasks = Task.objects.all()
        
        # Vérifier l'ordre descendant
        self.assertEqual(tasks[0], task3)  # La plus récente
        self.assertEqual(tasks[1], task2)
        self.assertEqual(tasks[2], task1)  # La plus ancienne
