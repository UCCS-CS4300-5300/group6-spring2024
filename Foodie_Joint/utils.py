import requests  # Used to request info from API
from geopy.distance import distance
from .models import LocationTag


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

# Created a function to create tag objects (trying tags as seperate model)
def instantiate_tags():
  for tag_name, _ in LocationTag.TAG_CHOICES:
    if not LocationTag.objects.filter(name=tag_name).exists():
      LocationTag.objects.create(name=tag_name)