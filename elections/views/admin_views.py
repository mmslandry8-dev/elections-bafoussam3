from django.shortcuts import render, redirect
from elections.models import (
    Election,
    Commune,
    Center,
    PollingStation,
    Party,
    ElectoralList,
    Vote,
    PhysicalResult
)


from django.contrib.auth.decorators import login_required

from elections.forms.electoral_forms import ElectoralListForm

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