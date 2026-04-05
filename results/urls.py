from django.urls import path
from .views import enter_results

urlpatterns = [
    path('enter/', enter_results, name='enter_results'),
]