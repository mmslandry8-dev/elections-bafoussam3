from django.shortcuts import render
from elections.services.results_engine import ResultsEngine
from elections.services.stats_service import StatsService

def dashboard(request):

    results = ResultsEngine.get_global_results()
    participation = StatsService.participation_rate()

    # classement
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return render(request, "elections/public/dashboard.html", {
        "results": sorted_results,
        "participation": participation
    })