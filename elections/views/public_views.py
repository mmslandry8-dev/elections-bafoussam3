from django.shortcuts import render

from elections.models import Vote, PhysicalResult, Party, ElectoralList, ElectionState
from django.db.models import Sum

from django.shortcuts import render
from elections.services.aggregation_service import AggregationService


# def dashboard(request):

#     results = AggregationService.get_global_results()

#     total_votes = sum(results.values())

#     processed_results = []

#     for name, score in results.items():
#         percentage = (score / total_votes) * 100 if total_votes > 0 else 0
#         processed_results.append((name, score, round(percentage, 2)))

#     processed_results = sorted(processed_results, key=lambda x: x[1], reverse=True)

#     # 🔥 participation
#     total_voters = ElectoralList.objects.count()
#     voted = ElectoralList.objects.filter(has_voted=True).count()

#     participation = (voted / total_voters) * 100 if total_voters > 0 else 0

#     return render(request, "elections/public/dashboard.html", {
#         "results": processed_results,
#         "participation": round(participation, 2)
#     })

def dashboard(request):
    config = ElectionState.objects.first()

    remaining_time = 0
    is_finished = True

    if config and config.is_active:
        remaining_time = config.time_remaining()
        is_finished = config.is_finished()
        # 🧠 si terminé automatiquement
        if remaining_time <= 0:
            config.is_active = False
            config.save()
            remaining_time = 0

    results = AggregationService.get_global_results()

    total_votes = sum(results.values())

    processed_results = []

    for party in Party.objects.all():
        score = results.get(party.name, 0)
        percentage = (score / total_votes) * 100 if total_votes > 0 else 0

        processed_results.append({
            "party": party,
            "score": score,
            "percentage": round(percentage, 2)
        })

    processed_results = sorted(processed_results, key=lambda x: x["score"], reverse=True)

    # 🔥 participation
    total_voters = ElectoralList.objects.count()
    voted = ElectoralList.objects.filter(has_voted=True).count()

    participation = (voted / total_voters) * 100 if total_voters > 0 else 0

    return render(request, "elections/public/dashboard.html", {
        "results": processed_results,
        "participation": round(participation, 2),
        "remaining_time": int(remaining_time),
        "is_finished": is_finished,
        "is_active": config.is_active if config else False,
    })