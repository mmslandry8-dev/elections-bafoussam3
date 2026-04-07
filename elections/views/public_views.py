from django.shortcuts import render
from elections.services.results_engine import ResultsEngine
from elections.services.stats_service import StatsService

from elections.services.seat_allocation import SeatAllocator

def dashboard(request):

    # results = ResultsEngine.get_global_results()
    results = ResultsEngine.get_global_results()

    total_votes = sum(results.values())

    processed_results = []

    for name, score in results.items():
        percentage = (score / total_votes) * 100 if total_votes > 0 else 0
        processed_results.append((name, score, round(percentage, 2)))

    # tri
    processed_results = sorted(processed_results, key=lambda x: x[1], reverse=True)
    participation = StatsService.participation_rate()

    # classement
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return render(request, "elections/public/dashboard.html", {
        "results": sorted_results,
        "participation": participation
    })


def seats_results(request):

    total_seats = 25  # ⚠️ à adapter selon commune

    seats = SeatAllocator.allocate_seats(total_seats)

    sorted_seats = sorted(seats.items(), key=lambda x: x[1], reverse=True)

    return render(request, "elections/public/seats_results.html", {
        "seats": sorted_seats
    })