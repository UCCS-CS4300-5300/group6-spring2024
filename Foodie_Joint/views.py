from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
#from django.contrib import messages
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
  return render(request, 'templates/login.html', {})
