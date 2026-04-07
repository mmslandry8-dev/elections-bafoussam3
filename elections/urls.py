from django.urls import path
from .views.location_views import centers_list

from .views.agent_views import create_vote_session

from .views.public_views import dashboard

urlpatterns = [
    path("centers/", centers_list, name="centers_list"),
    path("agent/vote/", create_vote_session, name="create_vote_session"),
    path("", dashboard, name="dashboard"),

]

from .views.public_views import seats_results

urlpatterns += [
    path("seats/", seats_results, name="seats_results"),
]