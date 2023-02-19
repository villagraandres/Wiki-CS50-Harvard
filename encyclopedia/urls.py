from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.showEntry, name="showEntry"),
    path("search", views.search, name="search"),
    path("add",views.add,name="add"),
    path("edit",views.edit,name="edit"),
    path("random",views.randomEntry,name="random")

]
