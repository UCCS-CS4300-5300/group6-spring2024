from django.contrib import admin

# Register your models here.
from .models import Location
from .models import Item
from .models import Review

admin.site.register(Location)
admin.site.register(Item)
admin.site.register(Review)