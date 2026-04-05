class VoteValidator:
    """
    Vérifie la cohérence des résultats électoraux
    """

    @staticmethod
    def is_valid(session):
        total_lists = session.total_list_votes()
        expected = session.total_voters

        return (total_lists + session.blank_votes) == expected