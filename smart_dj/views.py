from django.shortcuts import render
from smart_dj.utils import sp

import spotipy
import os

# Create your views here.
def index(request):
    return render(request, 'smart_dj/index.html', {})

def about(request):
    return render(request, 'smart_dj/about.html', {})

def profile(request):
    return render(request, 'smart_dj/profile.html', {})

def layout(request):
    return render(request, 'smart_dj/layout.html', {})

def login(request):
    return render(request, 'smart_dj/login.html', {})

def room(request):
    return render(request, 'smart_dj/room.html', {})
