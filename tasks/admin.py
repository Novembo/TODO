from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'truncated_description', 'is_completed', 'created_at', 'updated_at']
    list_editable = ['is_completed']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def truncated_description(self, obj):
        # Raccourcir la longueur de la description"""
        if len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description
    truncated_description.short_description = 'Description'
