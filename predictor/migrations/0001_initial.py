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
            name='Gameweek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameweekResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_points', models.IntegerField(default=0)),
                ('gameweek', models.ForeignKey(to='predictor.Gameweek')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('has_ended', models.BooleanField(default=0)),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
                ('is_doubled', models.BooleanField(default=0)),
                ('result', models.BooleanField(default=0)),
                ('goal_difference', models.BooleanField(default=0)),
                ('home_goals', models.BooleanField(default=0)),
                ('away_goals', models.BooleanField(default=0)),
                ('total_goals', models.BooleanField(default=0)),
                ('scoreline', models.BooleanField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('match', models.ForeignKey(to='predictor.Match')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='match',
            name='away_team',
            field=models.ForeignKey(related_name='match_away_team', to='predictor.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='gameweek',
            field=models.ForeignKey(to='predictor.Gameweek'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='home_team',
            field=models.ForeignKey(related_name='match_home_team', to='predictor.Team'),
            preserve_default=True,
        ),
    ]
