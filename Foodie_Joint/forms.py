from django import forms
from django.forms import ModelForm
from .models import Location, Item, Account, Review, ItemReview, TagCategory, TagItem
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .utils import verify_address

# NOTE: ADD VALIDATION TO ADDRESS PARAMETER ENSUIRNG ITS REAL (TC)


class RegistrationForm(ModelForm):
  # This part is used for the generic User model
  username = forms.CharField(
      max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
  email = forms.EmailField(widget=forms.EmailInput(
      attrs={'class': 'form-control'}))
  first_name = forms.CharField(
      max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
  last_name = forms.CharField(
      max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(widget=forms.PasswordInput(
      attrs={'class': 'form-control'}))

  # This part is used for the custom User model (Account)
  class Meta:
    model = Account
    fields = [
        'username', 'password', 'email', 'first_name', 'last_name', 'address',
        'state', 'city', 'profile_picture', 'bio'
    ]
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
        'address':
        forms.TextInput(attrs={'class': 'form-control'}),
        'state':
        forms.TextInput(attrs={'class': 'form-control'}),
        'city':
        forms.TextInput(attrs={'class': 'form-control'}),
        'profile_picture':
        forms.FileInput(attrs={'class': 'form-control'}),
        'bio':
        forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'This can be changed later...'
        })
    }

  # Address verification for user registration.
  def clean_address(self):
    address = self.cleaned_data.get('address')
    if not verify_address(address):
      raise ValidationError(
          'Please enter a valid Colorado Springs address. (Ex: 802 E Rio Grande St, APT 42)'
      )
    return address


class LocationForm(ModelForm):
  tags = forms.ModelMultipleChoiceField(queryset=TagItem.objects.all(),
                                        widget=forms.CheckboxSelectMultiple)

  class Meta:
    model = Location
    fields = [
        'name', 'description', 'location_type', 'address', 'tags', 'image'
    ]
    labels = {
        'name': 'Name',
        'description': 'Description',
        'location_type': 'Location Type',
        'address': 'Address',
        'tags': 'Tags',
        'image': 'Image'
    }
    widgets = {
        'name':
        forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name of Location'
        }),
        'description':
        forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Description of Location'
        }),
        'location_type':
        forms.Select(attrs={'class': 'form-control'}),
        'address':
        forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1111 A Place Lane'
        }),
        'image':
        forms.FileInput(attrs={'class': 'form-control'}),
    }

    # Address verification
  def clean_address(self):
    address = self.cleaned_data.get('address')
    if not verify_address(address):
      raise ValidationError(
          'Please enter a valid Colorado Springs address. (Ex: 802 E Rio Grande St, APT 42)'
      )
    return address


class ItemForm(forms.ModelForm):

  class Meta:
    model = Item
    fields = ['name', 'description', 'is_recommended', 'image']
    labels = {
        'name': 'Name',
        'description': 'Description',
        'is_recommended': 'Recommended?',
        'image': 'Image'
    }
    widgets = {
        'name':
        forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name of Item'
        }),
        'description':
        forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Description of Item'
        }),
        'image':
        forms.FileInput(attrs={'class': 'form-control'})
    }


class ReviewForm(forms.ModelForm):

  class Meta:
    model = Review
    fields = ['review', 'num_stars']
    labels = {
        'num_stars': 'Stars',
    }


class ItemReviewForm(forms.ModelForm):

  class Meta:
    model = ItemReview
    fields = ['review', 'num_stars']
    labels = {
        'num_stars': 'Stars',
    }


class UpdateAccountForm(forms.ModelForm):
  email = forms.EmailField(widget=forms.EmailInput(
      attrs={'class': 'form-control'}))

  class Meta:
    model = Account
    fields = ['address', 'state', 'city', 'email', 'profile_picture', 'bio']
    labels = {
        'address': 'Address',
        'state': 'State',
        'city': 'City',
        'email': 'Email',
        'profile_picture': 'Profile Picture',
        'bio': 'About Me'
    }
    widgets = {
        'address':
        forms.TextInput(attrs={'class': 'form-control'}),
        'state':
        forms.TextInput(attrs={'class': 'form-control'}),
        'city':
        forms.TextInput(attrs={'class': 'form-control'}),
        'profile_picture':
        forms.FileInput(attrs={'class': 'form-control'}),
        'bio':
        forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write something about yourself...'
            })
    }
    # Address verification for account update.
  def clean_address(self):
    address = self.cleaned_data.get('address')
    if not verify_address(address):
        raise ValidationError('Please enter a valid Colorado Springs address. (Ex: 802 E Rio Grande St, APT 42)')
    return address

