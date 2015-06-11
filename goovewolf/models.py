# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    pic = models.ImageField(upload_to='pics/profiles', blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username


class Artist(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    birthday = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=3, blank=True)  # TODO: crear una tabla o una lista para un choices...
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.user.username


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


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
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-release', 'name', ]

    def __unicode__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=150)
    artist = models.ForeignKey(Artist, null=True, blank=True, related_name='songs')
    featuring = models.ManyToManyField(Artist, blank=True, related_name='featuring_songs')
    genre = models.ForeignKey(Genre, null=True, blank=True)
    album = models.ForeignKey(Album)
    track_nro = models.PositiveSmallIntegerField(null=True, blank=True)
    file = models.FileField(upload_to='songs', blank=True)
    lyrics = models.TextField(blank=True)
    video = models.URLField(blank=True, help_text='Link to Youtube')
    created_by = models.ForeignKey(UserProfile)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['album', 'track_nro', 'name', ]

    def __unicode__(self):
        feats = [a.name for a in self.featuring.all()]
        return '%s - %s' % (self.name, self.artist.name if self.artist else ', '.join(feats))


class PlayList(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(UserProfile)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', 'author', 'name', ]

    def __unicode__(self):
        return self.name


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(PlayList)
    song = models.ForeignKey(Song)
    added = models.DateTimeField(auto_now_add=True)
    weight = models.SmallIntegerField()

    class Meta:
        ordering = ['weight', 'added']
