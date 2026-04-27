from django.urls import path
from . import views

from elections.views.admin_views import admin_dashboard, validate_session

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path("admin-panel/", admin_dashboard, name="admin_dashboard"),
    path("validate/<int:session_id>/", validate_session, name="validate_session"),

]

