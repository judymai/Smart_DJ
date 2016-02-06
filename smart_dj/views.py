from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db import transaction

from smart_dj.utils import sp
from smart_dj.models import *

import string
import random
import spotipy
import os

# Create your views here.
@login_required
def index(request):
    '''
    user = User.objects.filter(username=request.user.username)
    rooms = Room.objects.filter(Person=user) [:5]
    context = {rooms: rooms}
    '''
    return render(request, 'smart_dj/index.html', {})

def about(request):
    return render(request, 'smart_dj/about.html', {})

@login_required
def profile(request):
    user = Person.objects.filter(username=request.user.username)
    like = Song.objects.filter(Person=user, related_name='person_likes') [:5]
    dislike=Song.objects.filter(Person=user,related_name='person_dislikes')[:5]
    context = {likes: like, dislikes: dislike}
    return render(request, 'smart_dj/profile.html', context)

@transaction.atomic
def register(request):
    if request.user.is_authenticated():
        return redirect('index')

    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'smart_dj/register.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
            and request.POST['password1'] and request.POST['password2'] \
            and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        print errors
        return render(request, 'smart_dj/register.html', context)

    username = request.POST['username']
    password = request.POST['password1']
    new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
    new_user.save()

    new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
    login(request, new_user)
    return redirect('index')

def init_room(request):
    new_room = Room()

    room.name = request.POST['roomname']
    room.pin = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
    room.host = request.user
    others = room.otherPeople.all()

    room.current = ''
    room.last = ''
    room.playlist_length = request.POST['num_songs']

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
