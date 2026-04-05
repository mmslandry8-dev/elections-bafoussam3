from elections.models import ElectoralList

class ListManager:
    """
    Gestion centralisée des listes électorales
    """

    @staticmethod
    def get_active_lists():
        return ElectoralList.objects.filter(is_active=True)

    @staticmethod
    def create_list(data):
        return ElectoralList.objects.create(**data)