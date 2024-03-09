from django import forms
from django.forms import ModelForm
from .models import Location, Item, User, Review, ItemReview, Tag, ItemTag

class LocationForm(ModelForm):

  class Meta:
    model = Location
    fields = ['name', 'description', 'type', 'address']

class ItemForm(forms.ModelForm):

  class Meta:
    model = Item
    fields = ['name', 'description', 'location', 'is_recommended']

class UserForm(forms.ModelForm):

  class Meta:
    model = User
    fields = ['username', 'firstName', 'lastName', 'password', 'email', 'zipcode']

class ReviewForm(forms.ModelForm):

  class Meta:
    model = Review
    fields = ['user', 'location', 'review', 'num_stars']

class ItemReviewForm(forms.ModelForm):

  class Meta:
    model = ItemReview
    fields = ['user', 'item', 'review', 'num_stars']

class TagForm(forms.ModelForm):

  class Meta:
    model = Tag
    fields = ['title', 'location']

class ItemTagForm(forms.ModelForm):

  class Meta:
    model = ItemTag
    fields = ['title', 'item']