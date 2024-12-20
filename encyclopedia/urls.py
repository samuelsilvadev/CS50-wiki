from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_by_title, name="search_by_title"),
    path("wiki/<str:title>", views.get_by_title, name="get_by_title"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("delete", views.delete, name="delete"),
    path("random", views.get_random_entry, name="random"),
]
