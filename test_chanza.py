import pytest
import django
django.setup()
import Foodie_Joint.urls
import Foodie_Joint.views
from Foodie_Joint.models import Location, Item
from Foodie_Joint.forms import LocationForm, ItemForm

def test_add_location_form():
  form = LocationForm()
  assert form.fields['name'].required
  assert form.fields['description'].required
  assert form.fields['type'].required
  assert form.fields['address'].required

def test_add_location():
  locationForm = LocationForm(data={'name': 'test', 'description': 'test', 'type': 'test', 'address': 'test'})
  assert locationForm.is_valid()

@pytest.mark.django_db
def test_add_item():
  itemForm = ItemForm(data={'name': 'test', 'description': 'test', 'location': Location.objects.first(), 'is_recommended': False})
  assert itemForm.is_valid()

def test_add_item_form():
  form = ItemForm()
  assert form.fields['name'].required
  assert form.fields['description'].required
  assert form.fields['location'].required
  assert form.fields['is_recommended'].required is False

def test_urls():
  urlpatterns = Foodie_Joint.urls.urlpatterns
  assert 'add_location' in [url.name for url in urlpatterns]
  assert 'add_item' in [url.name for url in urlpatterns]
  