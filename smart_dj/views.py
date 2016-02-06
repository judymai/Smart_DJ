from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from smart_dj.utils import sp

import spotipy
import os

# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'smart_dj/index.html', {})
    user = Person.objects.filter(username=request.user.username)
    rooms = Room.objects.filter(Person=user) [:5]
    context = {rooms: rooms}
    return render(request, 'smart_dj/index.html', context)

def about(request):
    return render(request, 'smart_dj/about.html', {})

def profile(request):
    if not request.user.is_authenticated():
        return redirect('login')
    user = Person.objects.filter(username=request.user.username)
    like = Song.objects.filter(Person=user, related_name='person_likes') [:5]
    dislike=Song.objects.filter(Person=user,related_name='person_dislikes')[:5]
    context = {likes: like, dislikes: dislike}
    return render(request, 'smart_dj/profile.html', context)

def layout(request):
    return render(request, 'smart_dj/layout.html', {})

def register(request):
    if request.user.is_authenticated():
        return redirect('index')
    if request.method == 'GET':
        return render(request, 'smart_dj/register.html',{})
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username,'',password)
    person = Person()
    person.name = username
    return redirect ('index')

def login(request):
    if request.user.is_authenticated():
        return redirect('index')
    if request.method == 'GET':
        return render(request, 'smart_dj/login.html',{})
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
        else:
            context = {message: 'Disabled account'}
            return render('GET', 'smart_dj/index.html', context)
    context = {message: 'Invalid login'}
    return render(request, 'smart_dj/login.html', context)

def room(request):
    return render(request, 'smart_dj/room.html', {})
