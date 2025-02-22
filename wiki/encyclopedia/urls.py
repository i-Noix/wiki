from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("TITLE/<str:title>", views.entry_page, name="entry_page"),
    path("error_page/<str:title>", views.error_page, name="error_page"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("random_page", views.random_page, name="random_page")
]
