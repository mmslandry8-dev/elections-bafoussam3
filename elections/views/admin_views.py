from django.shortcuts import render, redirect
from elections.models import VoteSession, PollingStation
from elections.services.audit_service import AuditService

def admin_dashboard(request):

    sessions = VoteSession.objects.all()

    return render(request, "elections/admin/dashboard.html", {
        "sessions": sessions
    })


def validate_session(request, session_id):

    session = VoteSession.objects.get(id=session_id)

    station = session.polling_station

    # 🔒 verrouillage
    station.is_locked = True
    station.save()

    session.is_validated = True
    session.save()

    # 📝 audit
    AuditService.log(
        "VALIDATION",
        request.user,
        f"Validation du BV {station.code}"
    )

    return redirect("admin_dashboard")