from django.db import models
from core.models import BureauVote
from elections.models import ElectoralList

# Create your models here.

class ResultBV(models.Model):
    """
    Résultat global d’un bureau de vote
    """

    bureau = models.OneToOneField(BureauVote, on_delete=models.CASCADE)

    total_voters = models.PositiveIntegerField()
    null_votes = models.PositiveIntegerField()
    expressed_votes = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Résultat {self.bureau.code}"

class VoteScore(models.Model):
    """
    Score d’une liste dans un BV
    """

    result = models.ForeignKey(ResultBV, on_delete=models.CASCADE, related_name='scores')
    electoral_list = models.ForeignKey(ElectoralList, on_delete=models.CASCADE)

    votes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.electoral_list.name} - {self.votes}"