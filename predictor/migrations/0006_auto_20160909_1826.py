# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0005_leaderboard'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameweekAggregateResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('highest_score', models.IntegerField(default=0)),
                ('average_score', models.IntegerField(default=0)),
                ('gameweek', models.ForeignKey(to='predictor.Gameweek')),
                ('least_guessed_result', models.ForeignKey(related_name='least_guessed_result', to='predictor.Match')),
                ('most_guessed_result', models.ForeignKey(related_name='most_guessed_result', to='predictor.Match')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='away_goals',
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='goal_difference',
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='home_goals',
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='points',
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='result',
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='scoreline',
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='total_goals',
        ),
        migrations.AddField(
            model_name='predictionresult',
            name='away_goals',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='predictionresult',
            name='away_score',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='predictionresult',
            name='home_goals',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='predictionresult',
            name='home_scored',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='predictionresult',
            name='result',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='predictionresult',
            name='scoreline',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
