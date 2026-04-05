from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modèle utilisateur personnalisé
    On étend AbstractUser pour ajouter nos champs
    """

    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('AGENT', 'Agent électoral'),
        ('ELECTEUR', 'Électeur'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ELECTEUR')

    is_suspended = models.BooleanField(default=False)  # compte suspendu

    def __str__(self):
        return f"{self.username} ({self.role})"

class Appeal(models.Model):
    """
    Demande de réactivation de compte
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appeal de {self.user.username}"