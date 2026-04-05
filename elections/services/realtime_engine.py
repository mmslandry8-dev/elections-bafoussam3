class RealTimeEngine:
    """
    Simule la diffusion des résultats en temps réel
    (base pour WebSockets plus tard)
    """

    @staticmethod
    def push_update(session):
        return {
            "center": session.polling_station.center.name,
            "bv": session.polling_station.code,
            "validated": session.is_validated
        }