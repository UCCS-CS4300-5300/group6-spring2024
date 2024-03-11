from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Location, Item, User, Review, ItemReview, Tag
from .forms import LocationForm, ItemForm, ReviewForm, ItemReviewForm, TagForm, ItemTagForm, RegisterUserForm
from django.contrib.auth.forms import UserCreationForm



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

