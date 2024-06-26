import requests  # Used to request info from API
import re  # Used for regex
from geopy.distance import distance
from .models import TagCategory, TagItem

# References:
# https://geopy.readthedocs.io/en/stable/#module-geopy.distance
# https://nominatim.org/release-docs/latest/api/Search/
BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'
# Added user-agent to request header to avoid 403 error (forbidden)
# https://operations.osmfoundation.org/policies/nominatim/
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Foodie_Joint/1.0 (tcarroll@uccs.edu)"


# Function to request location info from API
def get_distance(address1, address2):
  try:
    headers = {'User-Agent': USER_AGENT}

    response1 = requests.get(f"{BASE_URL}&street={address1}", headers=headers)
    response2 = requests.get(f"{BASE_URL}&street={address2}", headers=headers)

    # Error handling: https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
    response1.raise_for_status()
    response2.raise_for_status()

    data1 = response1.json()
    data2 = response2.json()

    lat1 = float(data1[0]['lat'])
    lon1 = float(data1[0]['lon'])

    lat2 = float(data2[0]['lat'])
    lon2 = float(data2[0]['lon'])

    location1 = (lat1, lon1)
    location2 = (lat2, lon2)

    return distance(location1, location2).miles

  # In case request fails an error is printed to console
  except requests.exceptions.RequestException as err:
    print(f"An error occured: {err}")
    return None


def verify_address(street):
  # We are only going to grab the street from the user since the city and state
  # should always be the same. Also, allowing the user to specify city and state
  # bricked get_distance.
  address = f"{street}, Colorado Springs, CO"

  # I was having issues ensuring users could enter extra address details and have
  # it count; think apartment number, floor, unit, etc. This pattern ensures these
  # details can remain.
  pattern = r'^(\d+)\s+([a-zA-Z]+\s)*([a-zA-Z]+\.?|\d+[a-zA-Z]?|\d+)(?:\s+([NSEW]{1,2}))?(?:,?\s+(?:APT|BLDG|DEPT|FL|HNGR|LOT|PIER|RM|S?SPC|STOP|STE|TRLR|UNIT|#)\.?\s+(\w+))?$'

  if not re.match(pattern, street):
    print("Invalid street format.")
    return False
    
  # Resources used: https://nominatim.org/release-docs/latest/api/Search/#parameters
  # https://realpython.com/python-requests/#query-string-parameters
  headers = {'User-Agent': USER_AGENT}
  params = {'format': 'json', 'q': address, 'addressdetails': 1, 'limit': 1}
  try:
    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    #print("Raw Data Returned: " + data)
    if not data:
      print("No data returned from API.")
      return False
    address_components = data[0].get('address', {})
    #print("Address component: ", address_components)
    city = address_components.get('city', '')
    state = address_components.get('state', '')
    #print("City: ", city)
    #print("State: ", state)
    return 'Colorado Springs' in city and 'Colorado' in state
  except requests.exceptions.RequestException as err:
    print(f"Error verifying address: {err}")
    return False


# Created a function to create tag objects. If tag obj already exists its not created again.
def init_tags():
  food_cat, created = TagCategory.objects.get_or_create(name='Food')
  cuisine_cat, created = TagCategory.objects.get_or_create(name='Cuisine')
  drink_cat, created = TagCategory.objects.get_or_create(name='Drink')
  dietary_cat, created = TagCategory.objects.get_or_create(name='Dietary')
  meal_cat, created = TagCategory.objects.get_or_create(name='Meal')
  dining_cat, created = TagCategory.objects.get_or_create(name='Dining')
  accomodations_cat, created = TagCategory.objects.get_or_create(
      name='Accomodations')
  store_cat, created = TagCategory.objects.get_or_create(name='Store')
  other_cat, created = TagCategory.objects.get_or_create(name='Other')

  # This is where you add tags for a category!!!
  tags = [
      (food_cat, "Pizza"),
      (food_cat, "Chicken"),
      (food_cat, "Burgers"),
      (food_cat, "Sandwiches"),
      (food_cat, "Salads"),
      (food_cat, "Fish"),
      (food_cat, "Steak"),
      (food_cat, "Pasta"),
      (food_cat, "Soup"),
      (cuisine_cat, "American"),
      (cuisine_cat, "Mexican"),
      (cuisine_cat, "Chinese"),
      (cuisine_cat, "Japanese"),
      (cuisine_cat, "French"),
      (cuisine_cat, "Indian"),
      (cuisine_cat, "Italian"),
      (drink_cat, "Coffee"),
      (drink_cat, "Beer"),
      (drink_cat, "Wine"),
      (dietary_cat, "Vegetarian"),
      (dietary_cat, "Vegan"),
      (dietary_cat, "Gluten Free"),
      (dietary_cat, "Kosher"),
      (dietary_cat, "Halal"),
      (meal_cat, "Breakfast"),
      (meal_cat, "Lunch"),
      (meal_cat, "Dinner"),
      (meal_cat, "Snacks"),
      (meal_cat, "Dessert"),
      (dining_cat, "Bar"),
      (dining_cat, "Café"),
      (dining_cat, "Fast Food"),
      (dining_cat, "Fine Dining"),
      (dining_cat, "Casual Dining"),
      (accomodations_cat, "Pet Friendly"),
      (accomodations_cat, "Wheelchair Accessible"),
      (store_cat, "Gas Station"),
      (store_cat, "Grocery Store"),
      (store_cat, "Specialty Store"),
      (other_cat, "Other"),
  ]

  for category, tag_name in tags:
    TagItem.objects.get_or_create(category=category, name=tag_name)
