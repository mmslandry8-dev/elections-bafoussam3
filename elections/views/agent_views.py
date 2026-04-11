from django.shortcuts import render, redirect
from elections.forms.vote_forms import VoteSessionForm
from elections.models import ElectoralList, VoteEntry, VoteSession
from elections.services.validation import VoteValidator

def create_vote_session(request):

    lists = ElectoralList.objects.all()

    if request.method == "POST":

        form = VoteSessionForm(request.POST)

        if form.is_valid():
            session = form.save()

            # 🔥 Enregistrement des voix par liste
            for electoral_list in lists:
                votes = int(request.POST.get(f"list_{electoral_list.id}", 0))

                VoteEntry.objects.create(
                    session=session,
                    electoral_list=electoral_list,
                    votes=votes
                )

            # 🚨 validation
            if VoteValidator.is_valid(session):
                session.is_validated = True
                session.save()
                return redirect("vote_success")
            else:
                session.delete()
                return render(request, "elections/agent/vote_form.html", {
                    "form": form,
                    "lists": lists,
                    "error": "Données incohérentes : rejet automatique"
                })

    else:
        form = VoteSessionForm()

    return render(request, "elections/agent/vote_form.html", {
        "form": form,
        "lists": lists
    })

def vote_success(request):
    return render(request, "elections/agent/success.html")