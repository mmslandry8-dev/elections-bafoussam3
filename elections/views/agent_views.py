from django.shortcuts import render, redirect

from elections.models import PhysicalResult, PollingStation, Center, Party

from elections.forms.physical_vote_forms import PhysicalResultForm

from elections.models import ElectoralList
from django.db.models import Q

from django.contrib.auth.decorators import login_required

def physical_results_view(request):

    form = PhysicalResultForm(
        request.POST or None,
        user=request.user  # 🔥 TRÈS IMPORTANT
    )

    if request.method == "POST" and form.is_valid():

        station = form.cleaned_data["station"]

        # 🔒 sécurité : vérifier que l'agent ne triche pas
        if request.user.role == "AGENT" and hasattr(request.user, "center") and request.user.center:
            if station.center != request.user.center:
                return render(request, "elections/agent/physical_results.html", {
                    "form": form,
                    "error": "⚠️ Accès interdit à ce bureau."
                })

        # 🔒 blocage double saisie
        if PhysicalResult.objects.filter(station=station).exists():
            return render(request, "elections/agent/physical_results.html", {
                "form": form,
                "error": "⚠️ Résultats déjà enregistrés."
            })

        total_votes = 0

        for party in Party.objects.all():
            field_name = f"party_{party.id}"
            votes = form.cleaned_data.get(field_name) or 0
            total_votes += votes

        if total_votes == 0:
            return render(request, "elections/agent/physical_results.html", {
                "form": form,
                "error": "⚠️ Aucun vote saisi."
            })

        # 💾 ENREGISTREMENT
        for party in Party.objects.all():
            PhysicalResult.objects.create(
                station=station,
                party=party,
                votes=form.cleaned_data.get(f"party_{party.id}") or 0
            )

        return render(request, "elections/agent/physical_results.html", {
            "form": PhysicalResultForm(user=request.user),
            "success": "✅ Résultats enregistrés."
        })

    return render(request, "elections/agent/physical_results.html", {
        "form": form
    })

@login_required
def agent_electors(request):

    if request.user.role != "AGENT":
        return render(request, "core/access_denied.html")

    # 🔥 TEMPORAIRE : afficher tous les électeurs
    electors = ElectoralList.objects.all()

    return render(request, "elections/agent/electors.html", {
        "electors": electors
    })

# @login_required
# def agent_electors(request):

#     if request.user.role != "AGENT":
#         return render(request, "core/access_denied.html")

#     query = request.GET.get("q")

#     electors = ElectoralList.objects.filter(center=request.user.center)

#     if query:
#         electors = electors.filter(
#             Q(voter_id__icontains=query) |
#             Q(user__username__icontains=query)
#         )

#     return render(request, "elections/agent/electors.html", {
#         "electors": electors
#     })

@login_required
def mark_voted(request, elector_id):

    if request.user.role != "AGENT":
        return render(request, "core/access_denied.html")

    elector = ElectoralList.objects.get(id=elector_id)

    elector.has_voted = True
    elector.save()

    return redirect("agent_electors")