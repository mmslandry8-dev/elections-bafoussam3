from django.shortcuts import render, redirect
from .models import ResultBV, VoteScore
from core.models import BureauVote
from elections.models import ElectoralList
from .forms import ResultBVForm

# Create your views here.

def enter_results(request):
    """
    Saisie des résultats d’un BV
    """

    form = ResultBVForm(request.POST or None)

    lists = ElectoralList.objects.all()

    if request.method == "POST":
        if form.is_valid():
            result = form.save()

            total_scores = 0

            for electoral_list in lists:
                votes = int(request.POST.get(f'list_{electoral_list.id}', 0))

                VoteScore.objects.create(
                    result=result,
                    electoral_list=electoral_list,
                    votes=votes
                )

                total_scores += votes

            # 🔐 VALIDATION CRITIQUE
            if total_scores + result.null_votes != result.total_voters:
                result.delete()  # rollback
                return render(request, 'results/error.html', {
                    'message': "Erreur : incohérence des résultats"
                })

            result.expressed_votes = total_scores
            result.save()

            return redirect('home')

    return render(request, 'results/enter_results.html', {
        'form': form,
        'lists': lists
    })
