from elections.models import Vote, PhysicalResult, Party
from django.db.models import Count, Sum


class AggregationService:

    @staticmethod
    def get_global_results():
        """
        🔥 Fusionne les votes physiques + votes en ligne
        """

        results = {}

        # 🟢 Initialiser tous les partis à 0
        for party in Party.objects.all():
            results[party.name] = 0

        # =========================
        # 🗳️ VOTES EN LIGNE (CORRIGÉ)
        # =========================
        online_votes = Vote.objects.values("party__name").annotate(
            total=Count("id")   # ✅ CORRECTION ICI
        )

        for item in online_votes:
            results[item["party__name"]] += item["total"]

        # =========================
        # 🧾 VOTES PHYSIQUES
        # =========================
        physical_votes = PhysicalResult.objects.values("party__name").annotate(
            total=Sum("votes")
        )

        for item in physical_votes:
            results[item["party__name"]] += item["total"]

        return results