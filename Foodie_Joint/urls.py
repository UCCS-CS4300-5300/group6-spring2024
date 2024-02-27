from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("nav", views.nav, name="nav"),
    path("maybe", views.maybe, name="maybe"),
    path("backup", views.backup, name="backup"),
    path("base_template", views.base, name="base_template"),
    path("nearby", views.nearby, name="nearby")  # pass zip through url? Or only work when user logged in?
]
