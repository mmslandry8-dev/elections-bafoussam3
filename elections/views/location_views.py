# from django.shortcuts import render

# # Create your views here.

# from django.shortcuts import render, redirect
# from elections.models import ElectoralList, Center



# def list_list(request):
#     """
#     Affiche toutes les listes électorales
#     """
#     lists = ElectoralList.objects.all()
#     return render(request, "elections/lists/list_list.html", {"lists": lists})


# def centers_list(request):
#     """
#     Affiche tous les centres de vote
#     """
#     centers = Center.objects.all()
#     return render(request, "elections/location/centers.html", {"centers": centers})