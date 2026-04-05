from elections.models import VoteSession, VoteEntry, ElectoralList

class ResultsEngine:
    """
    Calcule les résultats globaux en temps réel
    """

    @staticmethod
    def get_global_results():

        results = {}

        for lst in ElectoralList.objects.all():
            results[lst.name] = 0

        sessions = VoteSession.objects.filter(is_validated=True)

        for session in sessions:
            for entry in session.entries.all():
                results[entry.electoral_list.name] += entry.votes

        return results