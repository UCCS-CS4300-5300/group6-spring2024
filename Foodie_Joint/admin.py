from django.contrib import admin

# Register your models here.
from .models import Location
from .models import Item
from .models import Review

# Create an Item Update Action and Interface for the Admin to Mark an Item as Recommended
# Resources used: 'https://docs.djangoproject.com/en/5.0/ref/contrib/admin/actions/'
#                 'https://docs.djangoproject.com/en/5.0/ref/contrib/admin/actions/#the-action-decorator'
#                 'https://docs.djangoproject.com/en/5.0/ref/models/querysets/#update'
#                 'https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_editable'

# Customize the Admin Interface for the Item Model
class ItemAdmin(admin.ModelAdmin):
  list_display = ["name", "is_recommended",
                  "description"]  # Fields to display in Admin panel
  list_editable = ["is_recommended",
                   "description"]  # Fields to allow for editing in Admin panel
  ordering = ["name"]  # Order by name in ascending order


admin.site.register(Location)
admin.site.register(Item, ItemAdmin)
admin.site.register(Review)
