from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("base_template", views.base, name="base_template"),
    path("nearby", views.nearby, name="nearby"),
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),
    path("add_location", views.add_location, name='add_location'),
    path("add_item", views.add_item, name='add_item'),
    path("location/<int:location_id>/details",
         views.show_location_items,
         name='location_details'),
    path("add_review/<int:location_id>", views.add_review, name='add_review'),
    path("add_review_item/<int:item_id>",
         views.add_review_item,
         name='add_review_item'),
    path("item_info/<int:item_id>", views.item_info, name='item_info'),
    path("remove_user", views.remove_user, name='remove_user'),
    path("user_profile/<int:account_id>", views.profile, name='profile'),
    path("user_profile/update_profile", views.update_profile, name='update_profile'),
    path("user_profile/favorite_list",
         views.favorite_list,
         name='favorite_list'),
    path("remove_store/<int:location_id>",
         views.remove_store,
         name='remove_store'),
    path('remove_item/<int:item_id>', views.remove_item, name='remove_item'),
    path('favorite_item/<int:location_id>',
         views.favorite_item,
         name='favorite_item'),
    path('recommend_location/<int:location_id>',
         views.recommend_location,
         name='recommend_location')
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
