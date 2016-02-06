from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from smart_dj.utils import sp
from models import *

import string
import random
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
    if len(User.objects.filter(username=username)) == 0:
        message = 'Username already taken'
        return render(request, 'smart_dj/register.html',{message: message})
    password = request.POST['password']
    user = User.objects.create_user(username,'',password)
    user.save()
    person = Person()
    person.name = username
    person.save()
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

def init_room(request):
    new_room = Room()

    room.name = request.POST['roomname']
    room.pin = ''.join(random.choice(string.ascii_letters+string.digits) 
                  for i in range(8)) 

    room.host = request.user
    others = room.otherPeople.all()

    room.current = ''
    room.last = ''
    room.playlistLength = request.POST['num_songs']

    #room.expiration = request.POST('')

def room(request):
    if request.method == 'GET':
        return render(request, 'smart_dj/room.html',{})
    my_room=init_room(request)
    playlist = []
    preflist = []
    blacklist = []

    j=0
    for k in otherPeople.all():
        preflist[j] = k.otherPeople.likes.all()
        blacklist[j] = k.otherPeople.dislikes.all()
        j=j+1

    i=0
    j=0
    while (my_room.current!=my_room.last):
        if(my_room.current==my_room.last):
            while (i < (my_room.playlistLength)):
                song = random.choice(preflist)
                if (song not in playlist) and (song not in blacklist):
                   playlist[i] = random.choice(preflist)
                   i=i+1
                current = playlist[0]
        last = playlist[my_room.playlistLength-1]
        j=j+1
        current=playlist[j]

    return render(request, 'smart_dj/room.html', {})
    
