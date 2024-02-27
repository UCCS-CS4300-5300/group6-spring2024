from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Location


def index(request):
  #return HttpResponse("hello world")
  return render(request, 'templates/index.html')


# Debugging: Added for easy viewing
# Will remove.
def nav(request):
  return render(request, 'templates/nav.html')


# Debugging: Added for easy viewing
# Will remove.
def maybe(request):
  return render(request, 'templates/maybe.html')


# Debugging: Added for easy viewing
# Will remove.
def backup(request):
  return render(request, 'templates/backup.html')


# Debugging: Added for easy viewing
# Will remove.
def base(request):
  return render(request, 'templates/base_template.html')


def nearby(request):
  data = Location.objects.all()
  context = {"locations": data}
  return render(request, 'templates/nearby.html', context)