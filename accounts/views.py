from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, AppealForm
from .models import User

def register_view(request):
    """
    Inscription utilisateur
    """
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Connexion utilisateur avec gestion suspension
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_suspended:
                # Rediriger vers page appel
                return redirect('appeal')
            login(request, user)
            return redirect('home')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def appeal_view(request):
    """
    Demande de réactivation
    """
    if not request.user.is_authenticated:
        return redirect('login')

    form = AppealForm(request.POST or None)

    if form.is_valid():
        appeal = form.save(commit=False)
        appeal.user = request.user
        appeal.save()
        return redirect('login')

    return render(request, 'accounts/appeal.html', {'form': form})