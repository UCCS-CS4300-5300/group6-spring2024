from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Location, Item, User, Review, ItemReview, Tag
from .forms import LocationForm, ItemForm, ReviewForm, ItemReviewForm, TagForm, ItemTagForm, RegisterUserForm
from django.contrib.auth.forms import UserCreationForm
from geopy.distance import distance
from geopy.units import miles
import requests  # Used to request info from API


def index(request):
  # Since only one item can be recommended for now, we can just get the first item marked as recommended from the database.
  recommended_item = Item.objects.filter(is_recommended=True).first()
  return render(request, 'templates/index.html',
                {'recommended_item': recommended_item})


def base(request):
  return render(request, 'templates/base_template.html')


# References:
# https://geopy.readthedocs.io/en/stable/#module-geopy.distance
# https://nominatim.org/release-docs/latest/api/Search/
BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'


# Potentially move out of views.py
def get_distance(address1, address2):
  try:
    response1 = requests.get(f"{BASE_URL}&street={address1}")
    response2 = requests.get(f"{BASE_URL}&street={address2}")

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


#@login_required(login_url='/login_user')
def nearby(request):
  context = {}
  # Static address as placeholder till User model working
  user_address = '1420 Austin Bluffs Pkwy'
  #user = request.user
  #user_address = user.address
  locations = Location.objects.all()

  if locations.exists():
    # Applying a filter (through href in navbar) on locations to only get store/restaurant objects
    loc_type = request.GET.get('type')
    if loc_type:
      locations = locations.filter(location_type=loc_type)

    sorted_locations = []
    for location in locations:
      distance = get_distance(user_address, location.address)
      # Checking get_distance request went through/didnt return None
      if distance is not None:
        rounded_distance = round(distance, 2)
        sorted_locations.append({
            'name': location.name,
            'description': location.description,
            'location_type': location.location_type,
            'address': location.address,
            'distance': distance,
            'rounded_distance': rounded_distance,
            'id': location.id  # needed for location_item_info template
        })

    # Sorting in ascending order of distance (https://blogboard.io/blog/knowledge/python-sorted-lambda/)
    # If the distance key is not found in sorted_locations, it will be sorted by the default value of float('inf')
    sorted_locations.sort(
        key=lambda location: location.get('distance', float('inf')))

    context = {
        'user_address': user_address,
        'sorted_locations': sorted_locations,
    }
    return render(request, 'templates/nearby.html', context)
  else:
    context['no_locations'] = True
    return render(request, 'templates/nearby.html', context)


def login_user(request):
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect("index")
    else:
      messages.error(request, "Invalid username or password")
      return redirect("login")
  else:
    return render(request, 'templates/login.html', {})


def logout_user(request):
  logout(request)
  messages.success(request, ("Successfully logged out"))
  return redirect("index")


def register_user(request):
  if request.method == "POST":
    form = RegisterUserForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(request, username=username, password=password)
      login(request, user)
      messages.success(request, ("Registration successful"))
      return redirect('index')
  else:
    form = RegisterUserForm()
  return render(request, 'templates/register_user.html', {
      'form': form,
  })


@login_required(login_url='/login_user')
def add_location(request):
  submitted = False
  if request.method == 'POST':
    form = LocationForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/add_location?submitted=True')
  else:
    form = LocationForm
    if 'submitted' in request.GET:
      submitted = True
  return render(request, 'templates/add_location.html', {
      'form': form,
      'submitted': submitted
  })


@login_required(login_url='/login_user')
def add_item(request):
  submitted = False
  if request.method == 'POST':
    form = ItemForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/add_item?submitted=True')
  else:
    form = ItemForm
    if 'submitted' in request.GET:
      submitted = True
  return render(request, 'templates/add_item.html', {
      'form': form,
      'submitted': submitted
  })


# Renders a specific location's details and its associated items.
def show_location_items(request, location_id):
  location = get_object_or_404(Location, pk=location_id)
  items = location.item_set.all()
  reviews = Review.objects.filter(location=location)
  context = {
      'location': location,
      'items': items,
      'reviews': reviews
  }
  return render(request, 'templates/location_item_info.html', context)

