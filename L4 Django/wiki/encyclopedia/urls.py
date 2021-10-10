from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("edit_entry", views.edit_entry, name="edit_entry"),
    path("save", views.save, name="save"),
    path("save_edit", views.save_edit, name="save_edit"),
    path("search", views.search, name="search"),
    path("random", views.random_entry, name="random"),
    path("<str:entry>", views.entry, name="entry")
]
