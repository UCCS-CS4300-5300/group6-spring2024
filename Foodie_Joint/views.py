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
import folium  # Potentially remove
import requests  # Used to request info from API


def index(request):
  # Since only one item can be recommended for now, we can just get the first item marked as recommended from the database.
  recommended_item = Item.objects.filter(is_recommended=True).first()
  return render(request, 'templates/index.html', {'recommended_item': recommended_item})

def base(request):
  return render(request, 'templates/base_template.html')

def nearby(request):
  data = Location.objects.all()
  context = {"locations": data}
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
  return render(request, 'templates/register_user.html', {'form': form,})

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
  return render(request, 'templates/add_location.html', {'form':form, 'submitted':submitted})

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
  return render(request, 'templates/add_item.html', {'form':form, 'submitted':submitted})



# Reference: https://www.youtube.com/watch?v=AeYxEDM1o2E&ab_channel=BugBytes
BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'

def get_distance(address1, address2):
  response1 = requests.get(f"{BASE_URL}&street={address1}")
  response2 = requests.get(f"{BASE_URL}&street={address2}")

  data1 = response1.json()
  data2 = response2.json()

  lat1 = float(data1[0]['lat'])
  lon1 = float(data1[0]['lon'])

  lat2 = float(data2[0]['lat'])
  lon2 = float(data2[0]['lon'])

  location1 = (lat1, lon1)
  location2 = (lat2, lon2)

  return distance(location1, location2).miles
  

def get_nearby(request):
  user_address = '1420 Austin Bluffs Pkwy'
  locations = Location.objects.all()

  sorted_locations = []
  for location in locations:
    distance = get_distance(user_address, location.address)
    sorted_locations.append({'name': location.name, 'distance': distance})

  sorted_locations.sort(key=lambda x: x['distance'])

  context = {
    'user_address': user_address,
    'sorted_locations': sorted_locations,
  }
  
  return render(request, 'templates/get_nearby.html', context)
  #return JsonResponse(response3.json(), safe=False)
  #return render(request, 'templates/get_nearby.html', response)