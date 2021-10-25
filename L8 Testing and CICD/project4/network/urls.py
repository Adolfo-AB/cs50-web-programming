
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("add", views.add, name="add"),
    path("posts/<str:page>/", views.load, name="load"),
    path("posts/profile/<str:username>", views.load_profile, name="load_profile")
]
