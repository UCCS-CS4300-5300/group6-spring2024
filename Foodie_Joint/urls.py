from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("base_template", views.base, name="base_template"),
    path("nearby", views.nearby, name="nearby"),
    path('login_user', views.login_user, name= 'login'),
    path('logout_user', views.logout_user, name = 'logout'),# pass zip through url? Or only work when user logged in?
]
