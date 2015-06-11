# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goovewolf', '0003_auto_20150611_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(blank=True, to='goovewolf.Album', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
            preserve_default=True,
        ),
    ]
