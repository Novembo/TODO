from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Task
from .serializers import TaskSerializer


class TaskPagination(PageNumberPagination):
    # Pagination pour les tâches
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ============ VUE D'ACCUEIL ============
@api_view(['GET'])
def home_view(request):
    data = {
        'api_name': 'TODO',
        'version': '1.0.0',
        'description': 'API REST pour la gestion de tâches',
        'endpoints': {
            'GET /api/tasks/': 'Liste toutes les tâches (avec pagination)',
            'POST /api/tasks/': 'Crée une nouvelle tâche',
            'GET /api/tasks/{id}/': 'Récupère une tâche spécifique',
            'PUT /api/tasks/{id}/': 'Met à jour complètement une tâche',
            'PATCH /api/tasks/{id}/': 'Met à jour partiellement une tâche',
            'DELETE /api/tasks/{id}/': 'Supprime une tâche',
        },
        'documentation': {
            'swagger_ui': '/api/docs/',
            'schema': '/api/schema/',
        }
    }
    return Response(data, status=200)


# ============ VUE COMBINÉE POUR LISTE ET CRÉATION ============
@extend_schema(
    summary="Liste ou crée des tâches",
    description="""
    - GET : Retourne une liste paginée de toutes les tâches
    - POST : Crée une nouvelle tâche avec les données fournies
    """,
    parameters=[
        OpenApiParameter(
            name='page',
            description='Numéro de page',
            required=False,
            type=int
        ),
        OpenApiParameter(
            name='page_size',
            description='Nombre de tâches par page (max 100)',
            required=False,
            type=int
        )
    ],
    request=TaskSerializer,
    examples=[
        OpenApiExample(
            'Exemple de création',
            value={
                'title': 'Acheter du lait',
                'description': 'N\'oublier pas le lait demi-écrémé',
                'is_completed': False
            },
            request_only=True
        )
    ],
    responses={
        200: TaskSerializer(many=True),
        201: TaskSerializer,
        400: None
    }
)
@api_view(['GET', 'POST'])
def task_list_create(request):
    """Gère à la fois la liste (GET) et la création (POST) des tâches"""
    
    if request.method == 'GET':
        # LISTE : Retourne toutes les tâches avec pagination
        tasks = Task.objects.all().order_by('-created_at')
        paginator = TaskPagination()
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        # CRÉATION : Crée une nouvelle tâche
        serializer = TaskSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============ VUE COMBINÉE POUR DÉTAIL, MISE À JOUR ET SUPPRESSION ============
@extend_schema(
    summary="Récupère, met à jour ou supprime une tâche",
    description="""
    - GET : Récupère une tâche spécifique par son ID
    - PUT : Met à jour complètement la tâche (tous les champs)
    - PATCH : Met à jour partiellement la tâche (champs spécifiés seulement)
    - DELETE : Supprime une tâche spécifique par son ID
    """,
    request=TaskSerializer,
    responses={
        200: TaskSerializer,
        201: TaskSerializer,
        204: None,
        400: None,
        404: None
    }
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_detail_update_delete(request, pk):
    """Gère toutes les opérations sur une tâche spécifique"""
    
    try:
        task = get_object_or_404(Task, pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Tâche non trouvée'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # DÉTAIL : récupère une tâche spécifique
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        # MISE À JOUR : complète (PUT) ou partielle (PATCH)
        partial = request.method == 'PATCH'
        serializer = TaskSerializer(task, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # SUPPRESSION : supprime la tâche
        task.delete()
        return Response({'message': 'Tâche supprimée avec succès'}, status=status.HTTP_204_NO_CONTENT)
