from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#class Music(models.Model):
#    name = models.TextField() 

#class Artist(Music):
#    ID = models.TextField()

#class Genre(Music):
#    pass

class Song(models.Model):
    title = models.TextField(default='Unknown Title')
    artist = models.TextField(default='Unknown Artist')

class Room(models.Model):
    name = models.CharField(max_length=50)
    pin = models.CharField(max_length=8)

    host = models.ForeignKey(User)
    otherPeople = models.ManyToManyField(User, related_name='guests')

    playlist_length = models.IntegerField(default=5)

class LikesList(models.Model):
	user = models.OneToOneField(User)
	songs = models.ManyToManyField(Song)

class DislikesList(models.Model):
	user = models.OneToOneField(User)
	songs = models.ManyToManyField(Song)


