from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bu", views.bu, name="bu"),
    path("<str:name>", views.greet, name="greet")
]