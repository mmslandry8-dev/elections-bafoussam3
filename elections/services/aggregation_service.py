# from elections.models import Vote, PhysicalResult, PollingStation, Center
# from elections.models import Party


# class AggregationService:

#     # =========================
#     # 🏫 BUREAU DE VOTE
#     # =========================
#     @staticmethod
#     def get_station_results(station):
#         results = {}

#         # votes physiques
#         physical = PhysicalResult.objects.filter(station=station)
#         for r in physical:
#             results[r.party.name] = results.get(r.party.name, 0) + r.votes

#         return results


#     # =========================
#     # 🏢 CENTRE DE VOTE
#     # =========================
#     @staticmethod
#     def get_center_results(center):
#         results = {}

#         stations = PollingStation.objects.filter(center=center)

#         for station in stations:
#             station_results = AggregationService.get_station_results(station)

#             for party, votes in station_results.items():
#                 results[party] = results.get(party, 0) + votes

#         return results


#     # =========================
#     # 🌍 GLOBAL
#     # =========================
#     @staticmethod
#     def get_global_results():

#         results = {}

#         # votes en ligne
#         for vote in Vote.objects.all():
#             results[vote.party.name] = results.get(vote.party.name, 0) + 1

#         # votes physiques
#         for r in PhysicalResult.objects.all():
#             results[r.party.name] = results.get(r.party.name, 0) + r.votes

#         return results

from elections.models import Vote, PhysicalResult, Party
from django.db.models import Sum


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
        # 🗳️ VOTES EN LIGNE
        # =========================
        online_votes = Vote.objects.values("party__name").annotate(total=Sum("id"))

        for item in online_votes:
            results[item["party__name"]] += item["total"]

        # =========================
        # 🧾 VOTES PHYSIQUES
        # =========================
        physical_votes = PhysicalResult.objects.values("party__name").annotate(total=Sum("votes"))

        for item in physical_votes:
            results[item["party__name"]] += item["total"]

        return results