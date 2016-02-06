from django.db import models

# Create your models here.
class Person(models.Model):
	likes =  models.ManyToManyField()
	dislikes =
	
	def addLike ():
	   return 0
	def addDislike ():
	   return 0
	def rmLike ():
	   return 0
	def rmDislike ():
	   return 0
	   
	   
class Room(models.Model):
    host = 0

class Songs(models.Model):