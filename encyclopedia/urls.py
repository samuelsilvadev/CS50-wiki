from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_by_title, name="search_by_title"),
    path("wiki/<str:title>", views.get_by_title, name="get_by_title"),
]
