import pytest
import django
django.setup()
import Foodie_Joint.urls
import Foodie_Joint.views
from Foodie_Joint.models import Location, TagCategory
from Foodie_Joint.forms import LocationForm, ItemForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
import random

# Run these tests with 'pytest'

def test_add_location_form():
  form = LocationForm()
  assert form.fields['name'].required
  assert form.fields['description'].required
  assert form.fields['location_type'].required
  assert form.fields['address'].required
  assert form.fields['tags'].required
  assert form.fields['image'].required is False

def test_add_item_form():
  form = ItemForm()
  assert form.fields['name'].required
  assert form.fields['description'].required
  assert form.fields['is_recommended'].required is False
  assert form.fields['image'].required is False

@pytest.mark.django_db
def test_add_location_failure():
  image = SimpleUploadedFile(name='test_image.png', content=open('media/images/foodie-joint-logo.png', 'rb').read(), content_type='image/png')
  locationForm = LocationForm(data={'name': 'test', 'description': 'test', 'location_type': None, 'address': 'test', 'tags': [1], 'image': image})
  assert not locationForm.is_valid()

@pytest.mark.django_db
def test_add_item():
  image = SimpleUploadedFile(name='test_image.png', content=open('media/images/foodie-joint-logo.png', 'rb').read(), content_type='image/png')
  itemForm = ItemForm(data={'name': 'test', 'description': 'test', 'is_recommended': False, 'image': image})
  assert itemForm.is_valid()

@pytest.mark.django_db
def test_add_item_failure():
  image = SimpleUploadedFile(name='test_image.png', content=open('media/images/foodie-joint-logo.png', 'rb').read(), content_type='image/png')
  itemForm = ItemForm(data={'name': '51aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaas', 'description': 'test', 'is_recommended': False, 'image': image})
  assert not itemForm.is_valid()

def test_urls():
  urlpatterns = Foodie_Joint.urls.urlpatterns
  assert 'add_location' in [url.name for url in urlpatterns]
  assert 'add_item' in [url.name for url in urlpatterns]

class TestViews(TestCase):
  @pytest.mark.django_db
  def test_add_location(self):
    client = Client()
    response = client.post(reverse('add_location'), {'name': 'test', 'description': 'test', 'location_type': next(iter(Location.LOCATION_CHOICES.keys())), 'address': 'test', 'tags': [1]})
    assert response.status_code == 302
  
  def test_favorite_item(self):
    client = Client()
    response = client.post(reverse('favorite_item', args=[1]))
    assert response.status_code == 302