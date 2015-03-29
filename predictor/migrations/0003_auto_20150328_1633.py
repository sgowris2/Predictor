# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_gameweek_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameweek',
            name='number',
        ),
        migrations.AddField(
            model_name='gameweek',
            name='name',
            field=models.CharField(default='Gameweek 0', max_length=15),
            preserve_default=False,
        ),
    ]
