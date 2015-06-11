# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goovewolf', '0004_auto_20150611_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playlistitem',
            name='added',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
            preserve_default=True,
        ),
    ]
