from django.db import models

# Create your models here.

class Commune(models.Model):
    """
    Représente une commune (ex: Bafoussam III)
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CentreVote(models.Model):
    """
    Représente un centre de vote (souvent une école)
    """

    name = models.CharField(max_length=150)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.commune.name}"
    
class BureauVote(models.Model):
    """
    Représente un bureau de vote (BV)
    """

    code = models.CharField(max_length=20, unique=True)
    centre = models.ForeignKey(CentreVote, on_delete=models.CASCADE)
    registered_voters = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.code} ({self.centre.name})"