from django import forms
from django.forms import ModelForm
from .models import Location, Item, Account, Review, ItemReview#, Tag, ItemTag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# NOTE: ADD VALIDATION TO ADDRESS PARAMETER ENSUIRNG ITS REAL (TC)

class RegistrationForm(ModelForm):
  # This part is used for the generic User model
  username = forms.CharField(
    max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
  first_name = forms.CharField(
    max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
  last_name = forms.CharField(
    max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

  # This part is used for the custom User model (Account)
  class Meta:
    model = Account
    fields = ['username',
              'password',
              'email',
              'first_name',
              'last_name',
              'address',
              'state',
              'city',
              'profile_picture',
              'bio']
    labels = {
      'username': 'Username',
      'password': 'Password',
      'email': 'Email',
      'first_name': 'First Name',
      'last_name': 'Last Name',
      'address': 'Address',
      'state': 'State',
      'city': 'City',
      'profile_picture': 'Profile Picture (Optional)',
      'bio': 'About Me (Optional)'
    }
    widgets = {
      'address': forms.TextInput(attrs={'class': 'form-control'}),
      'state': forms.TextInput(attrs={'class': 'form-control'}),
      'city': forms.TextInput(attrs={'class': 'form-control'}),
      'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
      'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'This can be changed later...'})
    }


class LocationForm(ModelForm):
  
  class Meta:
    model = Location
    fields = ['name', 'description', 'location_type', 'address', 'tags', 'image']
    labels = {
      'name': 'Name',
      'description': 'Description',
      'location_type': 'Location Type',
      'address': 'Address',
      'tags': 'Tags',
      'image': 'Image'
    }
    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of Location'}),
      'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description of Location'}),
      'location_type': forms.Select(attrs={'class': 'form-control'}),
      'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1111 A Place Lane'}),
      'image': forms.FileInput(attrs={'class': 'form-control'}),
      'tags': forms.CheckboxSelectMultiple
    }


class ItemForm(forms.ModelForm):

  class Meta:
    model = Item
    fields = ['name', 'description', 'location', 'is_recommended', 'image']
    labels = {
      'name': 'Name',
      'description': 'Description',
      'location': 'Location',
      'is_recommended': 'Recommended?',
      'image': 'Image'
    }
    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of Item'}),
      'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description of Item'}),
      'location': forms.Select(attrs={'class': 'form-control'}),
      'image': forms.FileInput(attrs={'class': 'form-control'})
    }


class ReviewForm(forms.ModelForm):

  class Meta:
    model = Review
    fields = ['user', 'location', 'review', 'num_stars']


class ItemReviewForm(forms.ModelForm):

  class Meta:
    model = ItemReview
    fields = ['user', 'item', 'review', 'num_stars']
    

# FINISH THIS!!!
class UpdateAccountForm(forms.ModelForm):
  #address = forms.CharField(max_length = 255, 
  #                          widget=forms.TextInput(attrs={'class': 'form-control'}))
  class Meta:
    model = Account 
    fields = ['address',
             ]
    labels = {
      'address': 'Address'
    }
    widgets = {
      'address': forms.TextInput(attrs={'class': 'form-control'}),
    }

