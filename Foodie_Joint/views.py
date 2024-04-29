import requests  # Used to request info from API
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from geopy.distance import distance

from .filters import ItemReviewFilter, ReviewFilter
from .forms import (
    ItemForm,
    ItemReviewForm,
    LocationForm,
    RegistrationForm,
    ReviewForm,
    UpdateAccountForm,
)
from .models import Item, ItemReview, Location, LocationTag, Review, Account, User
from .utils import instantiate_tags


def index(request):
  # Since only one item can be recommended for now, we can just get the first item marked as recommended from the database.
  carousel_restaurants = Location.objects.filter(
      location_type='Restaurant')[:3]
  carousel_stores = Location.objects.filter(location_type='Store')[:3]
  recommended_item = Item.objects.filter(is_recommended=True).first()
  recommended_location = Location.objects.filter(is_recommended=True).first()
  return render(
      request, 'templates/index.html', {
          'recommended_item': recommended_item,
          'carousel_restaurants': carousel_restaurants,
          'carousel_stores': carousel_stores,
          'recommended_location': recommended_location
      })


def base(request):
  return render(request, 'templates/base_template.html')


# References:
# https://geopy.readthedocs.io/en/stable/#module-geopy.distance
# https://nominatim.org/release-docs/latest/api/Search/
BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'
# Added user-agent to request header to avoid 403 error
# https://operations.osmfoundation.org/policies/nominatim/
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Foodie_Joint/1.0 (tcarroll@uccs.edu)"


# Potentially move out of views.py
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


#@login_required(login_url='/login_user')
def nearby(request):
  context = {}
  locations = Location.objects.all()
  all_tags = LocationTag.objects.all()

  # Providing static address in case of user not logged in
  if request.user.is_authenticated:
    user_address = request.user.account.address
  else:
    user_address = "1420 Austin Bluffs Pkwy"  # UCCS

  if locations.exists():
    # Applying a filter (through href in navbar) on locations to only get store/restaurant objects
    loc_type = request.GET.get('type')
    if loc_type:
      locations = locations.filter(location_type=loc_type)

    # Filtering results based on chosen tags
    # https://www.oreilly.com/library/view/python-in-a/0596001886/re928.html
    # https://docs.djangoproject.com/en/5.0/ref/models/querysets/#in
    selected_tags = request.GET.getlist('tag')
    if selected_tags:
      locations = locations.filter(tags__name__in=selected_tags)

    # Filtering results based on searched name
    search_name = request.GET.get('search_name')
    if search_name:
      locations = locations.filter(name__icontains=search_name)

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
            'id': location.id,  # needed for location_item_info template
            'tags': location.tags.all(),
            'image': location.image,
            'created_by': location.created_by,
        })

    # Sorting in ascending order of distance (https://blogboard.io/blog/knowledge/python-sorted-lambda/)
    # If the distance key is not found in sorted_locations, it will be sorted by the default value of float('inf')
    sorted_locations.sort(
        key=lambda location: location.get('distance', float('inf')))

    context = {
        'user_address': user_address,
        'sorted_locations': sorted_locations,
        'all_tags': all_tags,
        'selected_tags':
        selected_tags,  # Added this to have checkboxes stay marked in template
        'search_name': search_name,
    }
    return render(request, 'templates/nearby.html', context)
  else:
    context['user_address'] = user_address
    context['no_locations'] = True
    return render(request, 'templates/nearby.html', context)


def login_user(request):
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        return redirect("index")
      else:
        messages.error(request, "Account is not active.")
        return redirect("login_user")
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
    form = RegistrationForm(request.POST, request.FILES)
    if form.is_valid():
      username = form.cleaned_data['username']
      if User.objects.filter(username=username).exists():
        messages.error(
            request,
            "Username already exists. Please choose another username.")
        return render(request, 'templates/register_user.html', {'form': form})

      # Creating the user and account objects. Associating them to each other
      user = User.objects.create_user(
          username=username,
          password=form.cleaned_data['password'],
          first_name=form.cleaned_data['first_name'],
          last_name=form.cleaned_data['last_name'],
          email=form.cleaned_data['email'],
      )

      account = form.save(commit=False)
      account.user = user
      account.save()
      '''
      account = Account.objects.create(
          user=user,
          address=form.cleaned_data['address'],
          city=form.cleaned_data['city'],
          state=form.cleaned_data['state'],
          profile_picture=form.cleaned_data['profile_picture'],
      )
      '''
      
      user = authenticate(request,
                          username=user.username,
                          password=form.cleaned_data['password'])
      login(request, user)
      messages.success(request, ("Registration successful"))
      return redirect('index')
  else:
    form = RegistrationForm()
  return render(request, 'templates/register_user.html', {
      'form': form,
  })


@login_required(login_url='/login_user')
def add_location(request):
  # Calling function to create tag objects if they dont exist
  instantiate_tags()
  submitted = False
  if request.method == 'POST':
    form = LocationForm(request.POST, request.FILES)
    if form.is_valid():
      location = form.save(commit=False)
      location.created_by = request.user.account
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
def favorite_item(request, location_id):
  location = get_object_or_404(Location, id=location_id)
  if location.favorites.filter(id=request.user.id).exists():
    location.favorites.remove(request.user)
  else:
    fav = False
    location.favorites.add(request.user)
  return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login_user')
def favorite_list(request):
  new = Location.objects.filter(favorites=request.user)
  return render(request, 'templates/favorites.html', {'new': new})


@login_required(login_url='/login_user')
def add_item(request, location_id):
  submitted = False
  location = get_object_or_404(Location, id=location_id)
  if request.method == 'POST':
    form = ItemForm(request.POST, request.FILES)
    if form.is_valid():
      item = form.save(commit=False)
      item.created_by = request.user.account
      item.location = Location.objects.get(id=location_id)
      form.save()
      return HttpResponseRedirect('/add_item/'+str(location_id)+'?submitted=True')
  else:
    form = ItemForm
    if 'submitted' in request.GET:
      submitted = True
  return render(request, 'templates/add_item.html', {
      'location': location,
      'form': form,
      'submitted': submitted
  })


# Renders a specific location's details and its associated items.
def show_location_items(request, location_id):
  location = get_object_or_404(Location, pk=location_id)
  items = location.item_set.all()
  reviews = Review.objects.filter(location=location)
  reviews_filter = ReviewFilter(request.GET, queryset=reviews)
  reviews = reviews_filter.qs
  fav = bool
  if location.favorites.filter(id=request.user.id).exists():
    fav = True
  if items.exists():
    item_list = []
    for item in items:
      item_list.append({
          'name': item.name,
          'description': item.description,
          'location': item.location,
          'is_recommended': item.is_recommended,
          'id': item.id,
          'image': item.image.url,
          'created_by': item.created_by
      })
    context = {
        'location': location,
        'items': item_list,
        'reviews': reviews,
        'reviews_filter': reviews_filter,
        'id': location.id,
    }
  else:
    context = {
        'location': location,
        'items': items,
        'reviews': reviews,
        'reviews_filter': reviews_filter,
        'fav': fav,
        'id': location.id,
    }
  return render(request, 'templates/location_item_info.html', context)


@login_required(login_url='/login_user')
def add_review(request, location_id):
  submitted = False
  if request.method == 'POST':
    form = ReviewForm(request.POST,
                      initial={
                          'user': request.user.username,
                          'location': Location.objects.get(id=location_id)
                      })
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/add_review/%d?submitted=True' %
                                  location_id)
  else:
    form = ReviewForm(
        initial={
            'user': request.user.username,
            'location': Location.objects.get(id=location_id)
        })
    if 'submitted' in request.GET:
      submitted = True
  return render(request, 'templates/add_review.html', {
      'form': form,
      'submitted': submitted
  })


@login_required(login_url='/login_user')
def add_review_item(request, item_id):
  submitted = False
  if request.method == 'POST':
    form = ItemReviewForm(request.POST,
                          initial={
                              'user': request.user.username,
                              'item': Item.objects.get(id=item_id)
                          })
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/add_review_item/%d?submitted=True' %
                                  item_id)
  else:
    form = ItemReviewForm(initial={
        'user': request.user.username,
        'item': Item.objects.get(id=item_id)
    })
    if 'submitted' in request.GET:
      submitted = True
  return render(request, 'templates/add_review_item.html', {
      'form': form,
      'submitted': submitted
  })


def item_info(request, item_id):
  item = get_object_or_404(Item, pk=item_id)
  reviews = ItemReview.objects.filter(item=item)
  item_filter = ItemReviewFilter(request.GET, queryset=reviews)
  reviews = item_filter.qs
  context = {
      'item': item,
      'reviews': reviews,
      'item_filter': item_filter,
      'id': item.id,
      'created_by': item.created_by
  }
  return render(request, 'templates/item_info.html', context)


@login_required(login_url='/login_user')
def remove_user(request):
  user = request.user
  user.is_actived = False
  user.save()
  logout(request)
  response = HttpResponse(
      "You have been removed from the site. Please close this window.")
  return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def remove_store(request, location_id):
  location = get_object_or_404(Location, id=location_id)
  location.delete()
  return redirect('nearby')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def remove_item(request, item_id):
  item = get_object_or_404(Item, pk=item_id)
  store_id = item.location.id
  item.delete()
  return redirect('nearby')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def recommend_location(request, location_id):
  Location.objects.update(is_recommended=False)
  location = get_object_or_404(Location, id=location_id)
  location.is_recommended = True
  location.save()
  return redirect('index')

@login_required(login_url='/login_user')
def profile(request):
  if request.method == 'POST':
    account_form = UpdateAccountForm(request.POST, instance = request.user.account)
    
    if account_form.is_valid():
      account_form.save()
      messages.success(request, "Account updated successfully")
      return redirect('index')
  else:
    account_form = UpdateAccountForm(instance = request.user.account)
  
  return render(request, 'templates/profile.html', {'account_form': account_form})
      
