class StatsService:
    """
    Gère les statistiques globales électorales
    """

    @staticmethod
    def participation_rate():

        from elections.models import PollingStation, VoteSession

        total_registered = sum(p.registered_voters for p in PollingStation.objects.all())

        total_voted = sum(
            s.total_voters for s in VoteSession.objects.filter(is_validated=True)
        )

        if total_registered == 0:
            return 0

        return round((total_voted / total_registered) * 100, 2)