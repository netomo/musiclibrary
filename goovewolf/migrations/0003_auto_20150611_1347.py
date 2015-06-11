# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goovewolf', '0002_playlist_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlistitem',
            name='playlist',
            field=models.ForeignKey(related_name='items', to='goovewolf.PlayList'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playlistitem',
            name='weight',
            field=models.SmallIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
