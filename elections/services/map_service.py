class MapService:
    """
    Prépare les données pour affichage sur carte (Leaflet ou Google Maps)
    """

    @staticmethod
    def get_polling_points():
        from elections.models import PollingStation

        return [
            {
                "name": p.code,
                "lat": p.latitude,
                "lng": p.longitude,
                "center": p.center.name
            }
            for p in PollingStation.objects.filter(latitude__isnull=False)
        ]