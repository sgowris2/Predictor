# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0008_auto_20160909_2255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='predictionresult',
            old_name='away_score',
            new_name='away_scored',
        ),
    ]
