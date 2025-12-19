from django.urls import path
from .views import (
    home_view,
    task_list_create,
    task_detail_update_delete
)


urlpatterns = [
    # Home
    path('', home_view, name='home'),
    
    # Endpoints API
    # GET et POST sur la même URL
    path('api/tasks/', task_list_create, name='task-list-create'),
    
    # GET, PUT, PATCH, DELETE sur la même URL
    path('api/tasks/<int:pk>/', task_detail_update_delete, name='task-detail-update-delete')
]
