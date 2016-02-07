from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db import transaction

from django.core.urlresolvers import reverse

from smart_dj.utils import sp, get_artist_hits
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
    hosted_rooms = Room.objects.filter(host=user) [:5]
    guest_rooms = Room.objects.filter(otherPeople=user) [:5]
    context['hosted_rooms'] = []
    for room in hosted_rooms:
        context['hosted_rooms'].append((room.name,room.pin))
    context['guest_rooms'] = []
    for room in guest_rooms:
        context['guest_rooms'].append((room.name,room.pin))
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
    new_room.pin = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])

    new_room.playlist_length = request.POST['num_songs']
    new_room.save()
    return redirect(reverse('room', kwargs={'pin': new_room.pin}))

@login_required
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

@login_required
def join_room(request):
    pin = request.POST['pin']
    user = request.user
    host = Room.objects.filter(host=user,pin=pin)
    rooms = Room.objects.filter(otherPeople=user,pin=pin)
    if (len(host)==0 and len(rooms)==0):
        room=Room.objects.get(pin=pin)
        room.otherPeople.add(user)
        room.save()
    return redirect(reverse('room', kwargs={'pin': request.POST['pin']}))

@login_required
def room(request, pin):
    context = {}

    user = User.objects.get(id=request.user.id)
    room = Room.objects.get(pin=pin)
    guests = User.objects.filter(guests=room)

    guests = room.otherPeople.all()

    liked_artists = []
    for guest in guests:
        likes = guest.likeslist.songs.all()
        liked_artists = liked_artists + [s.artist for s in likes]

    context['room_name'] = room.name
    context['host'] = room.host.username
    context['pin'] = room.pin
    context['guests'] = guests

    top_songs = []
    for artist in liked_artists:
        top_songs = top_songs + get_artist_hits(artist)

    context['playlist_uri'] = ','.join(top_songs)
    context['playlist'] = []
    for song in top_songs:
        spotify_song = sp.track(song)
        context['playlist'].append((spotify_song['name'],spotify_song['artists'][0]['name']))
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
