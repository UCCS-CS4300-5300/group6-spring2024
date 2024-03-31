from django import forms
from django.forms import ModelForm
from .models import Location, Item, User, Review, ItemReview, Tag, ItemTag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# NOTE: ADD VALIDATION TO ADDRESS PARAMETER ENSUIRNG ITS REAL (TC)

class RegisterUserForm(UserCreationForm):
  email = forms.EmailField(widget=forms.EmailInput(
      attrs={'class': 'form-control'}))
  first_name = forms.CharField(
      max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
  last_name = forms.CharField(
      max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
  address = forms.CharField(
    max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

  class Meta:
    model = User
    fields = [
        'username', 'first_name', 'last_name', 'email', 'address', 'password1',
        'password2'
    ]

  def __init__(self, *args, **kwargs):
    super(RegisterUserForm, self).__init__(*args, **kwargs)

    self.fields['username'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].widget.attrs['class'] = 'form-control'


class LocationForm(ModelForm):

  class Meta:
    model = Location
    fields = ['name', 'description', 'location_type', 'address', 'tags', 'image']
    widgets = {
      'tags': forms.CheckboxSelectMultiple
    }


class ItemForm(forms.ModelForm):

  class Meta:
    model = Item
    fields = ['name', 'description', 'location', 'is_recommended', 'image']


#class UserForm(forms.ModelForm):

 # class Meta:
  #  model = User
   # fields = [
    #    'username', 'firstName', 'lastName', 'password', 'email', 'zipcode'
    #]


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
