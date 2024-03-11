from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import Location, Item


def index(request):
  # Since only one item can be recommended for now, we can just get the first item marked as recommended from the database.
  recommended_item = Item.objects.filter(is_recommended=True).first()
  return render(request, 'templates/index.html',
                {'recommended_item': recommended_item})


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