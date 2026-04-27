from django.shortcuts import render, redirect, get_object_or_404
from elections.models import ElectoralList, Party, Vote
from elections.forms.voter_forms import VoterLookupForm
from django.contrib.auth.decorators import login_required

# def voter_identification(request):

#     form = VoterLookupForm(request.POST or None)

#     if request.method == "POST" and form.is_valid():
#         voter_id = form.cleaned_data["voter_id"]

#         try:
#             voter = ElectoralList.objects.get(voter_id=voter_id)

#             if voter.has_voted:
#                 return render(request, "elections/vote/already_voted.html")

#             request.session["voter_id"] = voter_id
#             return redirect("vote_page")

#         except ElectoralList.DoesNotExist:
#             return render(request, "elections/vote/invalid_voter.html")

#     return render(request, "elections/vote/identify.html", {"form": form})

@login_required
def voter_identification(request):

    message = None

    if request.method == "POST":
        voter_id = request.POST.get("voter_id")

        try:
            electoral = ElectoralList.objects.get(voter_id=voter_id)

            # 🚫 déjà utilisé par un autre user
            if electoral.user and electoral.user != request.user:
                message = "❌ Cet identifiant est déjà utilisé"

            # 🚫 déjà voté
            elif electoral.has_voted:
                return render(request, "elections/vote/already_voted.html")

            else:
                # 🔗 liaison
                electoral.user = request.user
                electoral.save()

                return redirect("vote_page")

        except ElectoralList.DoesNotExist:
            message = "❌ Identifiant invalide"

    return render(request, "elections/vote/identify.html", {
        "message": message
    })

@login_required
def vote_page(request):

    # 🔐 récupérer électeur lié
    try:
        elector = ElectoralList.objects.get(user=request.user)
    except ElectoralList.DoesNotExist:
        return render(request, "core/access_denied.html")

    # 🚫 blocage si déjà voté (physique ou online)
    if elector.has_voted:
        return render(request, "elections/vote/already_voted.html")

    parties = Party.objects.all()

    if request.method == "POST":
        party_id = request.POST.get("party")

        party = get_object_or_404(Party, id=party_id)

        # 🗳️ enregistrer vote
        Vote.objects.create(
            electoral=elector,
            party=party
        )

        # 🔥 marquer comme voté (anti fraude global)
        elector.has_voted = True
        elector.save()

        return redirect("dashboard")

    return render(request, "elections/vote/vote_page.html", {
        "elector": elector,
        "parties": parties
    })

@login_required
def identify_voter(request):

    message = None

    if request.method == "POST":
        voter_id = request.POST.get("voter_id")

        try:
            elector = ElectoralList.objects.get(voter_id=voter_id)

            # 🔥 déjà lié ?
            if elector.user:
                message = "❌ Cet identifiant est déjà utilisé"
            else:
                elector.user = request.user
                elector.save()

                return redirect("vote_page")

        except ElectoralList.DoesNotExist:
            message = "❌ Identifiant invalide"

    return render(request, "elections/vote/identify.html", {
        "message": message
    })