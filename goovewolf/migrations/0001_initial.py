# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('pic', models.ImageField(upload_to='pics/albums', blank=True)),
                ('album_type', models.CharField(max_length=1, choices=[('s', 'Studio'), ('l', 'Live'), ('n', 'Single'), ('d', 'Demo'), ('b', '_bootleg')])),
                ('description', models.TextField(blank=True)),
                ('release', models.DateField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-release', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, db_index=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('nationality', models.CharField(max_length=3, blank=True)),
                ('bio', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created', 'author', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaylistItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('weight', models.SmallIntegerField()),
                ('playlist', models.ForeignKey(to='goovewolf.PlayList')),
            ],
            options={
                'ordering': ['weight', 'added'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('track_nro', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('file', models.FileField(upload_to='songs', blank=True)),
                ('lyrics', models.TextField(blank=True)),
                ('video', models.URLField(help_text='Link to Youtube', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(to='goovewolf.Album')),
                ('artist', models.ForeignKey(related_name='songs', blank=True, to='goovewolf.Artist', null=True)),
            ],
            options={
                'ordering': ['album', 'track_nro', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pic', models.ImageField(upload_to='pics/profiles', blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='song',
            name='created_by',
            field=models.ForeignKey(to='goovewolf.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='featuring',
            field=models.ManyToManyField(related_name='featuring_songs', to='goovewolf.Artist', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='genre',
            field=models.ForeignKey(blank=True, to='goovewolf.Genre', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playlistitem',
            name='song',
            field=models.ForeignKey(to='goovewolf.Song'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playlist',
            name='author',
            field=models.ForeignKey(to='goovewolf.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='artists',
            field=models.ManyToManyField(to='goovewolf.Artist'),
            preserve_default=True,
        ),
    ]
