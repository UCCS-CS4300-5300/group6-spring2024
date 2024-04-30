from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Location, Item, TagItem, TagCategory, Account, Review, ItemReview


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

# Extended the generic Django User model to include some account details (address, etc.).
# This makes it so that this relationship can be seen/edited in the Admin panel.
# Resource: https://www.youtube.com/watch?v=kRJpQxi2jIo&ab_channel=JimShapedCoding
class AccountInline(admin.StackedInline):
  model = Account
  can_delete = False
  verbose_name_plural = 'Accounts'

class CustomUserAdmin(UserAdmin):
  inlines = (AccountInline, )

admin.site.register(Location)
admin.site.register(TagCategory)
admin.site.register(TagItem)
admin.site.register(Item, ItemAdmin)
admin.site.unregister(User)  # Unregistering the default Django User model
admin.site.register(User, CustomUserAdmin)  # Registering the Custom User model
admin.site.register(Review)
admin.site.register(ItemReview)
#admin.site.register(Tag)
#admin.site.register(ItemTag)