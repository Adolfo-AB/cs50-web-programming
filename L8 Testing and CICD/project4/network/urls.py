
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post", views.new_post, name="new_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/follow", views.follow_unfollow, name="follow_unfollow"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
