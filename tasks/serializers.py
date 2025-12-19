from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    # Sérialiseur pour le modèle Task
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        # Validation personnalisée pour le champ title
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Le titre ne peut pas être vide.")
        if len(value) > 200:
            raise serializers.ValidationError("Le titre ne peut pas dépasser 200 caractères.")
        return value
    
    def validate_description(self, value):
        # Validation personnalisée pour le champ description
        return value.strip() if value else ""
    
    def create(self, validated_data):
        # Création d'une nouvelle tâche
        return Task.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Mise à jour d'une tâche existante
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.save()
        return instance
