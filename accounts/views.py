from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import RegisterForm, AppealForm
from .models import User, Appeal

from django.contrib.auth.decorators import login_required

from elections.models import Center, PollingStation

def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        # 🔥 FORCER LE ROLE
        user.role = "ELECTEUR"

        user.save()

        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/register.html', {'form': form})

# def login_view(request):
#     """
#     Connexion utilisateur avec gestion suspension
#     """
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is  not None:
#             if user.is_suspended:
#                 # Rediriger vers page appel
#                 return redirect('appeal_view')
#             login(request, user)
#             return redirect('dashboard')
#         return render(request, 'accounts/login.html', {
#             "error": "Identifiants invalides"
#         })

#     return render(request, 'accounts/login.html', {})

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 🔥 On récupère l'utilisateur AVANT authenticate
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            user_obj = None

        # 🔥 Vérification suspension AVANT auth
        if user_obj and user_obj.is_suspended:
            return redirect('appeal_view')

        # 🔐 Authentification normale
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'accounts/login.html', {
            "error": "Identifiants invalides"
        })

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def appeal_view(request):
    form = AppealForm(request.POST or None)

    if request.method == "POST":
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if form.is_valid() and user:
            appeal = form.save(commit=False)
            appeal.user = user
            appeal.save()
            return redirect('login')

    return render(request, 'accounts/appeal.html', {'form': form})

# def appeal_view(request):
#     """
#     Demande de réactivation
#     """
#     if not request.user.is_authenticated:
#         return redirect('appeal_view')

#     form = AppealForm(request.POST or None)

#     if form.is_valid():
#         appeal = form.save(commit=False)
#         appeal.user = request.user
#         appeal.save()
#         return redirect('login')

#     return render(request, 'accounts/appeal.html', {'form': form})

def users_list(request):

    if request.user.role != "ADMIN":
        return render(request, "core/access_denied.html")

    users = User.objects.all()
    centers = Center.objects.all()
    stations = PollingStation.objects.all()

    return render(request, "accounts/admin/users_list.html", {
        "users": users,
        "centers": centers,
        "stations": stations
    })


@login_required
def change_role(request, user_id):

    if request.user.role != "ADMIN":
        return render(request, "core/access_denied.html")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("role")
        center_id = request.POST.get("center")
        station_id = request.POST.get("station")

        user.role = new_role

        # 🔥 assignation centre
        if center_id:
            user.center = Center.objects.get(id=center_id)
        else:
            user.center = None

        # 🔥 assignation bureau
        if station_id:
            user.polling_station = PollingStation.objects.get(id=station_id)
        else:
            user.polling_station = None

        user.save()

    return redirect("users_list")


@login_required
def toggle_suspend(request, user_id):
    """
    Suspendre / activer utilisateur
    """
    if request.user.role != "ADMIN":
        return render(request, "core/access_denied.html")

    user = get_object_or_404(User, id=user_id)

    user.is_suspended = not user.is_suspended
    user.save()

    return redirect("users_list")


@login_required
def appeals_list(request):
    """
    Liste des demandes de réactivation
    """
    if request.user.role != "ADMIN":
        return render(request, "core/access_denied.html")

    appeals = Appeal.objects.filter(is_processed=False)

    return render(request, "accounts/admin/appeals_list.html", {
        "appeals": appeals
    })


@login_required
def process_appeal(request, appeal_id):
    """
    Traiter une demande
    """
    if request.user.role != "ADMIN":
        return render(request, "core/access_denied.html")

    appeal = get_object_or_404(Appeal, id=appeal_id)

    # 🔓 réactiver utilisateur
    appeal.user.is_suspended = False
    appeal.user.save()

    appeal.is_processed = True
    appeal.save()

    return redirect("appeals_list")