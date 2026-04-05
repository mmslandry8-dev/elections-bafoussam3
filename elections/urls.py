from django.urls import path
from .views.location_views import centers_list

urlpatterns = [
    path("centers/", centers_list, name="centers_list"),
]