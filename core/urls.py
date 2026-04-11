from django.urls import path
from .views import access_denied_view

urlpatterns = [
    path('access-denied/', access_denied_view, name='access_denied'),
]