# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0007_leaderboard_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameweekaggregateresult',
            name='least_guessed_result',
            field=models.ForeignKey(related_name='least_guessed_result', default=None, to='predictor.Match'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameweekaggregateresult',
            name='most_guessed_result',
            field=models.ForeignKey(related_name='most_guessed_result', default=None, to='predictor.Match'),
            preserve_default=True,
        ),
    ]
