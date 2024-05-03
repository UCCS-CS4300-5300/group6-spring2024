from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from Foodie_Joint.models import Item, Location, Account, TagCategory, TagItem, ItemReview
from Foodie_Joint.views import show_location_items
from unittest.mock import patch, Mock
from Foodie_Joint.utils import verify_address
from Foodie_Joint.forms import LocationForm
from django.contrib.messages import get_messages

# For reference: https://docs.djangoproject.com/en/5.0/topics/testing/tools/
# Run these tests with 'python manage.py test'


############# START OF TYLER CARROLL TESTS #############
class NearbyViewTest(TestCase):

  def setUp(self):
    self.user = User.objects.create_user(
        username='testUsername',
        email='user@test.com',
        password='testPass',
        first_name='firstName',
        last_name='lastName',
    )
    self.account = Account.objects.create(user=self.user,
                                          address="3650 N Nevada Ave",
                                          state="Test State",
                                          city="Test City",
                                          bio="Test Bio")
    self.client.login(username="testUsername", password="testPass")

    self.tag_category = TagCategory.objects.create(name="testCat")
    self.tag_item = TagItem.objects.create(category=self.tag_category,
                                           name="testName")

    self.restaurant = Location.objects.create(
        name="Albertacos",
        description="Taco joint",
        location_type=Location.RESTAURANT,
        address="4494 Austin Bluffs Pkwy",
        created_by=self.account)

    self.store = Location.objects.create(name="Family Dollar",
                                         description="Dollar store",
                                         location_type=Location.STORE,
                                         address="4609 Austin Bluffs Pkwy",
                                         created_by=self.account)

    self.restaurant.tags.add(self.tag_item)

  # Test to ensure that the Location Search is working
  class LocationSearchTestCase(TestCase):

    def setUp(self):
      Location.objects.create(name="Test Store",
                              address="123 Example St",
                              location_type="Store")
      Location.objects.create(name="Test Restaurant",
                              address="456 Sample Rd",
                              location_type="Restaurant")

    def test_search_locations(self):
      response = self.client.get(reverse('location_list'),
                                 {'search_name': 'store'})
      self.assertContains(response, "Test Store")
      self.assertNotContains(response, "Test Restaurant")

  # Ensuring that the nearby.html template is used/returned by the nearby view
  def test_nearby_view_renders_proper_template(self):
    response = self.client.get(reverse('nearby'))
    self.assertTemplateUsed(response, 'templates/nearby.html')

  # Testing that the nearby view returns the proper (created) tags
  def test_nearby_view_renders_template_with_created_tags(self):
    response = self.client.get(reverse('nearby'))
    # Ensuring the proper tags and categories are shown
    self.assertContains(response, self.tag_item.name)
    self.assertContains(response, self.tag_category.name)
    self.assertNotContains(response, "Not A Tag!")
    self.assertNotContains(response, "Not A Tag Category!")

  # Testing that a Restuarant object is shown on the 'nearby' page when 'Restaurant' selected in navbar
  def test_nearby_view_with_restaurant_nearby_page(self):
    # Simulating request after 'Resaurant' is selected in navbar. Should only list Restaurants.
    response = self.client.get('/nearby?type=Restaurant')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.restaurant.name)
    self.assertContains(response, self.restaurant.description)
    self.assertContains(response, self.restaurant.address)
    self.assertContains(response,
                        "4.01 mi")  # Distance from user to restaurant
    self.assertNotContains(response, self.store.name)
    self.assertContains(response, self.user.account.address
                        )  # Ensuring user address is shown on nearby page

  # Testing that a Store object is shown on the 'nearby' page when 'Store' selected in navbar
  def test_nearby_view_with_store_nearby_page(self):
    response = self.client.get('/nearby?type=Store')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.store.name)
    self.assertContains(response, self.store.description)
    self.assertContains(response, self.store.address)
    self.assertNotContains(response, self.restaurant.name)

  # Testing that both Store and Restaurant objects are shown on the 'nearby' page when nearby page is accessed without type parameter
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
    self.assertContains(
        response,
        "No locations found! Please add some locations to get started.")

  # Testing that when on the Restaurant page, only the restaurant obj is shown when its tag is selected
  def test_nearby_view_with_all_filters(self):
    response = self.client.get('/nearby?tag=testName&type=Restaurant')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.restaurant.name)
    self.assertContains(response, self.restaurant.description)
    self.assertContains(response, self.restaurant.address)
    self.assertNotContains(response, self.store.name)
    self.assertNotContains(response, self.store.description)
    self.assertNotContains(response, self.store.address)

  # Testing that when on the Store page, nothing is showed with the 'Mexican' filter
  def test_nearby_view_with_mexican_filter(self):
    response = self.client.get('/nearby?tag=Mexican&type=Store')
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, self.restaurant.name)
    self.assertNotContains(response, self.restaurant.description)
    self.assertNotContains(response, self.restaurant.address)
    self.assertNotContains(response, self.store.name)
    self.assertNotContains(response, self.store.description)
    self.assertNotContains(response, self.store.address)

  # Testing that the user's address is shown on the 'nearby' page when user logged in
  def test_nearby_view_renders_template_with_user_address_user_loggedIn(self):
    response = self.client.get(reverse('nearby'))
    self.assertContains(response, self.user.account.address)

  # Testing that the static address is shown on the 'nearby' page when user NOT logged in
  def test_nearby_view_renders_template_with_static_address_user_notLoggedIn(
      self):
    self.client.logout()
    response = self.client.get(reverse('nearby'))
    self.assertContains(response, "1420 Austin Bluffs Pkwy")
    self.assertNotContains(response, self.user.account.address)


class ProfileViewTest(TestCase):

  def setUp(self):
    self.user1 = User.objects.create_user(
        username='testUser1',
        email='user1@test.com',
        password='testPass',
        first_name='firstName1',
        last_name='lastName1',
    )
    self.account1 = Account.objects.create(user=self.user,
                                           address="3650 N Nevada Ave",
                                           state="Test State",
                                           city="Test City",
                                           bio="Test Bio")
    self.user2 = User.objects.create_user(
        username='testUser2',
        email='user2@test.com',
        password='testPass',
        first_name='firstName2',
        last_name='lastName2',
    )
    self.account2 = Account.objects.create(user=self.user,
                                           address="3504 N Academy Blvd",
                                           state="Test State",
                                           city="Test City",
                                           bio="Test Bio")

    self.restaurant = Location.objects.create(
        name="Albertacos",
        description="Taco joint",
        location_type=Location.RESTAURANT,
        address="4494 Austin Bluffs Pkwy",
        created_by=self.account1)

    # Note, this store object is created by a DIFFERENT user
    self.store = Location.objects.create(name="Family Dollar",
                                         description="Dollar store",
                                         location_type=Location.STORE,
                                         address="4609 Austin Bluffs Pkwy",
                                         created_by=self.account2)

    # Favoriting the store as account1
    self.account1.favorites.add(self.store)

    # Testing that the update_profile view returns the proper template
    def test_update_profile_view_renders_proper_template(self):
      response = self.client.get(reverse('update_profile'))
      self.assertTemplateUsed(response, 'templates/update_profile.html')

    # Testing trying to access account settings without logging in
    def test_update_profile_view_redirects_to_login_user_NOT_logged(self):
      response = self.client.get(reverse('update_profile'))
      self.assertRedirects(response, '/login/?next=/update_profile/')

    # Testing that the update_profile view renders with logged in user's info
    def test_update_profile_view_when_user_logged_in(self):
      self.client.login(username='testUser1', password='testPass')
      response = self.client.get(reverse('update_profile'))
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, "User settings for testUser1")
      self.assertContains(response, self.account1.address)
      self.assertContains(response, self.account1.state)
      self.assertContains(response, self.account1.city)
      self.assertContains(response, self.account1.bio)
      self.assertNotContains(response, "User settings for testUser2")
      self.client.logout()

    # Testing that the update_profile view does not render a user's info when not logged in
    def test_update_profile_view_when_user_NOT_logged_in(self):
      response = self.client.get(reverse('update_profile'))
      self.assertEqual(response.status_code, 200)
      self.assertNotContains(response, "User settings for testUser1")
      self.assertNotContains(response, self.account1.address)
      self.assertNotContains(response, self.account1.state)
      self.assertNotContains(response, self.account1.city)
      self.assertNotContains(response, self.account1.bio)
      self.assertNotContains(response, "User settings for testUser2")

    # Testing a user's public profile
    def test_user_profile_view_renders_proper_template(self):
      response = self.client.get(
          reverse('user_profile', args=[self.account1.id]))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'templates/user_profile.html')

    # Testing a user's public profile renders with proper context (not logged in - doesnt have to be)
    def test_user_profile_view_renders_proper_user(self):
      response = self.client.get(
          reverse('user_profile', args=[self.account1.id]))
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, "testUser1's Profile")
      self.assertContains(response, self.account1.bio)
      self.assertContains(
          response, self.restaurant.name)  # Should show user's created objects
      self.assertContains(response,
                          self.store.name)  # Should show a user's favorites
      self.assertNotContains(response, self.account2.user.first_name)


############# END OF TYLER CARROLL TESTS #############

############# START OF DEREK GARY TESTS #############


######### UNIT TESTS #########

class VerifyAddressTest(TestCase):

  def setUp(self):
    self.valid_address = "802 E Rio Grande St"
    self.invalid_address = "999 Fake St"

    self.valid_response = [{
        'address': {
            'city': 'Colorado Springs',
            'state': 'Colorado'
        }
    }]

    self.invalid_response = [{
        # Should be empty in the case of malformed input
        'address': {}
    }]

  @patch('Foodie_Joint.utils.requests.get')
  def test_verify_address_valid(self, mock_get):
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = self.valid_response

    self.assertTrue(verify_address(self.valid_address))

  @patch('Foodie_Joint.utils.requests.get')
  def test_verify_address_invalid(self, mock_get):
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = self.invalid_response

    self.assertFalse(verify_address(self.invalid_address))

  @patch('Foodie_Joint.utils.requests.get')
  def test_verify_address_no_data(self, mock_get):
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = []

    self.assertFalse(verify_address(self.valid_address))


######### INTEGRATION TESTS #########

class LocationItemResponseTest(TestCase):

  def setUp(self):
    user = get_user_model().objects.create_user(username='user',
                                                email='user@a.com',
                                                password='sadfgAQq43!')

    account = Account.objects.create(
        user=user,
        address="802 E Rio Grande St",
        city="Colorado Springs",
        state="CO",
    )

    self.location = Location.objects.create(name="Test Location",
                                            description="A test Description",
                                            location_type=Location.RESTAURANT,
                                            address="207 N Wahsatch Ave",
                                            created_by=account)

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


class StoreRecommendationTest(TestCase):

  def setUp(self):
    self.user = get_user_model().objects.create_superuser(
        'admin', 'admin@adminStuff.com', 'uniquePW1')
    self.client.login(username='admin', password='uniquePW1')

    self.location1 = Location.objects.create(name="Test Location 1",
                                             address="207 N Wahsatch Ave",
                                             description="A test Description",
                                             location_type=Location.RESTAURANT,
                                             is_recommended=False)

    self.location2 = Location.objects.create(name="Test Location 2",
                                             address="208 N Wahsatch Ave",
                                             description="A test Description",
                                             location_type=Location.RESTAURANT,
                                             is_recommended=False)

  def test_recommend_location(self):
    self.assertFalse(Location.objects.filter(is_recommended=True).exists())
    response = self.client.post(
        reverse('recommend_location', args=[self.location1.id]))
    self.assertTrue(Location.objects.get(id=self.location1.id).is_recommended)
    self.assertFalse(Location.objects.get(id=self.location2.id).is_recommended)
    self.assertRedirects(response, reverse('index'))

    self.client.post(reverse('recommend_location', args=[self.location2.id]))
    self.assertFalse(Location.objects.get(id=self.location1.id).is_recommended)
    self.assertTrue(Location.objects.get(id=self.location2.id).is_recommended)


class IndexViewTest(TestCase):

  def setUp(self):
    # Create a test user
    self.test_user = User.objects.create_user(username='testuser',
                                              email='testuser@example.com',
                                              password='testpassword')

    # Create an Account
    self.test_account = Account.objects.create(user=self.test_user,
                                               address="806 E Rio Grande St",
                                               city="Colorado Springs",
                                               state="Colorado",
                                               bio="Test Bio")

    # Create a location
    self.location = Location.objects.create(
        name="Test Location",
        description="This is a test location",
        location_type="Restaurant",
        address="803 E Rio Grande St.")

    # Create a recommended item
    self.recommended_item = Item.objects.create(
        name="Recommended Item",
        description="This is a recommended item",
        is_recommended=True,
        location=self.location)

    # Create item reviews with the test account
    self.item_review1 = ItemReview.objects.create(item=self.recommended_item,
                                                  user=self.test_account,
                                                  review="Great item!",
                                                  num_stars=5)
    self.item_review2 = ItemReview.objects.create(item=self.recommended_item,
                                                  user=self.test_account,
                                                  review="Average item",
                                                  num_stars=3)
    self.item_review3 = ItemReview.objects.create(item=self.recommended_item,
                                                  user=self.test_account,
                                                  review="Poor item",
                                                  num_stars=1)

  # Happy path test
  def test_index_view_with_recommended_item_and_reviews(self):
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'templates/index.html')
    self.assertEqual(response.context['recommended_item'],
                     self.recommended_item)
    self.assertQuerysetEqual(response.context['item_reviews'],
                             [self.item_review1, self.item_review2],
                             ordered=False)

  # Sad path test
  def test_index_view_with_recommended_item_and_no_reviews(self):
    ItemReview.objects.all().delete()
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'templates/index.html')
    self.assertEqual(response.context['recommended_item'],
                     self.recommended_item)
    self.assertQuerysetEqual(response.context['item_reviews'], [])


class UpdateProfileViewTest(TestCase):

  def setUp(self):
    self.user = User.objects.create_user(
        username='testUsername',
        email='user@test.com',
        password='testPass',
        first_name='firstName',
        last_name='lastName',
    )
    self.account = Account.objects.create(user=self.user,
                                          address="802 E Rio Grande St.",
                                          state="Test State",
                                          city="Test City",
                                          bio="Test Bio")

    self.url = reverse('update_profile')
    self.login_url = reverse('login')
    self.client.login(username="testUsername", password="testPass")

  # Test User Auth
  def test_redirect_if_not_logged_in(self):
    self.client.logout()
    response = self.client.get(self.url)
    self.assertRedirects(response, f'{self.login_url}?next={self.url}')

  # Test invalid form post request
  def test_post_invalid_form(self):
    self.client.login(username='testUsername', password='testPass')
    form_data = {
        'email': 'invalidemail',
        'address': '802 E Rio Grande St.',
    }
    response = self.client.post(self.url, form_data)
    self.assertEqual(response.status_code, 200)

    messages = [
        str(message) for message in get_messages(response.wsgi_request)
    ]
    print("Messages: ", messages)
    self.assertTrue(
        'Form is not valid. Please verify the address is within Colorado Springs.'
        in messages)

  def test_invalid_address(self):
    self.client.login(username='testUsername', password='testPass')
    form_data = {
        'email': 'user@example.com',
        'address': 'Invalid address',
        'city': 'Colorado Springs',
        'state': 'CO'
    }
    response = self.client.post(self.url, form_data)
    messages = [
        str(message) for message in get_messages(response.wsgi_request)
    ]
    self.assertIn(
        'Form is not valid. Please verify the address is within Colorado Springs.',
        messages)


class AddLocationViewTest(TestCase):

  def setUp(self):
    self.user = User.objects.create_user(
        username='testUsername',
        email='user@test.com',
        password='testPass',
        first_name='firstName',
        last_name='lastName',
    )
    self.account = Account.objects.create(user=self.user,
                                          address="802 E Rio Grande St.",
                                          state="Test State",
                                          city="Test City",
                                          bio="Test Bio")

    self.client.login(username="testUsername", password="testPass")

    # Create sample tags and categories
    self.tag_category = TagCategory.objects.create(name='Test Category')
    self.tag = TagItem.objects.create(category=self.tag_category,
                                      name='Test Tag')

    # URL for the add_location view
    self.url = reverse('add_location')

  def test_get_add_location(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'templates/add_location.html')
    self.assertIsInstance(response.context['form'], LocationForm)
    self.assertFalse(response.context['submitted'])

  def test_post_valid_add_location(self):
    form_data = {
        'name': 'New Location',
        'description': 'A great place to visit.',
        'location_type': 'Restaurant',
        'address': '806 E Rio Grande St',
        'tags': [self.tag.id]
    }
    response = self.client.post(self.url, form_data)
    self.assertEqual(response.status_code, 302)
    self.assertTrue(Location.objects.filter(name='New Location').exists())

  def test_post_invalid_add_location(self):
    response = self.client.post(self.url, {})
    self.assertEqual(response.status_code, 200)
    self.assertFormError(response, 'form', 'name', 'This field is required.')
    self.assertFalse(Location.objects.exists())

  def test_post_invalid_add_location(self):
    response = self.client.post(self.url, {})
    self.assertEqual(response.status_code, 200)
    form = response.context['form']
    self.assertFalse(form.is_valid())
    self.assertTrue('name' in form.errors)
    self.assertIn('This field is required.', form.errors['name'])
    self.assertFalse(Location.objects.exists())


######### FUNCTIONAL TESTS #########

# Tests the removal of an item by a superuser and verifies the redirect to the 'nearby' page.
class ItemRemovalTest(TestCase):

  def setUp(self):
    User = get_user_model()
    self.admin_user = User.objects.create_superuser('admin', 'admin@test.com',
                                                    'adminpass')
    # Ensure the account is linked correctly with the specific required address
    self.account = Account.objects.create(user=self.admin_user,
                                          address="802 E Rio Grande St.",
                                          city="Colorado Springs",
                                          state="CO",
                                          bio="Admin user bio")
    self.client.login(username='admin', password='adminpass')
    # Create a location with the specific test address
    self.location = Location.objects.create(name="Test Location",
                                            address="207 Wahsatch Ave",
                                            description="A test Description",
                                            location_type=Location.RESTAURANT)
    self.item = Item.objects.create(name="Test Item", location=self.location)

  def test_remove_item(self):
    items_before = Item.objects.count()
    response = self.client.post(
        reverse('remove_item', kwargs={'item_id': self.item.id}))
    items_after = Item.objects.count()
    self.assertEqual(items_before - 1, items_after)


# Tests the removal of a store by a superuser and ensures proper redirect to the 'nearby' page.
class StoreRemovalTest(TestCase):

  def setUp(self):
    User = get_user_model()
    self.admin_user = User.objects.create_superuser('admin',
                                                    'admin@adminStuff.com',
                                                    'uniquePW1')
    self.account = Account.objects.create(user=self.admin_user,
                                          address="802 E Rio Grande St.")
    self.location = Location.objects.create(name="Test Location",
                                            address="805 E Rio Grande St.")

  def test_remove_store(self):
    self.client.login(username='admin', password='uniquePW1')
    locations_before = Location.objects.count()
    response = self.client.post(
        reverse('remove_store', kwargs={'location_id': self.location.id}))
    locations_after = Location.objects.count()
    self.assertEqual(locations_before - 1, locations_after)


class UserRegistrationTest(TestCase):

  def test_valid_registration(self):
    response = self.client.post(
        reverse('register'), {
            'username': 'newuser',
            'password': 'password123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'address': '802 E Rio Grande St',
            'state': 'CO',
            'city': 'Colorado Springs',
            'profile_picture': '',
            'bio': 'Test bio',
        })
    self.assertRedirects(response, reverse('index'))
    self.assertTrue(User.objects.filter(username='newuser').exists())
    self.assertTrue(Account.objects.filter(user__username='newuser').exists())

  def test_taken_username_registration(self):
    User.objects.create_user(username='existinguser',
                             email='existinguser@example.com',
                             password='password123',
                             first_name='Existing',
                             last_name='User')
    Account.objects.create(user=User.objects.get(username='existinguser'),
                           address='802 E Rio Grande St',
                           state='CO',
                           city='Colorado Springs',
                           bio='Test bio')

    response = self.client.post(
        reverse('register'), {
            'username': 'existinguser',
            'password': 'password123',
            'email': 'existinguser@example.com',
            'first_name': 'Existing',
            'last_name': 'User',
            'address': '802 E Rio Grande St',
            'state': 'CO',
            'city': 'Colorado Springs',
            'profile_picture': '',
            'bio': 'Test bio',
        })

    # Trying to figure out wtf is going on here
    # print("Response content:", response.content.decode())

    self.assertContains(
        response, "Username already exists. Please choose another username.")
    self.assertEqual(User.objects.filter(username='existinguser').count(), 1)
    self.assertEqual(
        Account.objects.filter(user__username='existinguser').count(), 1)


######### VIEW TESTS #########

class BaseViewTest(TestCase):

  def test_base_view_200_response(self):
    response = self.client.get(reverse('base_template'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'templates/base_template.html')


############# END OF DEREK GARY TESTS ############


# Correct this test because it causes other tests not to run!
############# START OF LUKE FLANCHER TESTS #############
class UsersTests(TestCase):

  def setUp(self):
    User = get_user_model()
    self.new_user1 = User.objects.create_user(username='new_user1',
                                              password='adfjkfjk;fds2342',
                                              email='new1@user.com')
    self.new_user2 = User.objects.create_user(username='new_user2',
                                              password='adfjkfjk;fds2342',
                                              email='new2@user.com')

  def test_user_creation(self):
    # Assert that the users were actually created with matching attr.
    self.assertEqual(self.new_user1.username, 'new_user1')
    self.assertEqual(self.new_user1.email, 'new1@user.com')

    self.assertEqual(self.new_user2.username, 'new_user2')
    self.assertEqual(self.new_user2.email, 'new2@user.com')


############# END OF LUKE FLANCHER TESTS #############
