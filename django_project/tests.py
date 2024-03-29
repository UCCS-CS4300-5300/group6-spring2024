from django.test import TestCase
from django.urls import reverse, resolve
from Foodie_Joint.models import Location
from Foodie_Joint.views import show_location_items

# For reference: https://docs.djangoproject.com/en/5.0/topics/testing/tools/
# Run these tests with 'python manage.py test'

############# START OF TYLER CARROLL TESTS #############
class NearbyViewTest(TestCase):
  def setUp(self):
    self.restaurant = Location.objects.create(
      name = "Albertacos",
      description = "Taco joint",
      location_type = Location.RESTAURANT,
      address = "4494 Austin Bluffs Pkwy"
    )
    self.store = Location.objects.create(
      name = "Family Dollar",
      description = "Dollar store",
      location_type = Location.STORE,
      address = "4609 Austin Bluffs Pkwy"
    )

  # Ensuring that the nearby.html template is used/returned by the nearby view
  def test_nearby_view_renders_proper_template(self):
    response = self.client.get(reverse('nearby'))
    self.assertTemplateUsed(response, 'templates/nearby.html')
    
  # Testing that a Restuarant object is shown on the 'nearby' page when 'Restaurant' selected in navbar
  def test_nearby_view_with_restaurant_nearby_page(self):
    # Simulating request after 'Resaurant' is selected in navbar. Should only list Restaurants.
    response = self.client.get('/nearby?type=Restaurant')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.restaurant.name)
    self.assertContains(response, self.restaurant.description)
    self.assertContains(response, self.restaurant.address)
    self.assertNotContains(response, self.store.name)

  # Testing that a Store object is shown on the 'nearby' page when 'Store' selected in navbar
  def test_nearby_view_with_store_nearby_page(self):
    response = self.client.get('/nearby?type=Store')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.store.name)
    self.assertContains(response, self.store.description)
    self.assertContains(response, self.store.address)
    self.assertNotContains(response, self.restaurant.name)

  # Testing that both Store and Restaurant objects are shown on the 'nearby' page when nearby page is accessed without type parameter
  # Potentially remove this test if a different page is used to show all Location objects
  def test_nearby_view_with_both_nearby_page(self):
    response = self.client.get('/nearby')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.store.name)
    self.assertContains(response, self.store.description)
    self.assertContains(response, self.store.address)
    self.assertContains(response, self.restaurant.name)
    self.assertContains(response, self.restaurant.description)
    self.assertContains(response, self.restaurant.address)

  # Testing that a message is provided if there are no Location objects for the 'nearby' page
  def test_nearby_view_with_no_locations(self):
    Location.objects.all().delete()
    response = self.client.get(reverse('nearby'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No locations found! Please add some locations to get started.")

  # Add test, testing user logged in and gets user address (when implemented)
    
############# END OF TYLER CARROLL TESTS #############

############# START OF DEREK GARY TESTS #############

class LocationItemResponseTest(TestCase):

  # Sets up the test data used in the tests.
  def setUp(self):
    self.location = Location.objects.create(
      name = "Test Location",
      description = "A test Description",
      location_type=Location.RESTAURANT,
      address="207 N Wahsatch Ave",
    )

  # Verifies if location_details URL correctly redirects to location_item_info page.
  def test_location_details_url(self):
    path = reverse('location_details', args=[1])
    resolved_path = resolve(path)
    self.assertEqual(resolved_path.func, show_location_items)

  # Checks if the correct data was received by the location_item_info page.
  def test_location_item_info_response(self):
    url = reverse('location_details', args=[self.location.id])
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['location'].id, self.location.id)
    self.assertContains(response, "Test Location")
    self.assertContains(response, "A test Description")
    self.assertContains(response, "207 N Wahsatch Ave")
############# END OF DEREK GARY TESTS #############


