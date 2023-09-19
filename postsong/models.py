from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):

    objects = models.Manager()

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Song(models.Model):

    objects = models.Manager()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    key = models.CharField(max_length=3)
    tuning = models.CharField(max_length=50)
    chords = models.TextField(null=True)
    description = models.TextField(null=True)
    lyric = models.TextField(null=True)

    def __str__(self):
        return self.title





