# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


COLLECTION_KEYNAME = '_collection'


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    pic = models.ImageField(upload_to='pics/profiles', blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def get_collection(self):
        try:
            return self.playlist_set.get(system=True, name=COLLECTION_KEYNAME)
        except ObjectDoesNotExist:
            return self.playlist_set.create(system=True, name=COLLECTION_KEYNAME)


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
    album = models.ForeignKey(Album, null=True, blank=True)
    track_nro = models.PositiveSmallIntegerField(null=True, blank=True)
    file = models.FileField(upload_to='songs', blank=True)
    lyrics = models.TextField(blank=True)
    video = models.URLField(blank=True, help_text='Link to Youtube')
    created_by = models.ForeignKey(UserProfile)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['album', 'track_nro', 'name', ]

    def __unicode__(self):
        feats = [a.name for a in self.featuring.all()]
        return '%s - %s' % (self.name, self.artist.name if self.artist else ', '.join(feats))


class PlayList(models.Model):
    system = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    author = models.ForeignKey(UserProfile)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created', 'author', 'name', ]

    def __unicode__(self):
        return self.name

    def add_item(self, song, weight=None):
        collection = self if self.name == COLLECTION_KEYNAME else self.author.get_collection()

        if collection.items.filter(song=song).count() == 0:
            collection.items.create(song=song)

        if not (self.name == COLLECTION_KEYNAME):
            self.items.create(song=song)  # a song can be many times in the same playlist


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(PlayList, related_name='items')
    song = models.ForeignKey(Song)
    added = models.DateTimeField(auto_now_add=True, db_index=True)
    weight = models.SmallIntegerField(null=True, blank=True)  # TODO: sort the items in the list by this field...

    class Meta:
        ordering = ['weight', 'added']
