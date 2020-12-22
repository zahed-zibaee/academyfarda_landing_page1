# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-17 07:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0005_auto_20200916_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sent',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 11, 40, 18, 295119), editable=False),
        ),
        migrations.AlterField(
            model_name='verify',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 11, 45, 18, 295920), editable=False),
        ),
        migrations.AlterField(
            model_name='verify',
            name='token1',
            field=models.CharField(default='929', max_length=3),
        ),
        migrations.AlterField(
            model_name='verify',
            name='token2',
            field=models.CharField(default='997', max_length=3),
        ),
    ]
