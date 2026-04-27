from django.db import models
from django.conf import settings

from django.utils import timezone

def is_finished(self):
    if not self.end_time:
        return False
    return timezone.now() >= self.end_time

class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["electoral", "election"],
            name="unique_vote_per_elector_per_election"
        )
    ]

# =========================
# 🗳️ ELECTION
# =========================
class Election(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    is_active = models.BooleanField(default=False)
    end_time = models.DateTimeField(null=True, blank=True)

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

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="electoral_link"
    )

    has_voted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["voter_id", "election"],
                name="unique_voter_per_election"
            )
        ]

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

class ElectionConfig(models.Model):
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=60)

    def is_finished(self):
        if not self.start_time:
            return True

        from django.utils import timezone
        elapsed = (timezone.now() - self.start_time).total_seconds() / 60
        return elapsed > self.duration_minutes
    
from django.utils import timezone

class ElectionState(models.Model):
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def is_finished(self):
        if not self.start_time or not self.duration:
            return True
        return timezone.now() >= (self.start_time + self.duration)

    def time_remaining(self):
        if not self.start_time or not self.duration:
            return 0
        remaining = (self.start_time + self.duration) - timezone.now()
        return max(remaining.total_seconds(), 0)