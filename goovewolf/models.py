from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    pic = models.ImageField(upload_to='pics/profiles', blank=True)
    birthday = models.DateField(null=True, blank=True)


class Artist(models.Model):
    name = models.CharField(max_length=150)
    birthday = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=3, blank=True)
    bio = models.TextField(blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Album(models.Model):
    ALBUM_TYPES = (
        ('s', 'Studio'),
        ('l', 'Live'),
        ('n', 'Single'),
        ('d', 'Demo'),
        ('b', '_bootleg'),
    )

    name = models.CharField(max_length=150)
    artists = models.ManyToManyField(Artist)
    pic = models.ImageField(upload_to='pics/albums', blank=True)
    album_type = models.CharField(max_length=1, choices=ALBUM_TYPES)
    description = models.TextField(blank=True)
    release = models.DateField(null=True, blank=True)


class Song(models.Model):
    name = models.CharField(max_length=150)
    artist = models.ForeignKey(Artist, null=True, blank=True)
    featuring = models.ManyToManyField(Artist, blank=True)
    album = models.ForeignKey(Album)
    genre = models.ForeignKey(Genre, null=True, blank=True)
    file = models.FileField(upload_to='songs', blank=True)
    lyrics = models.TextField(blank=True)
    video = models.URLField(blank=True, help_text='Link to Youtube')
    created_by = models.ForeignKey(UserProfile)
    created = models.DateTimeField(auto_now_add=True)