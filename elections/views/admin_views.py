from django.shortcuts import render, redirect
from elections.models import (
    Election,
    Commune,
    Center,
    PollingStation,
    Party,
    ElectoralList,
    Vote,
    PhysicalResult,
    ElectionState,
    ElectionConfig
)



from django.contrib.auth.decorators import login_required

from elections.forms.electoral_forms import ElectoralListForm

from django.utils import timezone
from datetime import timedelta

@login_required
def electoral_list_admin(request):

    if request.user.role != "ADMIN":
        return render(request, "core/access_denied.html")

    electors = ElectoralList.objects.select_related("center", "station", "user")

    return render(request, "elections/admin/electoral_list.html", {
        "electors": electors
    })


@login_required
def add_elector(request):

    if request.user.role != "ADMIN":
        return render(request, "core/access_denied.html")

    form = ElectoralListForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("electoral_list_admin")

    return render(request, "elections/admin/add_elector.html", {
        "form": form
    })

@login_required
def reset_election(request):

    if request.user.role != "ADMIN":
        return render(request, "core/access_denied.html")

    # 🔥 supprimer données
    Vote.objects.all().delete()
    PhysicalResult.objects.all().delete()
    ElectoralList.objects.all().delete()

    # 🔥 désactiver toutes les élections
    Election.objects.all().update(is_active=False, end_time=None)    

    # 🔥 RESET COMPLET ÉTAT ÉLECTION
    config = ElectionState.objects.first()

    if config:
        config.is_active = False
        config.start_time = None
        config.end_time = None
        config.save()

    return redirect("dashboard")

@login_required
def start_election(request):

    if request.method == "POST":

        hours = int(request.POST.get("hours", 0))
        minutes = int(request.POST.get("minutes", 0))
        seconds = int(request.POST.get("seconds", 0))

        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)

        config, created = ElectionState.objects.get_or_create(id=1)

        config.is_active = True
        config.start_time = timezone.now()
        config.end_time = timezone.now() + duration

        config.save()

        return redirect("dashboard")

@login_required
def stop_election(request):

    if request.user.role != "ADMIN":
        return render(request, "core/access_denied.html")

    config = ElectionState.objects.first()

    if config:
        config.end_time = timezone.now()  # 🔥 force fin immédiate
        config.is_active = False
        config.save()

    return redirect("dashboard")