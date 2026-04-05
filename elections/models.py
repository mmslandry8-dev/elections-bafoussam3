from django.db import models
from core.models import Commune

# Create your models here.

class PoliticalParty(models.Model):
    """
    Représente un parti politique (RDPC, MRC, SDF...)
    """

    name = models.CharField(max_length=150)
    acronym = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='parties/logos/', null=True, blank=True)

    def __str__(self):
        return f"{self.acronym} - {self.name}"
    
class ElectoralList(models.Model):
    """
    Représente une liste candidate à une élection
    """

    name = models.CharField(max_length=150)
    party = models.ForeignKey(PoliticalParty, on_delete=models.CASCADE)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    head_candidate = models.CharField(max_length=150)  # mandataire

    total_seats = models.PositiveIntegerField()  # nombre de sièges à pourvoir

    def __str__(self):
        return f"{self.name} ({self.party.acronym})"