from django.db import models
from django.conf import settings


# =========================
# 🗳️ ELECTION
# =========================
class Election(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# =========================
# 🌍 COMMUNE
# =========================
class Commune(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# =========================
# 🏢 CENTRE DE VOTE
# =========================
class Center(models.Model):
    name = models.CharField(max_length=255)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.name} ({self.commune.name})"


# =========================
# 🏫 BUREAU DE VOTE
# =========================
class PollingStation(models.Model):
    name = models.CharField(max_length=255)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.center.name}"


# =========================
# 🧑‍🤝‍🧑 PARTI / LISTE
# =========================
class Party(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="parties/logos/", null=True, blank=True)
    document = models.FileField(upload_to="parties/docs/", null=True, blank=True)

    def __str__(self):
        return self.name


# =========================
# 🧾 LISTE ELECTORALE
# =========================
class ElectoralList(models.Model):
    voter_id = models.CharField(max_length=100)

    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    station = models.ForeignKey(PollingStation, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    has_voted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('voter_id', 'election')

    def __str__(self):
        return f"{self.voter_id} - {self.center.name}"


# =========================
# 🗳️ VOTE EN LIGNE
# =========================
class Vote(models.Model):
    electoral = models.ForeignKey(ElectoralList, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('electoral', 'election')

    def __str__(self):
        return f"{self.electoral.voter_id} -> {self.party.name}"


# =========================
# 🧾 RESULTATS PHYSIQUES (AGENT)
# =========================
class PhysicalResult(models.Model):
    station = models.ForeignKey(PollingStation, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True)

    votes = models.PositiveIntegerField(default=0)
    
    is_validated = models.BooleanField(default=False)  # 🔥 NOUVEAU
    
    class Meta:
        unique_together = ('station', 'party', 'election')

    def __str__(self):
        return f"{self.station.name} - {self.party.name} : {self.votes}"
    
class VoteSession(models.Model):
    station = models.ForeignKey(PollingStation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Session - {self.station.name}"
