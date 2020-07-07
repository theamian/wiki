from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:site>", views.site, name="site"),
    path("search", views.search, name="search")
]
