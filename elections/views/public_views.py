from django.shortcuts import render

from elections.models import Vote, PhysicalResult, Party, ElectoralList
from django.db.models import Sum

from django.shortcuts import render
from elections.services.aggregation_service import AggregationService


def dashboard(request):

    results = AggregationService.get_global_results()

    total_votes = sum(results.values())

    processed_results = []

    for name, score in results.items():
        percentage = (score / total_votes) * 100 if total_votes > 0 else 0
        processed_results.append((name, score, round(percentage, 2)))

    processed_results = sorted(processed_results, key=lambda x: x[1], reverse=True)

    # 🔥 participation
    total_voters = ElectoralList.objects.count()
    voted = ElectoralList.objects.filter(has_voted=True).count()

    participation = (voted / total_voters) * 100 if total_voters > 0 else 0

    return render(request, "elections/public/dashboard.html", {
        "results": processed_results,
        "participation": round(participation, 2)
    })