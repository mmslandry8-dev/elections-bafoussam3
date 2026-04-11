# from django.urls import path
# from .views.location_views import centers_list

# from .views.agent_views import create_vote_session

# from .views.public_views import dashboard
# from .views.public_views import seats_results
# from .views.agent_views import create_vote_session

# urlpatterns = [
#     path("centers/", centers_list, name="centers_list"),
#     path("agent/vote/", create_vote_session, name="create_vote_session"),
#     path("", dashboard, name="dashboard"),
#     path("seats/", seats_results, name="seats_results")
# ]
from django.urls import path
from .views.location_views import centers_list, list_list
from .views.agent_views import create_vote_session
from .views.public_views import dashboard, seats_results
from .views.admin_views import admin_dashboard, validate_session

from .views.agent_views import vote_success

urlpatterns = [
    path("", dashboard, name="dashboard"),

    path("seats/", seats_results, name="seats_results"),

    path("centers/", centers_list, name="centers_list"),

    path("lists/", list_list, name="list_list"),  # ✅ ajouté

    path("agent/vote/", create_vote_session, name="create_vote_session"),

    path("admin-panel/", admin_dashboard, name="admin_dashboard"),
    path("validate/<int:session_id>/", validate_session, name="validate_session"),

    path("success/", vote_success, name="vote_success"),

]