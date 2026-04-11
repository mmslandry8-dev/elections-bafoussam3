from django.urls import path
from .views import register_view, login_view, logout_view, appeal_view

from . import views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('appeal/', appeal_view, name='appeal_view'),

    path("users/", views.users_list, name="users_list"),
    path("users/<int:user_id>/role/", views.change_role, name="change_role"),
    path("users/<int:user_id>/toggle/", views.toggle_suspend, name="toggle_suspend"),

    path("appeals/", views.appeals_list, name="appeals_list"),
    path("appeals/<int:appeal_id>/process/", views.process_appeal, name="process_appeal"),
]