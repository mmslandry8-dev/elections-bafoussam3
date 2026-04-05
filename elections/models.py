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

class ElectoralList(models.Model):
    """
    Représente une liste électorale (parti + candidats).
    Cette entité est utilisée pour :
    - affichage public
    - calcul des résultats
    - saisie des voix
    """

    name = models.CharField(max_length=255)  # Nom du parti ou liste
    party_acronym = models.CharField(max_length=50, blank=True, null=True)

    # 🎨 VISUELS
    logo = models.ImageField(upload_to='lists/images/', null=True, blank=True)
    banner = models.ImageField(upload_to='lists/images/', null=True, blank=True)

    # 📄 DOCUMENT OFFICIEL (PDF des candidats)
    program_document = models.FileField(upload_to='lists/docs/', null=True, blank=True)

    # 🧠 STATUT
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class VotingCenter(models.Model):
    """
    Centre de vote = école ou lieu regroupant plusieurs bureaux
    """

    name = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)  # quartier / village

    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class PollingStation(models.Model):
    """
    Bureau de vote = unité de base du scrutin
    """

    center = models.ForeignKey(
        VotingCenter,
        on_delete=models.CASCADE,
        related_name="polling_stations"
    )

    code = models.CharField(max_length=50)  # BV1, BV2...
    registered_voters = models.PositiveIntegerField()

    # 📍 option géographique (future carte)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.center.name}"