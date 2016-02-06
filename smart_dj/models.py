from django.db import models

# Create your models here.
class Person(models.Model):
    email = models.TextField()

    likes =  models.ManytoManyField(Music)
    dislikes = models.ManyToManyField(Music)

    rooms = models.ManyToManyField(Room)
    
class Room(models.Model):
    name = models.CharField(max_length=50)
    pin = models.CharField(max_length=8)

    host = models.ForeignKey(Person)

    current = Song
    last = Song

    playlistLength = models.IntegerField()

    expiration = models.DateField()

class Music(models.Model):
    name = models.TextField() 

class Artist(Music):
    ID = models.TextField()

class Genre(Music):

class Song(Music):
    ID = models.TextField()
