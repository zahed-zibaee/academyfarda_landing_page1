# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-09-21 13:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0008_auto_20200921_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sent',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 21, 17, 0, 58, 837361), editable=False),
        ),
        migrations.AlterField(
            model_name='verify',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 21, 17, 5, 58, 838303), editable=False),
        ),
        migrations.AlterField(
            model_name='verify',
            name='token1',
            field=models.CharField(default='408', max_length=3),
        ),
        migrations.AlterField(
            model_name='verify',
            name='token2',
            field=models.CharField(default='055', max_length=3),
        ),
    ]
