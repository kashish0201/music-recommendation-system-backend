from django.db import models
from django.contrib.auth.models import User 

class Song(models.Model):
    genre = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    audio_file = models.URLField(max_length=200)


class Liked_song(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    song = models.ForeignKey(Song, on_delete= models.CASCADE)
