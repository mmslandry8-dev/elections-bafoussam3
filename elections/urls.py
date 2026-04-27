from django.urls import path
from .views import *
from .views.public_views import dashboard

from elections.views.vote_views import voter_identification, vote_page

from elections.views.agent_views import physical_results_view

from .views.admin_views import electoral_list_admin

from .views.admin_views import add_elector

from .views.agent_views import agent_electors, mark_voted

from .views.vote_views import vote_page

urlpatterns = [
    path("", dashboard, name="dashboard"),

    path("vote/", voter_identification, name="voter_identification"),
    path("vote/page/", vote_page, name="vote_page"),

    path("agent/physical-results/", physical_results_view, name="physical_results"),

    path("electors/", electoral_list_admin, name="electoral_list_admin"),
    
    path("electors/add/", add_elector, name="add_elector"),

    path("agent/electors/", agent_electors, name="agent_electors"),
    path("agent/electors/<int:elector_id>/vote/", mark_voted, name="mark_voted"),
    
    # path("vote/", vote_page, name="vote_page"),
]