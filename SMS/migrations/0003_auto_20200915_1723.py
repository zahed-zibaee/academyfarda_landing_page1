# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-15 12:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0002_auto_20200915_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sent',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 15, 17, 23, 25, 399506), editable=False),
        ),
        migrations.AlterField(
            model_name='verify',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 15, 17, 28, 25, 400295), editable=False),
        ),
        migrations.AlterField(
            model_name='verify',
            name='token1',
            field=models.CharField(default='549', max_length=3),
        ),
        migrations.AlterField(
            model_name='verify',
            name='token2',
            field=models.CharField(default='368', max_length=3),
        ),
    ]