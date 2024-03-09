from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
#from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Location, Item, User, Review, ItemReview, Tag
from .forms import LocationForm, ItemForm, UserForm, ReviewForm, ItemReviewForm, TagForm


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
  return render(request, 'templates/login.html', {})

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