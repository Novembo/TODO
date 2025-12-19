from django.db import models


class Task(models.Model):
    # Modèle représentant une tâche (TODO)
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    is_completed = models.BooleanField(default=False, verbose_name="Terminée",)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"

    def __str__(self):
        status = "Terminée" if self.is_completed else "En cours"
        return f"{self.title} => {status}"
