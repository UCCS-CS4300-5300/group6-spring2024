from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Location


def index(request):
  #return HttpResponse("hello world")
  return render(request, 'templates/index.html')


def base(request):
  return render(request, 'templates/base_template.html')


def nearby(request):
  data = Location.objects.all()
  context = {"locations": data}
  return render(request, 'templates/nearby.html', context)