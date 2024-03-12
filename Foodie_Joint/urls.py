from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("base_template", views.base, name="base_template"),
    path("nearby", views.nearby, name="nearby"),
    path('login_user', views.login_user, name= 'login'),
    path('logout_user', views.logout_user, name = 'logout'),
    path('register_user', views.register_user, name = 'register'),
    path("add_location", views.add_location, name='add_location'),
    path("add_item", views.add_item, name='add_item'),
    path("<str:type>/<int:location_id>/location_details", views.show_location_items, name='location_details')
]
