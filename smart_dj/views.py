from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.core.urlresolvers import reverse

from smart_dj.utils import sp
from smart_dj.forms import *
from smart_dj.models import *

import string
import random
import spotipy
import os

# Create your views here.
@login_required
def index(request):
    context = {}
    user = User.objects.get(username=request.user.username)
    rooms = Room.objects.filter(host=user) [:5]
    context['rooms'] = []
    for room in rooms:
        context['rooms'].append((room.name,room.pin))
    search_results = sp.search(q='Snoop Dogg',limit = 1,offset=0,type='artist')
    artist_uri = search_results['artists']['items'][0]['uri']
    for i in sp.artist_top_tracks(artist_uri)['tracks']:
        print i['name']
    return render(request, 'smart_dj/index.html', context)

def about(request):
    return render(request, 'smart_dj/about.html', {})

@login_required
def profile(request):
    context = {}

    user = User.objects.get(id=request.user.id)
    likes_content = LikesList.objects.get(user=user)
    dislikes_content = DislikesList.objects.get(user=user)
    context['form'] = PreferencesForm()
    context['liked_songs'] = []
    context['disliked_songs'] = []
    for likes in likes_content.songs.all():
        context['liked_songs'].append((likes.title, likes.artist))
    for dislikes in dislikes_content.songs.all():
        context['disliked_songs'].append((dislikes.title, dislikes.artist))
    return render(request, 'smart_dj/profile.html', context)

@transaction.atomic
def register(request):
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

    likes = LikesList(user=new_user)
    dislikes = DislikesList(user=new_user)
    likes.save()
    dislikes.save()

    new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
    login(request, new_user)
    return redirect('index')

@login_required
def make_room(request):
    new_room = Room(host=request.user)

    new_room.name = request.POST['room_name']
    pin = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
    #while (Room.objects.get(pin=pin)) {
    #    pin = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
    #}

    new_room.playlist_length = request.POST['num_songs']
    new_room.save()
    return redirect(reverse('room', kwargs={'pin': new_room.pin}))

@login_required
<<<<<<< Updated upstream
def join_room(request):
    return redirect(reverse('room', kwargs={'pin': request.POST['pin']}))
=======
def add_song(request):
    context = {}

    form = PreferencesForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'smart_dj/profile.html', context)

    song_title = form.cleaned_data['song_title']
    artist_name = form.cleaned_data['artist_name']
    preference = form.cleaned_data['preference']
    new_song = Song(title=song_title, artist=artist_name)
    new_song.save()

    if preference == 'L':
        request.user.likeslist.songs.add(new_song)
    else:
        request.user.dislikeslist.songs.add(new_song)

    return redirect(reverse('profile'))
>>>>>>> Stashed changes

@login_required
def room(request, pin):
    context = {}

    user = User.objects.get(id=request.user.id)
    room = Room.objects.get(host=user,pin=pin)

    context['room_name'] = room.name
    context['host'] = room.host.username
    context['pin'] = pin

    '''
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
    '''

    return render(request, 'smart_dj/room.html', context)    
